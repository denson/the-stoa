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

**A9 failure-mode acceptance (revised after ARGUS F2 cold-audit, rev2).** The renewal mechanism protects against THREE failure modes, with the recovery path explicit for each (full prose at §5.1.d "Failure-mode acceptance"):

1. **Cron-expiry boundary (+168h window).** Steady-state continuous protection via the renewal chain while the session stays alive and active.
2. **Renewal-chain break across multi-day continuous outage (> 6 days offline).** Recovery via peer-side radio-check escalation per §7.1 beat 3 (the original v1 framing — preserved).
3. **Session-lifecycle event — fresh conversation, `/clear`, session exit (ARGUS F2 cold-audit catch).** Per Claude Code docs Limitations + `MAJOR_POLYBIUS.md` §7.4 line 437: polling crons are session-only and die when the session exits. The design encodes `durable: true` on the renewal cron as honest intent (matches documented `CronCreate` tool schema) but does NOT rely on it as load-bearing recovery — the schema-documented flag has an open unresolved bug at anthropics/claude-code issue #40228 (opened 2026-03-28) where the persist does not actually happen. Load-bearing recovery is via `MAJOR_POLYBIUS.md` §13.4 step 2: autonomous-mode entry runs the §11 setup checklist, including step 1.5, which creates a fresh cron pair. STEP 1a of the renewal-cron prompt (the polling-cron-missing branch) handles the case where a durable-surviving renewal cron fires in a session that has already re-bootstrapped via §13.4 — no-op cleanly. The session-lifecycle failure mode is therefore NOT a multi-day outage but any fresh-conversation start at any time; recovery is transparent via §13.4 re-entry. The renewal mechanism and §13.4 re-entry compose; STEP 1a is the seam.

This A9 broader-failure-mode-acceptance is what ARGUS-rev2 evaluates against; the v1 single-failure-mode framing (continuous-outage only) was qualitatively wrong about the failure-mode shape per ARGUS F2.

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
awk '/^### 7\.4/,/^### 7\.5/' substrate/operating-disciplines.md | grep -iE 'upward[- ]only|cross-tier upward|UPWARD requests only'
# Expected: zero matches (old wording fully replaced)

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

awk '/^## Substitution slots/,/^---$/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\| \`\{\{SELF_SEAT_SLUG\}\}\`|\| \`\{\{PEER_SEAT_SLUG\}\}\`'
# Expected: 2 (both new slots present in the slot table itself)
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

awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'no.*watchdog|no additional'
# Expected: ≥1 (explicitly accepts the failure mode rather than mitigating via watcher cron)

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

**§4.2.2d — STEP 1a polling-cron-missing no-op branch present (rev2 F2 seam)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'STEP 1a|polling-cron-missing|orphan-renewal|no-op'
# Expected: ≥2 (the STEP 1a branch that handles a durable renewal cron firing in a session that has already re-bootstrapped via §13.4)
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

**§4.2.5 — `MAJOR_POLYBIUS.md` §13.4 renewal-confirm-on-entry note present** (arc-22 deliverable 2.4 — recommend keeping)

```bash
awk '/^### 13\.4/,/^## 14\./' substrate/MAJOR_POLYBIUS.md | grep -cE 'operating-disciplines\.md §11|cron.*expiry|renewal'
# Expected: ≥1 (one-line note in mode-entry procedure cites §11 step 1.5 renewal mechanism)
```

### §4.3 — Cite-comment resolution probes

Every new section cite in the diff must point to a real section after Phase 2 ship. The probe walks each cite-site and verifies the target exists.

**§4.3.1 — New cite-sites all resolve**

```bash
# Build a list of every "§7.7" / "§11 step 1.5" / new-bidirectional-§7.4 cite-site touched by the arc:
grep -rnE 'operating-disciplines\.md §7\.7|operating-disciplines\.md §11.*step 1\.5|MAJOR_POLYBIUS\.md §7\.4' substrate/ \
  | grep -vE '^Binary file|/arcs/'
# Expected: ≥5 (cites land at the new §7.7 from §7.1, §7.4, MAJOR_POLYBIUS.md §7.4, polling-cron-prompt-template.md STEP 1.5, and the renewal end-of-file pointer)

# For each cite, verify the target section exists:
grep -nE '^### 7\.7 |^### 7\.4 |^### 13\.4 |^\*\*1\.5' substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md
# Expected: each target header present exactly once at its expected file
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

**§4.4.2 — Part 2 self-app: polling cron applies §11 step 1.5 renewal mechanism (rev2 F1+F2+F3 fold)**

```bash
# Verify POLYBIUS's polling cron (c4482646 per init handshake) is registered with the renewal mechanism per the new §11 step 1.5:
# (CronList is the live check; PLINY signoff runs this at arc close)
# Expected: CronList shows c4482646 (polling cron, recurring */5) AND a one-shot renewal cron scheduled at the +144h (= +6 days) mark from polling-cron creation timestamp.
# For a sub-24h arc, the renewal cron will not yet have fired; its presence in CronList is the worked-example signal.

# Additional rev2 properties to verify when the cron pair is observable:
# - Renewal cron's CronList entry shows recurring: false (one-shot).
# - Renewal cron's CronList entry shows durable: true (or, if the field is not surfaced by CronList — the bug at #40228 may also affect the CronList display — verify via the renewal-cron's prompt-body inline mention of "durable: true" in STEP 4).
# - Renewal cron's prompt body (modulo ~80-char CronList truncation) contains the polling-cron-id c4482646 as an inline value (F1 + F3 properties observable from the truncation-window of CronList).
# Self-app honest-scope note: per §8.2 rev2 Session-lifecycle-failure-mode N framing, the worked-example property is "renewal cron exists in CronList at arc close, paired with the polling cron via inline POLLING_CRON_ID slot value, with durable: true encoded as honest intent." The cron-pair surviving a fresh-conversation start during the arc is NOT a worked-example property of this arc (and is in fact undermined by the open #40228 bug); the §13.4 re-entry recovery path is the load-bearing mechanism for session-lifecycle loss, observable only across a session-lifecycle event that did not occur during the arc.
```

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
grep -rE 'watcher cron|watchdog cron|separate watcher' substrate/operating-disciplines.md substrate/templates/
# Expected: zero matches in NEW content (existing references in arc-22 directive at substrate/arcs/ are reference material and excluded)
```

**§4.5.4 — install.sh untouched**

```bash
git diff main...arc-36/build -- substrate/install.sh
# Expected: empty diff (no install.sh changes per A14 — slot additions are template-internal)
```

### §4.6 — Cosmetic + voice probes

**§4.6.1 — Voice grep clean**

```bash
grep -rE '\b[Cc]olonel\b|\bthe user\b' substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md | grep -vE 'template-slot|arcs/' | head -10
# Expected: zero non-template hits
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
# Verify no credentialed-CLI invocation appears in any ADA-built script/template:
grep -rE 'op (read|run)|gcloud |gh auth |aws |kubectl |vercel |railway |fly ' substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md
# Expected: zero matches in arc-36's edits (existing references in unrelated sections are out-of-scope)
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

**Structural shape (rev2 after ARGUS F1+F2+F3 fold):**

- **F1 fix — inline slot values.** The renewal-cron prompt body is engagement-specific at setup time. Every slot value the renewal needs (all 12 polling-cron slots PLUS the polling cron's id PLUS the renewal-cron's own next-renewal scheduling parameters) is substituted INTO the renewal-cron prompt body at the moment the renewal cron is `CronCreate`d. The renewal cron does not reference any template by file at fire time; the renewal cron's prompt body IS the complete substituted instruction set. State-management across session-clear / compact / fresh-session is the union of (a) the renewal cron's prompt body (durable across the cron's lifetime per the CronCreate-side of the system) and (b) the bw record of the polling-cron's id (in the §7.1 beat 1 radio-check handshake comment). No re-substitution of any template happens at fire time.
- **F2 fix — session-lifecycle.** The renewal cron is `CronCreate`d with `durable: true`. Per the documented `CronCreate` tool schema, this flag specifies that the task persists to `.claude/scheduled_tasks.json` and survives session restarts. PER OPEN BUG (anthropics/claude-code issue #40228, opened 2026-03-28, unresolved at design time): the `durable: true` flag is documented but does NOT currently persist; tasks die on session exit regardless. The design encodes `durable: true` as honest intent (matches documented schema; works correctly once the bug is fixed without further canon revision) — but does NOT rely on it as the load-bearing recovery mechanism. Load-bearing recovery is via `MAJOR_POLYBIUS.md` §13.4 (autonomous-mode entry): on every entry into autonomous mode, §13.4 step 2 runs the §11 setup checklist, including this step 1.5 — which spins up a fresh renewal cron paired with the fresh polling cron. Session-lifecycle loss is recovered by the operator's normal autonomous-mode re-entry; no special escalation needed.
- **F3 fix — deterministic self-discovery.** The renewal cron carries the polling cron's id as an inline slot value (`{{POLLING_CRON_ID}}`). STEP 1 of the renewal-cron prompt body is `CronList; find cron-id == {{POLLING_CRON_ID}}` (exact-match on cron-id, not a text-search against prompt-body). The ~80-char CronList prompt-truncation observed in PLINY's A7 spike does not affect the match. Composes with the F3 Handle (a) template-body re-order at §5.3 (which helps a different consumer — peer audit reading CronList — but is not load-bearing for renewal self-discovery once F3 Handle (b) is in place).

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

STEP 1a — polling-cron-missing branch (session-lifecycle no-op guard).
If {{POLLING_CRON_ID}} is absent from CronList, this renewal cron has
outlived its paired polling cron — almost certainly because the polling
cron died on a session-lifecycle event (fresh conversation, /clear,
session exit). The correct response is no-op: post a single bw comment
on {{COORDINATION_TICKET}} noting the orphan-renewal observation, then
exit without rotating any cron. The polling cron will be re-created when
{{SELF_SEAT_NAME}} next re-enters autonomous mode (per
MAJOR_POLYBIUS.md §13.4 step 2 → operating-disciplines.md §11 setup);
that re-entry will create a fresh renewal cron paired with the fresh
polling cron via this same §11 step 1.5. Comment to post:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] renewal
  cron fired without a paired polling cron (id {{POLLING_CRON_ID}} not
  in CronList — session-lifecycle event likely). No-op; awaiting next
  autonomous-mode entry per MAJOR_POLYBIUS.md §13.4."
Exit.

STEP 2 — CronCreate replacement polling cron.
CronCreate a NEW recurring cron with cadence {{CADENCE}} and the
polling-cron prompt body with slot values inline (the same engagement-
specific body the original polling cron carried — slot values are pre-
substituted into this renewal-cron prompt at setup time and carried
inline through fire). Let the returned id be <new_polling_cron_id>.

STEP 3 — CronDelete {{POLLING_CRON_ID}} (the now-superseded polling cron).
Post on {{COORDINATION_TICKET}}:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] cron
  renewed: superseded {{POLLING_CRON_ID}} with <new_polling_cron_id>;
  cadence {{CADENCE}} unchanged."

STEP 4 — CronCreate next renewal one-shot.
CronCreate a one-shot cron at +144h from now, recurring: false,
durable: true. The prompt body for this new renewal is THIS SAME
renewal-cron prompt body with one substitution: replace
{{POLLING_CRON_ID}} with <new_polling_cron_id>. All other slot values
carry through unchanged. Let the returned id be <new_renewal_cron_id>.

STEP 5 — log renewal-chain extension.
Post on {{COORDINATION_TICKET}}:
  bw comment {{COORDINATION_TICKET}} "[from: {{SELF_SEAT_SLUG}}] renewal
  chain extended: new polling cron <new_polling_cron_id>; next renewal
  cron <new_renewal_cron_id> (one-shot at +144h, durable: true)."

Exit.
```

**Worked example — substituted renewal-cron prompt body for Arc 36's
own self-application.** When POLYBIUS_the_stoa creates its polling cron
at autonomous-mode-setup on stoa--jru (cron-id `c4482646`, cadence
`*/5 * * * *`), the paired renewal cron's prompt body — pre-substituted
inline at setup time — reads:

```
[scheduled renewal fire — polybius-the-stoa polling-cron rotation on
stoa--jru; current polling cron c4482646; renewal cron self]

STEP 1 — find current polling cron (deterministic).
CronList; find the entry whose cron-id == c4482646.
[... STEP 1a, STEP 2, STEP 3, STEP 4, STEP 5 as above, with
{{POLLING_CRON_ID}} = c4482646, {{COORDINATION_TICKET}} = stoa--jru,
{{SELF_SEAT_SLUG}} = polybius-the-stoa, {{CADENCE}} = */5 * * * *,
and all other slots resolved to their setup-time values...]
```

The substituted body is what `CronCreate` receives as the `prompt`
parameter; ADA can read the substituted body directly from the renewal
cron's CronList entry (modulo the ~80-char truncation, which is why
STEP 1 matches on cron-id not on prompt-text).

**Renewal-cron CronCreate parameters (load-bearing per ARGUS m2).**
- `cron`: a 5-field expression evaluating to +144h from polling-cron
  creation. Compute the wall-clock time and emit the cron expression
  for that single minute. Example: if polling cron is created at
  `2026-05-17T22:50Z`, renewal cron fires at `2026-05-23T22:50Z`;
  emit cron expression `50 22 23 5 *`.
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
   (ARGUS F2 cold-audit catch).** Per Claude Code docs (Limitations
   section): "Starting a fresh conversation clears all session-scoped
   tasks. Resuming with `claude --resume` or `claude --continue`
   restores tasks that have not expired." Per `MAJOR_POLYBIUS.md` §7.4
   line 437: polling crons are session-only (`durable: false` by default)
   and die when the session exits. The renewal cron uses `durable: true`
   as honest intent (documented tool-schema parameter; would survive
   session restart when working) — but is subject to the open bug at
   anthropics/claude-code issue #40228 (opened 2026-03-28, unresolved
   at design time) where `durable: true` does not currently persist.

   **Recovery path (load-bearing; works regardless of the durable bug):**
   the polling cron is session-only by canon; when the session exits or
   a fresh conversation starts, both the polling cron and the renewal
   cron are lost. The next time the operator re-enters autonomous mode
   for this seat — per `MAJOR_POLYBIUS.md` §13.4 step 2 (bare or
   self-qualified trigger → run §11 setup checklist) — §11 setup
   re-runs, which includes this step 1.5, which creates a NEW polling
   cron paired with a NEW renewal cron. The renewal mechanism is
   re-bootstrapped from a clean slate. If a renewal cron from a prior
   session survives (durable bug eventually fixed) and fires in a
   session that has already created a fresh polling cron via §13.4
   re-entry, STEP 1a's no-op guard handles the orphan-renewal cleanly.

   The session-lifecycle failure mode is therefore NOT a multi-day
   outage — it is any fresh-conversation start at any time, recovered
   transparently by §13.4 re-entry. The renewal mechanism does not
   need to protect against it directly; it composes with the §13.4
   recovery path. STEP 1a's no-op guard is the seam where the two
   mechanisms meet.

No additional watchdog cron ships — the alternative (peer-side renewal
monitoring, separate watcher cron, double-cron belt-and-suspenders)
adds the same coordination-dependency problems Option 2 was rejected
for in the A7 decision matrix. Bounded staleness is acceptable;
protocol-induced bugs cost more. The renewal cron is the per-seat
unilateral mechanism; §13.4 re-entry is the cross-session-lifecycle
mechanism; together they cover the failure modes the design accepts.

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

Cross-ref to mode-entry procedure: `MAJOR_POLYBIUS.md` §13.4 step 2
(autonomous-mode entry → §11 setup) is the load-bearing recovery path
for session-lifecycle loss of the cron pair. The §13.4 note added by
this arc (per §5.2.b) closes the loop.
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

**§5.3.a — Substitution-slot table additions**

Add two rows to the substitution-slots table immediately after the existing `{{SELF_SEAT_NAME}}` row:

```
| `{{SELF_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for own seat (LEADING tag uses this; display-form name uses `{{SELF_SEAT_NAME}}`) | `polybius-the-stoa` |
| `{{PEER_SEAT_SLUG}}` | normalized lowercase-hyphenated slug for peer seat | `user-tier-polybius` |
```

Add a sentence to the post-table prose: "Display-form slots (`{{SELF_SEAT_NAME}}` / `{{PEER_SEAT_NAME}}`) are used in human-readable prose within comment bodies; SLUG slots are used in the LEADING author tag per `operating-disciplines.md` §7.1 beat 5. Both must be supplied at template substitution time."

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

**§5.3.e — Update usage example block at bottom of template**

Add slot values for the two new SLUG slots:

```
- `{{SELF_SEAT_SLUG}}` = `polybius-the-stoa`
- `{{PEER_SEAT_SLUG}}` = `user-tier-polybius`
```

Update the example radio-check handshake comment at the very bottom of the file to use the slug-form leading tag:

```
bw comment <example>--abc "[radio-check polybius-the-stoa]
cron <returned-id> cadence */5 * * * * watching {<example>--abc, <example>--def}
+ {<other>--xyz}; expected duration ~3 hours; standing by for handshake ack."
```

(Display-form name "project-tier POLYBIUS_foo" can still appear in the comment body's prose for readability; the LEADING tag uses the slug.)

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
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | `MAJOR_POLYBIUS.md` §13.4 step 2 | "per MAJOR_POLYBIUS.md §13.4 step 2 (bare or self-qualified trigger → run §11 setup)" — rev2 cite naming §13.4 as load-bearing session-lifecycle recovery |
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | https://github.com/anthropics/claude-code/issues/40228 | "anthropics/claude-code issue #40228 (opened 2026-03-28, unresolved at design time)" — open-bug citation for `durable: true` honest-intent encoding |
| `operating-disciplines.md` §11 step 1.5 (rev2 F2 fold) | https://code.claude.com/docs/en/scheduled-tasks (Limitations section) | "per Claude Code docs (Limitations section): 'Starting a fresh conversation clears all session-scoped tasks.'" |

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

### §7.2 — Part 2 self-application check

```bash
# 1. POLYBIUS_the_stoa's polling cron exists and is recurring.
# (Run in the POLYBIUS session at arc close.)
# CronList output: confirm cron c4482646 (per init handshake) is present, recurring, prompt names stoa--jru.

# 2. A renewal cron exists scheduled at +144h from polling cron creation.
# CronList output: confirm exactly one additional one-shot cron exists whose prompt body matches the renewal-cron prompt body from §11 step 1.5.
```

For a sub-24h arc the renewal cron will not have fired during the arc. Its presence in CronList at arc close is the worked-example signal. If the renewal cron is ABSENT, Part 2 self-application has FAILED — POLYBIUS_the_stoa did not apply the canon being shipped, and PLINY surfaces to PRINCIPAL.

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
- **`durable: true` open-bug provenance (rev2):** the `CronCreate` `durable: true` parameter is documented in the tool schema as "persist to `.claude/scheduled_tasks.json` and survive restarts" but has an open unresolved bug (anthropics/claude-code issue #40228, opened 2026-03-28) at design time where the flag does not currently persist. The design encodes `durable: true` as honest intent — the flag matches documented schema, and when the bug is fixed the design works correctly without further canon revision. The load-bearing recovery is `MAJOR_POLYBIUS.md` §13.4 re-entry, not the durable flag. N=1 observation of the bug from the linked issue; the design's posture is to encode the documented-schema-honest path and not rely on the flag for recovery.
- **Why the discipline is in canon NOW despite zero observation:** same PRINCIPAL no-deferrals declaration. Part 2 is structural-not-observed; PRINCIPAL declared the structural concern warrants the fix NOW rather than waiting for the multi-day engagement that triggers it (which would carry a 6-day dead-air recovery cost).

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

### §9.4a — Renewal-cron prompt-body size + readability (rev2 residual concern)

The rev2 §5.1.d renewal-cron prompt body — with inline slot values, STEP 1a no-op branch, STEP 4 next-renewal-generation logic, and the worked-example block for Arc 36 self-application — is substantially longer than v1's template-reference shape. The renewal-cron prompt body for the worked example weighs ~50 lines of substituted instruction text per renewal cron. This is acceptable (the prompt is the renewal cron's executable instruction set; clarity is load-bearing) but pushes against the 25,000-byte loop.md ceiling the Claude Code docs name for the `/loop` default prompt — though that ceiling is documented for `/loop` specifically, not for arbitrary `CronCreate` prompts. ARGUS-rev2 may surface whether the size is an actual ceiling-concern for `CronCreate`, or whether it's only a readability concern.

**Why I shipped this shape anyway:** the F1+F2+F3 dispositions together require the inline-slot-values reshape; size is a downstream consequence of the structural correctness. A shorter renewal-cron prompt body would require either re-introducing template-reference (re-opens F1) or dropping the STEP 1a no-op guard (re-opens F2's session-lifecycle composition seam). The size is the load-bearing trade-off — accepting longer prompt-bodies for correctness across the cron-expiry, session-lifecycle, and renewal-chain failure modes.

### §9.4b — `durable: true` open-bug-dependence (rev2 residual concern)

The rev2 §5.1.d encodes `durable: true` on the renewal cron as honest intent against the documented `CronCreate` tool schema. Per anthropics/claude-code issue #40228 (opened 2026-03-28, unresolved at design time), the flag does not currently persist tasks. The design's posture is: encode the documented-schema flag (so the design works correctly when the bug is fixed without further canon revision), name the bug explicitly in the failure-mode acceptance (so the design's assumption is auditable), and rely on `MAJOR_POLYBIUS.md` §13.4 re-entry as the load-bearing recovery path (which works regardless of the bug). ARGUS-rev2 should evaluate whether (a) the honest-intent encoding is sufficient given the bug, or (b) the design should drop the `durable: true` flag entirely and rely solely on §13.4 re-entry until the bug is fixed and the flag is re-introduced in a future arc, or (c) the design should track the issue closure as a substrate-update trigger.

**Why I shipped this shape anyway:** dropping `durable: true` would lose the future-proof property (when the bug is fixed, the design starts working correctly without canon revision). Tracking the issue as a substrate-update trigger is correct and lives in a follow-up — surfaced at §10 follow-ups for the post-arc accretion. The honest-intent encoding with explicit bug citation is the cleanest middle: the design works correctly today (via §13.4 re-entry, not via durable flag) AND works correctly tomorrow (via durable flag, once the bug is fixed). The audit trail is explicit at §3.7 + §5.1.d + §8.2.

### §9.5 — Self-application probe (§4.4.2) is observational, not enforced

§4.4.2 verifies that POLYBIUS_the_stoa's polling cron has a renewal cron scheduled. The verification is run at arc close by PLINY signoff via `CronList`. If POLYBIUS_the_stoa did NOT schedule the renewal cron at autonomous-mode-setup time (i.e., the canon being shipped was not self-applied during the arc), the verification surfaces the failure — but only at arc close, after the gauntlet has run. This is the same observational-vs-enforced trade-off the §27 mechanical-narrow + agent-inspection pattern accepts: the verification is reactive, not preventive. For Arc 36 specifically, POLYBIUS_the_stoa's init handshake on stoa--jru did NOT explicitly cite §11 step 1.5 renewal-cron scheduling — only a §6.5 "STEP 7" reference per the v1 directive surface (which is being superseded by Option 3 anyway). PLINY signoff at arc close needs to verify that the renewal cron is actually present, not assume it. ARGUS should surface this as a residual question: does Part 2 self-application require an active POLYBIUS_the_stoa cron-state mid-arc (verifiable now) rather than at arc close (verifiable only retrospectively)?

**Why I shipped this shape anyway:** mid-arc verification would require PLINY or DAEDALUS to query POLYBIUS_the_stoa's session for `CronList` output, which requires either a cross-session communication primitive that does not exist in the substrate or a manual PRINCIPAL relay (which defeats autonomous mode's PRINCIPAL-as-exception-handler stance). The arc-close verification is the best-available observational shape. If POLYBIUS_the_stoa's pre-arc setup did not include §11 step 1.5 renewal-cron scheduling (because §11 step 1.5 didn't exist yet at setup time — chicken/egg), PLINY signoff should accept this as a known-limitation of the self-application property: Arc 36's own POLYBIUS setup pre-dates the canon being shipped, so the canon's self-application is technically "the canon WOULD be applied if POLYBIUS were re-initialized post-arc" rather than "the canon was applied during the arc itself." This is consistent with Arc 35's self-application limitation (per-CAPTAIN trailers exist on commits made during Arc 35, but Arc 35's own dispatch commits pre-date the trailer canon and don't carry it).

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
- **anthropics/claude-code issue #40228 closure tracking (rev2 follow-up).** The `durable: true` flag has an open unresolved bug at design time (encoded as honest-intent in §5.1.d). When the bug is fixed, the renewal cron's `durable: true` would become load-bearing (rather than honest-intent only). Tracking the issue closure as a substrate-update trigger is OUT of this arc's scope — file a substrate-watch ticket post-arc (`stoa--xxx`) so the canon revision happens cleanly when the bug closes. Per §9.4b residual question 2, ARGUS-rev2 may surface that the bug-closure surveillance belongs in canon (e.g., as a substrate-update beat in `MAJOR_POLYBIUS.md` §14 daily-cadence check) rather than as a post-arc follow-up.

---

## §11 — Residual questions for ARGUS (rev2)

(Carried forward to the verdict's `residual_questions_for_argus:` field at dispatch return.)

**Resolved in rev2 (kept as breadcrumbs for ARGUS-rev2 verification):**

- ~~§9.4 v1 renewal-cron prompt body state-management~~ — RESOLVED via F1 inline-slot-values reshape per §5.1.d rev2 (option (a) shipped). ARGUS-rev2 should verify the v1 → rev2 transition actually landed in §5.1.d prose.

**Open for ARGUS-rev2:**

1. **§9.4a — renewal-cron prompt-body size.** The rev2 renewal-cron prompt body weighs ~50 lines per cron (worked example). Is the size an actual ceiling-concern for `CronCreate` (the docs name a 25,000-byte ceiling for `loop.md` specifically; unclear if it extends to arbitrary `CronCreate` prompts), or purely a readability concern? If the former, the design needs a re-shape; if the latter, accept as the load-bearing trade-off for F1+F2+F3 correctness.
2. **§9.4b — `durable: true` open-bug dependence.** Should the design (a) keep the honest-intent `durable: true` encoding with explicit bug citation [current rev2 choice], (b) drop the flag entirely and rely solely on §13.4 re-entry until the bug is fixed and the flag is re-introduced in a future arc, or (c) track the issue closure as a substrate-update trigger? Current §10 follow-ups names (c) as a post-arc concern; ARGUS-rev2 may surface that the bug-closure surveillance belongs in canon (e.g., a substrate-update beat in §14 daily-cadence check), not just a follow-up.
3. **§9.3 — A5 (α) vs (β) reader-frame.** (Unchanged from rev1; not load-bearing per ARGUS-rev1 concurrence — recoverable within arc revision cycle.)
4. **§9.5 — Part 2 self-application observability.** (Unchanged from rev1; not load-bearing per ARGUS-rev1 concurrence — mirrors Arc 35 self-application limitation pattern.) The rev2 §4.4.2 honest-scope note explicitly names the cron-pair-surviving-fresh-conversation-start as NOT a worked-example property of this arc, undermined by the open #40228 bug.
5. **§9.1 — STEP 1.5 prose precision under load.** (Unchanged from rev1; not load-bearing per ARGUS-rev1 concurrence — §7.7's "Worked example (Arc 36 itself)" prose carries sufficient teaching weight.)
6. **§9.2 — cite-comment resolution probe precision.** (Unchanged from rev1; not load-bearing per ARGUS-rev1 concurrence — over-specification trap correctly named.)

**Rev2 fold confirmations (ARGUS-rev2 verifies the structural changes actually landed):**

- F1 fix: §5.1.d STEP 4 next-renewal generation logic carries `{{POLLING_CRON_ID}}` replacement inline; no template-reference at fire time. Verify §4.2.2c probes pass.
- F2 fix: §5.1.d STEP 1a no-op branch + `durable: true` + explicit session-lifecycle failure mode at A9 + `MAJOR_POLYBIUS.md` §13.4 re-entry as load-bearing recovery. Verify §4.2.2a + §4.2.2d probes pass; verify §3.7 A14 acceptance bullets reflect rev2 broader-failure-mode framing; verify §8.2 N=1 framing names the session-lifecycle failure mode + open-bug provenance.
- F3 fix: §5.1.d STEP 1 cron-id exact-match using `{{POLLING_CRON_ID}}` slot (Handle b); §5.3.0 template body re-order leading with `{{COORDINATION_TICKET}}` (Handle a). Verify §4.2.2b + §4.2.4a probes pass.
- m2 fix: `durable: true` named explicitly on the renewal cron (per §5.1.d "Renewal-cron CronCreate parameters" sub-block). Verify §4.2.2a probe passes.
- m3 fix: §5.1.a corrected to name the "Four beats:" line as plain prose introducing the numbered list, not a markdown heading. Verify §5.1.a literal read by ADA.

---

**End of design.md (rev2 — F1+F2+F3+m2+m3 folded; Part 1 untouched per ARGUS-rev1 clean verdict + PLINY routing).**
