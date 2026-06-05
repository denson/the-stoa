# ZENO spec-check — Arc 32

**Verdict:** PASS
**Spec:** bw stoa--ewn body (C1-C4) + 2026-05-17T09:12:21Z comment (C5) + directive A1-A11 (substrate/arcs/arc-32-build-directive.md) + design.md rev2 (verbatim canon prose)
**Built:** arc-32/build commits 66bed01 (C1+C2+Edit 3a) + 9ec851f (C3+C4+C5+Edit 4b)
**Spec-checker:** CAPTAIN_ZENO_the_stoa, 2026-05-17
**Authored by:** CAPTAIN_ZENO_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

(Transcribed to disk by PLINY because the ZENO envelope is read-only; ZENO returned the verdict block inline.)

---

## Per-candidate spec-vs-result

### C1 — §5.1.1 cross-project context leak extension
- **Ticket requirement:** extend §5.1.1 with explicit cross-project-sequencing sub-discipline + worked-example anti-pattern (sector-4 leak) + worked-example positive-pattern. Directive A2 LOCKS scope; design §3.1 specifies §5.1.1.1 sub-subsection insertion + categorical-exception provenance shape.
- **Design spec:** `agents/design/arc-32/design.md` §3.1 (verbatim canon prose lines 54-74) + §3.1 categorical-exception paragraph (lines 76-78).
- **Built artifact:** `substrate/MAJOR_POLYBIUS.md` §5.1.1.1 at line 226 ("Cross-project sequencing context is user-tier-only — never leak it to project-tier seats"). Anti-pattern block-quote with "Sector-4 corpus seed (separate follow-on..." at line 234. Positive pattern "Per §5.1.1, this paste scopes to ariadne-core work only..." at line 240. Inline closing provenance paragraph present (design's categorical-exception shape preserved; depth-5 header avoids depth-6 unreadability per ARGUS R4 resolution).
- **Status:** DONE

### C2 — Cron-hygiene canon (three-carrier mirror of Arc 30)
- **Ticket requirement:** three carriers + thin universal-team cross-ref. Carrier 1 source-of-truth section in MAJOR_POLYBIUS.md; Carrier 2 paste convention; Carrier 3 `{{CRON_HYGIENE_CLAUSE}}` slot in paste-instruction-template.md with canonical default expansion; thin universal-team cross-ref in operating-disciplines.md. Directive A3 LOCKS three-carrier framing.
- **Design spec:** `agents/design/arc-32/design.md` §3.2 — Carrier 1 = MAJOR_POLYBIUS.md §5.1.3 (verbatim prose lines 104-134); Carrier 2 = template Edits 2a/2b/2c/2d (lines 137-203); Carrier 3 = operating-disciplines.md §26 (verbatim prose lines 206-223); Edit 3a §24 narrowing (lines 225-235; ARGUS R1 resolution).
- **Built artifact:** `substrate/MAJOR_POLYBIUS.md` §5.1.3 at line 282 (Carrier 1). `substrate/templates/paste-instruction-template.md` `{{CRON_HYGIENE_CLAUSE}}` at line 46 (slot) + line 55 (slot-explanation paragraph with unique sentence "Default-include is the safety property..."). `substrate/operating-disciplines.md` §26 at line 1265 (Carrier 3 + thin cross-ref). §24 narrowing at line 1150 ("PLINY as the only seat creating arc-build branches"). Edit 3a back-pointer to §26 present.
- **Status:** DONE

### C3 — PLINY-signoff-accuracy discipline
- **Ticket requirement:** verify-before-claim rule for signoffs; DAEDALUS picks Option α (MAJOR_PLINY.md alongside §5.9) vs β (operating-disciplines.md). Directive A4 LOCKS scope.
- **Design spec:** `agents/design/arc-32/design.md` §3.3 — Option α picked; new §5.10 top-level subsection at MAJOR_PLINY.md inserted in the §5.9.3-close → `---` window (verbatim canon prose lines 284-323) + thin cross-ref bullet at operating-disciplines.md §24 (line 328-330).
- **Built artifact:** `substrate/MAJOR_PLINY.md` §5.10 at line 422 ("Signoff-accuracy — verify cleanup claims before posting") with §5.10.1 empirical anchor (line 437), §5.10.2 cross-references (line 443), §5.10.3 N=1 provenance (line 451). `substrate/operating-disciplines.md` §24 bullet "`MAJOR_PLINY.md` §5.10 — PLINY-signoff-accuracy discipline (Arc 32 / `stoa--ewn`)..." at line 1158. C3 ↔ C4 reciprocal cross-ref at §5.10.2 (line 446 names §19.6 as "the canonical home for the root-cause discipline").
- **Status:** DONE

### C4 — Attestation-confabulation §19 extension
- **Ticket requirement:** extend §19 with attestation sub-rule + live-verified-vs-assumed-from-context distinction + Arc 30 empirical anchor. Directive A5 LOCKS scope.
- **Design spec:** `agents/design/arc-32/design.md` §3.4 — new §19.6 sub-subsection (verbatim canon prose lines 349-395) + Edit 4b append-paragraph to §19.4 (lines 398-406; ARGUS R2 resolution).
- **Built artifact:** `substrate/operating-disciplines.md` §19.6 at line 849 ("Attestation-confabulation — cite live-verified state, not assumed-from-context state"). Live-verified-vs-assumed distinction at line 851. §19.6.1 Empirical anchor at line 861 references Arc 30 `140b398` (ticket-spec anchor). §19.6.2 explicit reverse cross-ref to MAJOR_PLINY.md §5.10 present. §19.6.3 + §19.6.4 cross-refs + N=1 provenance present. Edit 4b §19.4 append at line 843 names §19.6 explicitly.
- **Status:** DONE

### C5 — Arc-build worktree convention
- **Ticket requirement (C5 comment):** Option A (require separate worktree) vs Option B (allow main-worktree checkout); DAEDALUS picks. If Option A, also encode worktree-cleanup convention. Directive A6 LOCKS scope.
- **Design spec:** `agents/design/arc-32/design.md` §3.5 — Option A picked; new §5.9.4 sub-subsection at MAJOR_PLINY.md (verbatim canon prose lines 458-489) including `git worktree add .claude/worktrees/arc-N-build -b arc-N/build` invocation + arc-close cleanup sequence (`git worktree remove` + `git branch -D` + `git push origin --delete`).
- **Built artifact:** `substrate/MAJOR_PLINY.md` §5.9.4 at line 390 ("Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/"). Worktree-add invocation at line 395. Cleanup sequence at lines 409-411. §5.9.4.1 Empirical anchor and provenance at line 416 (Arc 26-30 de-facto + Arc 31 divergence). Self-applied: this very arc's build occurred in `.claude/worktrees/arc-32-build/`.
- **Status:** DONE

## Canonical post-build ordering check (per design §3.3 / §3.5; ARGUS R3 resolution)
- §5.9.4 at line 390 (depth-4, `####`)
- §5.10 at line 422 (depth-3, `###`)
- `---` family-boundary at line 462
- §6 at line 464 (depth-2, `##`)

Order verified: §5.9.4 < §5.10 < `---` < §6. §5.9-family closes before §5.10 top-level peer opens. §5.10 sits above the `---` so it is a top-level peer of §5.1-§5.9 rather than nested.

## Out-of-spec additions

None observed. Diff scope: 4 substrate files. All within A1 phasing + A2-A6 scopes. A9 out-of-scope hard lock honored. A8 authorship: per ADA signoff + CATO authorship audit, only existing `author: Denson Smith` at paste-instruction-template.md:2 unchanged.

## Spec ambiguities

None requiring escalation. The DAEDALUS sub-decisions (C3 Option α, C5 Option A) were explicitly within A4/A6 discretion per the directive's pick-language; both rationales surfaced honestly in design §3.3 / §3.5.

## Drifts

None. All 5 candidates DONE.

## Summary

PASS — all 5 candidates (C1-C5) DONE by mechanical artifact reference. Each ticket-spec requirement maps to design-spec verbatim canon prose to built-artifact section + line number. Canonical post-build ordering (§5.9.4 < §5.10 < `---` < §6) preserved as design §3.3/§3.5 specify (ARGUS R3 resolution holds in artifact). Edit 3a (§24 narrowing per ARGUS R1) and Edit 4b (§19.4 append per ARGUS R2) both land in artifact. Reciprocal cross-refs C3 ↔ C4 land. C5 Option A self-applied. No out-of-spec additions; no spec ambiguities requiring escalation.

**Verdict: PASS** — 5/5 DONE.
