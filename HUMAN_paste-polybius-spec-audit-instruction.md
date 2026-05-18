Re-read .claude/MAJOR_POLYBIUS.md and assume the project-tier chief-of-staff role for the-stoa. (This is post-`/clear`; role refresh from the canon file.)

**Your immediate intent for this engagement:** orchestrate a SPEC AUDIT of `SPECIFICATION.md` at the the-stoa repo root. You + project-tier PLINY (paste at `HUMAN_paste-pliny-spec-audit-instruction.md`) are dispatched together. This is NOT an arc dispatch. You will NOT trigger the Arc 38 build. Your sole deliverable is `SPEC_AUDIT.md` at the repo root, capturing fresh-eyes concerns about the spec for PRINCIPAL + user-tier POLYBIUS review.

**Why this engagement exists:** the spec was authored 2026-05-17 by user-tier POLYBIUS. The author cannot see their own ambiguities, contradictions, and aspirational-vs-descriptive drift. A fresh team reading the spec cold has diagnostic power that disappears the moment they start building against it. Front-loads §13.9 Pass 7 (spec accuracy reconciliation) BEFORE §13.5 Pass 4 (Arc 38 dispatch) so all subsequent arcs ship against a validated spec.

**Operating mode:** Mode 2 (exploration / scoping; per `operating-disciplines.md` §10 + §11 mode canon) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes). The "gauntlet" for this engagement is structured around the audit, not the arc lifecycle (§5).

---

## Read first (in order)

1. **`SPECIFICATION.md`** at repo root — the artifact under audit. Read end-to-end including §14 PRINCIPAL editing notes.
2. **`docs/validation/stellation-SPECIFICATION.md`** — paired test-project spec. Audit for cross-coherence with SPECIFICATION.md §13.11 Pass 9 framing.
3. **`/CLAUDE.md`** at repo root — project-tier authorship + ops rules SPECIFICATION.md references.
4. **`~/.claude/CLAUDE.md`** — global PRINCIPAL preferences SPECIFICATION.md cross-refs (Author rule; fix-now rule; authorship attribution discipline).
5. **`substrate/operating-disciplines.md`** sections SPECIFICATION.md cross-refs heavily: §1-§6 (universal disciplines preamble), §7 (POLYBIUS-pair coordination + Arc 36 §7.7 author-tag canon), §10 + §11 (modes + autonomous-mode-setup), §17 + §23 (base-vs-custom), §19.6 (attestation-confabulation), §25 (PRINCIPAL-gate), §27 (mechanical/agent split), §28 (Co-Authored-By trailer), §29 (multi-team interop — just shipped Arc 37), §30 (four-layer identity — just shipped Arc 37).
6. **`substrate/MAJOR_PLINY.md`** §5.9 + §5.9.4 + §5.10 + §5.11 + §5.12 — pre-branch hygiene + worktree + signoff-accuracy + paste archival + seat-identity-in-dispatch-brief.
7. **`substrate/MAJOR_POLYBIUS.md`** §18 (user-tier housekeeping discipline) + §19 (just shipped Arc 37 — two-team forge/shop).
8. **`substrate/templates/polling-cron-prompt-template.md`** — Arc 36 v2 just landed STEP 1.5 + STEP 4 cadence-switch lock-step rotation; verify spec §7 coordination canon references resolve.

---

## Your job

Produce `SPEC_AUDIT.md` at the the-stoa repo root, structured by category:

### Required audit categories

1. **Ambiguities** — sections that read multiple ways. For each: cite the section, quote the ambiguous phrasing, name the multiple readings.
2. **Contradictions** — places where section X says A and section Y says not-A. For each: cite both, quote both, name the conflict.
3. **Cross-ref errors** — `§N.M` pointers that don't resolve to actual sections; cited ticket IDs that don't match `bw list --all` current state; file paths that don't exist; commit SHAs that aren't in `git log`. For each: cite the source location, name the missing target.
4. **Aspirational-vs-descriptive drift** — sections that claim "the team does X" but the substrate doesn't actually have shipped canon for X. For each: cite the claim, name the missing canon, distinguish "future work with filed ticket + gating" (acceptable per §13.12 criterion 1) from "asserted as shipped reality" (audit finding).
5. **Missing pieces** — concepts referenced but not defined; workflows the spec assumes exist but doesn't document. For each: cite where the assumption appears, name what's missing.
6. **Honest 'I don't understand'** — sections where a fresh reader cannot operationalize the prose into action. For each: cite the section, articulate the gap between reading-it and being-able-to-execute-against-it.
7. **Self-applicability check** — can a fresh team execute §13's workplan as written? Walk through Pass 4 (Arc 38 dispatch) in your head; surface any place the team would need to ask "what does this mean / what comes next." Report each gap.
8. **Substrate-state-vs-spec mismatches** — does §12.3's enumerated open-ticket list match `bw list --all` reality? Does §12.4 working-tree state match `git status`? Run the checks; report discrepancies.

### Optional additional categories (use if observations don't fit above)

- **Naming / mnemonic feedback** (e.g., does "CAPTAIN_TIRO" land as intended? Does "stellation" land as a test-project name?)
- **Workplan-shape feedback** (e.g., is Arc 40's 9-candidate bundle too large per Arc 36's 5-rev-cycle precedent? Should it split?)
- **Out-of-scope observations** (things you noticed that the spec deliberately defers; document them so PRINCIPAL can confirm the deferral is intentional)

### Output discipline

- **Surface concerns; do NOT propose fixes.** ARGUS-discipline: the fix-shape decisions belong to PRINCIPAL + user-tier POLYBIUS after reading your audit, not to the audit team. If you find a contradiction, name it; don't suggest which side to keep.
- **Honest "this is fine" entries are also useful** — for each audit category, an explicit "no items surfaced in this category" is more honest than silence.
- **N=1 honesty per `operating-disciplines.md` §6.7.1:** if you find one instance of a concern, frame it as N=1; if it appears multiple times across sections, name the pattern + cite instances.

---

## Constraints

- **DO NOT dispatch Arc 38** (or Arc 39, Arc 40, or any other arc). The audit is upstream of dispatch.
- **DO NOT propose fixes** — surface concerns only. ARGUS-discipline.
- **DO NOT edit SPECIFICATION.md** — read-only for this engagement. Audit findings inform a future user-tier POLYBIUS edit after PRINCIPAL review.
- **DO NOT execute substrate-deploy changes** — `install.sh` / `apply.sh` / canon edits all out of scope.
- **DO NOT touch the stellation workspace** — `~/claude_projects/stellation/` does not exist yet and is not your concern for this audit.

## bw query discipline (load-bearing for §12.3 cross-check)

**CAPTAIN_TIRO does NOT exist yet** — it's a §13.5 Pass 4 Arc 38 candidate (stoa--ojz). The spec's §4.6 + §9.1 reference TIRO as the delegated-bw-query specialist, but you must use bw directly for this audit.

**For completeness audits (especially §12.3 vs reality cross-check): ALWAYS use `bw list --all`** per `operating-disciplines.md` §12.1 cookbook. The unflagged `bw list` truncates by default; the `--all` flag unhides truncation. This is the empirical anchor for TIRO — user-tier POLYBIUS demonstrated three times on 2026-05-17 that forgetting the flag produces silent under-counting. The cookbook documents the gotcha; operator behavior must apply it.

**If you find the cookbook-without-specialist insufficient for your audit work, note it as audit feedback** — the friction you encounter IS empirical anchor evidence for §4.6 TIRO. Conversely, if you find the cookbook fully sufficient, that's also audit feedback (the spec's TIRO framing may be over-engineered).

---

## Sub-dispatch authority

You orchestrate the audit; PLINY handles per-CAPTAIN dispatch. Recommended dispatches PLINY may run at your request:

- **CAPTAIN_ARGUS** — cold-audit `SPECIFICATION.md` for load-bearing risks. ARGUS's normal job (audit designs without proposing fixes) maps cleanly to spec-as-design.
- **CAPTAIN_BARTLEBY** — verify every §N.M cross-ref in SPECIFICATION.md resolves to an actual section in the cited file. Mechanical work; produces a file:line citation list of any breaks.
- **CAPTAIN_CATO** — cold-read SPECIFICATION.md for craft / consistency / scope hygiene (CATO's normal role applied to spec instead of diff).
- **CAPTAIN_ZENO** — if you frame the audit categories as a "spec" against which the SPECIFICATION.md is the "implementation," ZENO can do a mechanical structural check.

You may also do audit work directly without dispatching, where it's cheaper.

---

## Coordination

- **Project-tier PLINY** is your radio-check peer for this engagement. Paste at `HUMAN_paste-pliny-spec-audit-instruction.md`. Both peers post `[from: polybius-the-stoa]` / `[from: pliny-the-stoa]` author tags per Arc 36 §7.7 canon.
- **Coordination ticket:** file a fresh bw ticket at activation for this engagement (e.g., "spec-audit engagement coordination") or co-opt one of the open tickets if relevant. Use it for radio-check + heartbeats.
- **User-tier POLYBIUS** (the spec's author) is the upper-tier escalation target via `[for: user-tier-polybius] [from: polybius-the-stoa]` cross-tier comments. Use sparingly — only for clarifying questions where the spec's intent is genuinely unrecoverable from the prose.
- **PRINCIPAL** is exception-handler. Surface only on: substance disagreement after one round-trip with peer; irreducible ambiguity that blocks the audit; end-of-engagement deliverable handoff.

## Polling cron + renewal (per Arc 36 v2 canon now shipped)

- Set up your polling cron at `*/5 * * * *` per substrate-canonical default; name the cron id in your init handshake.
- **Schedule the one-shot renewal cron per `operating-disciplines.md` §11 step 1.5** (new Arc 36 v2 canon) at +144 hours from polling-cron creation. This audit engagement is short (~1-2 hours expected); the renewal won't fire, but you ARE the first forward-arc applying the renewal canon (per Arc 37 ship which spec'd it; you operationalize it).

## Closure

When `SPEC_AUDIT.md` is complete:
1. Final commit of `SPEC_AUDIT.md` is the deliverable (user-tier housekeeping per `MAJOR_POLYBIUS.md` §18.1; you have authority for direct-to-main on this audit artifact).
2. Post `[from: polybius-the-stoa]` closure comment on your coordination ticket.
3. Tag `[for: user-tier-polybius]` on the same ticket — that's the handoff.
4. Surface to PRINCIPAL with one-line summary: "spec audit complete; SPEC_AUDIT.md at repo root; N findings across M categories; standing by for PRINCIPAL + user-tier POLYBIUS review."
5. Stand down with `[radio-check polybius-the-stoa standing down]`; CronDelete your polling + renewal crons.

---

## Self-application

You are operating under the spec being audited. The §6 multi-checker discipline, the §19.6 attestation-honesty discipline, the §7 author-tag convention, the §5.10 signoff-accuracy discipline — ALL apply to your audit work. If you catch yourself slipping any of these during the audit, that's a piece of audit feedback (the spec is hard to operationalize even by an in-spec team).

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-polybius-spec-audit-instruction.md` in the project root.
