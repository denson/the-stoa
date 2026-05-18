# Arc 36 v2 — Design (bundled coordination-hygiene canon)

**Author seat:** CAPTAIN_DAEDALUS_the-stoa
**Branch:** `arc-36/build` (worktree at `.claude/worktrees/arc-36-build/`)
**Work-units:** `stoa--jru` (parent EPIC) + `stoa--e39` (Part 1) + `stoa--cgn` (Part 2)
**Directive (LOCKED):** `substrate/arcs/arc-36-build-directive.md`
**Architectural reference (inherited):** `git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md`
**PLINY A7 spike result:** stoa--jru comment 2026-05-17T~23:xxZ `[from: pliny-the-stoa]` (verbatim findings consumed; not re-executed per §6.3 consume-research discipline)
**Operating mode:** AUTONOMOUS (peer = MAJOR_PLINY_the_stoa via stoa--jru; user-tier POLYBIUS via QA pass at arc close per A15)

---

## §1 — Brief (restatement)

Arc 36 v2 ships the bundled coordination-hygiene canon that arc-22 originally specified and v1 deferred (`stoa--cgn` carved out under gating criteria). PRINCIPAL reversed the v1 scope-recut pre-dispatch under the no-deferrals stance; both Parts now ship in a single gauntlet. Part 1 hardens POLYBIUS-on-POLYBIUS coordination against the bw-timeline misattribution failure mode empirically observed 2026-05-04 (stoa--e39: ~25-min coordination stall when project-tier POLYBIUS attributed a `[for: POLYBIUS_the_stoa]` comment as own self-heartbeat). The fix is a mandatory `[from: <self-seat-slug>]` author-tag on POLYBIUS coordination comments + universal-team parsing teaching that drives `last_self_activity` / `last_peer_activity` arithmetic from tag-attributed comments only. Part 2 hardens autonomous-mode polling crons against CronCreate's 7-day expiry; PLINY's A7 spike confirmed cron metadata is fully opaque (no backward-looking or forward-looking fields; no CronUpdate primitive), routing to Option 3 (setup-time scheduled renewal cron chain at +144h with a 24h buffer-from-expiry) per the A7 decision matrix. Both fixes are forward-only — no retroactive tagging, no historical bw-history rewrite, no mechanical parser enforcement.

**Restatement-gate (§6.1) check:** the brief is unusually specific (A1-A17 LOCKED, A5/A6 sub-decisions enumerated, A7 spike pre-executed). The restatement above is faithful and names two imported assumptions: (a) the parse-by-tag teaching enters substrate as a NEW §7.7 (DAEDALUS sub-decision per A5 below; user-tier lean accepted), and (b) STEP 1.5 ships as MANDATORY in the polling-cron-prompt template (DAEDALUS sub-decision per A6 below; user-tier lean accepted). Neither sub-decision is PRINCIPAL-gate by the §25.3 "would the wrong pick require substantive substrate-canon-edit unwind" bar — both are recoverable inside the same arc's revision cycle. Restatement converges with the brief; no `refused` route.

---

## §2 — Inputs

### §2.1 — What was read (load-bearing)

1. `substrate/arcs/arc-36-build-directive.md` — A1-A17 LOCKED spec; both Parts bundled per original arc-22; integration surface refreshed against current substrate (Arcs 23-35 numbering).
2. `bw show stoa--jru` (parent EPIC, v2-superseding framing in 2026-05-17 comment) + `bw show stoa--e39` (Part 1 empirical anchor 2026-05-04) + `bw show stoa--cgn` (Part 2 surfacing during arc-21 review).
3. `git show arcs/22-coordination-hygiene:substrate/arcs/arc-22-build-directive.md` — arc-22's architectural reference. Deliverables 1.1 / 1.2 / 1.3 / 1.4 / 1.5 (Part 1) + 2.1 / 2.2 / 2.3 / 2.4 (Part 2) carry the inherited content shape.
4. `substrate/operating-disciplines.md` — §7 entire (§7.1 four-beat radio-check; §7.2 adaptive cadence; §7.3 unified poll; §7.4 cross-tier routing with current "cross-tier UPWARD requests only" wording; §7.5 write boundaries; §7.6 empirical lineage); §11 current 6-step autonomous-mode-setup checklist; §25 (PRINCIPAL-gate); §27 (mechanical-script / agent-inspection split — A14 precedent for "ship prose canon now; defer mechanical enforcement"); §28 (Co-Authored-By trailer canon — applies to this design.md commit).
5. `substrate/MAJOR_POLYBIUS.md` §7 (POLYBIUS-tier bw-handling; §7.1 write boundaries with `MAJOR_POLYBIUS.md` §7.1 ↔ op-disc §7.5 bidirectional cite; §7.4 polling capability; cite-comment target for A5 Part 1) + §13.4 (mode entry/exit; arc-22 deliverable 2.4 names this as renewal-confirm-on-entry surface) + §18 (user-tier housekeeping; reference for A17).
6. `substrate/MAJOR_PLINY.md` §5.9 / §5.9.4 (pre-branch hygiene + worktree convention) / §5.10 (signoff-accuracy; live-verify-before-claim) / §5.11 (HUMAN_paste archival) / §5.12 (dispatch-brief seat-identity naming). All self-applied per A11/A17 — orchestrator-side; cited here for downstream-reader awareness.
7. `substrate/templates/polling-cron-prompt-template.md` (161 lines; STEPs 1-6 + 6.5; substitution-slot table has 10 entries; this is the Part 1 STEP 1.5 insertion surface).
8. `substrate/templates/autonomous-mode-activation-template.md` (paste template; step-2 framing is the §7.1 author-tag instruction surface per arc-22 deliverable 1.5; recommend retaining).

### §2.2 — What PLINY's A7 spike consumed (per §6.3 — not re-derived)

The A7 spike is fully executed; this design.md consumes the verbatim findings posted on `stoa--jru` 2026-05-17 `[from: pliny-the-stoa]`. Summary (cited, not re-probed):

- **CronList fields:** `id` (8-char) / `cron-expression` / `recurrence` (one-shot|recurring) / `persistence` (session-only|durable) / `prompt` (truncated). NO backward-looking fields (`start_time`/`created_at`/`age`). NO forward-looking fields (`expires_at`/`next_fire`/`valid_until`).
- **CronUpdate primitive:** does NOT exist (ToolSearch returned only CronDelete + CronList).
- **Empirical expiry:** 7 days for recurring tasks; unambiguous per https://code.claude.com/docs/en/scheduled-tasks §Seven-day expiry + the CronCreate tool description self-document. One-shot tasks have no 7-day cap.
- **A7 decision-matrix verdict:** "Neither (cron metadata fully opaque)" row → Option 3 (setup-time scheduled renewal) → §11 step 1.5 insertion locus.
- **Substitution-slot values:** `{{EXPIRY_TOTAL_HOURS}}` = `168`; `{{RENEWAL_BUFFER_HOURS}}` = `24`; renewal cron fires at +144h (+6 days) from polling-cron creation.

I do not re-execute the spike. WebFetch / WebSearch is also not exercised against the docs page — PLINY's citation is authoritative; bypassing it would (a) waste the upstream seat per §6.3, (b) burn agent-time latency budget per op-disc §17.2 for zero new signal.

### §2.3 — What is LOCKED vs sub-decision

| ID | Status | DAEDALUS scope |
|---|---|---|
| A1 — single gauntlet | LOCKED | Cite-only |
| A2 — `[from:]` convention + 3-form layout | LOCKED | Cite + inline in §7.1 5th-beat |
| A2.5 — POLYBIUS-on-POLYBIUS scope | LOCKED | Cite in §7.7 procedure |
| A3 — slug normalization | LOCKED | Cite + inline in §7.1 + slot table |
| A4 — parsing teaching at op-disc §7 (4 cases) | LOCKED | Cite + content shape in §7.7 |
| **A5 — Part 1 insertion locus** | **DAEDALUS sub-decision** | **Picked below: (α) §7.7 new + §7.4 inline update + §7.1 5th-beat + MAJOR_POLYBIUS body-cite** |
| **A6 — STEP 1.5 mandatory vs optional** | **DAEDALUS sub-decision** | **Picked below: MANDATORY** |
| A7 — spike-first decision matrix | LOCKED (spike executed by PLINY) | Consume result |
| A8 — 24h renewal buffer | LOCKED | Cite |
| A9 — renewal-failure-mode acceptance | LOCKED | Inline at §11 step 1.5 (Option 3 path) per A10 |
| **A10 — Part 2 implementation locus** | **DAEDALUS sub-decision GATED by A7** | **Determined: §11 step 1.5 (Option 3); polling-cron template gets end-of-file pointer only** |
| A11 — self-application both Parts | LOCKED | Verify probes cover |
| A12 — cite-comment discipline | LOCKED | Plan listed §6 |
| A13 — authorship attribution unchanged | LOCKED | Verify probe |
| A14 — out-of-scope hard-locks | LOCKED | Cite + verify no probe-overshoot |
| A15 — source-ticket closure | LOCKED | Out of design.md scope (PLINY signoff) |
| A16 — §15 N=1 honesty | LOCKED | §8 below |
| A17 — pre-branch hygiene + worktree | LOCKED (self-applied) | PLINY-side; cited |

---

## §3 — Architectural decisions

### §3.1 — A5 pick: (α) new §7.7 + §7.4 inline update + §7.1 5th-beat + MAJOR_POLYBIUS.md §7 body-cite

**Pick:** (α) new top-level subsection §7.7 "bw-timeline parsing: author-attribution via tags"; §7.4 wording updated inline to bidirectional `[for:]`; §7.1 fifth-beat added introducing `[from:]` convention; MAJOR_POLYBIUS.md §7 cross-ref as small body-paragraph cite in an existing subsection.

**Rationale (why α not β):**

- **Parallel to existing §7.1-§7.6 numbering.** Arc 33's §27 (mechanical-script / agent-inspection split) and Arc 35's §28 (Co-Authored-By trailer) both added new top-level numbered subsections rather than densely extending existing ones. The pattern is established. §7.6 (Empirical lineage) is short and reads as a closer to the existing five-discipline section; appending §7.7 *after* §7.6 keeps §7.6's closer-position intact and gives the new parsing teaching its own load-bearing locus. (Note: arc-22 deliverable 1.2 suggested inserting §7.7 BEFORE §7.6 and renumbering §7.6 → §7.8; I am rejecting that — renumbering existing §7.6 breaks every cite-site that references §7.6 in current substrate. Append-only at §7.7 with §7.6 unchanged is strictly safer for cite-comment resolution.)
- **Cleaner reader contract.** A peer landing in §7 looking for "how do I parse a bw timeline" finds a top-level subsection with that exact framing rather than a dense §7.1 that mixes radio-check protocol + author-tag convention + parsing procedure into one wall. §7.7's job is parsing; §7.1's job stays the four-beat radio-check protocol + a fifth beat that introduces the tag convention (~10 lines), pointing forward to §7.7 for procedure.
- **MAJOR_POLYBIUS.md §7 body-cite (not new subsection).** Arcs 26-35 use a body-paragraph cite shape for POLYBIUS-tier specific framings that point back to universal-team canon in operating-disciplines.md (e.g., MAJOR_POLYBIUS.md §7.1 closes with "see `operating-disciplines.md` §7.5 for the universal-team framing"). Same shape here: add a short paragraph in MAJOR_POLYBIUS.md §7.4 (polling capability) — that section already names the polling-cron-prompt-template and cross-tier coordination context, so a one-paragraph cite "bw-timeline parsing per operating-disciplines.md §7.7" lands in the right semantic spot without growing a new §7.x subsection. Smaller surface; matches Arcs 26-35 cite pattern.

**Rejected alternative (β):** densely extending §7.1 with both the convention introduction AND the parsing procedure would (a) make §7.1 ~80 lines (currently ~10), (b) bury the four-beat radio-check protocol under sub-headings, (c) violate the "one section, one disciplinary surface" pattern that §7.1-§7.6 currently maintains. β reads cleaner if you imagine someone reading §7.1 top-to-bottom for the first time, but it reads worse for any of the dozens of cite-sites that point at "§7.1" intending "the four-beat radio-check protocol."

**§7.4 inline wording update:** §7.4's current first paragraph reads "When a project-tier or sub-project POLYBIUS needs cross-project context... post a comment on a relevant ticket in YOUR OWN bw prefixed with `[for: <upper-seat>]`." The "cross-tier UPWARD" framing is implicit in "project-tier or sub-project POLYBIUS needs cross-project context." Arc 36 v2 expands this to bidirectional: the `[for:]` tag means "addressed comment by sender to recipient" — either direction across any POLYBIUS pair. The wording update inlines this expansion in §7.4 and adds the `[from:]` cross-ref pointing forward to §7.1 5th-beat + §7.7. Exact wording in §5.1 deliverable spec below.

### §3.2 — A6 pick: STEP 1.5 mandatory

**Pick:** STEP 1.5 ships as MANDATORY in `substrate/templates/polling-cron-prompt-template.md`. Inserted between current STEP 1 (substantive read) and STEP 2 (peer-silence escalation). The polling cron parser mechanically executes the author-attribution step rather than relying on common-sense reading.

**Rationale:** the stoa--e39 empirical (~25-min coordination stall, 2026-05-04) is precisely the failure mode of "common-sense reading without mechanical author-attribution." The parser saw a `[for: POLYBIUS_the_stoa]` comment, attributed it to itself by content-pattern inference, and dropped the actual peer-activity signal on the floor. §7.7 prose canon is necessary but not sufficient — without a mechanical step in the polling-cron prompt body that builds `last_self_activity` / `last_peer_activity` from slug-matched tags, the prose canon is a discipline the parser is expected to perform from memory, which under load (multi-store unified poll, complex timeline, time pressure) is exactly when memory-based discipline fails. The template's job is to remove that memory load by encoding the procedure in the fire-loop body. arc-22 A6 documented this trade-off explicitly; user-tier POLYBIUS leans mandatory; I concur.

**Slot additions follow A3 normalization:** `{{SELF_SEAT_SLUG}}` + `{{PEER_SEAT_SLUG}}` join the substitution-slot table (lowercase, hyphenated, no whitespace; e.g., `polybius-the-stoa`). Display-form slots (`{{SELF_SEAT_NAME}}` / `{{PEER_SEAT_NAME}}`) remain for human-readable prose in heartbeat messages. STEP 1.5 slug-matches against the slug slots; STEP 3 heartbeat-post uses the slug slot in the leading `[radio-check <slug>]` tag.

### §3.3 — A10: §11 step 1.5 (Option 3) per PLINY A7 spike

**Determined:** Option 3 (setup-time scheduled renewal). Implementation lands at `substrate/operating-disciplines.md` §11 as new step 1.5 between current step 1 (Polling cron) and step 2 (Radio-check pattern). polling-cron-prompt-template.md gets an end-of-file pointer note ("cron expiry handled by separate one-shot renewal cron per op-disc §11 step 1.5; empirically-confirmed expiry: 168 hours / 7 days"). No STEP 7 added to the template — A7 spike confirmed Option 1's in-fire arithmetic path is non-applicable (no backward-looking or forward-looking field exposed).

**A9 failure-mode acceptance one-liner lands inline at the new §11 step 1.5** per arc-22 A6 placement guidance. Exact wording in §5.2 deliverable spec.

### §3.4 — A11 self-application acceptance

**Part 1 self-app:** POLYBIUS_the_stoa's coordination heartbeats on `stoa--jru` during this arc already carry `[from: polybius-the-stoa]` per the convention being shipped (verified live on the 2026-05-17T22:56:53Z POLYBIUS init handshake comment and subsequent heartbeats). PLINY signoff verifies Part 1 self-app at arc close by spot-checking that all POLYBIUS coordination comments on stoa--jru posted during the arc window carry the leading author-tag. Arc 36 IS the first worked example of the convention; design.md §7.7 mentions this property explicitly.

**Part 2 self-app:** POLYBIUS_the_stoa's polling cron (registered `c4482646` per init handshake) applies the §11 step 1.5 renewal logic that ships in Part 2. For an arc expected to ship in under 24 hours, the renewal cron will not fire during the arc itself, but the cron IS-able to fire it — which is the worked-example property. PLINY signoff verifies the polling cron's setup-state via `CronList` at arc close; the renewal-cron's existence (or, in the short-arc case, the renewal-cron-as-scheduled-but-not-yet-fired property) is the verifiable signal.

**Pattern parity:** mirrors Arc 35 (per-CAPTAIN trailers on own commits), Arc 34 / C2 (paste-archival in same gauntlet commit), Arc 33 (skill in same arc that defines pattern), Arc 29 (custom/ dir used by arc that defines it).

### §3.5 — A12 cite-comment discipline acceptance

Every new cross-ref site listed in §6 below resolves at every read-site after Phase 2 (ADA) ships. Specifically the cross-refs between:

- `operating-disciplines.md` §7.7 (new) ↔ §7.1 (5th-beat update) ↔ §7.4 (bidirectional update) ↔ §11 step 1.5 (new) ↔ §27 (mechanical-narrow precedent for "prose canon now; mechanical enforcement future if recurs" — referenced from §7.7 N=1 framing) ↔ §28 (trailer; cited by this design.md commit; not new cite-site from this arc)
- `MAJOR_POLYBIUS.md` §7.4 (Part 1 body-cite) ↔ §13.4 (Part 2 renewal-confirm-on-entry note)
- `substrate/templates/polling-cron-prompt-template.md` STEP 1.5 + end-of-file pointer → cite both new op-disc §7.7 (parsing teaching) and op-disc §11 step 1.5 (renewal mechanism)
- `substrate/templates/autonomous-mode-activation-template.md` step 2 prose → cite §7.1 5th-beat (author-tag convention)

The full plan + read-site verification table lives at §6.

### §3.6 — A13 authorship attribution acceptance

Arc 36 v2 changes prose only — no new files added under substrate/ that carry frontmatter `author:` fields (both polling-cron-prompt-template.md and autonomous-mode-activation-template.md already exist with `author: Denson Smith` and that line is NOT touched). design.md itself (this file) has no frontmatter author field — it's a build artifact under `agents/design/` consumed by the gauntlet, not a substrate canon file. PRE-COMMIT discipline per CAPTAIN_ADA.md §5.5 (which applies to any CAPTAIN committing files) audits frontmatter `author:` immutability on the ADA commit. §4.7 probe codifies this as a VERA-runnable check.

### §3.7 — A14 out-of-scope acceptance

Design.md hard-locks the following exclusions per A14 (so ADA does not scope-creep and ARGUS can frame what risks belong in this arc vs a future one):

- **No non-POLYBIUS author-tag extension.** PLINY, CAPTAINs, pair-programmer Majors are NOT required to author-tag in Arc 36. §7.7 procedure case 4 ("non-POLYBIUS comments") classifies them as substance comments that do NOT enter timeline-arithmetic. Future arc may extend with explicit scope.
- **No `[radio-check <slug>]` form change.** That form is already established (arc-21); §7.1 5th-beat introduces `[from:]` as the new sibling, not a replacement.
- **No retroactive legacy tagging.** Arc 36 is forward-only; §7.7 procedure case 4 also covers untagged pre-Arc-36 comments as "non-POLYBIUS or legacy — does NOT enter timeline-arithmetic" (low-confidence fallback).
- **No Option 2 watcher-cron.** A7 decision matrix rejected Option 2 up-front; the renewal logic stays per-seat unilateral (chained one-shots).
- **No mechanical parser enforcement.** No pre-comment hook that rejects un-tagged POLYBIUS comments. Arc 36 ships prose canon + parser-step template; mechanical enforcement is a future arc following §27's mechanical-narrow + agent-inspection pattern IF non-compliance recurs after Arc 36 ships.
- **No install.sh changes beyond what slot-table extension may require.** The new slots (`{{SELF_SEAT_SLUG}}`, `{{PEER_SEAT_SLUG}}`) are template-internal — install.sh deploys polling-cron-prompt-template.md as-is and the slots are filled by POLYBIUS at template-substitution time, not by install.sh. No new install.sh deploy-list wiring required. (§8.4 install.sh smoke beat is non-applicable for this arc since no new substrate files are added.)
- **No cross-tier-write-upward.** §7.5 write boundary is unchanged. §7.4 bidirectional `[for:]` is about TAG-direction (addressed-comment-meets-in-lower-tier), not write-direction.

**A9 failure-mode acceptance (revised after ARGUS F2 cold-audit, rev2; extended after ARGUS F4 cold-audit, rev3; rev5 F6 terminating-shape fold).** The renewal mechanism protects against FOUR failure modes / composition scenarios, with the recovery path explicit for each (full prose at §5.1.d "Failure-mode acceptance"):

1. **Cron-expiry boundary (+168h window).** Steady-state continuous protection via the renewal chain while the session stays alive and active.
2. **Renewal-chain break across multi-day continuous outage (> 6 days offline).** Recovery via peer-side radio-check escalation per §7.1 beat 3 (the original v1 framing — preserved).
3. **Session-lifecycle event — fresh conversation, `/clear`, session exit (ARGUS F2 cold-audit catch).** Per Claude Code docs Limitations + `MAJOR_POLYBIUS.md` §7.4 line 437: polling crons are session-only and die when the session exits. The design encodes `durable: true` on the renewal cron as honest intent (matches documented `CronCreate` tool schema) but does NOT rely on it as load-bearing recovery — the schema-documented flag has an open unresolved bug at anthropics/claude-code issue #40228 (opened 2026-03-28) where the persist does not actually happen. Load-bearing recovery is via `MAJOR_POLYBIUS.md` §9 step 7: long-running-engagement polling re-setup. This recovery is **PRINCIPAL-consent-required**, not transparent — §9 step 7 explicitly names "request PRINCIPAL consent and set up a polling cron." The operator's fresh-session activation surfaces the re-setup to PRINCIPAL; PRINCIPAL consents (or PRINCIPAL re-issues the autonomous-mode trigger, which then routes through `MAJOR_POLYBIUS.md` §13.4 step 2 → §11 setup checklist). Either way, a fresh cron pair is created. The orphan-renewal cleanup at the seam where a durable-surviving renewal cron fires in a session that has already re-bootstrapped is handled by **one-shot auto-delete** per Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks: "Claude schedules a single-fire task that deletes itself after running") — the renewal cron's STEP 1a no-op path posts an orphan-observation comment and exits; the post-fire auto-delete removes the stale renewal cron without any explicit self-CronDelete needed (rev5 F6 terminating-shape fold; see §5.1.d STEP 1a rev5 collapse). The session-lifecycle failure mode is therefore NOT a multi-day outage but any fresh-conversation start at any time; recovery is consent-mediated, not transparent. The renewal mechanism and §9 step 7 re-setup compose; one-shot auto-delete is the seam.
4. **Cadence-switch × renewal composition (ARGUS F4 cold-audit catch, rev3; rev4 m11 partial-failure-state recovery named; rev5 F6 terminating-shape fold).** The `substrate/templates/polling-cron-prompt-template.md` STEP 4 cadence-switch path rotates the polling cron (`CronDelete` old + `CronCreate` new at the new cadence) when a `[cadence: active|quiet]` tag is detected. Without rev3's F4 fix, this rotation would leave the paired renewal cron's inline `{{POLLING_CRON_ID}}` + `{{CADENCE}}` slot values stale — at +144h fire time, the renewal cron's STEP 1 cron-id exact-match would no-op AND the renewal chain would die silently. Rev3 fix: STEP 4 of the polling-cron template ALSO rotates the paired renewal cron — `CronDelete {{RENEWAL_CRON_ID}}` (best-effort cleanup; tolerates stale id — see rev5 terminating-shape note below) then `CronCreate` a fresh renewal cron carrying the NEW `POLLING_CRON_ID` + NEW `CADENCE` (rev4 F5: sourced from the polling cron's inline `{{RENEWAL_CRON_PROMPT_BODY}}` slot value per §5.3.a, enabling STEP 4.2 to execute deterministically). The renewal mechanism now composes cleanly with the cadence-switching pattern (§7.2 per-seat-unilateral) — each cadence-switch rotates BOTH crons in lock-step. **Rev5 F6 terminating-shape fold:** the rev4 4-step dance (STEP 4.1-4.4 with double re-bind for the chicken/egg of `{{RENEWAL_CRON_ID}}` cross-reference) collapses to a 2-step dance (STEP 4.1 polling rotate / STEP 4.2 renewal rotate). The collapse is structurally enabled by removing the renewal cron's STEP 1a self-CronDelete dependency on its own id (rev5 m10 collapse continued at structural layer): with one-shot auto-delete confirmed reliable per Claude Code docs, the renewal cron no longer needs to know its own id at fire time, so the polling cron's `{{RENEWAL_CRON_ID}}` slot can carry a "best-effort cleanup id that may be stale" — STEP 4.1's `CronDelete {{RENEWAL_CRON_ID}}` no-ops gracefully when the id refers to a dead renewal cron (CronDelete on a nonexistent id is a no-op per typical tool semantics; if the stale renewal cron is also still alive as an orphan, it self-cleans via one-shot auto-delete at +144h). The two re-bind sub-steps (rev4 STEP 4.3 + STEP 4.4) are dropped — the cron pair is structurally allowed to carry stale-id references without breakage because the cleanup mechanism is the one-shot auto-delete property, not the explicit self-CronDelete chain. **Partial-failure-state surface (rev4 m11; rev5 narrowed):** the rev5 2-step lock-step rotation has 2 CronCreate operations per cadence-switch (down from 4 in rev4). If the polling-cron fire is interrupted between STEP 4.1 and STEP 4.2, the cron pair is left in an intermediate state with a new polling cron alive but no paired renewal cron yet; the orphaned old renewal cron self-cleans at its +144h auto-delete and the new polling cron expires at +168h with no successor. Recovery is via the SAME peer-side radio-check escalation surface as the broader cron-mechanism-failure modes — §7.1 beat 3 self-silence threshold (>60 min) trips, peer surfaces "lost contact" to PRINCIPAL, PRINCIPAL re-triggers or §9 step 7 fires on next-session activation, both converging on a fresh §11 step 1.5 setup. One-shot auto-delete cleans up any surviving partial-state renewal cron. No new recovery infrastructure required. See §5.1.d Failure-mode scenario 4 for the full prose.

This A9 broader-failure-mode-acceptance is what ARGUS-rev5 evaluates against; the rev2 framing missed the cadence-switch composition scenario per ARGUS-rev2 F4. Rev3 adds scenario 4 as a fourth composition concern STEP 4 of the polling-cron template handles directly (vs accept-as-failure-mode). Rev4 names the 4-step-dance partial-failure-state recovery explicitly. Rev5 collapses the 4-step dance to a 2-step dance by adopting the terminating-shape pick (skip STEP 1a self-CronDelete; rely on one-shot auto-delete per Claude Code docs — verified by WebFetch on https://code.claude.com/docs/en/scheduled-tasks "Set a one-time reminder" section: "Claude schedules a single-fire task that deletes itself after running"). The structural property the design now rests on is the one-shot auto-delete reliability; see §8.2 N=1 for the honest framing of that dependency.

### §3.8 — A16 §15 N=1 honesty acceptance

§8 below carries the §N=1 provenance subsection per the Arcs 27-35 pattern, framed for both Parts.

### §3.9 — A17 self-applied pre-branch hygiene + worktree convention

PLINY-side already executed per MAJOR_PLINY.md §5.9 / §5.9.4 (worktree at `.claude/worktrees/arc-36-build/` exists; local main = origin/main at `e71615f`; no orphan arc-build branches per pre-flight verification). PLINY signoff per §5.10 live-verifies cleanup at arc close. Cited here for downstream-reader awareness — no design.md action required.

---

## §4 — Falsification probes (for VERA)

Each probe is a concrete command or check VERA can re-execute against the built artifact. PASS = expected output observed; FAIL = output deviates and ADA's edit needs revision before VERA verdict.

### §4.1 — Part 1 probes

**§4.1.1 — `operating-disciplines.md` §7.1 fifth-beat present with correct convention text + header count updated**

```bash
awk '/^### 7\.1/,/^### 7\.2/' substrate/operating-disciplines.md | grep -cE '^Five beats:'
# Expected: 1 ("Four beats:" header updated to "Five beats:" to match the new count)

awk '/^### 7\.1/,/^### 7\.2/' substrate/operating-disciplines.md | grep -cE '^Four beats:'
# Expected: 0 (old "Four beats:" header fully replaced)

grep -nE '^5\. \*\*Author-tag convention' substrate/operating-disciplines.md
# Expected: one match inside §7.1 (line number > §7.1 header line, < §7.2 header line)

awk '/^### 7\.1/,/^### 7\.2/' substrate/operating-disciplines.md | grep -cE '\[radio-check <self-seat-slug>\]|\[for: <recipient-seat-slug>\] \[from: <sender-seat-slug>\]|\[from: <self-seat-slug>\]'
# Expected: ≥3 (all three tag-form examples present in the 5th-beat body; beats 1 + 4 also use slug-form placeholders so total may be > 3)

awk '/^### 7\.1/,/^### 7\.2/' substrate/operating-disciplines.md | grep -c 'Slug normalization'
# Expected: ≥1 (slug-normalization paragraph present per A3)

awk '/^### 7\.1/,/^### 7\.2/' substrate/operating-disciplines.md | grep -cE '\[radio-check <seat>\]|\[radio-check <self>'
# Expected: 0 (legacy `<seat>` / `<self>` placeholder shape fully replaced with slug-form in beats 1 + 4)
```

**§4.1.2 — `operating-disciplines.md` §7.4 wording updated to bidirectional (no "UPWARD-only" framing remains)**

```bash
awk '/^### 7\.4/,/^### 7\.5/' substrate/operating-disciplines.md | grep -E 'upward[- ]only|UPWARD requests only|^[^a-zA-Z]*upward\.only'
# Expected: zero matches (anchored to old wording shape; case-sensitive to avoid bidirectional-prose hits; drops over-broad `cross-tier upward` per Arc 41 pqn Item 1.a)

awk '/^### 7\.4/,/^### 7\.5/' substrate/operating-disciplines.md | grep -cE 'bidirectional|either direction|sender to recipient'
# Expected: ≥1 (new bidirectional framing present)
```

**§4.1.3 — `operating-disciplines.md` §7.7 (new) present with parsing procedure covering all 4 cases**

```bash
grep -nE '^### 7\.7 ' substrate/operating-disciplines.md
# Expected: one match (the new §7.7 header present)

awk '/^### 7\.7/,/^### 7\.8|^## /' substrate/operating-disciplines.md | grep -cE '\[radio-check|\[for: .* \[from: |\[from: |untagged|non-POLYBIUS|legacy'
# Expected: ≥4 (all four cases — radio-check, for+from, from-only, untagged/non-POLYBIUS/legacy — appear in procedure)

awk '/^### 7\.7/,/^### 7\.8|^## /' substrate/operating-disciplines.md | grep -cE 'last_self_activity|last_peer_activity'
# Expected: ≥1 (procedure names the load-bearing derived values)

awk '/^### 7\.7/,/^### 7\.8|^## /' substrate/operating-disciplines.md | grep -c '2026-05-04'
# Expected: ≥1 (empirical anchor for stoa--e39 named)
```

**§4.1.4 — `MAJOR_POLYBIUS.md` §7 cross-ref body-cite present**

```bash
awk '/^### 7\.4/,/^### 7\.5/' substrate/MAJOR_POLYBIUS.md | grep -cE 'operating-disciplines\.md §7\.7|bw-timeline parsing'
# Expected: ≥1 (cross-ref cite-comment lands in §7.4 polling-capability subsection)
```

**§4.1.5 — `polling-cron-prompt-template.md` STEP 1.5 present with attribution-build logic**

```bash
grep -nE '^STEP 1\.5' substrate/templates/polling-cron-prompt-template.md
# Expected: one match between STEP 1 and STEP 2 in the template body

awk '/^STEP 1\.5/,/^STEP 2/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\{\{SELF_SEAT_SLUG\}\}|\{\{PEER_SEAT_SLUG\}\}'
# Expected: ≥2 (both slug slots referenced in attribution logic)

awk '/^STEP 1\.5/,/^STEP 2/' substrate/templates/polling-cron-prompt-template.md | grep -cE 'last_self_activity|last_peer_activity'
# Expected: ≥2 (STEP 1.5 builds both derived timestamp values)

awk '/^STEP 1\.5/,/^STEP 2/' substrate/templates/polling-cron-prompt-template.md | grep -c 'operating-disciplines.md §7.7'
# Expected: ≥1 (STEP 1.5 cites §7.7 parsing procedure)
```

**§4.1.6 — Substitution-slot table extended with SLUG slots**

```bash
grep -cE '\{\{SELF_SEAT_SLUG\}\}|\{\{PEER_SEAT_SLUG\}\}' substrate/templates/polling-cron-prompt-template.md
# Expected: ≥4 (each slot named in table once, then referenced in STEP 1.5 ≥1 time each, then in usage example ≥1 time each)

awk '/^## Substitution slots/,/^---$/' substrate/templates/polling-cron-prompt-template.md \
  | grep -cE '\{\{SELF_SEAT_SLUG\}\}|\{\{PEER_SEAT_SLUG\}\}'
# Expected: 2 (both new slots present in the slot table itself; pattern drops the table-row-pipe + backtick anchors per Arc 41 pqn Item 1.c — the slot-name match alone is unambiguous within the slot-table awk-bracketed region, no shell-escape fragility)
```

**§4.1.7 — STEP 2 and STEP 3 reference derived timestamps from STEP 1.5**

```bash
awk '/^STEP 2/,/^STEP 3/' substrate/templates/polling-cron-prompt-template.md | grep -c 'last_peer_activity'
# Expected: ≥1 (STEP 2 reads peer-silence from STEP 1.5's derived value, not raw timestamps)

awk '/^STEP 3/,/^STEP 4/' substrate/templates/polling-cron-prompt-template.md | grep -c 'last_self_activity'
# Expected: ≥1 (STEP 3 reads self-heartbeat-due from STEP 1.5's derived value)
```

**§4.1.8 — STEP 3 heartbeat-post uses SLUG slot in leading tag**

```bash
awk '/^STEP 3/,/^STEP 4/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\[radio-check \{\{SELF_SEAT_SLUG\}\}\]'
# Expected: ≥1 (radio-check heartbeat uses slug, not display-form name)
```

**§4.1.9 — Usage example at bottom of template populates SLUG slots + shows slug-form tags**

```bash
awk '/^## Usage example/,EOF' substrate/templates/polling-cron-prompt-template.md | grep -cE '\{\{SELF_SEAT_SLUG\}\}.*=.*polybius-the-stoa|\{\{PEER_SEAT_SLUG\}\}.*=.*user-tier-polybius|polybius-the-stoa|user-tier-polybius'
# Expected: ≥2 (example block populates both slug slots with slug-form values)

awk '/^## Usage example/,EOF' substrate/templates/polling-cron-prompt-template.md | grep -cE '\[radio-check (polybius-the-stoa|user-tier-polybius|project-tier-polybius)'
# Expected: ≥1 (example handshake shows slug-form leading tag, not display-form)
```

**§4.1.10 — `autonomous-mode-activation-template.md` step 2 carries author-tag instruction**

```bash
awk '/^2\. Radio-check pattern/,/^3\. Cross-tier/' substrate/templates/autonomous-mode-activation-template.md | grep -cE 'operating-disciplines\.md §7\.1|author-tag|\[from:'
# Expected: ≥1 (one-line author-tag instruction landed per arc-22 deliverable 1.5)
```

### §4.2 — Part 2 probes

**§4.2.1 — `operating-disciplines.md` §11 step 1.5 present with renewal-cron CronCreate body + 168h expiry + 24h buffer**

```bash
awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -cE '^\*\*1\.5'
# Expected: 1 (step 1.5 bolded numbered entry between step 1 and step 2)

awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -cE '168|7 days|seven[- ]day'
# Expected: ≥1 (empirically-confirmed expiry constant named)

awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -cE '24h|24 hours|RENEWAL_BUFFER_HOURS'
# Expected: ≥1 (24h buffer named)

awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -cE '\+144|144 hours|144h|expiry_total.*buffer'
# Expected: ≥1 (renewal cron fires at +144h / +(expiry - buffer))

awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -c 'CronCreate'
# Expected: ≥1 (renewal-cron CronCreate primitive named in body)

awk '/^## 11\./,/^## 12\./' substrate/operating-disciplines.md | grep -cE 'one-shot|chained'
# Expected: ≥1 (the renewal cron is one-shot; chained self-renewal property named)
```

**§4.2.2 — A9 broader-failure-mode acceptance present at §11 step 1.5 (rev2 broadened per ARGUS F2)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'radio-check|peer-side|recovery|§7\.1|§C\.1'
# Expected: ≥1 (failure-mode acceptance names peer-side radio-check escalation as recovery for failure mode 2)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -ciE 'no.*watchdog|no additional'
# Expected: ≥1 (case-insensitive to match 'No' / 'no' prose variants; explicitly accepts the failure mode rather than mitigating via watcher cron; -i added per Arc 41 pqn Item 1.b)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'session-lifecycle|fresh conversation|/clear|session exit'
# Expected: ≥1 (rev2 F2 fold — session-lifecycle failure mode named explicitly, not just continuous-outage)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'MAJOR_POLYBIUS\.md §13\.4|§13\.4 step 2|autonomous-mode entry'
# Expected: ≥1 (rev2 F2 fold — §13.4 re-entry named as the load-bearing recovery path for session-lifecycle loss)
```

**§4.2.2a — `durable: true` named explicitly on the renewal cron (rev2 F2 + ARGUS m2)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'durable: true|durable:.*true|durable.*true'
# Expected: ≥1 (renewal cron's durable parameter named explicitly; resolves ARGUS m2)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE '40228|issue.*40228|github\.com/anthropics/claude-code'
# Expected: ≥1 (open-bug provenance cited so the design's honest-intent encoding is auditable)
```

**§4.2.2b — Renewal-cron self-discovery uses {{POLLING_CRON_ID}} exact-match (rev2 F3 Handle b)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE '\{\{POLLING_CRON_ID\}\}|POLLING_CRON_ID'
# Expected: ≥2 (slot named in renewal-cron prompt body; cron-id exact-match strategy depends on it)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'cron-id == |exact-match|cron-id, not text-search|cron-id not on prompt-text'
# Expected: ≥1 (STEP 1 of renewal-cron prompt body matches by cron-id, NOT by prompt-body text)
```

**§4.2.2c — Renewal-cron prompt body carries slot values inline (rev2 F1)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'inline|slot values inline|engagement-specific at setup time|pre-substituted'
# Expected: ≥2 (the F1 structural property — slot values are pre-substituted INTO the renewal-cron prompt body at CronCreate time)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'no template-reference at fire time|does not reference any template by file|template-reference at fire time'
# Expected: ≥1 (explicit no-template-reference-at-fire-time property)
```

**§4.2.2d — STEP 1a polling-cron-missing no-op branch (rev2 F2 seam; rev5 F6 terminating-shape: explicit self-CronDelete REMOVED, one-shot auto-delete handles cleanup)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'STEP 1a|polling-cron-missing|orphan-renewal|no-op'
# Expected: ≥2 (the STEP 1a branch present)

# Rev5 F6 fold: STEP 1a no longer carries explicit self-CronDelete; relies on one-shot
# auto-delete per Claude Code docs. The probe checks that one-shot auto-delete is named
# as the cleanup mechanism + that the {{RENEWAL_CRON_ID}} slot's best-effort semantics
# are surfaced:
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'one-shot auto-delete|auto-delete|single-fire task that deletes itself|RENEWAL_CRON_ID'
# Expected: ≥2 (one-shot auto-delete named as the cleanup mechanism + RENEWAL_CRON_ID slot named — slot is now best-effort cleanup per rev5 F6)
```

**§4.2.2e — Renewal-cron STEP 4 specifies LOCAL-TIME arithmetic (rev3 m8)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'LOCAL|local time|local-time|local timezone'
# Expected: ≥2 (STEP 4 prose + Claude Code docs cite both name local-time interpretation)

# Worked-example cron expression must NOT carry a Z suffix (Z is UTC-zulu shorthand; misleading for local-time-interpreted cron expressions):
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE '20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z'
# Expected: 0 (no Z-suffix timestamps in worked example post-rev3 m8 fix)

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'code\.claude\.com/docs/en/scheduled-tasks'
# Expected: ≥1 (cite to Claude Code docs for local-time-interpretation property)
```

**§4.2.2f — Renewal-cron worked-example enumerates all 13 slot values inline (rev3 m4)**

```bash
# All 13 slot names should appear in the worked-example block at §5.1.d (10 polling + 2 SLUG + 1 RENEWAL_CRON_ID):
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE '\{\{COORDINATION_TICKET\}\}|\{\{WATCHED_STORES\}\}|\{\{WATCHED_TICKETS\}\}|\{\{PEER_SEAT_NAME\}\}|\{\{SELF_SEAT_NAME\}\}|\{\{SELF_SEAT_SLUG\}\}|\{\{PEER_SEAT_SLUG\}\}|\{\{CRON_ID\}\}|\{\{POLLING_CRON_ID\}\}|\{\{RENEWAL_CRON_ID\}\}|\{\{ALARM_THRESHOLD_MINUTES\}\}|\{\{HEARTBEAT_INTERVAL_MINUTES\}\}|\{\{CADENCE\}\}|\{\{ESCALATION_TRIGGERS\}\}'
# Expected: ≥13 (all slot names appear at least once each in the worked-example enumeration block; some may appear multiple times, so the floor is 13)
```

**§4.2.2g — Renewal-cron F4 lock-step composition with cadence-switch (rev3)**

```bash
# §11 step 1.5 prose must reference the slot-lifecycle dance + name §5.3 STEP 4 as the cadence-switch composition site:
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'slot-lifecycle|chicken/egg|F4|lock-step|RENEWAL_CRON_ID'
# Expected: ≥2 (slot-lifecycle note present + F4 composition named)

# Cite to §9 step 7 (PRINCIPAL-consent-required recovery; rev3 m5):
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'MAJOR_POLYBIUS\.md §9 step 7|§9 step 7|PRINCIPAL consent|PRINCIPAL-consent|consent-required|consent.required'
# Expected: ≥2 (§9 step 7 cited + consent-required property named explicitly)
```

**§4.2.3 — `polling-cron-prompt-template.md` end-of-file pointer present**

```bash
tail -25 substrate/templates/polling-cron-prompt-template.md | grep -cE 'operating-disciplines\.md §11.*step 1\.5|cron expiry handled|empirically-confirmed expiry'
# Expected: ≥1 (end-of-file pointer cites §11 step 1.5; names empirically-confirmed expiry)

tail -25 substrate/templates/polling-cron-prompt-template.md | grep -cE '168|7 days'
# Expected: ≥1 (empirical expiry constant named in pointer)
```

**§4.2.4 — No STEP 7 mistakenly added to polling-cron-prompt-template.md**

```bash
grep -cE '^STEP 7' substrate/templates/polling-cron-prompt-template.md
# Expected: 0 (Option 1 path does NOT apply; no STEP 7 — only end-of-file pointer per Option 3)
```

**§4.2.4a — Polling-cron template body opens with {{COORDINATION_TICKET}} (rev2 F3 Handle a)**

```bash
# The re-ordered opening line per §5.3.0 must lead with the ticket id slot, not the SELF_SEAT_NAME slot:
grep -nE '^\[scheduled poll fire — ticket \{\{COORDINATION_TICKET\}\}' substrate/templates/polling-cron-prompt-template.md
# Expected: 1 match (rev2 F3 Handle a re-order shipped)

grep -nE '^\[scheduled poll fire — \{\{SELF_SEAT_NAME\}\} watching' substrate/templates/polling-cron-prompt-template.md
# Expected: 0 matches (the v1 ordering is fully replaced)
```

**§4.2.4b — Polling-cron template STEP 4 cadence-switch ALSO rotates paired renewal cron (rev3 F4 Handle (i))**

```bash
# STEP 4 must reference RENEWAL_CRON_ID slot in its body (lock-step rotation):
awk '/^STEP 4/,/^STEP 5/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\{\{RENEWAL_CRON_ID\}\}|RENEWAL_CRON_ID|renewal cron|paired renewal'
# Expected: ≥2 (STEP 4 body names the renewal-cron rotation)

# STEP 4 must perform CronDelete on the renewal cron in addition to the polling cron:
awk '/^STEP 4/,/^STEP 5/' substrate/templates/polling-cron-prompt-template.md | grep -cE 'CronDelete.*RENEWAL_CRON_ID|CronDelete \{\{RENEWAL_CRON_ID\}\}'
# Expected: ≥1 (renewal cron CronDelete'd as part of lock-step rotation)

# STEP 4 must perform CronCreate for the new renewal cron with new polling-cron-id + new cadence:
awk '/^STEP 4/,/^STEP 5/' substrate/templates/polling-cron-prompt-template.md | grep -cE 'CronCreate.*renewal|new renewal|fresh renewal|<new_renewal_cron_id>'
# Expected: ≥1 (replacement renewal cron created with updated slots)

# Substitution-slot table must include {{RENEWAL_CRON_ID}} (rev3 F4 slot addition):
awk '/^## Substitution slots/,/^---$/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\| \`\{\{RENEWAL_CRON_ID\}\}\`'
# Expected: 1 (new slot present in slot table)

# End-of-file usage example must include {{RENEWAL_CRON_ID}} slot value populated:
awk '/^## Usage example/,EOF' substrate/templates/polling-cron-prompt-template.md | grep -cE '\{\{RENEWAL_CRON_ID\}\}'
# Expected: ≥1 (usage example block populates the new slot)
```

**§4.2.5 — `MAJOR_POLYBIUS.md` §13.4 renewal-confirm-on-entry note present** (arc-22 deliverable 2.4 — recommend keeping)

```bash
awk '/^### 13\.4/,/^## 14\./' substrate/MAJOR_POLYBIUS.md | grep -cE 'operating-disciplines\.md §11|cron.*expiry|renewal'
# Expected: ≥1 (one-line note in mode-entry procedure cites §11 step 1.5 renewal mechanism)
```

### §4.3 — Cite-comment resolution probes

Every new section cite in the diff must point to a real section after Phase 2 ship. The probe walks each cite-site and verifies the target exists.

**§4.3.1 — New cite-sites all resolve (rev3 extension per ARGUS m7)**

```bash
# Build a list of every section-form cite-site touched by the arc:
grep -rnE 'operating-disciplines\.md §7\.7|operating-disciplines\.md §11.*step 1\.5|MAJOR_POLYBIUS\.md §7\.4|MAJOR_POLYBIUS\.md §9 step 7' substrate/ \
  | grep -vE '^Binary file|/arcs/'
# Expected: ≥6 (cites land at the new §7.7 from §7.1, §7.4, MAJOR_POLYBIUS.md §7.4, polling-cron-prompt-template.md STEP 1.5, the renewal end-of-file pointer, and §11 step 1.5's session-lifecycle recovery cite to MAJOR_POLYBIUS.md §9 step 7)

# Build a list of URL-form cite-sites (rev3 m7 extension — three new URL-form cites
# added in rev2 F2 fold; m7 surfaced that the rev2 regex did not cover them):
grep -rnE 'github\.com/anthropics/claude-code/issues/[0-9]+|code\.claude\.com/docs/en/scheduled-tasks' substrate/ \
  | grep -vE '^Binary file|/arcs/'
# Expected: ≥2 (issue #40228 + Claude Code docs scheduled-tasks URL both referenced from §11 step 1.5; may also be referenced from polling-cron-template end-of-file pointer)

# For each cite, verify the target section exists:
grep -nE '^### 7\.7 |^### 7\.4 |^### 13\.4 |^\*\*1\.5|^7\. \*\*If this engagement is long-running' substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md
# Expected: each target header / numbered list item present exactly once at its expected file
# (Note: §9 step 7 is a numbered-list item, not a `### N.N` heading — the `^7\. ` pattern catches the long-running-engagement entry per MAJOR_POLYBIUS.md §9 numbered list line 507.)
```

**§4.3.2 — No dangling cite to a section the arc removed or renumbered**

```bash
# §7.6 (Empirical lineage) is preserved at §7.6 (not renumbered to §7.8 per design pick); existing §7.6 cites still resolve:
grep -nE 'operating-disciplines\.md §7\.6' substrate/ -r | grep -vE '^Binary file|/arcs/' | head -5
# Expected: any cite-sites that reference §7.6 still find the §7.6 Empirical-lineage section at its original location
grep -nE '^### 7\.6 Empirical lineage' substrate/operating-disciplines.md
# Expected: one match (section preserved)
```

### §4.4 — Self-application probes

**§4.4.1 — Part 1 self-app: POLYBIUS comments on stoa--jru during arc-36 carry [from:] tag**

```bash
bw show stoa--jru 2>&1 | grep -cE '\[from: polybius-the-stoa\]|\[from: user-tier-polybius\]|\[from: pliny-the-stoa\]|\[from: daedalus-the-stoa\]|\[from: argus-the-stoa\]|\[from: ada-the-stoa\]|\[from: vera-the-stoa\]|\[from: cato-the-stoa\]|\[from: zeno-the-stoa\]'
# Expected: ≥3 (every POLYBIUS coordination comment during arc-36 has leading [from:] author-tag; sub-CAPTAIN comments may also use the convention voluntarily — Arc 36 mandates POLYBIUS only per A2.5, but extension is non-rejecting)

# PLINY signoff verifies that NO POLYBIUS coordination comment posted during the arc window LACKS a [from:] tag:
bw show stoa--jru 2>&1 | awk '/^\*\*2026-05-1[7-9]T/,EOF' | grep -B 1 '^> ' | grep -cE '^> \[from: '
# Expected: a count consistent with the number of POLYBIUS comments observed in the window
```

**§4.4.2 — Part 2 self-app: polling cron observable + chicken/egg honest-scope (rev3 m6 rewrite)**

ARGUS-rev2 m6 surfaced that the rev2 §4.4.2 probe was internally inconsistent: it asserted that the POLYBIUS_the_stoa polling cron `c4482646` should be "registered with the renewal mechanism per the new §11 step 1.5," but `c4482646` was created at autonomous-mode-setup time BEFORE the canon shipping in this arc was available — so by construction, no renewal cron exists paired with it. The probe rewrite below names the chicken/egg honestly per the PLINY-routed disposition.

```bash
# (a) WORKED-EXAMPLE SIGNAL for Arc 36 self-app: c4482646 still in CronList at arc close.
# This is the signal that POLYBIUS_the_stoa's polling cron survived the arc engagement
# (proving the cron-as-coordination-substrate worked). Run in the POLYBIUS session at arc close:
# Expected (CronList output): cron id c4482646 present, recurring: true, cadence */5,
# prompt body references stoa--jru.

# (b) NO RENEWAL CRON IS EXPECTED for Arc 36 itself (per §9.5 chicken/egg).
# The §11 step 1.5 renewal-mechanism canon does NOT ship until this arc closes.
# POLYBIUS_the_stoa's autonomous-mode-setup at 2026-05-17 ran the pre-Arc-36 §11 checklist
# (which had no step 1.5), so the polling cron c4482646 has NO paired renewal cron and
# none is expected. PLINY signoff at arc close MUST NOT assert "renewal cron present for
# c4482646" — that would be a false-positive failure of the Part 2 self-app probe.
# Expected (CronList output): exactly one cron entry related to stoa--jru (the polling
# cron c4482646); no paired renewal cron at the +144h mark.

# (c) FUTURE ARCS are where renewal-cron registration begins being observable.
# The first POLYBIUS autonomous-mode setup that runs AFTER Arc 36 ships executes the
# new §11 step 1.5 — that setup creates the first observable polling-cron + renewal-cron
# pair under shipped canon. PLINY signoff for Arc 36 itself relies on (a) above as the
# worked-example signal; the renewal-mechanism worked-example accretes on future engagements.

# Self-app honest-scope: this matches Arc 35's self-application limitation pattern
# (per-CAPTAIN trailers exist on commits made during Arc 35, but Arc 35's own dispatch
# commits pre-date the trailer canon and don't carry it). §9.5 captures this as a
# known-limitation parallel to Arc 35; the §8.2 N=1 framing names the renewal-mechanism
# as N=0 worked-when-applied at arc close (worked-when-applied accretes on next arc).
```

(Resolves ARGUS-rev2 m6 internal-consistency concern. The §9.5 cross-ref is updated to reflect this rewrite — the chicken/egg is the worked-example property of THIS arc, not a limitation that needs apologizing for.)

### §4.5 — Out-of-scope / A14 probes (no probe-overshoot)

**§4.5.1 — No non-POLYBIUS author-tag enforcement built**

```bash
# Verify the arc does NOT add any pre-comment hook, lint, or CI check enforcing author-tags:
ls .claude/hooks/ 2>&1 | head -3
git diff main...arc-36/build -- '.claude/hooks/' 2>&1 | head -3
# Expected: no hook additions

# Verify §7.7 procedure case 4 explicitly names PLINY / CAPTAIN / pair-programmer Majors as exempt:
awk '/^### 7\.7/,/^### 7\.8|^## /' substrate/operating-disciplines.md | grep -cE 'PLINY|CAPTAIN|pair-programmer'
# Expected: ≥1 (the exempt-class is named per A2.5; A14 hard-lock visible at canon-read time)
```

**§4.5.2 — No retroactive tagging**

```bash
git diff main...arc-36/build -- 'beadwork/' 2>&1 | head -3
# Expected: zero diff on the beadwork branch from this arc (the arc-build branch should not touch bw history at all)
```

**§4.5.3 — No Option 2 watcher-cron prose**

```bash
# Search for NEW watcher-cron prose, excluding rejection-context lines
# (per Arc 41 pqn Item 1.d — original probe matched the anti-pattern's
# rejection prose, not new affirmative use):
grep -rnE 'watcher cron|watchdog cron|separate watcher' substrate/operating-disciplines.md substrate/templates/ \
  | grep -vE 'rejected|anti-pattern|Option 2|not the substrate|do NOT'
# Expected: zero matches (rejection-context lines excluded; only NEW watcher-cron prose surfaces)
```

**§4.5.4 — install.sh untouched**

```bash
git diff main...arc-36/build -- substrate/install.sh
# Expected: empty diff (no install.sh changes per A14 — slot additions are template-internal)
```

### §4.6 — Cosmetic + voice probes

**§4.6.1 — Voice grep clean**

```bash
# Scope to git-diff +-lines added by arc-36/build relative to main
# (per Arc 41 pqn Item 1.e — whole-file grep caught pre-existing legacy
# `the user` references unrelated to the arc's new content):
git diff main...arc-36/build -- substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md \
  | grep -E '^\+' | grep -vE '^\+\+\+' | grep -E '\b[Cc]olonel\b|\bthe user\b'
# Expected: zero non-template +-line hits in new arc-36 content
```

**§4.6.2 — Author-tag example tags appear in new content**

```bash
grep -E '\[from: |\[for: .* \[from: ' substrate/operating-disciplines.md substrate/templates/polling-cron-prompt-template.md | head -10
# Expected: ≥3 matches across new content (5th-beat + §7.7 procedure + STEP 1.5 + usage example)
```

### §4.7 — Authorship audit (per A13)

```bash
# Verify file-frontmatter author: fields are unchanged on every edited substrate file:
head -5 substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md | grep -E '^author:'
# Expected: every file shows `author: Denson Smith` exactly; no name-substitution

# Verify Co-Authored-By trailer present on DAEDALUS design.md commit + every ADA build commit:
git log arc-36/build --pretty='%H %s%n%(trailers:key=Co-Authored-By)' -n 20 | grep -cE 'CAPTAIN_DAEDALUS_the-stoa|CAPTAIN_ADA_the-stoa'
# Expected: ≥2 (design commit + at least one ADA build commit)
```

### §4.8 — Credential-discipline non-applicability gate (per `CAPTAIN_DAEDALUS_the_stoa.md` §6.6)

Arc 36 v2 touches no credentialed third-party API or cloud service. CronCreate / CronList / CronDelete are local Claude Code primitives (not credentialed third-party). bw operations are local git ops. No CI workflow authored; no API token, OAuth scope, or service account in scope. §6.6 credential discipline is NON-APPLICABLE to this arc; explicit gate-check probe:

```bash
# Verify no credentialed-CLI invocation appears in any arc-36 +-line edit
# (per Arc 41 pqn Item 1.e — git-diff +-line scoping to arc-36/build content
# only; existing references in unrelated sections are scoped out structurally
# rather than by stale "unrelated sections" hand-wave):
git diff main...arc-36/build -- substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md \
  | grep -E '^\+' | grep -vE '^\+\+\+' \
  | grep -E 'op (read|run)|gcloud |gh auth |aws |kubectl |vercel |railway |fly '
# Expected: zero +-line matches in arc-36/build edits
```

---

## §5 — Deliverables

File-by-file edit specs concrete enough that ADA can build deterministically. Wording is the design's recommendation; ADA may refine voice/phrasing inside the structural constraint each spec sets.

### §5.1 — `substrate/operating-disciplines.md`

**§5.1.a — §7.1 fifth-beat insert (immediately before `### 7.2 Adaptive polling cadence`)**

Insert at the end of §7.1's "Four beats" numbered list — extending it to 5 beats. ALSO update the plain-prose line introducing the numbered list from "Four beats:" to "Five beats:" to match the new count (per ARGUS m3 — this is a plain-prose paragraph at line ~125 introducing the numbered list, not a markdown heading; ADA should read §5.1.a literally and not look for a `#`/`##` heading), AND tighten the in-bracket placeholder names in beats 1 + 4 to slug-form (`<self-seat-slug>` in place of `<seat>` / `<self>`) so the existing beats' examples match the §7.1 beat 5 + §7.7 slug-normalization rule. This is a cosmetic-but-load-bearing change — it removes the example-vs-canon drift that would otherwise let a reader of beats 1 + 4 reach for the legacy `<seat>` placeholder shape:

```
1. **Initialization handshake.** When two seats begin coordinating on a shared
   ticket, each posts a `[radio-check <self-seat-slug>]` comment naming its
   cron id and current cadence. ...
4. **Closure handshake.** When the coordination ticket closes, both peers post
   a final `[radio-check <self-seat-slug> standing down]` comment ...
```

Then insert the new beat 5 at the end:

```
5. **Author-tag convention (POLYBIUS-on-POLYBIUS coordination).** Every
   coordination comment posted by a POLYBIUS instance carries an explicit
   sender tag. Three forms cover the cases:
   - Self-heartbeat: `[radio-check <self-seat-slug>]` — form unchanged from
     beat 1; slug-normalization rule below applies.
   - Cross-seat addressed: `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]`
     — both tags mandatory. This expands the prior `[for:]` convention
     (currently §7.4) from cross-tier upward only (project→user) to bidirectional;
     `[from:]` is new in Arc 36.
   - Own-bw substantive (not addressed to a specific peer):
     `[from: <self-seat-slug>]` — for status updates, gauntlet phase comments,
     decisions logged in own bw without a specific recipient.

   **Slug normalization:** lowercase, hyphenated, no whitespace. Example
   slugs: `user-tier-polybius`, `polybius-the-stoa`, `polybius-ariadne-core`.
   The slug matches the role-file slug used by
   `substrate/templates/autonomous-mode-activation-template.md`. Display-form
   names (e.g., "user-tier POLYBIUS") may appear in prose within comment
   bodies; the LEADING tag always uses the slug.

   **Scope:** the convention applies to POLYBIUS instances only (user-tier
   POLYBIUS, project-tier POLYBIUS, sub-project POLYBIUS). PLINY, CAPTAINs,
   and pair-programmer Majors are NOT required to author-tag — their
   substantive comments do not enter the timeline-arithmetic that drives
   radio-check / heartbeat thresholds. See §7.7 for the parsing procedure
   and the empirical anchor.

   The convention exists so peers reading the timeline can attribute each
   POLYBIUS comment to its sender without inferring from timestamp +
   content — the inference step that failed in the 2026-05-04 stoa--e39
   empirical (~25-min coordination stall during arc-21 §5.4 review handoff).
```

**§5.1.b — §7.4 inline wording update**

Current §7.4 first paragraph reads (lines ~170-172):

> When a project-tier or sub-project POLYBIUS needs cross-project context, an empirical anchor from another project, or a sanity check that benefits from upper-tier visibility, post a comment on a relevant ticket in YOUR OWN bw prefixed with `[for: <upper-seat>]` (e.g., `[for: user-tier POLYBIUS]`). The upper-tier seat polls down via unified poll (§7.3) and responds on the same ticket within poll cadence (~5 min default). This is the cross-tier-coordination-meets-in-lower-tier pattern (§7.5 + `MAJOR_POLYBIUS.md` §7.1).

Replace with (preserves the cross-tier-upward use case as the primary; adds bidirectional expansion as the general framing):

> The `[for: <recipient-seat-slug>] [from: <sender-seat-slug>]` tag pair marks an addressed POLYBIUS comment — either direction across any POLYBIUS pair. The most common use is cross-tier upward (project-tier → user-tier needing cross-project context, an empirical anchor from another project, or a sanity check that benefits from upper-tier visibility): the project-tier seat posts on a ticket in YOUR OWN bw prefixed with `[for: user-tier-polybius] [from: <self-seat-slug>]`. The upper-tier seat polls down via unified poll (§7.3) and responds on the same ticket within poll cadence (~5 min default). This is the cross-tier-coordination-meets-in-lower-tier pattern (§7.5 + `MAJOR_POLYBIUS.md` §7.1).
>
> The same tag pair is also used for in-tier peer addressing (e.g., user-tier POLYBIUS addressing project-tier POLYBIUS on a project-tier coordination ticket: `[for: polybius-the-stoa] [from: user-tier-polybius]`) — Arc 36 promoted the convention to bidirectional. The `[from:]` tag is mandatory on every addressed comment per §7.1 beat 5; see §7.7 for the parsing procedure that consumes both tags.

(Note for ADA: the section's remaining paragraphs after this opener — "PRINCIPAL is exception-handler", the universal escalation triggers table, the empirical anchor — stay unchanged.)

**§5.1.c — NEW §7.7 "bw-timeline parsing: author-attribution via tags"**

Insert AFTER current §7.6 "Empirical lineage" and BEFORE the `---` separator that closes §7. §7.6 numbering is preserved (no renumbering — see §3.1 design rationale).

```
### 7.7 bw-timeline parsing: author-attribution via tags

When a POLYBIUS peer reads a bw timeline to compute "last own activity" /
"last peer activity" / "missed-check threshold" (§7.1 beats 2 and 3), the
attribution step is load-bearing. A misattributed comment causes silent
coordination stalls — the failure mode that surfaced in the 2026-05-04
stoa--e39 empirical (project-tier POLYBIUS attributed a
`[for: POLYBIUS_the_stoa]` peer comment as own self-heartbeat; ~25-min
review-handoff stall before the misread was caught).

**Parse-by-tag, not by inference.** Every POLYBIUS coordination comment
carries a `[from: <seat-slug>]` or `[radio-check <seat-slug>]` tag per §7.1
beat 5. Read the tag first; do NOT infer authorship from timestamp,
content pattern, or position. Timestamp-and-content inference is exactly
what failed in the e39 empirical.

**Procedure (executed per fire of the polling cron — encoded mechanically
at `substrate/templates/polling-cron-prompt-template.md` STEP 1.5):**

For each new comment in the timeline since the last fire, extract the
leading tag and classify into one of four cases:

1. **`[radio-check <slug>]`** — POLYBIUS heartbeat by `<slug>`. Slug-match
   against `{{SELF_SEAT_SLUG}}` and `{{PEER_SEAT_SLUG}}` (lowercase,
   hyphenated, whitespace-tolerant comparison): on self-match, this is
   own heartbeat → contributes to `last_self_activity`. On peer-match,
   this is peer heartbeat → contributes to `last_peer_activity`.

2. **`[for: <slug-Y>] [from: <slug-X>]`** — addressed POLYBIUS comment by
   `<slug-X>` to `<slug-Y>`. Same slug-match procedure: `<slug-X>` self-match
   contributes to `last_self_activity`; `<slug-X>` peer-match contributes
   to `last_peer_activity`. The `<slug-Y>` recipient tag is advisory for
   readers — it does NOT enter timeline-arithmetic.

3. **`[from: <slug-X>]`** — own-bw substantive POLYBIUS comment by
   `<slug-X>`, no specific recipient. Same slug-match: self-match →
   `last_self_activity`; peer-match → `last_peer_activity`.

4. **Untagged, OR tag-slug does not match a known POLYBIUS slug** —
   non-POLYBIUS comment (PLINY phase status, CAPTAIN verdicts,
   pair-programmer outputs, legacy pre-Arc-36 POLYBIUS comments). These
   are SUBSTANCE comments — they do NOT enter `last_self_activity` /
   `last_peer_activity` timeline-arithmetic. They may be substance-load-
   bearing for OTHER reads (the substantive content of the comment is
   read for its own value); they simply do not contribute to coordination-
   attentiveness signals.

**Compute peer-silence threshold and self-heartbeat-due timing from
tagged-POLYBIUS comments only.** This is the load-bearing rule: only
case-1, case-2, and case-3 (with slug-match) contribute timestamps to
`last_self_activity` / `last_peer_activity`. Case-4 comments do NOT.

**Why non-POLYBIUS comments are excluded.** PLINY / CAPTAIN comments are
SUBSTANCE comments (gauntlet phase status, ambiguity surfaces, dispatch
results) — not coordination-attribution comments. Including them in
`last_peer_activity` would defeat the radio-check protocol (peer-silence
threshold would never fire because PLINY comments would mask actual
POLYBIUS silence). The protocol intentionally tracks POLYBIUS-on-POLYBIUS
attentiveness as a separate signal from team activity-volume.

**Self-misattribution guard.** Never assume the most recent comment is
"yours" by timestamp proximity. Always verify by tag-slug match. The e39
empirical was precisely this misattribution shape.

**Worked example (Arc 36 itself).** Arc 36 IS the first worked example
under this canon. During this arc's coordination on `stoa--jru`,
POLYBIUS_the_stoa's heartbeats carry `[from: polybius-the-stoa]` per §7.1
beat 5; cross-tier comments to user-tier POLYBIUS carry
`[for: user-tier-polybius] [from: polybius-the-stoa]`. A peer reading the
stoa--jru timeline applies this §7.7 procedure to attribute each
coordination comment without inference.

**N=1 provenance (per §6.7.1).** The empirical anchor is single — the
2026-05-04 stoa--e39 misread (~25-min stall). Informal-partial-adoption
of `[radio-check <slug>]` tags has been in practice across Arcs 32-35
(N=4 bit-by-it of the legacy form). Worked-when-applied with full canon
is N=0 prior to Arc 36; Arc 36's self-application is the first observation.
Future arcs operating under §7.7 + §7.1 beat 5 either succeed and accrete
the worked-when-applied count, or surface a fresh failure mode and surface
back to the canon-promotion gate per §6.7.1. The fix is in canon NOW
because PRINCIPAL declared (under the no-deferrals stance, 2026-05-17)
and the e39 empirical is a single concrete bit-by-it; structural-lesson
status accretes over future engagement-evidence per §6.7.1.

**Future scope.** Extending the convention to PLINY / CAPTAIN / pair-
programmer Majors (i.e., promoting case-4 attribution to first-class
timeline-arithmetic) is hard-locked OUT of Arc 36 per A2.5 + A14. A future
arc may extend with explicit scope expansion if a recurring gauntlet-pacing
failure mode surfaces. The mechanical-enforcement layer (pre-comment hook,
CI lint) is also hard-locked OUT per A14 — Arc 36 ships prose canon +
parser-step template per §27's mechanical-narrow + agent-inspection pattern;
mechanical enforcement is a future arc IF non-compliance recurs.
```

(Section is ~70 lines; matches the ~40-60 line target from arc-22 deliverable 1.2 with the worked-example + N=1 framing additions warranted by §3.4 + §3.8 design picks.)

**§5.1.d — §11 step 1.5 (new) — renewal mechanism**

Insert immediately after current step 1 (Polling cron) — that is, between the existing step 1 paragraph block (lines ~409-415 + the "The cron prompt body comes from..." paragraph) and the existing `**2. Radio-check pattern...**` heading.

**Structural shape (rev5 after ARGUS F1+F2+F3+F4+F5+F6 fold):**

- **F1 fix — inline slot values.** The renewal-cron prompt body is engagement-specific at setup time. Every slot value the renewal needs (all 13 polling-cron slots — 10 original + 2 SLUG slots from Part 1 fold + 1 RENEWAL_CRON_ID slot from rev3 F4 fold — PLUS the polling cron's id PLUS the renewal-cron's own next-renewal scheduling parameters) is substituted INTO the renewal-cron prompt body at the moment the renewal cron is `CronCreate`d. The renewal cron does not reference any template by file at fire time; the renewal cron's prompt body IS the complete substituted instruction set. State-management across session-clear / compact / fresh-session is the union of (a) the renewal cron's prompt body (durable across the cron's lifetime per the CronCreate-side of the system) and (b) the bw record of the polling-cron's id (in the §7.1 beat 1 radio-check handshake comment). No re-substitution of any template happens at fire time.
- **F2 fix — session-lifecycle.** The renewal cron is `CronCreate`d with `durable: true`. Per the documented `CronCreate` tool schema, this flag specifies that the task persists to `.claude/scheduled_tasks.json` and survives session restarts. PER OPEN BUG (anthropics/claude-code issue #40228, opened 2026-03-28, unresolved at design time): the `durable: true` flag is documented but does NOT currently persist; tasks die on session exit regardless. The design encodes `durable: true` as honest intent (matches documented schema; works correctly once the bug is fixed without further canon revision) — but does NOT rely on it as the load-bearing recovery mechanism. Load-bearing recovery is via `MAJOR_POLYBIUS.md` §9 step 7 (long-running-engagement polling re-setup; rev3 m5 fix re-cites away from §13.4 — see m5 note below): on the operator's next session activation while autonomous-mode is desired, §9 step 7 requests PRINCIPAL consent and runs the §11 setup checklist, including this step 1.5 — which spins up a fresh renewal cron paired with the fresh polling cron. **The recovery is PRINCIPAL-consent-required, not transparent re-bootstrap** — §9 step 7 explicitly names the consent step. (Alternatively, if PRINCIPAL re-issues the autonomous-mode trigger, `MAJOR_POLYBIUS.md` §13.4 step 2 routes the same setup checklist. Both paths converge on §11 step 1.5; both require some form of PRINCIPAL action — consent OR trigger.) Session-lifecycle loss is recovered by the operator's normal autonomous-mode re-entry with PRINCIPAL in the loop.
- **F3 fix — deterministic self-discovery.** The renewal cron carries the polling cron's id as an inline slot value (`{{POLLING_CRON_ID}}`). STEP 1 of the renewal-cron prompt body is `CronList; find cron-id == {{POLLING_CRON_ID}}` (exact-match on cron-id, not a text-search against prompt-body). The ~80-char CronList prompt-truncation observed in PLINY's A7 spike does not affect the match. Composes with the F3 Handle (a) template-body re-order at §5.3 (which helps a different consumer — peer audit reading CronList — but is not load-bearing for renewal self-discovery once F3 Handle (b) is in place).
- **F4 fix — cadence-switch × renewal composition (rev3).** The `substrate/templates/polling-cron-prompt-template.md` STEP 4 cadence-switch path now ALSO rotates the paired renewal cron in lock-step with the polling-cron rotation. The polling-cron template's substitution-slot table gains a `{{RENEWAL_CRON_ID}}` slot (populated AFTER initial setup once the renewal cron exists — see §11 step 1.5's setup-time slot-lifecycle note below). STEP 4 of the polling-cron template performs the existing polling-cron rotation (CronDelete old + CronCreate new at the new cadence) AND additionally CronDeletes the paired renewal cron (id = `{{RENEWAL_CRON_ID}}`) + CronCreates a fresh renewal cron carrying the NEW polling-cron-id + NEW cadence as inline slot values. Without this fix, the renewal cron's STEP 1 cron-id exact-match would no-op after any cadence-switch, the renewal chain would die silently, and the replacement polling cron from the cadence-switch would have no successor renewal cron. The F4 fix makes the cadence-switching pattern (§7.2 per-seat-unilateral) compose cleanly with the renewal mechanism. The full edit-spec lives in §5.3; this bullet names the structural property §5.1.d depends on. STEP 1a's session-lifecycle no-op branch (below) is also updated in rev3 to self-CronDelete — with F4 shipped, STEP 1a fires ONLY on the genuine session-lifecycle failure mode where exiting + cleaning up is correct (don't perpetuate stale renewal chain; let §9 step 7 / §13.4 recover).
- **F5 fix — STEP 4.2 deterministic renewal-cron CronCreate (rev4).** The F4 fix at §5.3.d1 STEP 4 requires that STEP 4.2 (rotate paired renewal cron at the new POLLING_CRON_ID + CADENCE) CronCreate a FRESH renewal cron — but the polling cron at cadence-switch fire time has no F1+F3-consistent source for the renewal-cron prompt body. F1 hard-locks template-reference-at-fire-time out; F3 hard-locks CronList-prompt-text recovery out (~80-char truncation). The F5 fix adds a `{{RENEWAL_CRON_PROMPT_BODY}}` slot to the polling-cron template's substitution-slot table; the polling cron carries the full renewal-cron prompt body as inline literal text at engagement-setup time (with `<PLACEHOLDER:POLLING_CRON_ID>` + `<PLACEHOLDER:CADENCE>` markers left for cadence-switch re-substitution). STEP 4.2 CronCreates the fresh renewal cron using this slot value, re-substituting the placeholders to the new polling-cron-id + new cadence. Cost: polling-cron prompt body grows from ~50 to ~130 lines per fire (~6,500 bytes; well within any documented `CronCreate` prompt size constraints per PLINY A7 spike + ARGUS-rev2 re-verify). Without this fix, STEP 4.2 cannot execute deterministically; with it, the F4 4-step dance is fully buildable. (Rev5 F6 collapse, below, reduces the dance to 2-step and supersedes the rev4 4-step framing.)
- **F6 fix — terminating-shape collapse via one-shot auto-delete (rev5).** The rev4 F5 fold left a residual chicken/egg that ARGUS-rev4 surfaced: the rev4 5-step setup dance + rev4 4-step cadence-switch dance both required the renewal cron to carry its own id as an inline slot value (for STEP 1a explicit self-CronDelete). The cross-reference re-bind sub-steps (setup steps 4a + 4b; cadence-switch STEPs 4.3 + 4.4) generated F6-style stale-id residuals at the polling cron's `{{RENEWAL_CRON_ID}}` slot; attempting to extend the dance further to fix the residuals generates infinite re-bind regress. The F6 fix removes the renewal cron's STEP 1a explicit self-CronDelete entirely; cleanup of fired one-shot crons is handled by the documented one-shot auto-delete property per Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks "Set a one-time reminder": "Claude schedules a single-fire task that deletes itself after running"). Removing the consumer that REQUIRED the renewal cron's self-id collapses the setup dance from 5-step to 4-step terminating shape + the cadence-switch dance from 4-step to 2-step terminating shape, with explicit acceptance of one-time-stale `{{RENEWAL_CRON_ID}}` residual at the polling cron's slot (bounded by one-shot auto-delete; converges at +144h renewal-chain extension via §5.1.d STEP 4a hygiene re-bind). The slot-lifecycle dance at §11 step 1.5 is the 4-step rev5 terminating shape; the cadence-switch dance at §5.3.d1 STEP 4 is the 2-step rev5 terminating shape. The full edit-spec lives in §5.1.d + §5.3.a + §5.3.d1 + §11 step 1.5; this bullet names the structural property §5.1.d depends on. The rev5 design now structurally depends on one-shot auto-delete reliability (Claude Code docs verified by WebFetch); see §8.2 N=1 framing + §9.8 residual concerns for the honest encoding of that dependency.

**§11 step 1.5 prose to land:**

````
**1.5 Schedule renewal.** Polling crons created via `CronCreate` have a
documented expiry of 168 hours (7 days) for recurring tasks per Claude
Code docs (https://code.claude.com/docs/en/scheduled-tasks §Seven-day
expiry: "Recurring tasks automatically expire 7 days after creation.
The task fires one final time, then deletes itself."). To prevent silent
loss of the polling cron on multi-day engagements, schedule a one-shot
renewal cron at +144 hours (= 168 - 24h buffer) from polling-cron
creation. The 24h buffer (= `{{RENEWAL_BUFFER_HOURS}}`) absorbs
renewal-fire jitter, session-offline windows, and clock skew. (One-shot
tasks are not subject to the 7-day cap — the cap applies only to
recurring tasks per the docs; one-shot tasks expire when their scheduled
time passes.)

**Renewal-cron prompt body — engagement-specific, slot values inline.**
The renewal-cron prompt body is generated at autonomous-mode-setup time
with ALL slot values pre-substituted (no template-reference at fire
time). The substituted body carries: every slot the polling cron carries
(so a replacement polling cron can be re-created from it deterministically);
the polling cron's id (`{{POLLING_CRON_ID}}` — for deterministic
self-discovery at fire time); and the renewal-cron's own next-renewal
scheduling parameters.

Renewal-cron prompt body template (substitute at setup time, not at fire
time):

```
[scheduled renewal fire — {{SELF_SEAT_SLUG}} polling-cron rotation on
{{COORDINATION_TICKET}}; current polling cron {{POLLING_CRON_ID}};
renewal cron self]

STEP 1 — find current polling cron (deterministic).
CronList; find the entry whose cron-id == {{POLLING_CRON_ID}}.
(Exact-match on cron-id, not text-search on prompt-body — the CronList
prompt-body display is truncated to ~80 chars and is not load-bearing
for matching.) If the cron is not found in CronList: see STEP 1a.

STEP 1a — polling-cron-missing branch (session-lifecycle no-op; rev5
terminating-shape: explicit self-CronDelete REMOVED).
If {{POLLING_CRON_ID}} is absent from CronList, this renewal cron has
outlived its paired polling cron — almost certainly because the polling
cron died on a session-lifecycle event (fresh conversation, /clear,
session exit). (With rev3 F4 shipped, cadence-switch rotations of the
polling cron also rotate THIS renewal cron in lock-step at the polling-
cron-template STEP 4 site, so a cadence-switch can no longer be the
cause of {{POLLING_CRON_ID}}-not-in-CronList.) The correct response is
no-op AND exit: post a single bw comment on {{COORDINATION_TICKET}}
noting the orphan-renewal observation, then exit. No explicit
self-CronDelete is needed — this renewal cron was CronCreate'd with
recurring: false (one-shot), and per Claude Code docs
(https://code.claude.com/docs/en/scheduled-tasks "Set a one-time
reminder" section: "Claude schedules a single-fire task that deletes
itself after running") the cron is removed by the runtime after this
fire completes. The polling cron will be re-created when
{{SELF_SEAT_NAME}} next re-enters autonomous mode at the operator's
next session activation (per MAJOR_POLYBIUS.md §9 step 7 long-running-
engagement polling re-setup, which requests PRINCIPAL consent; OR per
MAJOR_POLYBIUS.md §13.4 step 2 if PRINCIPAL re-issues the autonomous-
mode trigger); that re-entry will create a fresh renewal cron paired
with the fresh polling cron via this same §11 step 1.5. Comment to post:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] renewal
  cron fired without a paired polling cron (id {{POLLING_CRON_ID}} not
  in CronList — session-lifecycle event likely; cadence-switch path
  ruled out by F4 lock-step rotation). Exiting; one-shot auto-delete
  removes this cron from the session per Claude Code docs. Awaiting next
  autonomous-mode entry per MAJOR_POLYBIUS.md §9 step 7 (PRINCIPAL
  consent required) or §13.4 (PRINCIPAL re-trigger)."
Exit.

(Rev5 F6 terminating-shape note: prior revisions of STEP 1a invoked an
explicit CronDelete against {{RENEWAL_CRON_ID}} as a "self-cleanup"
step. That mechanism required the renewal cron's prompt body to carry
its own id as an inline slot value — a chicken/egg dependency that
forced the §11 step 1.5 setup-time dance into a 5-step shape and broke
silently if the slot value was stale (as ARGUS-rev4 F6 surfaced). The
one-shot auto-delete property the runtime provides is the deterministic
cleanup mechanism; STEP 1a's explicit self-CronDelete was redundant. The
rev5 removal eliminates the chicken/egg dependency entirely and collapses
the setup-dance to 3 steps + the cadence-switch dance to 2 steps. See
§9.7 for the residual concerns the removal introduces — primarily the
structural dependence on one-shot auto-delete reliability.)

STEP 2 — CronCreate replacement polling cron.
CronCreate a NEW recurring cron with cadence {{CADENCE}} and the
polling-cron prompt body with slot values inline (the same engagement-
specific body the original polling cron carried — slot values are pre-
substituted into this renewal-cron prompt at setup time and carried
inline through fire). The polling cron's {{RENEWAL_CRON_ID}} slot is
substituted with the OLD/current paired renewal cron's id (i.e., the
renewal cron currently executing this STEP — which will self-clean
via one-shot auto-delete after this fire per Claude Code docs); the
slot will be re-bound to the live <new_renewal_cron_id> in STEP 4a
(rev5 hygiene optimization). Let the returned id be <new_polling_cron_id>.

STEP 3 — CronDelete {{POLLING_CRON_ID}} (the now-superseded polling cron).
Post on {{COORDINATION_TICKET}}:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] cron
  renewed: superseded {{POLLING_CRON_ID}} with <new_polling_cron_id>;
  cadence {{CADENCE}} unchanged."

STEP 4 — CronCreate next renewal one-shot (LOCAL-TIME arithmetic, rev3 m8;
rev5 F6 terminating-shape: chicken/egg re-bind dance collapsed).
Compute the next-renewal fire time in LOCAL time:
  next_renewal_local = NOW (interpreted in local tz) + 144 hours.
Per Claude Code docs https://code.claude.com/docs/en/scheduled-tasks:
"All times are interpreted in your local timezone." A cron expression
emitted from UTC arithmetic would fire at the wrong wall-clock moment
by the UTC-local offset (potentially up to ~12h off the intended +144h
window, eroding the 24h buffer). Always compute and emit in local time.
CronCreate a one-shot cron with cron-expression for next_renewal_local,
recurring: false, durable: true. The prompt body for this new renewal
is THIS SAME renewal-cron prompt body with ONE substitution:
  - replace {{POLLING_CRON_ID}} with <new_polling_cron_id>
The {{RENEWAL_CRON_ID}} slot inside the renewal cron's own body is no
longer consumed at fire time (rev5 STEP 1a removed the self-CronDelete
that was its only reader); it may be left as a placeholder marker, as
its old value, or removed entirely — its value is now informational
only and ADA-discretion. All other slot values carry through unchanged.
Let the returned id be <new_renewal_cron_id>.

STEP 4a — re-bind the new polling cron's {{RENEWAL_CRON_ID}} slot
(F4 lock-step composition, rev3; rev5 best-effort framing).
The new polling cron created in STEP 2 was substituted with a "best-
effort cleanup id" placeholder for {{RENEWAL_CRON_ID}} (the slot's
rev5 semantics — see §5.3.a slot definition). To keep the polling
cron's cadence-switch STEP 4.1 best-effort `CronDelete {{RENEWAL_CRON_ID}}`
pointing at the live renewal cron (so the explicit delete actually
succeeds rather than relying on one-shot auto-delete as the fallback),
CronDelete <new_polling_cron_id> and CronCreate it AGAIN with
{{RENEWAL_CRON_ID}} = <new_renewal_cron_id>. Let the returned id be
<final_polling_cron_id>. The re-bind is a hygiene optimization — the
cron pair survives without it (STEP 4.1's CronDelete no-ops on the
stale id; the orphan renewal cron self-cleans via one-shot auto-delete
at +144h) — but the re-bind keeps the cadence-switch path tidy and
avoids accumulating short-lived orphan renewal crons inside an
engagement that cadence-switches frequently. SHIP STEP 4a.

STEP 5 — log renewal-chain extension.
Post on {{COORDINATION_TICKET}}:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] renewal
  chain extended: new polling cron <final_polling_cron_id>; next renewal
  cron <new_renewal_cron_id> (one-shot at +144h LOCAL, durable: true).
  Polling cron carries new renewal id in {{RENEWAL_CRON_ID}} slot for
  best-effort cleanup on cadence-switch; renewal cron's own
  {{RENEWAL_CRON_ID}} slot is informational-only per rev5 F6
  terminating-shape (no fire-time consumer)."

Exit.
```

**Worked example — substituted renewal-cron prompt body for Arc 36's
own self-application (rev3 m4: ALL 13 slot values enumerated inline;
rev4 F5: 14th slot `{{RENEWAL_CRON_PROMPT_BODY}}` on the polling-cron
side enumerated inline immediately after this block).**

Hypothetical example: if POLYBIUS_the_stoa had set up its autonomous-mode
engagement on stoa--jru AT a moment when Arc 36 canon were already shipped
(which is not actually the case for Arc 36's own self-application per
§4.4.2 chicken/egg — but the worked example demonstrates the
substituted-body structure). Assume polling-cron creation at local time
`2026-05-17 17:50` (operator's local tz), with cron-id `c4482646` and
cadence `*/5 * * * *`. The paired renewal cron's prompt body — pre-
substituted inline at setup time — would read (all 13 slot values
enumerated; F1 structural property demonstrated):

```
[scheduled renewal fire — polybius-the-stoa polling-cron rotation on
stoa--jru; current polling cron c4482646; current renewal cron
<set after CronCreate returns; see slot-lifecycle note below>;
renewal cron self]

Slot values inline at setup time:
  {{COORDINATION_TICKET}} = stoa--jru
  {{WATCHED_STORES}} = ["/path/to/the-stoa"]
  {{WATCHED_TICKETS}} = [["stoa--jru", "stoa--e39", "stoa--cgn"]]
  {{PEER_SEAT_NAME}} = MAJOR_PLINY_the_stoa
  {{SELF_SEAT_NAME}} = project-tier POLYBIUS_the_stoa
  {{SELF_SEAT_SLUG}} = polybius-the-stoa
  {{PEER_SEAT_SLUG}} = pliny-the-stoa
  {{CRON_ID}} (polling cron's id, == {{POLLING_CRON_ID}}) = c4482646
  {{POLLING_CRON_ID}} = c4482646
  {{RENEWAL_CRON_ID}} = <populated after CronCreate; chicken/egg
    per slot-lifecycle note: CronCreate returns the new id, then
    a second CronCreate substitutes that id into the renewal cron's
    own prompt body — or equivalently, the renewal cron knows its
    own id via CronList enumeration at fire time when {{RENEWAL_CRON_ID}}
    needs to be CronDelete'd self in STEP 1a or referenced in STEP 4a>
  {{ALARM_THRESHOLD_MINUTES}} = 60
  {{HEARTBEAT_INTERVAL_MINUTES}} = 30
  {{CADENCE}} = */5 * * * *
  {{ESCALATION_TRIGGERS}} = project-direction, ship/no-ship, substance
    disagreement, authorship, ambiguity, peer-silence > 60 min

STEP 1 — find current polling cron (deterministic).
CronList; find the entry whose cron-id == c4482646.
(If absent → STEP 1a: post no-op comment AND EXIT — rev5 F6
terminating-shape; one-shot auto-delete handles cleanup.)

STEP 2 — CronCreate replacement polling cron at cadence */5 * * * *
with the engagement-specific polling-cron prompt body (slot values
inline from this engagement's setup; not re-substituted from any file).
Let returned id be <new_polling_cron_id>.

STEP 3 — CronDelete c4482646 (the now-superseded polling cron).
Post on stoa--jru:
  bw comment stoa--jru "[from: polybius-the-stoa] cron renewed:
  superseded c4482646 with <new_polling_cron_id>; cadence */5 * * * *
  unchanged."

STEP 4 — CronCreate next renewal one-shot (LOCAL-TIME arithmetic;
rev5 collapse: only POLLING_CRON_ID substituted at fire time).
Compute next_renewal_local = 2026-05-23 17:50 (local; 144 hours after
the 2026-05-17 17:50 local polling-cron creation moment).
Emit cron expression: `50 17 23 5 *` (minute=50, hour=17, day=23,
month=5, any-day-of-week). NO Z suffix; no UTC conversion — per
Claude Code docs all times interpreted local.
CronCreate with cron-expression `50 17 23 5 *`, recurring: false,
durable: true. Prompt body = THIS SAME renewal-cron prompt body with
{{POLLING_CRON_ID}} replaced by <new_polling_cron_id>. (The
{{RENEWAL_CRON_ID}} slot inside this body is no longer consumed at
fire time per rev5 F6 terminating-shape — STEP 1a has no explicit
self-CronDelete; one-shot auto-delete handles cleanup. ADA-discretion
on the slot's value at this re-substitution: pass through unchanged,
clear to placeholder, or omit entirely.) Let returned id be
<new_renewal_cron_id>.

STEP 4a — re-bind new polling cron's {{RENEWAL_CRON_ID}}
(rev5 hygiene optimization — keeps best-effort cleanup pointing at
live id; the cron pair survives without it via one-shot auto-delete
fallback).
CronDelete <new_polling_cron_id>; CronCreate same body with
{{RENEWAL_CRON_ID}} substituted to <new_renewal_cron_id>. Let
returned id be <final_polling_cron_id>.

STEP 5 — log:
  bw comment stoa--jru "[from: polybius-the-stoa] renewal chain
  extended: new polling cron <final_polling_cron_id>; next renewal
  cron <new_renewal_cron_id> (one-shot at 2026-05-23 17:50 local,
  durable: true)."

Exit.
```

(The worked example above demonstrates: F1 = all 13 slot values pre-
substituted inline at setup time, no template-reference at fire time;
F2 = `durable: true` encoded as documented-schema honest intent;
F3 = STEP 1 cron-id exact-match on `c4482646`, not text-search;
F4 = `{{RENEWAL_CRON_ID}}` slot exists for the polling cron's best-
effort cleanup on cadence-switch (rev5 best-effort framing); F6 = STEP 1a
relies on one-shot auto-delete (rev5 terminating-shape; no explicit
self-CronDelete) and STEP 4 no longer needs the chicken/egg double-
re-bind dance — STEP 4a remains as a hygiene optimization, not a
correctness requirement; m8 = LOCAL-time arithmetic, cron expression
`50 17 23 5 *` not `50 17 23 5 *Z`, worked-example timestamps
`2026-05-17 17:50` and `2026-05-23 17:50` without Z suffix per
Claude Code local-time interpretation.)

The substituted body is what `CronCreate` receives as the `prompt`
parameter; ADA can read the substituted body directly from the renewal
cron's CronList entry (modulo the ~80-char truncation, which is why
STEP 1 matches on cron-id not on prompt-text).

**Worked example — polling-cron-side `{{RENEWAL_CRON_PROMPT_BODY}}`
slot value inline (rev4 F5: F5 structural property demonstrated).**

The polling cron's substituted prompt body (NOT shown in full here —
the full polling-cron template is at `substrate/templates/polling-cron-
prompt-template.md` and lives outside this design's body) carries 14
slot values inline. Thirteen of the 14 are the same as the renewal
cron's slot values enumerated above (modulo `{{POLLING_CRON_ID}}`
which is the polling cron's own id — same value `c4482646` for the
initial polling cron, then `<final_polling_id>` after the setup-time
re-CronCreate dance). The 14th slot is `{{RENEWAL_CRON_PROMPT_BODY}}`,
which carries the FULL renewal-cron prompt body as an inline literal
string. For the same hypothetical Arc-36-shipped engagement above, the
polling cron's `{{RENEWAL_CRON_PROMPT_BODY}}` slot would be substituted
to (showing the literal text the polling cron would receive at
CronCreate time per §11 step 1.5 slot-lifecycle step 3):

```
{{RENEWAL_CRON_PROMPT_BODY}} =
"[scheduled renewal fire — polybius-the-stoa polling-cron rotation on
stoa--jru; current polling cron <PLACEHOLDER:POLLING_CRON_ID>; renewal
cron self — rev5 F6 terminating-shape: own id is informational-only,
not consumed at fire time]

Slot values inline at setup time:
  {{COORDINATION_TICKET}} = stoa--jru
  {{WATCHED_STORES}} = [\"/path/to/the-stoa\"]
  {{WATCHED_TICKETS}} = [[\"stoa--jru\", \"stoa--e39\", \"stoa--cgn\"]]
  {{PEER_SEAT_NAME}} = MAJOR_PLINY_the_stoa
  {{SELF_SEAT_NAME}} = project-tier POLYBIUS_the_stoa
  {{SELF_SEAT_SLUG}} = polybius-the-stoa
  {{PEER_SEAT_SLUG}} = pliny-the-stoa
  {{CRON_ID}} (polling cron's id, == {{POLLING_CRON_ID}}) =
    <PLACEHOLDER:POLLING_CRON_ID>
  {{POLLING_CRON_ID}} = <PLACEHOLDER:POLLING_CRON_ID>
  {{RENEWAL_CRON_ID}} = <PLACEHOLDER:RENEWAL_CRON_ID> (rev5: no
    fire-time consumer; pass through unchanged, ADA-discretion on
    representation; left as placeholder here for clarity)
  {{ALARM_THRESHOLD_MINUTES}} = 60
  {{HEARTBEAT_INTERVAL_MINUTES}} = 30
  {{CADENCE}} = <PLACEHOLDER:CADENCE>
  {{ESCALATION_TRIGGERS}} = project-direction, ship/no-ship, substance
    disagreement, authorship, ambiguity, peer-silence > 60 min

STEP 1 — find current polling cron (deterministic).
CronList; find the entry whose cron-id == <PLACEHOLDER:POLLING_CRON_ID>.
(If absent → STEP 1a: post no-op comment AND EXIT — rev5 F6
terminating-shape; one-shot auto-delete handles cleanup.)

STEP 1a — polling-cron-missing branch (session-lifecycle no-op).
If <PLACEHOLDER:POLLING_CRON_ID> is absent from CronList, this
renewal cron has outlived its paired polling cron — session-lifecycle
event likely. Post the orphan-renewal observation comment on stoa--jru
and exit. No explicit self-CronDelete (rev5 F6 terminating-shape;
one-shot auto-delete per Claude Code docs removes this cron after
fire completes).

STEP 2 — CronCreate replacement polling cron at cadence
<PLACEHOLDER:CADENCE> with the engagement-specific polling-cron prompt
body. Let returned id be <new_polling_cron_id>.

STEP 3 — CronDelete <PLACEHOLDER:POLLING_CRON_ID>; log on stoa--jru.

STEP 4 — CronCreate next renewal one-shot at +144h LOCAL with this
same body except <PLACEHOLDER:POLLING_CRON_ID> replaced by
<new_polling_cron_id>. (Rev5 F6 terminating-shape: the renewal cron's
own {{RENEWAL_CRON_ID}} slot is no longer consumed at fire time;
ADA-discretion on its substitution at this point — typically pass
through unchanged.) Let returned id be <new_renewal_cron_id>.

STEP 4a — re-bind new polling cron's {{RENEWAL_CRON_ID}} (rev5
hygiene optimization).
CronDelete <new_polling_cron_id>; CronCreate same body with
{{RENEWAL_CRON_ID}} substituted to <new_renewal_cron_id>. Keeps
best-effort cleanup pointing at the live renewal cron id for the
next cadence-switch.

STEP 5 — log renewal-chain extension on stoa--jru.
Exit."
```

(Two things to notice about this literal value. First, the
`<PLACEHOLDER:POLLING_CRON_ID>` markers are LEFT as placeholders
inside this inline literal — the polling cron carries this slot
value WITHOUT a polling-cron-id substituted, so that at STEP 4.2
cadence-switch time the polling cron can re-substitute the new
`<new_polling_cron_id>` into the placeholder before CronCreating the
fresh renewal cron. The same applies to `<PLACEHOLDER:CADENCE>` —
the polling cron knows its own current cadence via `{{CADENCE}}` and
substitutes it AT cadence-switch time, not at setup time. This is
why the literal contains placeholder markers: the polling cron's
F5-slot value is a TEMPLATE for the fresh renewal cron, with the
two values that change on cadence-switch left as placeholders for
re-substitution. Second, the renewal cron's own `{{RENEWAL_CRON_ID}}`
internal reference (rev4 used `<final_renewal_id>` here) is now
ADA-discretion per rev5 F6 terminating-shape — STEP 1a no longer
consumes it, so the literal can carry a placeholder or be left blank;
the polling cron's TOP-LEVEL `{{RENEWAL_CRON_ID}}` slot still
carries the paired renewal cron's id for STEP 4.1 best-effort
cleanup, but that's the polling cron's slot, not an internal
reference inside the renewal cron's literal body.)

The polling cron's polling-prompt-template prompt body would
therefore be ~50 lines of polling-cron STEPs (per the existing
template) PLUS the ~80-line `{{RENEWAL_CRON_PROMPT_BODY}}` slot
value above, for a total of ~130 lines per polling-cron prompt body
fire. Per Claude Code docs (PLINY A7 spike + ARGUS-rev2 re-verify)
no documented prompt-size ceiling applies to arbitrary `CronCreate`
prompts; 130 lines × ~50 chars ≈ 6,500 bytes is well within any
reasonable bound.

(The polling-cron-side worked example demonstrates: F5 =
`{{RENEWAL_CRON_PROMPT_BODY}}` slot exists, carries the renewal
cron's full prompt body as inline literal, contains placeholder
markers for the two values that change on cadence-switch
(`<PLACEHOLDER:POLLING_CRON_ID>` + `<PLACEHOLDER:CADENCE>`), and
provides the deterministic source STEP 4.2 needs to CronCreate the
fresh renewal cron without referencing any template file (F1-
consistent) and without recovering the body from the renewal cron's
CronList entry (F3-consistent).)

**Renewal-cron CronCreate parameters (load-bearing per ARGUS m2; rev4 m9
local-time sweep).**
- `cron`: a 5-field expression evaluating to +144h from polling-cron
  creation, computed in the operator's LOCAL timezone (per m8 +
  Claude Code docs https://code.claude.com/docs/en/scheduled-tasks
  "All times are interpreted in your local timezone"). Compute the
  wall-clock time in local tz and emit the cron expression for that
  single minute. Example: if polling cron is created at local time
  `2026-05-17 17:50` (operator's local tz, NO Z suffix — Z would
  imply UTC and mis-fire by the local-UTC offset), renewal cron fires
  at local time `2026-05-23 17:50`; emit cron expression
  `50 17 23 5 *` (minute=50, hour=17, day=23, month=5, any-day-of-
  week). NO Z suffix on either timestamp.
- `recurring`: `false` (one-shot — the renewal fires once, performs
  STEPs 1-5, and exits; the next renewal in the chain is created
  inside STEP 4).
- `durable`: `true`. Documented in the `CronCreate` tool schema as
  "persist to .claude/scheduled_tasks.json and survive restarts." See
  the failure-mode acceptance below for the open bug at design time
  and why the design encodes `durable: true` as honest-intent rather
  than load-bearing recovery.

Record both cron ids (initial polling cron + first renewal cron) in the
radio-check initialization handshake on the coordination ticket per §7.1
beat 1. Subsequent renewal-fire rotations log to the same ticket per
STEPs 3 and 5 above.

**Slot-lifecycle note (rev3 F4 + rev4 F5 + rev5 F6 fold — collapsed to
3-step minimum-CronCreate-count setup).** The polling-cron template
gains TWO substitution slots that support the F4 + F5 lock-step
composition with the cadence-switching pattern (per §5.3 STEP 4
extension): `{{RENEWAL_CRON_ID}}` (rev3 F4) and
`{{RENEWAL_CRON_PROMPT_BODY}}` (rev4 F5). The setup-time dance
populates both slots via a chicken/egg-resolving sequence.

The lifecycle has two layers. Layer 1 is the prompt-body literal
itself — the renewal-cron prompt body is generated at autonomous-mode
setup time with all engagement-specific slot values pre-substituted
(per the F1 inline-slot-values shape), then captured as a literal
string. Layer 2 is the cron-id cross-references between the two crons —
the renewal cron needs to know the polling cron's id (used at STEP 1
exact-match self-discovery; load-bearing); the polling cron carries
the renewal cron's id as a best-effort cleanup hint in its
`{{RENEWAL_CRON_ID}}` slot (used at cadence-switch STEP 4.1 to
CronDelete the paired renewal cron; tolerates stale id per rev5 F6
terminating-shape — see below).

**Rev5 F6 terminating-shape collapse — load-bearing structural
property.** The rev4 5-step setup dance + rev4 4-step cadence-switch
dance both grew out of a chicken/egg dependency that no longer exists:
the renewal cron's STEP 1a explicit self-CronDelete required the
renewal cron's body to carry its own id as an inline slot value, which
forced the dance to re-bind the polling cron AND the renewal cron with
mutually-known ids. Per ARGUS-rev4 F6, the rev4 5-step dance left the
polling cron's two RENEWAL-pointing slots baked to the step-2 renewal
id which was CronDeleted in step 4 — the only way out of that regress
without adding more re-bind steps (which generate further regress) is
to drop the renewal cron's dependency on its own id. With one-shot
auto-delete confirmed reliable per Claude Code docs
(https://code.claude.com/docs/en/scheduled-tasks "Set a one-time
reminder": "Claude schedules a single-fire task that deletes itself
after running"), the renewal cron's STEP 1a no longer needs an
explicit self-CronDelete; the runtime removes the cron after fire
completes. This removes the renewal cron's RENEWAL_CRON_ID-in-own-body
dependency entirely and collapses the setup dance to 3-step minimum
and the cadence-switch dance to 2-step minimum (per §5.3.d1).

**Setup-time ordering (rev5 terminating-shape — 4-step minimum
CronCreate count).** Two ids must be threaded through the dance: the
renewal cron's body needs the LIVE polling cron's id (load-bearing
for STEP 1 self-discovery) and the polling cron's `{{RENEWAL_CRON_ID}}`
slot needs the live renewal cron's id (best-effort cleanup; tolerates
staleness per rev5 F6). The renewal cron's own id is no longer
threaded into its own body (rev5 F6: STEP 1a's explicit self-CronDelete
removed; one-shot auto-delete handles cleanup). The 4-step dance is
the minimum that resolves both required threadings without infinite
regress.

  0. Generate the renewal-cron prompt body literal text from the
     renewal-cron template at `operating-disciplines.md` §11 step 1.5
     (the renewal-cron STEPs 1-5 block). Substitute ALL engagement-
     specific slot values inline (per F1) EXCEPT the polling-cron
     cross-reference + cadence, which become PLACEHOLDERS at this
     stage:
       `{{POLLING_CRON_ID}}` = `<PLACEHOLDER:POLLING_CRON_ID>`
       `{{CADENCE}}` = `<PLACEHOLDER:CADENCE>` (for STEP 4.2 cadence-
         switch re-substitution at fire time)
     The renewal cron's own `{{RENEWAL_CRON_ID}}` slot is ADA-discretion
     per rev5 F6 (no fire-time consumer): pass through as a placeholder,
     leave as the template default, or omit; the renewal cron does not
     consume the value at fire time. Capture the substituted-with-
     placeholders literal as `RENEWAL_CRON_PROMPT_BODY_LITERAL` for
     use in subsequent steps.
  1. CronCreate polling cron with `{{RENEWAL_CRON_ID}}` =
     `<PLACEHOLDER:RENEWAL_CRON_ID>` (placeholder; re-bound in step 3)
     and `{{RENEWAL_CRON_PROMPT_BODY}}` =
     `RENEWAL_CRON_PROMPT_BODY_LITERAL`.
     → returned id = `<polling_id_v1>`
  2. CronCreate renewal cron with prompt body =
     `RENEWAL_CRON_PROMPT_BODY_LITERAL` with `<PLACEHOLDER:POLLING_CRON_ID>`
     → `<polling_id_v1>` and `<PLACEHOLDER:CADENCE>` → the engagement
     cadence. recurring: false; +144h LOCAL cron expression per §5.1.d
     STEP 4 / §5.3.d1 STEP 4.2 arithmetic.
     → returned id = `<renewal_id_v1>`
  3. CronDelete `<polling_id_v1>`; CronCreate polling cron AGAIN with
     the same body except `{{RENEWAL_CRON_ID}}` = `<renewal_id_v1>`.
     `{{RENEWAL_CRON_PROMPT_BODY}}` is the same literal from step 1
     (still carries `<PLACEHOLDER:POLLING_CRON_ID>` + `<PLACEHOLDER:
     CADENCE>` markers — that is correct, the polling cron uses this
     slot ONLY for STEP 4.2 cadence-switch re-substitution, not at any
     current-fire-time consumer).
     → returned id = `<final_polling_id>`
  4. CronDelete `<renewal_id_v1>`; CronCreate renewal cron AGAIN with
     body = `RENEWAL_CRON_PROMPT_BODY_LITERAL` with
     `<PLACEHOLDER:POLLING_CRON_ID>` → `<final_polling_id>` and
     `<PLACEHOLDER:CADENCE>` → cadence. recurring: false; the +144h
     LOCAL cron expression (re-computed from "now" at step 4 — minutes
     of setup latency are absorbed by the 24h buffer).
     → returned id = `<final_renewal_id>` (this is the renewal cron
     that goes into the radio-check initialization handshake; the
     `<final_polling_id>` is the polling cron)

(The 4-step dance is the rev5 terminating shape. Comparison to rev4's
5-step dance with sub-steps 4a/4b: rev4 needed `<actually_final_renewal_id>`
threaded into the renewal cron's own body for STEP 1a self-CronDelete,
which forced an extra CronDelete-CronCreate-again sub-step at the final
position AND a re-bind of the polling cron's `{{RENEWAL_CRON_ID}}`
slot — and that re-bind itself was what ARGUS-rev4 F6 identified as
incomplete. Rev5 removes the STEP-1a-self-CronDelete consumer entirely
(one-shot auto-delete handles cleanup), so the renewal cron's id does
NOT need to be threaded into anything that fires later. One fewer
CronCreate; the renewal cron itself does not need to know its own id.)

(**Where the rev5 4-step dance terminates without regress.** After
step 4: the renewal cron `<final_renewal_id>` carries the LIVE polling
cron id `<final_polling_id>` (load-bearing for STEP 1; ARGUS-rev4
F6's (b) failure mode resolved — the renewal cron's STEP 1 will find
the polling cron correctly at +144h). The polling cron `<final_polling_id>`
carries `{{RENEWAL_CRON_ID}}` = `<renewal_id_v1>` (DEAD — CronDeleted
in step 4). This is the rev5 trade-off named explicitly: the polling
cron's `{{RENEWAL_CRON_ID}}` slot carries a one-time-stale id after
setup, persisted across cadence-switches at the cadence-switch path
(since rev5 §5.3.d1 STEP 4 does not re-bind that slot — the new
polling cron carries forward whatever value was current at substitution
time, which is the about-to-be-deleted old renewal id). At the next
cadence-switch, STEP 4.1's `CronDelete {{RENEWAL_CRON_ID}}` no-ops
gracefully against the dead id, and the live `<final_renewal_id>`
is orphaned-but-self-cleaning via its own one-shot auto-delete at
+144h. The slot converges to a LIVE id only at the +144h renewal-chain
extension event — per §5.1.d STEP 4a (hygiene optimization), the
renewal cron re-CronCreates the polling cron with `{{RENEWAL_CRON_ID}}`
= `<new_renewal_cron_id>` so the new polling cron knows the next
renewal in the chain. The terminating property: one stale
id at the polling cron's slot at any time, with self-cleaning via
one-shot auto-delete bounded at +144h (which is also when the slot
converges to a live id via the renewal-chain extension); no regress
because no further fire-time consumer depends on the stale id. This
is what "accept stale RENEWAL_CRON_ID in polling cron" means in the
rev5 terminating-shape pick — exactly framing 1 from ARGUS-rev4 /
PLINY routing, with one-shot auto-delete as the cleanup property
that makes the acceptance bounded rather than open-ended.)

(**Why no 5-step or 6-step variant.** A 5-step dance with step 5 =
re-CronCreate polling cron a third time with
`{{RENEWAL_CRON_ID}}` = `<final_renewal_id>` would clean up the
one-time stale id at the polling cron's slot — but step 5 would
return `<truly_final_polling_id>`, which the renewal cron's body
does NOT carry. The renewal cron would then fail STEP 1 at +144h
because it looks for `<final_polling_id>` which is dead. Fixing that
requires step 6 = re-CronCreate renewal cron with
`<truly_final_polling_id>` — which returns `<truly_final_renewal_id>`,
which the polling cron does NOT carry. Infinite regress; same shape
ARGUS-rev4 F6 identified. Rev5 stops at the 4-step dance with
explicit acceptance of the one-time polling-cron-slot stale-id
residual, on the load-bearing rule that one-shot auto-delete handles
the orphan cleanly. Strict-mutual-awareness is not achievable
without a CronUpdate primitive that does not exist.)

(Implementation note: the placeholder-substitution approach above
treats the prompt body as a string-templating exercise — substitute
literal `<PLACEHOLDER:POLLING_CRON_ID>` and `<PLACEHOLDER:
RENEWAL_CRON_ID>` markers with the returned cron ids at the moment
they are known. ADA may choose any equivalent representation —
`{{POLLING_CRON_ID}}`-style braces with a sentinel value, named-
group regex substitution, or any other deterministic mechanism —
as long as the post-substitution body contains the actual cron ids
literally and the un-substituted placeholder cannot survive into a
CronCreate prompt that an executing renewal cron would read.)

**Failure-mode acceptance (broader than the v1 single-failure-mode
framing; folds ARGUS F2).** The renewal mechanism protects against the
+168h cron-expiry boundary. It does NOT, by itself, protect against
session-lifecycle events:

1. **Cron-expiry boundary (the +168h window).** Addressed by the renewal
   chain: at +144h the renewal cron fires, rotates the polling cron, and
   schedules the next renewal at +144h-from-now. Steady-state continuous
   protection while the session stays alive and active.

2. **Renewal-chain break across multi-day continuous outage.** If the
   session is offline through BOTH the renewal fire AND the +168h cron
   expiry that follows (only possible when an autonomous engagement is
   left offline for > 6 days), the polling cron expires before the next
   renewal fires. Recovery is via peer-side radio-check escalation per
   §7.1 beat 3 (> 60-min peer-silence threshold fires; peer surfaces
   "lost contact with `<peer>`" to PRINCIPAL).

3. **Session-lifecycle event — fresh conversation, /clear, session exit
   (ARGUS F2 cold-audit catch; rev3 m5 re-cite away from §13.4).** Per
   Claude Code docs (Limitations section): "Starting a fresh
   conversation clears all session-scoped tasks. Resuming with
   `claude --resume` or `claude --continue` restores tasks that have
   not expired." Per `MAJOR_POLYBIUS.md` §7.4 line 437: polling crons
   are session-only (`durable: false` by default) and die when the
   session exits. The renewal cron uses `durable: true` as honest
   intent (documented tool-schema parameter; would survive session
   restart when working) — but is subject to the open bug at
   anthropics/claude-code issue #40228 (opened 2026-03-28, unresolved
   at design time) where `durable: true` does not currently persist.

   **Recovery path (load-bearing; works regardless of the durable bug;
   PRINCIPAL-consent-required, NOT transparent re-bootstrap — rev3
   m5 honesty):** the polling cron is session-only by canon; when the
   session exits or a fresh conversation starts, both the polling cron
   and the renewal cron are lost. Recovery is NOT transparent. The
   load-bearing recovery cite is `MAJOR_POLYBIUS.md` §9 step 7
   (Activation checklist long-running-engagement entry): "If this
   engagement is long-running (multi-session arc work, cross-tier
   coordination, an active PLINY in a separate session): **request
   PRINCIPAL consent and set up a polling cron per §7.4**." On the
   operator's next session activation, POLYBIUS executes §9 of the
   activation checklist, which (a) reads bw state, (b) detects an
   open coordination ticket on a long-running engagement, (c)
   **requests PRINCIPAL consent** to re-setup the polling cron, (d)
   on consent, runs the §11 setup checklist including this step 1.5,
   which creates a NEW polling cron paired with a NEW renewal cron.
   The renewal mechanism is re-bootstrapped from a clean slate.
   Alternative recovery path: PRINCIPAL re-issues the autonomous-mode
   trigger ("go autonomous on this work") — `MAJOR_POLYBIUS.md` §13.4
   step 2 detects the trigger and routes through the same §11 setup
   checklist. Both paths converge on §11 step 1.5; both require
   PRINCIPAL action (consent OR trigger). Neither is transparent.
   (The prior rev2 framing implied transparent recovery via §13.4
   alone; that was qualitatively wrong about §13.4's semantics —
   §13.4 fires on HITL→Autonomous trigger DETECTION, not on
   fresh-session-mid-autonomous re-bootstrap. ARGUS-rev2 m5 caught
   this; rev3 names the consent-required property explicitly.)

   If a renewal cron from a prior session survives (durable bug
   eventually fixed) and fires in a session that has already created
   a fresh polling cron via §9 step 7 or §13.4 re-entry, STEP 1a's
   no-op-and-exit branch handles the orphan-renewal cleanly — the
   renewal cron posts the orphan-observation comment and exits;
   one-shot auto-delete per Claude Code docs (rev5 F6 terminating-
   shape) removes the cron from the session after fire completes,
   so the stale chain does not perpetuate alongside the fresh chain.

   The session-lifecycle failure mode is therefore NOT a multi-day
   outage — it is any fresh-conversation start at any time, recovered
   consent-mediated (not transparent) by the operator's next session
   activation running §9 step 7 (or by PRINCIPAL's autonomous-mode
   re-trigger routing §13.4 step 2). The renewal mechanism does not
   need to protect against it directly; it composes with the §9 step 7
   / §13.4 recovery paths. STEP 1a's no-op-plus-self-delete is the
   seam where the orphan-renewal-from-prior-session meets the fresh
   chain.

4. **Cadence-switch × renewal composition (ARGUS F4 cold-audit catch,
   rev3; rev4 m11 partial-failure-state recovery named).** Without
   the F4 fix, polling-cron-template STEP 4 cadence-switch (CronDelete
   old + CronCreate new at new cadence) would leave the paired
   renewal cron's inline `{{POLLING_CRON_ID}}` + `{{CADENCE}}` slot
   values stale. At +144h the renewal cron's STEP 1 exact-match would
   no-op AND STEP 1a would mis-classify the case as session-lifecycle
   (the polling cron is alive at the new id, not session-dead) AND
   the replacement polling cron from the cadence-switch would have no
   successor renewal cron. The renewal chain dies silently AND the
   new chain never starts. Recovery: same as scenario 3 above (peer-
   side radio-check on >60 min self-silence, then PRINCIPAL-consent-
   mediated re-setup) — but AFTER silent expiry of the new polling
   cron at +168h. The F4 fix at §5.3 polling-cron-template STEP 4
   eliminates this scenario by rotating BOTH crons in lock-step:
   cadence-switch CronDeletes old polling AND old renewal, CronCreates
   new polling AND new renewal, with cross-referenced slot values
   populated post-CronCreate per the slot-lifecycle note above. With
   F4 shipped (and F5 supplying the `{{RENEWAL_CRON_PROMPT_BODY}}`
   slot per §5.3.a so STEP 4.2 can CronCreate deterministically),
   cadence-switching composes cleanly with the renewal mechanism.

   **Partial-failure-state surface of the F4 dance (rev4 m11 recovery
   prose; rev5 F6 narrowing).** The rev3 F4 + rev4 lock-step rotation
   was a FOUR CronCreate-operation dance per cadence-switch (STEP 4.1
   polling rotate → STEP 4.2 renewal rotate → STEP 4.3 polling re-bind
   → STEP 4.4 renewal re-bind). The rev5 F6 terminating-shape collapse
   reduces this to TWO CronCreate operations (STEP 4.1 polling rotate
   → STEP 4.2 renewal rotate; no re-bind sub-steps — one-shot auto-
   delete handles orphan cleanup; polling cron's `{{RENEWAL_CRON_ID}}`
   slot tolerates one-cycle staleness per §5.3.a best-effort semantics).
   The partial-failure-state surface is therefore HALVED vs rev4 (2x
   operations vs rev3's single CronCreate cadence-switch; same as a
   pre-F4 polling-only rotation plus one renewal CronCreate). If the
   polling cron's prompt-body execution is interrupted between STEP 4.1
   and STEP 4.2 (session crash, tool failure mid-fire, context
   exhaustion within the fire), the cron pair is left in an intermediate
   state — e.g., STEP 4.1 completes leaving a new polling cron alive
   with stale `{{RENEWAL_CRON_ID}}` pointing at the just-CronDelete'd
   old renewal cron, and no live paired renewal cron at all (the
   `<new_renewal_cron_id>` that STEP 4.2 would have created is never
   created). Recovery from any such partial-failure state is via the
   SAME peer-side radio-check escalation surface as the broader cron-
   mechanism-failure modes: §7.1 beat 3 — when the self-silence
   threshold (>60 min) trips on the polling-cron side, the peer
   POLYBIUS surfaces "lost contact with `<peer>`" to PRINCIPAL, and
   PRINCIPAL re-issues the autonomous-mode trigger (routing through
   `MAJOR_POLYBIUS.md` §13.4 step 2 → §11 setup checklist including
   step 1.5), OR the operator's next session activation runs
   `MAJOR_POLYBIUS.md` §9 step 7 (long-running-engagement polling
   re-setup; PRINCIPAL-consent-required). Either path converges on
   a clean §11 setup that creates a fresh polling-cron + renewal-cron
   pair from scratch, discarding any intermediate-state artifacts —
   the orphan renewal cron from the partial state self-cleans via
   one-shot auto-delete at +144h (rev5 F6 terminating-shape; no
   explicit cleanup needed). No new recovery infrastructure
   is required — the broader cron-mechanism failure-mode recovery
   surface already covers this partial-failure-state shape. The
   cost is the same as scenario 3: PRINCIPAL-consent-required, not
   transparent; recovery latency is bounded by the >60 min peer-
   silence threshold + the operator's next-session activation
   cadence.

No additional watchdog cron ships — the alternative (peer-side renewal
monitoring, separate watcher cron, double-cron belt-and-suspenders)
adds the same coordination-dependency problems Option 2 was rejected
for in the A7 decision matrix. Bounded staleness is acceptable;
protocol-induced bugs cost more. The renewal cron is the per-seat
unilateral mechanism; §9 step 7 / §13.4 re-entry is the cross-session-
lifecycle mechanism; polling-cron-template STEP 4 F4 fix is the
cadence-switch composition mechanism; together they cover the failure
modes the design accepts.

This mirrors the per-seat-unilateral cadence-switching pattern in §7.2
("Cadence-switching is per-seat unilateral. Each peer reads complexity
tags on incoming comments and adjusts ITS OWN cron"). Each seat renews
its OWN polling cron unilaterally; no cross-seat renewal coordination
exists.

Cross-ref to template: the polling-cron-prompt template at
`substrate/templates/polling-cron-prompt-template.md` does NOT carry
in-fire renewal logic — cron-expiry handling lives in this step 1.5
instead. See the end-of-file pointer note at the template for the
back-cite.

Cross-ref to recovery paths: `MAJOR_POLYBIUS.md` §9 step 7 (long-running-
engagement polling re-setup, PRINCIPAL-consent-required) is the load-
bearing recovery path for session-lifecycle loss of the cron pair on
the operator's next session activation while autonomous-mode is
still desired. `MAJOR_POLYBIUS.md` §13.4 step 2 (autonomous-mode trigger
detection → §11 setup) is the recovery path when PRINCIPAL re-issues
the autonomous-mode trigger. Both converge on the §11 setup checklist
including this step 1.5. The §13.4 note added by this arc (per §5.2.b)
closes the loop by mentioning renewal-cron presence as part of setup-
complete confirmation.
````

(Sub-decision note for ADA: the §11 step 1.5 outer block uses 4-backtick fencing to enclose the inner triple-backtick code blocks per Arc 35 deliverable convention. The semantic content — the F1+F2+F3-resolving structural choices — is the load-bearing part; the fencing choice may be adjusted in ADA's edit to match the local markdown-rendering reality without changing semantic content.)

### §5.2 — `substrate/MAJOR_POLYBIUS.md`

**§5.2.a — §7.4 body-paragraph cite (Part 1 cross-ref)**

§7.4 "Polling capability + consent discipline (Arc 18)" already cross-refs `substrate/templates/polling-cron-prompt-template.md` for the cron prompt body and `operating-disciplines.md` §7` for coordination-engagement crons. Add a short body paragraph at the end of §7.4 — immediately before §7.5 begins — that cites the new parsing teaching:

```
**bw-timeline parsing (Arc 36).** When you (the polling-cron parser, or any
POLYBIUS reading a coordination timeline) compute peer-silence freshness
or self-heartbeat-due timing from the bw timeline, parse comments by their
leading author tag (`[from: <seat-slug>]`, `[radio-check <seat-slug>]`,
`[for: <recipient>] [from: <sender>]`) per the four-case procedure in
`operating-disciplines.md` §7.7. Do not infer authorship from timestamp
or content pattern — that inference failed in the 2026-05-04 stoa--e39
empirical (~25-min coordination stall) and the §7.7 procedure exists
precisely to remove the memory-load that the inference step imposed on
the parser. The polling-cron-prompt-template.md STEP 1.5 mechanically
executes this procedure per fire; see the template body for the
substitution-slot wiring.
```

**§5.2.b — §13.4 renewal-confirm-on-entry note (Part 2)**

§13.4 "Mode entry / exit procedures" is the autonomous-entry procedure surface. Add a one-line note to the bare/self-qualified entry step (step 2 in the current §13.4 numbered list) immediately after "Begin polling.":

```
Cron 7-day expiry handling per `operating-disciplines.md` §11 step 1.5:
schedule the one-shot renewal cron at +144 hours from polling-cron
creation; record both cron ids in the radio-check initialization handshake.
Confirm renewal cron is in place before declaring setup complete.
```

### §5.3 — `substrate/templates/polling-cron-prompt-template.md`

**§5.3.0 — Template body opening-line re-order (rev2 F3 Handle a)**

Current template body opens at line 41 with: `[scheduled poll fire — {{SELF_SEAT_NAME}} watching {{COORDINATION_TICKET}} +` (followed by `peer {{PEER_SEAT_NAME}}; cron {{CRON_ID}}; cadence {{CADENCE}}]` on line 42). For worked-example slot values (`{{SELF_SEAT_NAME}} = project-tier POLYBIUS_the_stoa`, `{{COORDINATION_TICKET}} = stoa--jru`), `{{COORDINATION_TICKET}}` lands at approximately char 65 — fits inside the ~80-char CronList prompt-body truncation observed in PLINY's A7 spike. For longer SEAT_NAME values, longer ticket-id sets, or unified-poll seats watching multiple stores, `{{COORDINATION_TICKET}}` can land past truncation — making peer audit of CronList ambiguous.

Re-order the opening line so `{{COORDINATION_TICKET}}` leads. Replace the current lines 41-42 body opening:

```
[scheduled poll fire — {{SELF_SEAT_NAME}} watching {{COORDINATION_TICKET}} +
peer {{PEER_SEAT_NAME}}; cron {{CRON_ID}}; cadence {{CADENCE}}]
```

With:

```
[scheduled poll fire — ticket {{COORDINATION_TICKET}}; {{SELF_SEAT_NAME}}
watching peer {{PEER_SEAT_NAME}}; cron {{CRON_ID}}; cadence {{CADENCE}}]
```

(Rev2 F3 Handle a rationale: leads with `{{COORDINATION_TICKET}}` so the ticket id always fits inside the ~80-char CronList truncation — preserves peer-audit observability of which ticket a polling cron watches. This is structurally complementary to F3 Handle b — the renewal-cron self-discovery uses cron-id exact-match per §5.1.d STEP 1 and does NOT depend on the prompt-body text — but the re-order helps the OTHER CronList consumer, which is humans / agents reading CronList output to audit live cron state. Both handles ship; they cover different consumers, not the same one.)

**§5.3.a — Substitution-slot table additions (rev4 extends to 4 new slots)**

Add FOUR rows to the substitution-slots table — two SLUG slots (Part 1) immediately after the existing `{{SELF_SEAT_NAME}}` row, plus `{{RENEWAL_CRON_ID}}` (Part 2, rev3 F4 fold) AND `{{RENEWAL_CRON_PROMPT_BODY}}` (Part 2, rev4 F5 fold) immediately after the existing `{{CRON_ID}}` row:

```
| `{{SELF_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for own seat (LEADING tag uses this; display-form name uses `{{SELF_SEAT_NAME}}`) | `polybius-the-stoa` |
| `{{PEER_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for peer seat | `user-tier-polybius` |
```

And, after the existing `{{CRON_ID}}` row:

```
| `{{RENEWAL_CRON_ID}}` | id of the paired one-shot renewal cron scheduled per `operating-disciplines.md` §11 step 1.5. **Rev5 best-effort semantics:** the slot value is used at cadence-switch STEP 4.1 for `CronDelete {{RENEWAL_CRON_ID}}` as a hygiene optimization — the explicit delete keeps the cron table tidy when the slot value is fresh, and no-ops gracefully when the slot value is stale. Staleness is bounded by the renewal cron's +144h one-shot auto-delete per Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks "Set a one-time reminder": single-fire tasks auto-delete after running), which guarantees orphan cleanup even when STEP 4.1's CronDelete no-ops. Populated AFTER initial setup per the §11 step 1.5 slot-lifecycle note (rev5 4-step dance; the slot may carry a one-time-stale value between setup and the first cadence-switch — see §11 step 1.5 explicit acceptance prose). | `<renewal-id>` (e.g., `a1b2c3d4`) |
| `{{RENEWAL_CRON_PROMPT_BODY}}` | full renewal-cron prompt body as inline literal text — the complete, slot-substituted body the paired renewal cron carries (per `operating-disciplines.md` §11 step 1.5 renewal-cron template, with all engagement-specific slot values pre-substituted at setup time). Sourced at autonomous-mode-setup time per §11 step 1.5 slot-lifecycle dance (renewal-cron prompt body is generated FIRST as a literal string with placeholders for `{{POLLING_CRON_ID}}` and `{{CADENCE}}`, captured as this slot's literal value, then folded into the polling cron's body at the dance's CronCreate steps). Consumed at cadence-switch by STEP 4.2 (cadence-switch renewal CronCreate) — the polling cron uses this literal body to deterministically CronCreate the fresh renewal cron at the new cadence, re-substituting the internal `{{POLLING_CRON_ID}}` placeholder to the NEW polling-cron-id captured from STEP 4.1's CronCreate return and the internal `{{CADENCE}}` placeholder to the new cadence. The internal `{{RENEWAL_CRON_ID}}` slot inside the literal has no fire-time consumer (rev5 F6: STEP 1a no longer self-CronDeletes); ADA-discretion on representation (placeholder, default value, or omitted). | `<multi-line literal — the full ~80-line renewal-cron prompt body the paired renewal cron was CronCreate'd with at setup time; see §11 step 1.5 worked example for the literal text>` |
```

Add a sentence to the post-table prose: "Display-form slots (`{{SELF_SEAT_NAME}}` / `{{PEER_SEAT_NAME}}`) are used in human-readable prose within comment bodies; SLUG slots are used in the LEADING author tag per `operating-disciplines.md` §7.1 beat 5. Both must be supplied at template substitution time. The `{{RENEWAL_CRON_ID}}` slot is used by STEP 4.1 (cadence-switch) as a best-effort cleanup hint — it identifies the paired renewal cron for explicit CronDelete on rotation, tolerating staleness because one-shot auto-delete handles orphan cleanup as a fallback (rev5 F6 terminating-shape). The `{{RENEWAL_CRON_PROMPT_BODY}}` slot carries the paired renewal cron's complete prompt-body text as an inline literal — STEP 4.2 uses it to CronCreate the FRESH renewal cron at cadence-switch time without referencing any template file (preserving F1 inline-slot-values shape) and without recovering the body from CronList (preserving F3 deterministic non-text-search shape). See §11 step 1.5 slot-lifecycle note for the post-setup substitution sequence covering both new slots."

(Rev3 F4 rationale for adding `{{RENEWAL_CRON_ID}}` as a slot rather than discovering the renewal cron via CronList text-search: same as F3 — CronList prompt-body display is truncated to ~80 chars, text-search is fragile under truncation, exact-match on cron-id is deterministic. Adding the slot is structurally consistent with F3's choice for the renewal-cron's own self-discovery of the polling cron. Rev5 reframes the slot as best-effort cleanup rather than load-bearing cross-reference; the one-shot auto-delete fallback per Claude Code docs makes the staleness bounded rather than fatal.)

(Rev4 F5 rationale for adding `{{RENEWAL_CRON_PROMPT_BODY}}` as a slot rather than referencing the renewal-cron template at cadence-switch time or recovering the body from the renewal cron's CronList entry: the F1 fix hard-locks template-reference-at-fire-time out of the design (renewal-cron prompt body is engagement-specific and pre-substituted at setup); the F3 fix hard-locks CronList-prompt-text recovery out (~80-char truncation, text-search fragility). Without the slot, STEP 4.2 cannot execute deterministically — the polling cron context at cadence-switch fire time has no source for the fresh renewal cron's prompt body. Inlining the literal as a slot value is the only F1+F3-consistent path. Cost: polling-cron prompt body grows from ~50 to ~130 lines per fire (the ~80-line renewal-cron prompt body is inlined). Per Claude Code docs and PLINY's A7 spike re-verified by ARGUS-rev2, there is no documented prompt-size ceiling for arbitrary `CronCreate` prompts — the 25,000-byte ceiling applies only to `loop.md`. ~130 lines × ~50 chars ≈ 6,500 bytes; well within any reasonable bound. The cost is visible but bounded; no F1/F3 regression; deterministic STEP 4.2 execution.)

**§5.3.b — Insert STEP 1.5 between STEP 1 (substantive read) and STEP 2 (peer-silence escalation)**

```
STEP 1.5 — author-attribute aggregated comments.
For each new comment in the aggregated state from STEP 1, extract the
leading author tag per operating-disciplines.md §7.7 (four-case procedure):
  - [radio-check <slug>]: POLYBIUS heartbeat by <slug>
  - [for: <slug-Y>] [from: <slug-X>]: POLYBIUS comment by <slug-X> to <slug-Y>
  - [from: <slug-X>]: POLYBIUS comment by <slug-X>
  - other / no tag: non-POLYBIUS or legacy — does NOT enter timeline-arithmetic

Build two timestamp lists, slug-matching against the substitution slots
(whitespace-tolerant, case-insensitive on the right-hand side — e.g., a
tag accidentally posted as `[from: User-Tier-POLYBIUS]` still matches
`user-tier-polybius`):
  - last_self_activity: most recent comment where author-slug == {{SELF_SEAT_SLUG}}
  - last_peer_activity: most recent comment where author-slug == {{PEER_SEAT_SLUG}}

These two derived timestamps drive STEP 2 (peer-silence escalation) and
STEP 3 (self-heartbeat refresh). Without explicit POLYBIUS attribution,
neither computation is reliable — the 2026-05-04 stoa--e39 empirical.
```

**§5.3.c — Update STEP 2 to consume `last_peer_activity`**

Current STEP 2 (line ~55): "Compute time-since-last-{{PEER_SEAT_NAME}}-activity from aggregated state."

Replace with: "Compute time-since-last-peer-activity from `last_peer_activity` per STEP 1.5."

(The rest of STEP 2 is unchanged.)

**§5.3.d — Update STEP 3 to consume `last_self_activity` AND use SLUG slot in heartbeat-post**

Current STEP 3 (lines ~63-66):
```
STEP 3 — self-radio-check refresh.
Compute time-since-last-{{SELF_SEAT_NAME}}-comment-on-{{COORDINATION_TICKET}}.
If > {{HEARTBEAT_INTERVAL_MINUTES}} minutes:
  bw comment {{COORDINATION_TICKET}} "[radio-check {{SELF_SEAT_NAME}}]
  cron {{CRON_ID}} cadence {{CADENCE}} — <one-line state>"
```

Replace with:
```
STEP 3 — self-radio-check refresh.
Compute time-since-last-self-activity from `last_self_activity` per STEP 1.5.
If > {{HEARTBEAT_INTERVAL_MINUTES}} minutes:
  bw comment {{COORDINATION_TICKET}} "[radio-check {{SELF_SEAT_SLUG}}]
  cron {{CRON_ID}} cadence {{CADENCE}} — <one-line state>"
```

(Leading tag now uses `{{SELF_SEAT_SLUG}}` per §7.1 beat 5; the comment body's <one-line state> can still reference the display-form name for human readability.)

**§5.3.d1 — Extend STEP 4 (cadence-tag detection) to ALSO rotate the paired renewal cron (rev3 F4 fix, Handle (i))**

Current STEP 4 (lines 69-80 of the template) rotates ONLY the polling cron on a cadence-switch:
```
STEP 4 — cadence-tag detection.
Scan aggregated state for [complexity: ...] or [cadence: ...] tags posted
since last fire.
If a tag warrants a cadence change (active / default / quiet per
operating-disciplines.md §7.2):
  CronDelete {{CRON_ID}}
  CronCreate at the new cadence with this same prompt body (slot
  {{CRON_ID}} updated to the new id, {{CADENCE}} updated to the new
  schedule)
  bw comment {{COORDINATION_TICKET}} "[cadence-change {{SELF_SEAT_NAME}}]
  switching to <new cadence>; new cron <new id>; superseding {{CRON_ID}}"
Else: continue.
```

Without the F4 fix, this leaves the paired renewal cron's inline `{{POLLING_CRON_ID}}` + `{{CADENCE}}` slot values stale — at +144h fire time the renewal cron's STEP 1 cron-id exact-match would no-op and STEP 1a's session-lifecycle path would fire incorrectly (the polling cron is alive at the new id, not session-dead). The chain dies silently and the new polling cron has no successor renewal cron. See §5.1.d Failure-mode-acceptance scenario 4 for the full prose.

Replace STEP 4 with the extended version that rotates BOTH crons in lock-step (rev5 terminating-shape collapse: 2-step dance, no chicken/egg re-bind sub-steps):

```
STEP 4 — cadence-tag detection (with renewal-cron lock-step rotation
per F4 + rev5 F6 terminating-shape collapse).
Scan aggregated state for [complexity: ...] or [cadence: ...] tags posted
since last fire.
If a tag warrants a cadence change (active / default / quiet per
operating-disciplines.md §7.2):

  STEP 4.1 — rotate polling cron at new cadence + best-effort cleanup
  of paired renewal cron.
  CronDelete {{CRON_ID}}
  CronDelete {{RENEWAL_CRON_ID}} (best-effort hygiene; no-ops gracefully
    against stale id per rev5 F6 — see §5.3.a slot definition and
    §11 step 1.5 terminating-shape acceptance prose. The orphan
    renewal cron self-cleans via one-shot auto-delete at +144h if
    this CronDelete no-ops.)
  CronCreate at the new cadence with this same prompt body (slot
  {{CRON_ID}} updated to the new id, {{CADENCE}} updated to the new
  schedule, {{RENEWAL_CRON_ID}} will be re-substituted at STEP 4.2
  return — see below). Let returned id be <new_polling_cron_id>.

  STEP 4.2 — rotate paired renewal cron at new POLLING_CRON_ID + CADENCE.
  CronCreate a fresh renewal cron deterministically from the inline
  literal slot value {{RENEWAL_CRON_PROMPT_BODY}} (rev4 F5):
    prompt = {{RENEWAL_CRON_PROMPT_BODY}} with internal placeholders
             re-substituted:
               {{POLLING_CRON_ID}} → <new_polling_cron_id>
               {{CADENCE}} → <new cadence>
               {{RENEWAL_CRON_ID}} → ADA-discretion (rev5: no fire-time
                 consumer; pass through unchanged, set to placeholder,
                 or omit)
    cron = wall-clock for NOW + 144 hours in LOCAL timezone (m8;
           emit a 5-field expression for that minute, no UTC
           conversion — per Claude Code docs all times interpreted
           local; jitter absorbed by the 24h buffer)
    recurring = false
    durable = true
  All other engagement-specific slot values inside
  {{RENEWAL_CRON_PROMPT_BODY}} (e.g., {{COORDINATION_TICKET}},
  {{WATCHED_STORES}}, {{SELF_SEAT_SLUG}}, {{PEER_SEAT_SLUG}}, etc.)
  carry through unchanged — they were pre-substituted as literals at
  setup time per §11 step 1.5 slot-lifecycle and remain valid across
  the cadence-switch (only the cron-id pair and the cadence rotate).
  Let returned id be <new_renewal_cron_id>.

  (Rev4 F5 rationale: the polling cron has no source for the fresh
  renewal cron's prompt body other than the inline literal slot value
  it carries — F1 hard-locks out template-reference-at-fire-time, F3
  hard-locks out CronList-prompt-text recovery. The
  {{RENEWAL_CRON_PROMPT_BODY}} slot is the only F1+F3-consistent
  source; STEP 4.2 consumes it directly.)

  (Rev5 F6 terminating-shape: prior revisions had STEP 4.3 + STEP 4.4
  re-bind sub-steps to thread <new_renewal_cron_id> back into the
  polling cron's {{RENEWAL_CRON_ID}} slot AND <new_polling_cron_id>
  back into the renewal cron's {{POLLING_CRON_ID}} slot. STEP 4.4 was
  required because the renewal cron's STEP 1a self-CronDelete needed
  the renewal cron to know its own id — but rev5 removes STEP 1a's
  self-CronDelete (relies on one-shot auto-delete per Claude Code
  docs). STEP 4.3 was required to keep the polling cron's
  {{RENEWAL_CRON_ID}} slot pointing at the live renewal cron — but
  rev5 reframes that slot as best-effort cleanup, tolerating one-time
  staleness between cadence-switches. The polling cron's slot
  carries <new_renewal_cron_id> from this STEP 4.2's return — which
  is captured into the slot of the polling cron CREATED in STEP 4.1
  via in-process substitution before STEP 4.1's CronCreate executes.
  See "Sub-step ordering note" below for the operational detail.)

  STEP 4.5 — log cadence-change with lock-step pair.
  bw comment {{COORDINATION_TICKET}} "[cadence-change {{SELF_SEAT_SLUG}}]
  switching to <new cadence>; new polling cron <new_polling_cron_id>
  superseding {{CRON_ID}}; new renewal cron <new_renewal_cron_id>
  superseding {{RENEWAL_CRON_ID}} (one-shot at +144h LOCAL, durable:
  true); F4 lock-step rotation per §11 step 1.5, rev5 F6 terminating-
  shape (2-step dance; one-shot auto-delete as orphan-cleanup
  fallback)."

Else: continue.
```

**Sub-step ordering note (rev5 F6 — operational detail for the in-fire
two-CronCreate dance).** STEP 4.1 must precede STEP 4.2 because STEP
4.2's CronCreate of the fresh renewal cron requires `<new_polling_cron_id>`
substituted into the renewal body's `<PLACEHOLDER:POLLING_CRON_ID>`
marker (so the new renewal cron's STEP 1 self-discovery at +144h
finds the live polling cron). The new polling cron in STEP 4.1 is
CronCreate'd carrying its `{{RENEWAL_CRON_ID}}` slot substituted with
the value AT SUBSTITUTION TIME — which is the current `{{RENEWAL_CRON_ID}}`
(the about-to-be-CronDeleted-by-STEP-4.1 old renewal cron). After
STEP 4.1 completes:
  - New polling cron `<new_polling_cron_id>` is alive, carrying
    `{{RENEWAL_CRON_ID}}` = OLD renewal id (DEAD — just CronDeleted
    in same STEP 4.1).
  - Old polling cron (the one that just fired this STEP 4) is dead.
  - Old renewal cron is dead.
After STEP 4.2 completes:
  - New renewal cron `<new_renewal_cron_id>` is alive, carrying
    `{{POLLING_CRON_ID}}` = `<new_polling_cron_id>` (LIVE — STEP 1
    self-discovery at +144h will find the live polling cron correctly).
  - New polling cron's `{{RENEWAL_CRON_ID}}` slot still points at
    the dead old renewal id. NOT re-bound (rev5 F6 terminating-
    shape; no STEP 4.3).

The new polling cron's slot is stale-by-one-cycle. At the next
cadence-switch, STEP 4.1's `CronDelete {{RENEWAL_CRON_ID}}` against
the dead old renewal id no-ops gracefully; the live new renewal cron
`<new_renewal_cron_id>` is orphaned-relative-to-the-polling-cron's-
slot at that point, but is cleaned up via one of two converging
mechanisms: (1) the new renewal cron's own +144h one-shot auto-delete
fires per Claude Code docs, OR (2) the renewal-chain extension at
the new renewal cron's STEP 4 emits the NEXT renewal cron and re-binds
the polling cron's slot in STEP 4a (per §5.1.d STEP 4a hygiene
optimization). Either path makes the staleness bounded; one-shot
auto-delete is the load-bearing guarantee.

This is the rev5 trade-off named explicitly: one stale-id residual
per cadence-switch cycle at the polling cron's `{{RENEWAL_CRON_ID}}`
slot, in exchange for cadence-switch-dance termination (no STEP 4.3
+ STEP 4.4 re-bind regress). Same acceptance as the rev5 setup-dance
terminating shape per §11 step 1.5; consistent design across both
the setup and cadence-switch surfaces.

(Rev3 F4 fix rationale per PLINY routing Handle (i) on ARGUS-rev2 verdict: lock-step rotation is the cleanest composition; symmetric to existing STEP 4 polling-cron rotation. Rev5 F6 terminating-shape collapse: removes the double-re-bind dance per the one-shot auto-delete property; the 2-step dance + best-effort {{RENEWAL_CRON_ID}} slot + one-shot-auto-delete orphan-cleanup is the genuine terminating shape that does not regress into further re-binds.)

**§5.3.e — Update usage example block at bottom of template (rev4 extends to 4 new slots; rev5 reframes slot semantics)**

Add slot values for the two new SLUG slots PLUS `{{RENEWAL_CRON_ID}}` (rev3 F4 fold) PLUS `{{RENEWAL_CRON_PROMPT_BODY}}` (rev4 F5 fold):

```
- `{{SELF_SEAT_SLUG}}` = `polybius-the-stoa`
- `{{PEER_SEAT_SLUG}}` = `user-tier-polybius`
- `{{RENEWAL_CRON_ID}}` = `a1b2c3d4` (example renewal cron id — best-effort cleanup hint, may be one-cycle-stale per rev5 F6 terminating-shape; orphan cleanup via one-shot auto-delete; populated post-setup per §11 step 1.5 slot-lifecycle 4-step dance)
- `{{RENEWAL_CRON_PROMPT_BODY}}` = `<full ~80-line renewal-cron prompt body literal, with placeholder markers for POLLING_CRON_ID and CADENCE — see operating-disciplines.md §11 step 1.5 worked example for the literal text; this slot's value is captured at autonomous-mode-setup time per the slot-lifecycle 4-step dance and inlined into the polling cron at dance step 1>`
```

Update the example radio-check handshake comment at the very bottom of the file to use the slug-form leading tag AND name both cron ids (per §11 step 1.5 initialization handshake requirement):

```
bw comment <example>--abc "[radio-check polybius-the-stoa]
polling cron <returned-id> cadence */5 * * * * watching {<example>--abc, <example>--def}
+ {<other>--xyz}; renewal cron a1b2c3d4 (one-shot at +144h LOCAL, durable: true,
per operating-disciplines.md §11 step 1.5); expected duration ~3 hours;
standing by for handshake ack."
```

(Display-form name "project-tier POLYBIUS_foo" can still appear in the comment body's prose for readability; the LEADING tag uses the slug. Both cron ids in the handshake per §11 step 1.5 record-both-cron-ids requirement.)

**§5.3.f — End-of-file pointer note (Part 2)**

Append a new section to the bottom of the file, after the existing "The empirical lineage for this protocol stack lives in..." closing paragraph:

```
---

## Cron expiry handling

Cron expiry is handled OUT OF THIS TEMPLATE. CronCreate's recurring-task
expiry is empirically confirmed at 168 hours (7 days) per Claude Code
docs (https://code.claude.com/docs/en/scheduled-tasks §Seven-day expiry).
Renewal is via a separate one-shot renewal cron scheduled at autonomous-
mode-setup time per `operating-disciplines.md` §11 step 1.5 — no in-fire
renewal logic exists in this template. See §11 step 1.5 for the renewal-
cron prompt body and the failure-mode acceptance (peer-side radio-check
recovery; no additional watchdog ships).

The CronList primitive (per the 2026-05-17 Arc 36 spike on stoa--jru)
exposes neither backward-looking fields (`start_time`/`created_at`/`age`)
nor forward-looking fields (`expires_at`/`next_fire`/`valid_until`),
and no CronUpdate primitive exists — so in-fire arithmetic against
expiry is not implementable. The §11 step 1.5 setup-time scheduled
renewal is the structural workaround.
```

### §5.4 — `substrate/templates/autonomous-mode-activation-template.md`

**§5.4.a — Step 2 author-tag instruction (arc-22 deliverable 1.5 — retained)**

§3 design rationale: the activation-template's job is to onboard the downstream seat into the engagement-specific conventions. Adding a one-line author-tag instruction in step 2 (radio-check pattern) gives the seat a single-place pointer at activation time, before any coordination comment is posted. Cost is one line; benefit is removing the memory-load of "find §7.1 beat 5 in operating-disciplines.md before posting your first coordination comment." User-tier POLYBIUS leans keep; I concur.

Current step 2 (lines 50-54):
```
2. Radio-check pattern with {{PEER_SEAT_NAME}}
   (operating-disciplines.md §7.1) — post initialization handshake on
   {{COORDINATION_TICKET}} naming your cron id and cadence. Peer's
   cron id (if known): {{PEER_CRON_ID}}. Heartbeat every <=30 min.
   Escalate peer-silence > 60 min to PRINCIPAL.
```

Append one sentence at the end of step 2:
```
   All coordination comments use the author-tag convention from
   operating-disciplines.md §7.1 beat 5: `[from: <self-seat-slug>]` on
   every coordination post; `[for: <recipient-slug>] [from: <self-slug>]`
   on addressed comments; `[radio-check <self-slug>]` on heartbeats.
```

---

## §6 — Cite-comment plan

Every cross-ref site that lands in the diff + its anchor section. ADA verifies cite-comment resolution as part of the Phase 2 commit; VERA re-verifies per §4.3 probes.

### §6.1 — New cite-sites Arc 36 creates

| From-site | To-site | Shape |
|---|---|---|
| `operating-disciplines.md` §7.1 beat 5 | `operating-disciplines.md` §7.7 | "See §7.7 for the parsing procedure and the empirical anchor." |
| `operating-disciplines.md` §7.4 (bidirectional update) | `operating-disciplines.md` §7.1 beat 5 | "per §7.1 beat 5" |
| `operating-disciplines.md` §7.4 (bidirectional update) | `operating-disciplines.md` §7.7 | "see §7.7 for the parsing procedure that consumes both tags" |
| `operating-disciplines.md` §7.7 (new) | `operating-disciplines.md` §7.1 beat 5 | "per §7.1 beat 5" (in framing + procedure intro) |
| `operating-disciplines.md` §7.7 (new) | `substrate/templates/polling-cron-prompt-template.md` STEP 1.5 | "encoded mechanically at ... STEP 1.5" |
| `operating-disciplines.md` §7.7 (new) | `operating-disciplines.md` §6.7.1 | "Per §6.7.1" (N=1 provenance subsection) |
| `operating-disciplines.md` §7.7 (new) | `operating-disciplines.md` §27 | "per §27's mechanical-narrow + agent-inspection pattern" (future-mechanical-enforcement framing) |
| `operating-disciplines.md` §7.7 (new) | A2.5 + A14 (the directive itself, cited as "Arc 36 / A2.5 + A14") | "hard-locked OUT of Arc 36 per A2.5 + A14" |
| `operating-disciplines.md` §11 step 1.5 (new) | `operating-disciplines.md` §7.1 beat 1 | "Record both cron ids... per §7.1 beat 1" |
| `operating-disciplines.md` §11 step 1.5 (new) | `operating-disciplines.md` §7.1 beat 3 | "Recovery is via peer-side radio-check escalation per §7.1 beat 3" |
| `operating-disciplines.md` §11 step 1.5 (new) | `operating-disciplines.md` §7.2 | "mirrors the per-seat-unilateral cadence-switching pattern in §7.2" |
| `operating-disciplines.md` §11 step 1.5 (new) | `substrate/templates/polling-cron-prompt-template.md` end-of-file pointer | "See the end-of-file pointer note at the template for the back-cite." |
| `MAJOR_POLYBIUS.md` §7.4 (body cite) | `operating-disciplines.md` §7.7 | "per the four-case procedure in operating-disciplines.md §7.7" |
| `MAJOR_POLYBIUS.md` §7.4 (body cite) | `substrate/templates/polling-cron-prompt-template.md` STEP 1.5 | "STEP 1.5 mechanically executes this procedure per fire" |
| `MAJOR_POLYBIUS.md` §13.4 (renewal note) | `operating-disciplines.md` §11 step 1.5 | "per operating-disciplines.md §11 step 1.5" |
| `polling-cron-prompt-template.md` STEP 1.5 | `operating-disciplines.md` §7.7 | "per operating-disciplines.md §7.7 (four-case procedure)" |
| `polling-cron-prompt-template.md` STEP 1.5 | `operating-disciplines.md` §7.1 beat 5 | "slug-matching against the substitution slots" (implicit cite via convention name) |
| `polling-cron-prompt-template.md` end-of-file pointer | `operating-disciplines.md` §11 step 1.5 | "per operating-disciplines.md §11 step 1.5" |
| `autonomous-mode-activation-template.md` step 2 | `operating-disciplines.md` §7.1 beat 5 | "from operating-disciplines.md §7.1 beat 5" |
| `operating-disciplines.md` §11 step 1.5 (rev3 m5 re-cite) | `MAJOR_POLYBIUS.md` §9 step 7 | "per MAJOR_POLYBIUS.md §9 step 7: long-running-engagement polling re-setup (PRINCIPAL-consent-required)" — rev3 m5 fix re-cites the load-bearing session-lifecycle recovery away from §13.4 (which fires on HITL→Autonomous trigger detection, not on fresh-session-mid-autonomous re-bootstrap). §13.4 still appears as an alternative recovery path (when PRINCIPAL re-issues the trigger). |
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | `MAJOR_POLYBIUS.md` §13.4 step 2 | "alternative recovery path: PRINCIPAL re-issues the autonomous-mode trigger → §13.4 step 2 → §11 setup" — kept as alternative recovery path, no longer load-bearing per rev3 m5 |
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | https://github.com/anthropics/claude-code/issues/40228 | "anthropics/claude-code issue #40228 (opened 2026-03-28, unresolved at design time)" — open-bug citation for `durable: true` honest-intent encoding |
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | https://code.claude.com/docs/en/scheduled-tasks (Limitations section) | "per Claude Code docs (Limitations section): 'Starting a fresh conversation clears all session-scoped tasks.'" |
| `operating-disciplines.md` §11 step 1.5 (rev3 m8) | https://code.claude.com/docs/en/scheduled-tasks (local-time interpretation) | "per Claude Code docs: 'All times are interpreted in your local timezone.'" — rev3 m8 timezone-explicit cite for STEP 4 local-time arithmetic |
| `polling-cron-prompt-template.md` STEP 4 (rev3 F4 extension) | `operating-disciplines.md` §11 step 1.5 | "F4 lock-step rotation per §11 step 1.5" — STEP 4 cadence-switch path cites the slot-lifecycle note + the failure-mode-acceptance scenario 4 |
| `polling-cron-prompt-template.md` substitution-slot table (rev3 F4 extension) | `operating-disciplines.md` §11 step 1.5 | "see §11 step 1.5 slot-lifecycle note" — `{{RENEWAL_CRON_ID}}` slot's post-setup population sequence cite |
| `polling-cron-prompt-template.md` substitution-slot table (rev4 F5 extension; rev5 reframe) | `operating-disciplines.md` §11 step 1.5 | "see §11 step 1.5 slot-lifecycle note (rev5 4-step dance: steps 0 + 1 + 2 + 3 + 4)" — `{{RENEWAL_CRON_PROMPT_BODY}}` slot's source-at-setup + re-substitution mechanism cite; `{{RENEWAL_CRON_ID}}` slot's best-effort cleanup semantics cite |
| `polling-cron-prompt-template.md` STEP 4.2 (rev4 F5 extension; rev5 F6 collapse) | `polling-cron-prompt-template.md` substitution-slot table | "the polling cron CronCreates the fresh renewal cron using `{{RENEWAL_CRON_PROMPT_BODY}}` per §5.3.a slot definition" — STEP 4.2 consumes the slot value defined in §5.3.a; rev5 2-step dance collapse removes prior STEP 4.3 + STEP 4.4 re-bind sub-steps |
| `polling-cron-prompt-template.md` STEP 4 + `operating-disciplines.md` §11 step 1.5 (rev5 F6 extension) | https://code.claude.com/docs/en/scheduled-tasks ("Set a one-time reminder" section) | "Per Claude Code docs: 'Claude schedules a single-fire task that deletes itself after running.'" — load-bearing citation for the rev5 terminating-shape pick (STEP 1a self-CronDelete removed; one-shot auto-delete is the cleanup mechanism; setup dance + cadence-switch dance both collapse to terminating shapes without infinite re-bind regress) |

### §6.2 — Read-site verification rule

For each cite-site in §6.1, after Phase 2 ADA build, the to-site target MUST exist at the cited location. §4.3 probe walks each cite and verifies. ADA confirms in the Phase 2 commit message that every new cite resolves; VERA re-runs §4.3 probe independently.

### §6.3 — Existing cite-sites NOT touched (no renumbering side-effects)

- `operating-disciplines.md` §7.6 (Empirical lineage) — unchanged location (NOT renumbered to §7.8 per §3.1 design pick). All existing cites to §7.6 across substrate continue to resolve.
- `operating-disciplines.md` §11 steps 2-6 — numbering preserved (step 1.5 inserts BETWEEN step 1 and step 2; existing steps 2-6 keep their numbers). All existing cites to "§11 step 2" / "§11 step 6" / "§11 setup-complete confirmation" continue to resolve.
- `MAJOR_POLYBIUS.md` §7.1 / §7.2 / §7.3 / §7.5 / §7.6 — unchanged. The §7.4 body-cite is an addition; surrounding subsection numbering is preserved.

---

## §7 — Self-application checks

PLINY signoff (per `MAJOR_PLINY.md` §5.10 verify-before-claim) executes both checks live at arc close before posting clean-PASS.

### §7.1 — Part 1 self-application check

```bash
# 1. Every POLYBIUS coordination comment on stoa--jru during the arc window carries a leading [from:] tag.
bw show stoa--jru 2>&1 | awk '/2026-05-1[7-9]/' | head -200 | \
  grep -cE '^\*\*2026-05-1[7-9]T'
# Expected: equals the count of POLYBIUS coordination comments in the arc window

bw show stoa--jru 2>&1 | grep '^> \[' | grep -cE '^> \[(from|radio-check|for):'
# Expected: matches the POLYBIUS-only subset; PLINY signoff cross-references by reading the timeline manually for any [from:]-less POLYBIUS coordination comment
```

If any POLYBIUS coordination comment posted during the arc window LACKS a `[from:]` / `[radio-check]` / `[for:][from:]` tag, the Part 1 self-application has FAILED — Arc 36's worked-example property is not satisfied and PLINY surfaces to PRINCIPAL.

### §7.2 — Part 2 self-application check (rev3 m6 chicken/egg-honest rewrite)

```bash
# 1. POLYBIUS_the_stoa's polling cron exists and is recurring.
# (Run in the POLYBIUS session at arc close.)
# CronList output: confirm cron c4482646 (per init handshake) is present,
# recurring, prompt body references stoa--jru.

# 2. NO renewal cron is expected for Arc 36 itself.
# Per §9.5 chicken/egg: c4482646 was set up at 2026-05-17 autonomous-mode
# activation, BEFORE the §11 step 1.5 renewal-mechanism canon ships at
# arc close. There is no paired renewal cron and none is expected; PLINY
# signoff MUST NOT assert one exists (false-positive failure).
# CronList output: exactly one cron entry related to stoa--jru (c4482646);
# no paired renewal cron at the +144h mark.

# 3. Worked-example signal for renewal-mechanism is FUTURE arcs.
# The first POLYBIUS autonomous-mode setup that runs AFTER Arc 36 ships
# executes the new §11 step 1.5 — that setup creates the first observable
# polling-cron + renewal-cron pair under shipped canon. The renewal-cron
# worked-example accretes on future engagements; Arc 36's signal is
# c4482646 still in CronList (cron survived the arc engagement).
```

The Arc 36 self-application property is "the polling cron set up at autonomous-mode activation survived the arc engagement (c4482646 still in CronList at close)" — this is the Part-2 worked-example signal achievable WITHIN the chicken/egg. The renewal-mechanism worked-example accretes on future arcs operating under shipped canon. If c4482646 is ABSENT from CronList at arc close, the polling-cron-as-coordination-substrate property has failed and PLINY surfaces to PRINCIPAL.

---

## §8 — N=1 provenance

Per `MAJOR_POLYBIUS.md` §15 honest-scope + `operating-disciplines.md` §6.7.1 canon-promotion gate, framed parallel to Arcs 27-35's N=1 framing pattern.

### §8.1 — Part 1 (author tags) N=1 framing

- **N=1 bit-by-it of the defect (full failure mode in observed practice):** the original stoa--e39 misread, 2026-05-04, ~25-min coordination stall during arc-21 §5.4 review handoff. Single observation today; defect class is "POLYBIUS-pair bw-timeline misattribution under timestamp-and-content-pattern inference."
- **N=4 bit-by-it of informal-partial-adoption:** the `[radio-check <slug>]` heartbeats observed across Arcs 32 / 33 / 34 / 35. Each is an instance of the legacy-form tag in practice; none was a worked-when-applied test of the full §7.1 beat 5 + §7.7 canon because the `[from:]` convention is new in Arc 36.
- **N=0 worked-when-applied (controlled comparison):** no prior arc has operated under the full §7.1 beat 5 + §7.7 canon. Arc 36's self-application (per A11 Part 1) is the first observation. Accretes as future arcs ship under the canon and surface either successful application (timeline-arithmetic compute reliably from tagged comments) or fresh failure modes (e.g., a slug-match edge case the four-case procedure does not cover, a non-POLYBIUS-but-attribution-relevant comment class).
- **Why the discipline is in canon NOW despite the single observation:** PRINCIPAL declared the no-deferrals stance (2026-05-17) explicitly reversing the v1 scope-recut. §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

### §8.2 — Part 2 (cron expiry) N=1 framing

- **N=0 bit-by-it of the failure mode in observed practice:** the concern is structural-not-observed. Multi-day autonomous engagements exceeding the 7-day cap have not yet bitten POLYBIUS_the_stoa or any other PLINY-side autonomous engagement in 13+ days of substrate operation. Defect class is "polling-cron silent expiry under multi-day autonomous engagement" — the failure mode the docs document but has not yet been observed in this team's practice.
- **N=0 worked-when-applied:** no arc has yet operated under the §11 step 1.5 renewal canon. Arc 36's self-application (per A11 Part 2) is the first observation. For a sub-24h arc the renewal will not actually fire during the arc; the worked-example property is "cron IS-able to fire it" (renewal cron exists in CronList at arc close per §7.2). Accretes as future arcs operating under §11 step 1.5 either successfully extend through the renewal moment or surface fresh failure modes (renewal-cron miss-fires, chain breaks, etc.).
- **Session-lifecycle failure mode N framing (added rev2 per ARGUS F2):** a separate failure mode the v1 design framed implicitly and rev2 names explicitly: fresh-conversation / `/clear` / session exit destroys both crons regardless of the renewal mechanism. N=structural — this is documented at https://code.claude.com/docs/en/scheduled-tasks (Limitations section) as a known property of session-scoped tasks, and `MAJOR_POLYBIUS.md` §7.4 line 437 confirms substrate canon. N=0 observed-in-practice for the specific class "POLYBIUS lost a polling cron to a session-lifecycle event during an autonomous engagement on the-stoa" (the substrate has been operating for ~13 days; long-running engagements have spanned compactions but not session restarts in observed practice). N=0 worked-when-applied for the §13.4 → §11 setup re-bootstrap path being the recovery for this class — Arc 36's design names it as the recovery; future engagements will accrete observations as session-lifecycle events occur.
- **`durable: true` open-bug provenance (rev2):** the `CronCreate` `durable: true` parameter is documented in the tool schema as "persist to `.claude/scheduled_tasks.json` and survive restarts" but has an open unresolved bug (anthropics/claude-code issue #40228, opened 2026-03-28) at design time where the flag does not currently persist. The design encodes `durable: true` as honest intent — the flag matches documented schema, and when the bug is fixed the design works correctly without further canon revision. The load-bearing recovery is `MAJOR_POLYBIUS.md` §9 step 7 long-running-engagement re-setup (PRINCIPAL-consent-required; rev3 m5 re-cited away from §13.4), not the durable flag. N=1 observation of the bug from the linked issue; the design's posture is to encode the documented-schema-honest path and not rely on the flag for recovery.
- **Cadence-switch × renewal composition N framing (added rev3 per ARGUS F4):** a composition concern between two pieces of existing canon — the §7.2 cadence-switching pattern (per-seat-unilateral; rotate own cron on `[cadence: …]` tag detection) and the new §11 step 1.5 renewal mechanism. Without the rev3 F4 fix, any cadence-switch invalidates the paired renewal cron's inline `{{POLLING_CRON_ID}}` + `{{CADENCE}}` slot values; at +144h fire time the renewal cron mis-classifies the case as session-lifecycle (via STEP 1a) and the renewal chain dies silently. N=0 observed-in-practice for this specific composition failure (substrate has been operating ~13 days; no autonomous engagement has yet exercised both a cadence-switch AND a +144h renewal in the same engagement). N=structural for the composition concern — derivable from reading §7.2 + §11 step 1.5 side-by-side, which is exactly what ARGUS-rev2 did. N=0 worked-when-applied for the F4 fix — Arc 36's design names the fix at §5.3 polling-cron-template STEP 4 extension; future engagements that exercise both cadence-switching AND multi-day renewal will accrete the worked-when-applied evidence. The F4 fix is structurally clean (lock-step rotation of both crons via existing CronDelete + CronCreate primitives + the existing slot-lifecycle dance from §11 step 1.5 initial setup) — no new primitive required.
- **One-shot auto-delete dependency N framing (added rev5 per ARGUS F6 terminating-shape fold):** the rev5 design rests structurally on the runtime's one-shot auto-delete property — Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks "Set a one-time reminder" section: "Claude schedules a single-fire task that deletes itself after running") guarantee that a non-recurring scheduled task is removed by the runtime after its single fire completes. The rev5 fold removes the renewal cron's STEP 1a explicit self-CronDelete (which had forced a chicken/egg cross-reference that ARGUS-rev4 F6 surfaced as broken) and replaces it with reliance on the auto-delete property — both the setup dance + cadence-switch dance collapse to terminating shapes only because the property holds. N=0 observed-in-practice for one-shot auto-delete failure (the substrate has not had an autonomous engagement that observed a one-shot fire and verified the cron was removed from CronList post-fire — but the property is documented behavior and the docs do NOT name any caveat about prompt errors affecting deletion, so the encoding is documented-honest). N=structural for the dependency — if the runtime's auto-delete were to fail (e.g., an undocumented edge case where the cron-firing process is interrupted between prompt execution and the runtime's post-fire cleanup), the failure mode would be silent accumulation of dead one-shot crons in the session's cron-table; detection surface would be CronList output growing unboundedly across engagement, recovery would be operator-side explicit cleanup or session restart. The dependency is honestly encoded — if a future observation surfaces an auto-delete failure mode, the appropriate response is to add the explicit self-CronDelete back at STEP 1a (re-opening the F6 chicken/egg but with the trade-off then explicit) OR to ship a periodic operator-side cleanup beat. Neither is needed under the documented behavior. N=0 worked-when-applied for the rev5 terminating-shape — Arc 36's design picks the shape; future engagements that span multiple cadence-switches OR multi-day renewals will accrete worked-when-applied evidence of the auto-delete property holding (or surface the failure mode if it does not).
- **Why the discipline is in canon NOW despite zero observation:** same PRINCIPAL no-deferrals declaration. Part 2 is structural-not-observed; PRINCIPAL declared the structural concern warrants the fix NOW rather than waiting for the multi-day engagement that triggers it (which would carry a 6-day dead-air recovery cost). The F4 + F5 + F6 fixes are all in the same arc because shipping the renewal mechanism without them would create the composition gap explicitly — accepting it as a documented failure mode (PLINY routing rejected option (iv) per fix-known-bugs-immediately discipline). Better to ship them together. The rev5 F6 terminating-shape fold is the convergence point — the design's structural dependency surface is now: one-shot auto-delete reliability (documented; rev5 dependency), `durable: true` honest-intent encoding (rev2; not load-bearing per rev3 reframe), and bug #40228 closure surveillance (out-of-scope per §10 follow-up).

### §8.3 — Same N=1 framing as Arcs 27-35

Mirrors Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's `MAJOR_POLYBIUS.md` §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, Arc 32's family (§5.10.3 / §5.9.4.1 / §5.1.3 / §19.6.4), Arc 33's §27.6, Arc 34's §18.5 + §5.11.6, Arc 35's §28.7.

---

## §9 — Self-assessed weak points

Per CAPTAIN_DAEDALUS §6.2 — honest gap-naming so ARGUS picks up what I missed.

### §9.1 — STEP 1.5 prose precision (parser-mechanical-execution discipline is subtle)

The STEP 1.5 prose in §5.3.b is the load-bearing structural surface of Part 1 — it's where the §7.7 procedure becomes mechanical in the polling-cron parser. The prose I drafted names the four-case procedure + slug-match + derived-timestamp lists, but the mechanical execution under load (when the parser is in a unified-poll over multiple stores, processing dozens of new comments per fire) requires the four-case classification to be applied to EVERY new comment, not just POLYBIUS-shaped ones. A parser that short-circuits "looks like a POLYBIUS comment → apply case 1/2/3; everything else → skip" works in most cases but misses the case-4 branch where an untagged COMMENT-BY-POLYBIUS (legacy or accidentally-untagged) needs to fall to low-confidence handling rather than being silently dropped from `last_self_activity` / `last_peer_activity`. The current STEP 1.5 wording covers this implicitly via the "any/no tag" case-4 branch, but the prose could be tightened to make the per-comment classification explicit. ARGUS should evaluate whether the STEP 1.5 prose-precision is sufficient for the parser-mechanical-execution to be deterministic under load, or whether a worked example (e.g., a 5-comment timeline walked through the four cases) belongs in the template body.

**Why I shipped this shape anyway:** worked-example expansion in the TEMPLATE body would push the template from 161 → ~180 lines and split the "fire-loop body" framing — the template's job is the fire-loop, not a teaching artifact. The §7.7 procedure prose carries the teaching (with the worked example landing in §7.7's "Worked example (Arc 36 itself)" subsection). STEP 1.5 is the mechanical executor; §7.7 is the procedural canon. ARGUS may surface this as needing a parallel worked-example block in STEP 1.5 — if so, the right shape is a 5-line commented example inside the STEP 1.5 block, not a full teaching expansion.

### §9.2 — Cite-comment resolution coverage (easy to miss one site)

The §6.1 cite-site table enumerates 19 new cross-references. The §4.3 probe walks each and verifies, but the probe walks by `grep` patterns — any cite I FORGOT to enumerate in §6.1 will not be probed-for in §4.3, and any cite ADA introduces that is NOT in §6.1 will not be probed-for either. The failure mode is silent: a cite that points to "§7.7" reads as resolved against any line beginning `### 7.7`, but a cite that points to "§7.1 beat 5" requires the prose at §7.1 to actually contain "beat 5" (numbered list item 5) — if ADA's edit makes the 5th item a sub-bullet rather than a numbered top-level item, the cite reads as resolved but the content the cite expects is not at the resolved location. ARGUS should evaluate whether the §4.3 probe set is precise enough to catch structural-but-not-text-level drift, or whether a tighter cite-resolution probe (e.g., one that asserts the §7.1 numbered list has exactly 5 items, with the 5th item containing the convention introduction) belongs in §4.3.

**Why I shipped this shape anyway:** the §4.3 probe set is calibrated to catch the failure modes that have actually surfaced in prior arcs (renumbered sections, missing cross-refs, dropped section headers). Structural-but-not-text-level drift has not been an observed failure mode in Arcs 27-35; designing probes against unobserved failure modes is the over-specification trap. ARGUS may surface this as needing tighter probes; if so, the §4.1.1 probe block (line-counting awk on §7.1's numbered-list items) is the right surface for the addition.

### §9.3 — A5 choice rationale (α vs β has stakes worth naming)

The §3.1 rationale for picking (α) over (β) rests on three properties: parallel-to-existing-numbering, cleaner-reader-contract, and small-MAJOR_POLYBIUS-cite. All three are judgment calls. A reader who prefers dense-integration-over-new-structure (β) would dispute property 1 ("§27 and §28 are not actually parallel — they're top-level discipline additions; §7.7 inside an existing §7 numbered subsection is structurally different") and property 2 ("§7.1 reads densely already; one more sub-heading is not load-bearing"). I picked (α) because the precedent is structural (Arcs 33 + 35 both append-only at new top-level numbers) and because the §7.4 wording update + §7.1 5th-beat addition keeps the disciplinary surfaces separated (radio-check vs. tag-convention vs. parsing-procedure). ARGUS should evaluate whether (β) reads cleaner from a different reader-frame (e.g., the reader who lands at §7.1 looking for the full coordination protocol surface in one place) and whether the (α) split adds navigation cost that outweighs the structural clarity. The α choice is recoverable inside the same arc's revision cycle (per §25.3 DAEDALUS-discretion bar), so this is not a PRINCIPAL-gate; ARGUS may surface (β) as the better pick without blocking the arc.

### §9.4 — Renewal-cron prompt body complexity (Part 2) — RESOLVED in rev2 (kept as breadcrumb)

(rev2 status: ARGUS-rev1 F1 confirmed this as load-bearing; PLINY-rev1 routed disposition to ship the inline-slot-values shape per the §9.4 v1 "Why I shipped this shape anyway" defense — option (a). Rev2 §5.1.d implements option (a): the renewal-cron prompt body is engagement-specific at setup time with ALL slot values pre-substituted INTO the body before `CronCreate`. STEP 4 of the renewal-cron prompt body carries the next-renewal's prompt-body generation logic inline — replace `{{POLLING_CRON_ID}}` with the new id, keep all other slot values unchanged. No template re-substitution at fire time. The state-management concern is resolved structurally.

This breadcrumb is preserved (not deleted) so ARGUS-rev2 can verify the v1 → rev2 transition was actually made in §5.1.d. The §9.4 v1 framing was load-bearing because it correctly identified the failure mode; the rev2 §5.1.d structural change is what resolves it.)

### §9.4a — Renewal-cron prompt-body size + readability — RESOLVED in rev3 per ARGUS-rev2 concurrence (kept as breadcrumb; rev5 m12 fact-precise reframe of 50-task-ceiling math)

(rev3 status: ARGUS-rev2 concurred with DAEDALUS rev2 disposition — readability-not-ceiling. The renewal-cron prompt body weighs ~50 lines per cron in the rev2 worked example; rev3 m4 enumeration of all 13 slots inline pushes the worked-example block to ~75 lines but the underlying renewal-cron PROMPT itself remains ~50 lines of executable text — the slot-table enumeration is documentation/auditing context, not part of the substituted CronCreate prompt. The 25,000-byte `loop.md` ceiling is `/loop`-specific per Claude Code docs and does not extend to arbitrary `CronCreate` prompts. The size is the load-bearing trade-off for F1+F2+F3+F4 correctness; ARGUS-rev2 concurred as non-load-bearing. No rev3 action.

**Rev5 m12 fact-precise reframe of 50-task-per-session ceiling math.** Prior framings in §9.4a / §10 / surrounding citations called the 50-task-per-session CronCreate ceiling "abundant headroom" given 2 crons per engagement = 25 concurrent engagements. ARGUS-rev4 surfaced the precise reading: 25 concurrent engagements is the EXACT-FIT capacity ceiling, not abundant headroom. Per Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks "Manage scheduled tasks": "A session can hold up to 50 scheduled tasks at once"), the rev5 design's 2-crons-per-engagement (polling + renewal) shape means 25 concurrent engagements is the hard ceiling — a 26th engagement would fail to CronCreate. This is hygiene-only for Arc 36 (typical engagement count per session is far below 25; the substrate has not yet had a session with > 3 concurrent engagements in observed practice), but the math is exact-fit not abundant. Surfaced for future-arc capacity-planning awareness; the 25-engagement ceiling becomes a load-bearing constraint if multi-engagement scale-out becomes a project goal.)

### §9.4b — `durable: true` open-bug-dependence — RESOLVED in rev3 per ARGUS-rev2 concurrence (kept as breadcrumb)

(rev3 status: ARGUS-rev2 concurred with DAEDALUS rev2 posture — honest-intent encoding with explicit bug citation + §9 step 7 / §13.4 re-entry as load-bearing recovery (rev3 m5 re-cite away from §13.4-as-sole-recovery). Per ARGUS-rev2 concurrence the bug-closure surveillance belongs in §10 follow-ups (post-arc substrate-watch ticket) NOT in canon (e.g., not a §14 daily-cadence beat). No rev3 action; design posture unchanged.)

### §9.4c — Cadence-switch × renewal composition — RESOLVED in rev3 per F4 fold (kept as breadcrumb)

(rev3 status: ARGUS-rev2 F4 surfaced this as load-bearing composition concern between §7.2 cadence-switching and §11 step 1.5 renewal mechanism. PLINY-rev3 routed to Handle (i) — extend polling-cron-template STEP 4 to ALSO rotate the paired renewal cron. Rev3 §5.3.d1 implements Handle (i): STEP 4 of the polling-cron template now performs lock-step rotation of BOTH the polling cron AND the paired renewal cron on any cadence-switch event. New `{{RENEWAL_CRON_ID}}` slot added at §5.3.a (substitution-slot table); §11 step 1.5 slot-lifecycle note documents the chicken/egg setup ordering; STEP 1a's session-lifecycle no-op branch now self-CronDeletes (no longer perpetuates stale renewal chain). The composition concern is structurally resolved. This breadcrumb is preserved so ARGUS-rev3 can verify the rev2 → rev3 transition actually landed across §5.1.d + §5.3.a + §5.3.d1 + §3.7 + §4.4.2 + §8.2.)

### §9.5 — Self-application probe (§4.4.2) — REFRAMED in rev3 per m6 chicken/egg honesty

§4.4.2's rev2 framing was internally inconsistent (ARGUS-rev2 m6): the probe asserted that the POLYBIUS_the_stoa polling cron `c4482646` should be "registered with the renewal mechanism per the new §11 step 1.5," but `c4482646` was created BEFORE the canon shipping in this arc was available. Rev3 §4.4.2 (per PLINY routing of m6) rewrites the probe to name the chicken/egg honestly: signal (a) is `c4482646` still in CronList at arc close (polling-cron-survived-the-engagement worked-example); signal (b) is that NO renewal cron is expected for Arc 36 itself; signal (c) is that future arcs are where renewal-cron registration becomes observable under shipped canon. This is consistent with Arc 35's self-application limitation pattern (per-CAPTAIN trailers exist on commits made during Arc 35, but Arc 35's own dispatch commits pre-date the trailer canon and don't carry it).

The rev3 reframing makes the self-application probe internally consistent. The earlier rev2 framing's "renewal cron is expected" assertion was a residual artifact of the v1 design assumption that POLYBIUS_the_stoa would re-bootstrap mid-arc; that assumption was already wrong by rev2 (chicken/egg) but the probe text was not updated. ARGUS-rev2 m6 caught the inconsistency; rev3 fixes the probe. The fundamental observational-vs-enforced trade-off (mid-arc verification requires cross-session primitive that does not exist) is still a known limitation — ARGUS-rev2 concurred as non-load-bearing — but the probe NOW honestly names what it is and is not checking.

### §9.6 — F4 fix's double-re-bind dance complexity (rev3 residual concern) — CONCURRED non-load-bearing by ARGUS-rev3; SUPERSEDED in rev5 by F6 terminating-shape collapse (kept as breadcrumb)

The rev3 F4 fix at §5.3.d1 STEP 4 introduced a four-step CronCreate dance on every cadence-switch (STEP 4.1 polling rotate → STEP 4.2 renewal rotate → STEP 4.3 polling re-bind → STEP 4.4 renewal re-bind) due to the chicken/egg need to populate `{{RENEWAL_CRON_ID}}` and `{{POLLING_CRON_ID}}` cross-references between the two crons. The same dance happened at initial autonomous-mode setup (per §11 step 1.5 slot-lifecycle note).

**ARGUS-rev3 verdict (rev4 status):** PASS — dance shape IS the cleanest available given primitive constraints; chicken/egg inherent to CronCreate's return-id-after-prompt-fixed semantics; without CronUpdate, CronCreate + CronCreate-again is the only deterministic path; 4-step structure is minimum-op-count; complexity IS irreducible cost of A7/A10/A14 commits already locked in directive. NOT load-bearing-on-its-own (correctly-shaped solution). Breadcrumb retained so ARGUS-rev4 can verify the rev3 → rev4 transition (m11 names the partial-failure-state recovery; otherwise §9.6 remains concurred).

**Rev5 status (F6 terminating-shape collapse SUPERSEDES this concern's framing):** ARGUS-rev4 F6 surfaced that the 4-step cadence-switch dance + 5-step setup dance were both leaving the polling cron's RENEWAL-pointing slots baked to dead step-2 renewal ids, with the rev4 fix incomplete. PLINY routing enumerated 4 candidate terminating shapes; DAEDALUS-rev5 picked framing 4 (skip explicit STEP 1a self-CronDelete; rely on one-shot auto-delete per Claude Code docs verified by WebFetch). This collapses the cadence-switch dance from 4-step → 2-step and the setup dance from 5-step → 4-step. The "double-re-bind dance complexity" §9.6 named is now reduced to a single-stale-id residual at the polling cron's `{{RENEWAL_CRON_ID}}` slot per cadence-switch cycle, with one-shot auto-delete as the orphan-cleanup mechanism. See §9.8 (rev5) for the new structural-dependency surface that replaces the prior dance complexity.

**Why I shipped the rev3/rev4 shape (historical):** the chicken/egg was assumed inherent to the primitive set (CronCreate returns id; no way to substitute the new id into the body in the same call). The two-step CronDelete+CronCreate dance was the same pattern used at initial setup per §11 step 1.5 slot-lifecycle note — consistent design across both setup and cadence-switch surfaces. The actual terminating-shape pick (rev5) was to remove the consumer that REQUIRED knowing the renewal cron's own id (STEP 1a self-CronDelete) by replacing it with the one-shot auto-delete property. The rev3/rev4 shape was correct given the assumed primitive constraints; rev5 finds that the runtime provides a stronger primitive (one-shot auto-delete) that obsoletes one whole chicken/egg layer.

### §9.7 — F5 fix's prompt-body-literal inlining (rev4 residual concern) — CONCURRED non-load-bearing by ARGUS-rev4 (kept as breadcrumb)

The rev4 F5 fix at §5.3.a adds a `{{RENEWAL_CRON_PROMPT_BODY}}` slot to the polling-cron template, carrying the full renewal-cron prompt body as inline literal text (~80 lines per polling cron). The structural property F5 establishes is good — STEP 4.2 cadence-switch can now CronCreate the fresh renewal cron deterministically without F1 or F3 regression. Two residual concerns ARGUS-rev4 evaluated:

1. **Polling-cron / renewal-cron prompt-body drift across hand-edits.** If a future arc edits the renewal-cron prompt body at `operating-disciplines.md` §11 step 1.5 (extending STEPs 1-5, changing the log-comment text, adding a new STEP, etc.) but does NOT propagate the same edit into the polling-cron template's inline `{{RENEWAL_CRON_PROMPT_BODY}}` slot value (which lives outside the renewal-cron template — it's a captured literal at engagement-setup time), the polling cron's STEP 4.2 will CronCreate the fresh renewal cron with the OLD body. The drift is silent: the freshly-CronCreate'd renewal cron at the new cadence executes the OLD STEPs, not the new ones. Recovery is via the operator's next autonomous-mode setup (which re-captures the current renewal-cron template body into the slot value), but engagements that don't re-setup will run with the stale body until the next +144h renewal. Detection surface: the worked example block at §5.1.d (rev4 polling-cron-side enumeration) MUST be kept in sync with the renewal-cron prompt body template above it; if they drift visually in design.md they will drift mechanically in deployed substrate. This is the same drift surface as any duplicate-source-of-truth in canon (cite-comment plan at §6.1 exists precisely to catch this), but the F5 slot value is a literal copy of the renewal-cron template body rather than a section cite — drift detection cannot rely on cite resolution.

2. **Placeholder-substitution mechanism for cadence-switch re-substitution.** The §5.1.d worked example uses `<PLACEHOLDER:POLLING_CRON_ID>` and `<PLACEHOLDER:CADENCE>` markers inside the `{{RENEWAL_CRON_PROMPT_BODY}}` literal — markers that STEP 4.2 re-substitutes at cadence-switch time. The slot-lifecycle note (§11 step 1.5 step 0) names this approach but explicitly allows ADA-discretion on the representation (named-group regex, sentinel value, `{{}}` braces with sentinel, etc.). Allowing the discretion is correct (mechanism-not-prescribed-from-design) but creates an ambiguity surface: ADA's chosen representation MUST be unambiguous against the renewal-cron prompt body's existing literal content. If ADA chooses `<PLACEHOLDER:X>` and the renewal-cron prompt body happens to contain literal `<PLACEHOLDER:X>` text in a comment or example, the substitution would fire on both occurrences. The risk is low (the renewal-cron prompt body's literal content does not naturally contain such markers), but ARGUS-rev4 evaluated whether the slot-lifecycle note should prescribe a single canonical placeholder format (e.g., `__POLLING_CRON_ID__` with a specific sentinel) rather than ADA-discretion. The trade-off is between prescribed-format-with-low-ambiguity-risk vs ADA-discretion-with-implementation-flexibility.

**ARGUS-rev4 verdict (rev5 status):** PASS on both sub-concerns. (1) drift surface: NOT load-bearing; maintenance-discipline equivalent to any duplicate-source-of-truth in canon (mitigation is procedural; review-time + grep-pattern catch reasonable; bounded recovery via operator's next autonomous-mode setup). (2) placeholder marker format: NOT load-bearing; ADA-discretion appropriate (notation inconsistency in design text is a presentation matter ADA resolves at build time; substrate-internal implementation detail). Both concurred. Breadcrumb retained.

**Why I shipped this shape anyway (historical):** F5 is the only F1+F3-consistent path for STEP 4.2 to CronCreate the fresh renewal cron deterministically. The drift concern (1) is a maintenance-discipline issue that applies to ANY inline-literal duplicate-source-of-truth in canon — Arc 36 cannot solve it structurally without re-opening F1 (template-reference-at-fire-time, which was rejected on engagement-specificity grounds) or F3 (CronList-prompt-text recovery, which was rejected on ~80-char truncation grounds). The placeholder-substitution concern (2) is genuinely ADA-discretion since the substrate-internal representation does not affect the substrate's external behavior. ARGUS-rev4 concurred on both.

### §9.8 — Rev5 F6 terminating-shape: one-shot auto-delete dependency + best-effort slot semantics (rev5 residual concerns)

The rev5 F6 terminating-shape fold (§3.7 + §5.1.d STEP 1a + §5.3.d1 STEP 4 + §11 step 1.5 4-step dance) collapses the renewal mechanism's setup + cadence-switch dances from rev4's 5-step / 4-step shapes to rev5's 4-step / 2-step shapes. The collapse rests structurally on the runtime's one-shot auto-delete property — Claude Code docs (https://code.claude.com/docs/en/scheduled-tasks "Set a one-time reminder": "Claude schedules a single-fire task that deletes itself after running") guarantee that a non-recurring scheduled task is removed by the runtime after its single fire completes, with no documented caveat about prompt-execution affecting deletion. Two residual concerns ARGUS-rev5 should evaluate:

1. **One-shot auto-delete property is undocumented as unconditional.** The docs phrase the property as a positive statement ("Claude schedules a single-fire task that deletes itself after running") but do NOT explicitly enumerate the edge cases that would prevent the auto-delete (prompt error during fire, session crash mid-fire, runtime bug, etc.). The rev5 design treats the property as load-bearing — if it fails, the failure mode is silent accumulation of dead one-shot crons in the session's cron-table; detection surface would be CronList output growing unboundedly across cadence-switches or renewal chains; recovery is operator-side explicit cleanup OR session restart (both consent-mediated, not transparent). The rev4 design did NOT rely on this property — it had an explicit STEP 1a self-CronDelete that worked regardless of runtime auto-delete behavior. The trade-off rev5 makes: better dance shape (terminating, not regress-prone) in exchange for a load-bearing dependency on a runtime property that is documented but not explicitly guaranteed-unconditional. ARGUS-rev5 may evaluate whether the property's robustness should be probed by an additional §4 falsification probe (e.g., a CronList-count-stability probe across an engagement) OR whether the documented-honest encoding is sufficient.

2. **Polling cron's `{{RENEWAL_CRON_ID}}` slot may carry a one-time stale id between setup and the first cadence-switch (and between successive cadence-switches).** Per §11 step 1.5 rev5 4-step dance + §5.3.d1 STEP 4 rev5 2-step dance, the polling cron's slot is populated with the LIVE renewal cron's id at setup step 3, then becomes stale-by-one-cycle after step 4's renewal re-CronCreate. At the next cadence-switch, STEP 4.1's `CronDelete {{RENEWAL_CRON_ID}}` no-ops gracefully against the dead id; the live renewal cron is orphaned-relative-to-the-polling-cron's-slot but self-cleans via one-shot auto-delete at +144h. The trade-off rev5 accepts: at most one orphan renewal cron self-cleaning per cadence-switch cycle, in exchange for setup + cadence-switch dance termination. The orphan-count is bounded (1 per cycle), the self-clean is bounded (+144h max), and the slot converges to a live id only at the next +144h renewal-fire's STEP 4a hygiene re-bind (per §5.1.d STEP 4a) — NOT at the next cadence-switch (per §5.3.d1 STEP 4 sub-step ordering note: STEP 4.2 does not re-bind the polling cron's slot; the new polling cron created in STEP 4.1 carries forward the stale value at substitution time). ARGUS-rev5 may evaluate whether the bounded staleness is acceptable OR whether the strict-mutual-awareness alternative (5-step setup dance with explicit polling-cron-slot re-bind to `<final_renewal_id>` at step 5, accepting the recursive nature) should be the default ship.

**Why I shipped this shape anyway:** the rev4 design hit the F6 regress that PLINY routing surfaced — any attempt to maintain strict mutual awareness between the two crons via explicit cross-reference re-bind generates infinite re-bind regress (step 5 needs step 6, step 6 needs step 7, ...). PLINY enumerated 4 candidate terminating shapes; framings 2 + 3 were ruled out (framing 2 makes the renewal-cron self-discovery broken; framing 3 re-opens F3 truncation-fragility); framing 1 + 4 both rely on a "best-effort tolerance for stale ids" property. Framing 4 (skip STEP 1a self-CronDelete entirely; rely on one-shot auto-delete) is the more aggressive terminating shape — it removes the renewal cron's `{{RENEWAL_CRON_ID}}` slot dependency ENTIRELY, not just for cadence-switch — which collapses the setup dance further than framing 1 would. WebFetch on the Claude Code docs verified the one-shot auto-delete property as documented behavior; no caveat about prompt errors. The dependency is honestly encoded per rev5 §8.2 N=1 framing; if a future observation surfaces an auto-delete failure mode, the appropriate response is to add the explicit self-CronDelete back at STEP 1a (re-opening the F6 chicken/egg but with the trade-off then explicit) OR to ship a periodic operator-side cleanup beat. Neither is needed under the documented behavior; documented-honest encoding is the appropriate posture.

---

## §10 — Out of scope (A14 hard-locked)

Bullet list of related concerns Arc 36 v2 deliberately does NOT address, with one-line reasons. These match the directive's A14 hard-locks (cited here so ADA does not scope-creep and ARGUS can frame what risks belong to this arc vs a future one):

- **Non-POLYBIUS author-tag extension** — A2.5 + A14 hard-lock; future arc may extend with explicit scope. Arc 36's parser case 4 explicitly classifies PLINY / CAPTAIN / pair-programmer comments as substance-only.
- **`[radio-check <slug>]` form modification** — already established in arc-21; Arc 36's §7.1 beat 5 introduces `[from:]` as new sibling, not replacement.
- **Retroactive bw-history tagging** — Arc 36 is forward-only; §7.7 procedure case 4 covers legacy untagged comments via low-confidence fallback.
- **Option 2 watcher-cron** — A7 decision matrix rejected up-front; renewal stays per-seat unilateral (chained one-shots) per §11 step 1.5.
- **Mechanical parser enforcement** — no pre-comment hook, no CI lint. Arc 36 ships prose canon + parser-step template; mechanical enforcement is a future arc per §27 mechanical-narrow + agent-inspection precedent IF non-compliance recurs.
- **install.sh changes** — slot additions are template-internal; no deploy-list wiring required. (§8.4 install.sh smoke beat non-applicable; no new substrate files added.)
- **Cross-tier-write-upward capability** — §7.5 write boundary unchanged. §7.4 bidirectional `[for:]` is about TAG direction, not write direction.
- **CronList wrapper utility** — no helper module ships; the renewal cron's STEP 1 reads CronList directly per A7 spike's confirmed primitive set.
- **Cross-seat renewal coordination** — each seat renews its OWN cron unilaterally per §11 step 1.5 (mirror of §7.2 per-seat-unilateral cadence-switching).
- **Cloud-cron renewal** — cloud cron is a documented limitation per arc-21 §A8; no cloud-cron renewal logic ships.
- **anthropics/claude-code issue #40228 closure tracking (rev2 follow-up; rev3 confirmed by ARGUS-rev2 concurrence).** The `durable: true` flag has an open unresolved bug at design time (encoded as honest-intent in §5.1.d). When the bug is fixed, the renewal cron's `durable: true` would become load-bearing (rather than honest-intent only). Tracking the issue closure as a substrate-update trigger is OUT of this arc's scope — file a substrate-watch ticket post-arc (`stoa--xxx`) so the canon revision happens cleanly when the bug closes. ARGUS-rev2 concurred that this belongs in §10 follow-ups (not §14 daily-cadence canon).
- **Cadence-switch × renewal worked-when-applied (rev3 follow-up per F4 fold; rev5 narrowed per F6 terminating-shape collapse).** The F4 + F5 + F6 stack at §5.3.d1 STEP 4 lock-step rotation has N=0 worked-when-applied (per §8.2 N framing) — the substrate has not yet had an engagement that exercised BOTH cadence-switching AND multi-day renewal in the same arc. Future arcs operating under shipped canon either (a) cleanly exercise both (lock-step 2-step rotation observed in CronList over the arc lifetime; renewal chain extends correctly across cadence-switch events; orphan renewal crons self-clean via one-shot auto-delete) or (b) surface fresh failure modes (e.g., one-shot auto-delete fails to remove a fired cron, accumulating dead one-shots in the session's cron-table; OR the 2-step dance's sub-step ordering races against an interrupted polling-cron fire). File a substrate-watch ticket post-arc to accrete the worked-when-applied evidence as engagements naturally exercise the composition.
- **One-shot auto-delete reliability worked-when-applied (rev5 follow-up per F6 terminating-shape fold).** The rev5 design rests structurally on the runtime's one-shot auto-delete property (Claude Code docs verified by WebFetch at design time: "Claude schedules a single-fire task that deletes itself after running"). N=0 observed-in-practice (the substrate has not yet had a one-shot cron fire under autonomous-mode operation in a way that was verified to be removed from CronList post-fire). Future arcs operating under §11 step 1.5 rev5 will accrete worked-when-applied evidence — either the property holds (one-shot crons are removed from CronList after fire; no accumulation observed) or surfaces a failure mode (CronList output grows unboundedly across engagement; manual cleanup needed). File a substrate-watch ticket post-arc to track. If the property fails in observed practice, the appropriate canon revision is to re-add explicit STEP 1a self-CronDelete (re-opening the F6 chicken/egg but with the trade-off then empirically justified) OR to ship a periodic operator-side cleanup beat in `MAJOR_POLYBIUS.md` §14.

---

## §11 — Residual questions for ARGUS (rev5)

(Carried forward to the verdict's `residual_questions_for_argus:` field at dispatch return.)

**Resolved in rev2 + rev3 + rev4 + rev5 (kept as breadcrumbs for ARGUS-rev5 verification):**

- ~~§9.4 v1 renewal-cron prompt body state-management~~ — RESOLVED via F1 inline-slot-values reshape per §5.1.d rev2 (option (a) shipped). ARGUS-rev2 verified.
- ~~§9.4a renewal-cron prompt-body size~~ — ARGUS-rev2 concurred readability-not-ceiling; rev5 m12 fact-precise reframe of 50-task-ceiling math (exact-fit at 25 engagements, not abundant headroom; hygiene-only for Arc 36).
- ~~§9.4b `durable: true` open-bug dependence~~ — ARGUS-rev2 concurred honest-intent encoding + §10 follow-up tracking is correct posture; no rev3/rev4/rev5 action.
- ~~§9.4c cadence-switch × renewal composition (F4)~~ — RESOLVED via F4 Handle (i) at §5.3.d1 STEP 4 lock-step rotation + new `{{RENEWAL_CRON_ID}}` slot at §5.3.a + slot-lifecycle dance at §11 step 1.5 + STEP 1a self-CronDelete. ARGUS-rev3 verified the rev2 → rev3 transition landed; ARGUS-rev4 verified additional rev3 → rev4 work on partial-failure-state recovery prose (m11).
- ~~m4 (worked-example all slots inline)~~ — RESOLVED via §5.1.d worked-example block enumerating all 13 slot values inline. ARGUS-rev3 verified.
- ~~m5 (§13.4 cite re-target)~~ — RESOLVED via re-cite to §9 step 7 (PRINCIPAL-consent-required). ARGUS-rev3 verified.
- ~~m6 (§4.4.2 self-app probe internal consistency)~~ — RESOLVED via §4.4.2 rewrite naming chicken/egg honestly + §9.5 reframed + §7.2 self-app block updated. ARGUS-rev3 verified.
- ~~m7 (§4.3.1 cite-resolution probe regex extension)~~ — RESOLVED via §4.3.1 grep pattern extended. ARGUS-rev3 verified.
- ~~m8 (§5.1.d STEP 4 local-time arithmetic)~~ — RESOLVED via STEP 4 explicit local-time arithmetic prose + cite + worked-example local-time cron expression. ARGUS-rev3 PASS-with-residual-m9; rev4 m9 fix landed.
- ~~§9.6 F4 fix's double-re-bind dance complexity~~ — CONCURRED non-load-bearing by ARGUS-rev3 + ARGUS-rev4; SUPERSEDED in rev5 by F6 terminating-shape collapse (dance reduced from 4-step → 2-step at cadence-switch; from 5-step → 4-step at setup). §9.6 breadcrumb retained for rev3 → rev5 transition trace.
- ~~F5 (ARGUS-rev3 signature; load-bearing local-fix)~~ — RESOLVED via `{{RENEWAL_CRON_PROMPT_BODY}}` slot added at §5.3.a + STEP 4.2 deterministic CronCreate at §5.3.d1 + §11 step 1.5 slot-lifecycle 5-step dance (rev4) / 4-step dance (rev5 collapse) + §5.1.d worked example polling-cron-side enumeration + §3.7 A9 scenario 4 cite. ARGUS-rev4 verified rev3 → rev4 landed.
- ~~m9 (m8 residual: §5.1.d "Renewal-cron CronCreate parameters" Z-suffix sweep)~~ — RESOLVED via rev4 sweep. ARGUS-rev4 verified.
- ~~m10 (§5.1.d STEP 1a parens hedge collapse)~~ — RESOLVED via rev4 collapse to slot-population-only path. ARGUS-rev4 verified. Rev5 F6 fold further removes the slot-population-only path entirely (STEP 1a now exits without explicit self-CronDelete; one-shot auto-delete handles cleanup); m10's collapse direction is consistent with rev5's terminating-shape direction.
- ~~m11 (§5.3.d1 4-step dance partial-failure-state recovery prose)~~ — RESOLVED via rev4 explicit recovery prose at §3.7 A9 scenario 4 + §5.1.d Failure-mode scenario 4. ARGUS-rev4 verified. Rev5 narrows the dance to 2-step so the partial-failure-state surface is also narrowed (2x ops vs pre-F4 collapses back to 2x ops vs rev3 single-cron, but the surface is half what rev4 had — see §3.7 A9 scenario 4 rev5 fold).
- ~~F6 (ARGUS-rev4 signature; load-bearing terminating-shape design)~~ — RESOLVED via rev5 framing-4 pick (skip explicit STEP 1a self-CronDelete; rely on one-shot auto-delete per Claude Code docs WebFetch-verified): §5.1.d STEP 1a explicit self-CronDelete removed; §5.1.d STEP 4 collapsed (single substitution, no re-bind); §11 step 1.5 slot-lifecycle dance collapsed from 5-step to 4-step terminating shape with explicit acceptance of one-time polling-cron-slot stale-id residual; §5.3.d1 STEP 4 collapsed from 4-step to 2-step terminating shape; §5.3.a {{RENEWAL_CRON_ID}} slot semantics reframed to best-effort cleanup; §5.3.e usage example updated; §3.7 A9 scenarios 3+4 reframed around one-shot auto-delete as the cleanup mechanism; §8.2 N=1 framing extended with one-shot-auto-delete dependency honesty; §6.1 cite-table gains 1 rev5 row for the Claude Code docs citation. ARGUS-rev5 verifies the rev4 → rev5 transition landed.
- ~~m12 (50-task-per-session ceiling exact-fit math)~~ — RESOLVED via §9.4a fact-precise reframe (25-engagement exact-fit ceiling, not abundant headroom; hygiene only).

**Open for ARGUS-rev5:**

1. **§9.8 (NEW) — rev5 F6 terminating-shape: one-shot auto-delete dependency + best-effort slot semantics.** Two sub-concerns: (a) one-shot auto-delete property is documented as positive but not explicitly enumerated as unconditional (no caveat about prompt errors affecting deletion is named in docs; encoded as documented-honest; if a future observation surfaces an auto-delete failure mode, the fix is to re-add explicit STEP 1a self-CronDelete or ship a periodic operator-side cleanup beat); (b) polling cron's `{{RENEWAL_CRON_ID}}` slot may carry a one-time stale id between rotations, with one-shot auto-delete as the orphan-cleanup property (bounded staleness, bounded orphan count). See §9.8 for full framing and the "Why I shipped this shape anyway" defense.
2. **§9.3 — A5 (α) vs (β) reader-frame.** (Unchanged from rev1 / rev2 / rev3 / rev4; not load-bearing per ARGUS concurrence — recoverable within arc revision cycle.)
3. **§9.5 — Part 2 self-application observability** (reframed per m6 rewrite). The fundamental observational-vs-enforced trade-off remains. Concurred non-load-bearing across rev1-rev4; mirrors Arc 35 self-application limitation.
4. **§9.1 — STEP 1.5 prose precision under load.** (Unchanged from rev1-rev4; not load-bearing per ARGUS concurrence.)
5. **§9.2 — cite-comment resolution probe precision.** (Unchanged from rev1-rev4; not load-bearing per ARGUS concurrence.)

**Rev5 fold confirmations (ARGUS-rev5 verifies the structural changes actually landed):**

- F6 fold: §5.1.d renewal-cron STEP 1a explicit self-CronDelete REMOVED (replaced with documented-honest reliance on one-shot auto-delete per Claude Code docs); §5.1.d renewal-cron STEP 4 collapsed (single POLLING_CRON_ID substitution; no re-bind sub-step 4a/4b dance — STEP 4a remains as hygiene optimization, not correctness requirement); §5.1.d worked examples (renewal-cron-side + polling-cron-side) STEPs 1a + 4 updated; §11 step 1.5 slot-lifecycle dance collapsed from rev4 5-step (with sub-step 4a + 4b) to rev5 4-step terminating shape (steps 0/1/2/3/4) with explicit acceptance of one-time polling-cron-slot stale-id residual; §5.3.a `{{RENEWAL_CRON_ID}}` slot semantics reframed as best-effort cleanup hint; `{{RENEWAL_CRON_PROMPT_BODY}}` slot definition updated to drop "internal `{{RENEWAL_CRON_ID}}`" consumer reference; §5.3.d1 STEP 4 cadence-switch dance collapsed from rev4 4-step (with STEP 4.3 + 4.4 re-bind) to rev5 2-step terminating shape (STEP 4.1 + 4.2 only) + sub-step ordering note documenting the in-fire chicken/egg resolution; §5.3.e usage example slot descriptions updated; §3.7 A9 scenarios 3+4 reframed around one-shot auto-delete as cleanup mechanism (scenario 4 also names the 2-step dance partial-failure-state narrowing); §8.2 N=1 framing extended with new "One-shot auto-delete dependency N framing" bullet; §6.1 cite-table gains 1 rev5 row (Claude Code docs URL for one-shot auto-delete); §9.6 retained as breadcrumb with rev5-supersession note; §9.7 retained as breadcrumb with ARGUS-rev4 PASS markers; §9.8 NEW: rev5 F6 fold's two residual concerns documented honestly (one-shot auto-delete documented-but-not-explicitly-unconditional + best-effort slot semantics one-time stale residual).
- m12 fold: §9.4a fact-precise reframe of 50-task-per-session ceiling (exact-fit at 25 engagements, not abundant headroom; hygiene only).

---

**End of design.md (rev5 — F6 terminating-shape + m12 folded; Part 1 untouched per ARGUS-rev1 + rev2 + rev3 + rev4 clean verdicts + PLINY routing scope-discipline across all revs; rev2 F1+F2+F3+m2+m3 PASS-verified by ARGUS-rev2; rev3 F4+m4+m5+m6+m7+m8 PASS-verified by ARGUS-rev3 with PARTIAL on F4 closed by rev4 F5 fix + residual-m9 closed by rev4 m9 sweep; rev4 F5+m9+m10+m11 PASS-verified by ARGUS-rev4 with PARTIAL on F5 closed by rev5 F6 terminating-shape fold + minor-m12 fact-precise reframe). The cycle terminates at rev5 with the F6 fold collapsing the dance complexity into a genuine terminating shape — no further re-bind regress is structurally possible given the primitive set; the design's structural dependency surface is now (a) one-shot auto-delete reliability (documented; rev5 dependency), (b) `durable: true` honest-intent encoding (rev2; not load-bearing), and (c) bug #40228 closure surveillance (out-of-scope per §10 follow-up).**
