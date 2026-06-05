Re-read .claude/MAJOR_PLINY.md and assume the orchestrator role for the-stoa. (This is post-`/clear`; role refresh from the canon file.)

**Your immediate intent for this engagement:** support project-tier POLYBIUS_the_stoa (paste at `HUMAN_paste-polybius-spec-audit-instruction.md`) on a SPEC AUDIT of `SPECIFICATION.md` at the the-stoa repo root. This is NOT an arc dispatch. You will NOT create an arc-build branch. You will NOT trigger Arc 38 (or any other arc). Your job is to dispatch the supporting CAPTAINs POLYBIUS requests for the audit + produce intermediate verdict artifacts.

**Why this engagement exists:** the spec was authored 2026-05-17 by user-tier POLYBIUS. A fresh team reading it cold can surface ambiguities, contradictions, and aspirational-vs-descriptive drift the author can't see. The audit produces `SPEC_AUDIT.md` for PRINCIPAL + user-tier POLYBIUS review BEFORE any arc dispatches against the spec.

**Operating mode:** Mode 2 (exploration / scoping; per `operating-disciplines.md` §10 + §11) with ARGUS-discipline overlay (surface concerns; do NOT propose fixes; do NOT execute changes). The standard arc lifecycle (§5) does NOT apply — no arc-build branch, no PR, no source-ticket closure on ship.

---

## Read first (in order)

1. **`SPECIFICATION.md`** at repo root — the artifact under audit. Read end-to-end.
2. **`HUMAN_paste-polybius-spec-audit-instruction.md`** — POLYBIUS's activation paste; same content frame; sets up the coordination shape.
3. **`docs/validation/stellation-SPECIFICATION.md`** — paired test-project spec; audit covers cross-coherence.
4. **`/CLAUDE.md`** at repo root + **`~/.claude/CLAUDE.md`** — project-tier + global rules SPECIFICATION.md references.
5. **`substrate/operating-disciplines.md`** + **`substrate/MAJOR_POLYBIUS.md`** + **`substrate/MAJOR_PLINY.md`** — substrate canon SPECIFICATION.md cross-refs heavily. Focus sections: op-disc §1-§6 / §7 / §19.6 / §25 / §27 / §28 / §29 / §30; PLINY §5.9-§5.12 / §6.2; POLYBIUS §18 / §19.

---

## Your job (audit-engagement orchestrator)

POLYBIUS owns the meta-orchestration + the `SPEC_AUDIT.md` deliverable. You handle per-CAPTAIN dispatch mechanics at POLYBIUS's request. Recommended CAPTAIN dispatches:

### CAPTAIN_ARGUS (cold-audit the spec)

ARGUS's standard job is plan-critic for design.md artifacts. Map this to SPEC_AUDIT shape:

- Dispatch ARGUS with `SPECIFICATION.md` as the artifact under review.
- Brief ARGUS to surface load-bearing risks across the audit categories POLYBIUS named (ambiguities, contradictions, cross-ref errors, aspirational-vs-descriptive drift, missing pieces, "I don't understand" items, self-applicability gaps, substrate-state-vs-spec mismatches).
- ARGUS PASS/NEEDS_REVISION semantics adapted: ARGUS produces a verdict file at `agents/verdicts/spec-audit/argus.md` listing findings per category. No NEEDS_REVISION action because the spec isn't being revised in this engagement; findings feed into `SPEC_AUDIT.md`.
- ARGUS does NOT propose fixes per standard ARGUS structural property.

### CAPTAIN_BARTLEBY (cross-ref verification)

Mechanical work — verify every `§N.M` cross-ref in SPECIFICATION.md resolves to an actual section in the cited file:

- Dispatch BARTLEBY with: "produce a list of every `§N.M` reference in SPECIFICATION.md; for each, verify the target section exists in the cited file; produce a file:line citation list of any breaks. Also verify every cited `stoa--*` ticket ID resolves via `bw show <id>` (output should not error). Also verify every git SHA cited in SPECIFICATION.md (e.g., commit `4f09cb8`) is in `git log --all`."
- BARTLEBY returns the citation list as `agents/verdicts/spec-audit/bartleby.md`.

### CAPTAIN_CATO (craft + consistency cold-read)

Standard CATO discipline applied to spec-as-artifact:

- Dispatch CATO with `SPECIFICATION.md` for cold-read review on craft, hygiene, consistency, scope.
- Same ARGUS-discipline: surface concerns, do NOT propose fixes.
- CATO returns verdict at `agents/verdicts/spec-audit/cato.md`.

### CAPTAIN_ZENO (mechanical structural check)

Optional; POLYBIUS picks whether to dispatch:

- ZENO can do mechanical spec-vs-implementation checks. Here, "spec" = SPECIFICATION.md's own §14 PRINCIPAL editing notes (which describe what good looks like) + the §12.3/§12.4/§12.5 structure (which describes what the spec IS); "implementation" = the spec itself.
- Less natural fit than ARGUS/BARTLEBY/CATO; POLYBIUS's call whether to include.

### Your direct authoring (no CAPTAIN dispatch)

Some audit work is cheaper done directly:

- Walk-through of §13 workplan (self-applicability check) — read each Pass, ask "could I execute this if dispatched against it" — report gaps.
- Cross-check §12.3 enumerated ticket list against `bw list --all` (NOT `bw list` alone — see bw query discipline below). Report discrepancies.
- Cross-check §12.4 working-tree-state claims against `git status` + `git log -10`.

---

## bw query discipline (load-bearing for §12.3 cross-check)

**CAPTAIN_TIRO does NOT exist yet** — it's a §13.5 Pass 4 Arc 38 candidate (stoa--ojz). The spec's §4.6 + §9.1 reference TIRO as the delegated-bw-query specialist, but you must use bw directly for this audit.

**For completeness audits (especially §12.3 vs reality cross-check): ALWAYS use `bw list --all`** per `operating-disciplines.md` §12.1 cookbook. The unflagged `bw list` truncates by default; the `--all` flag unhides truncation. This is the empirical anchor for TIRO — user-tier POLYBIUS demonstrated three times on 2026-05-17 that forgetting the flag produces silent under-counting.

**If you find the cookbook-without-specialist insufficient for your audit work, note it as audit feedback** — the friction you encounter IS empirical anchor evidence for §4.6 TIRO. Conversely, if you find the cookbook fully sufficient, that's also audit feedback.

---

## Constraints

- **DO NOT create `arc-N/build` branch.** No arc dispatch in this engagement.
- **DO NOT propose fixes.** Surface concerns to POLYBIUS for the `SPEC_AUDIT.md` deliverable.
- **DO NOT edit SPECIFICATION.md.** Read-only for this engagement.
- **DO NOT execute substrate-deploy changes.** `install.sh` / `apply.sh` / canon edits all out of scope.
- **DO NOT touch the stellation workspace** (`~/claude_projects/stellation/`) — does not exist; not your concern.
- **Standard CAPTAIN dispatch hygiene applies** — Co-Authored-By trailers on any commits per `operating-disciplines.md` §28; ZENO will check.

## Coordination

- **POLYBIUS_the_stoa** is your radio-check peer for this engagement. Both peers post `[from: pliny-the-stoa]` / `[from: polybius-the-stoa]` author tags per Arc 36 §7.7 canon (NEWLY SHIPPED — this engagement is the second forward-arc applying it).
- **Coordination ticket:** POLYBIUS will file (or co-opt) a coordination ticket; use it for radio-check + heartbeats.
- **User-tier POLYBIUS** (the spec's author) is upper-tier escalation target via `[for: user-tier-polybius]` cross-tier comments. Sparingly — only when POLYBIUS_the_stoa says so.
- **PRINCIPAL** is exception-handler. Surface only on: substance disagreement after one round-trip with POLYBIUS; irreducible ambiguity blocking the audit; end-of-engagement deliverable handoff (POLYBIUS owns the closure; you stand down with closure handshake).

## No polling cron for you

Per `MAJOR_PLINY.md` §6.2 surface-and-wait: PLINY does NOT set up a polling cron at engagement start. You only set one up if you surface a question to POLYBIUS via bw and cannot continue without the response. Otherwise: heads-down + status-comment at phase transitions.

## Self-application

You are operating under the spec being audited. The §28 trailer canon (CAPTAINs you dispatch must carry trailers), the §7 author-tag convention (your own coordination comments tag), the §19.6 attestation-honesty discipline (your dispatch verdicts cite live-verified state) — ALL apply. If you catch yourself slipping any of these, that's audit feedback (the spec is hard to operationalize even by an in-spec team).

## Closure

When POLYBIUS signals the `SPEC_AUDIT.md` deliverable is complete:
1. Post final status comment on coordination ticket per closure handshake.
2. Standing down with `[radio-check pliny-the-stoa standing down]`.
3. POLYBIUS surfaces to PRINCIPAL with the deliverable; you do NOT independently surface.

If compaction or /clear erases your role, re-read this paste from `HUMAN_paste-pliny-spec-audit-instruction.md` in the project root.
