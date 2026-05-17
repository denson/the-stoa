# Arc 35 build directive — per-CAPTAIN git seat identity via Co-Authored-By trailer (stoa--kjo)

**Status:** LOCKED at dispatch authoring (2026-05-17). A1-A16 are not DAEDALUS-revisable; sub-decisions inside A5/A6/A7/A9 are DAEDALUS discretion unless surfaced as PRINCIPAL-gate per `operating-disciplines.md` §25.

**Work-unit:** `stoa--kjo` (P3, filed 2026-05-04 by user-tier POLYBIUS after CAPTAIN_ARGUS for ariadne--xft.4 cited git blame to claim "docstring authored by PRINCIPAL himself in commit ebb9ecca" — PRINCIPAL: "I am 100% sure I did not personally write that." The commit was a ticket-driven gauntlet commit almost certainly authored by an ADA session running under PRINCIPAL's git identity per standard workspace practice).

**Audit-before-dispatch (2026-05-17):** user-tier POLYBIUS surfaced the load-bearing tension between stoa--kjo's original proposal (per-agent `Author:` override) and the global `~/.claude/CLAUDE.md` absolute rule "Git commit `Author:` — always use the user's configured git identity, never override" to PRINCIPAL pre-dispatch. PRINCIPAL adjudicated three architectural questions; the picks below are PRINCIPAL-decided, not DAEDALUS discretion:

- **Fix-shape:** Option β — Co-Authored-By trailer (preserves global rule literally; same trailer shape global CLAUDE.md already uses for `Claude Opus 4.7 <noreply@anthropic.com>`).
- **Scope:** CAPTAINs only — PLINY orchestrator commits + user-tier POLYBIUS housekeeping commits stay PRINCIPAL-attributed.
- **Global CLAUDE.md interaction:** Arc 35 ALSO lands a positive cross-ref in the global rule (substrate's seat-identity convention is the Co-Authored-By trailer; `Author:` still never overrides).

## A1 — One arc, one gauntlet

Arc 35 ships as a single end-to-end gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → ZENO → PLINY signoff → PR merge). No sub-arc decomposition. Mirrors Arcs 27-34.

## A2 — Fix-shape: Co-Authored-By trailer (PRINCIPAL-decided)

Every CAPTAIN commit (any commit authored inside `.claude/worktrees/arc-N-build/` by a CAPTAIN agent during the gauntlet) carries a `Co-Authored-By:` trailer naming the seat + project. The commit `Author:` field remains PRINCIPAL's configured identity (`denson <densonsmith2@gmail.com>`); git blame line-level attribution stays PRINCIPAL.

**The trailer is the seat-identity signal. `Author:` is not touched.** This preserves `~/.claude/CLAUDE.md`'s "Git commit `Author:` — always use the user's configured git identity, never override" rule literally.

GitHub renders Co-Authored-By trailers as additional contributor avatars on the commit + the PR; squash-merge preserves trailers from the squashed commits into the squash-merge commit's body. The squash-merge commit on main therefore carries the trailer chain from every CAPTAIN commit that contributed to the arc, even after the `arc-N/build` branch is deleted.

## A3 — Scope: CAPTAINs only (PRINCIPAL-decided)

**Tagged (Co-Authored-By trailer required):**
- CAPTAIN_ADA build commits inside arc-build worktrees
- CAPTAIN_DAEDALUS commits (if DAEDALUS commits design artifacts directly — uncommon but possible)
- Any other CAPTAIN that commits during the gauntlet (verdicts are usually committed as artifacts by ADA, but if a CAPTAIN commits directly, tag it)

**Not tagged (Author = PRINCIPAL, no trailer required):**
- PLINY orchestrator commits (PLINY rarely direct-commits; merges via `gh pr merge` which inherits PRINCIPAL identity)
- User-tier POLYBIUS direct-to-main housekeeping commits per `MAJOR_POLYBIUS.md` §18.1 (directive tracking, paste tracking, self-apply, etc.)
- PRINCIPAL hand-authored commits
- Squash-merge commits on main (created by `gh pr merge`; carry the trailers from squashed commits via GitHub's trailer-preservation)

Rationale: PLINY + POLYBIUS commits are coordination + housekeeping, not authorial work. Tagging them adds noise without read-side signal. CAPTAIN commits ARE authorial work and ARE the empirical-anchor case (ADA wrote the docstring that ARGUS later misattributed).

## A4 — Global `~/.claude/CLAUDE.md` cross-ref fold-in (PRINCIPAL-decided)

Arc 35's user-tier portion (a separate POLYBIUS direct-to-main commit per §18.1, NOT inside the arc-build/gauntlet) updates the global CLAUDE.md authorship-attribution section to acknowledge the substrate's Co-Authored-By convention. The shape:

> The "never override `Author:`" rule stands absolute. Projects following the Stoa substrate's seat-identity convention add a `Co-Authored-By: <SEAT>_<project-slug> <seat-mnemonic@<project>.local>` trailer to CAPTAIN commits inside arc-build worktrees. The trailer is the seat-identity signal; `Author:` remains PRINCIPAL's configured identity. This is the substrate's compliance-with-spirit pattern, not an exception.

DAEDALUS picks the exact wording + placement inside the existing authorship-attribution section. The point: a reader of global CLAUDE.md who operates in substrate workspaces sees both the absolute rule AND the substrate's compliant trailer convention, preventing drift in either direction.

The global CLAUDE.md edit is a user-tier action (it's the PRINCIPAL's personal global config, not a project file). It lands as a user-tier POLYBIUS direct edit OUTSIDE the arc-build gauntlet — but it is part of Arc 35's shipped scope and is named here so PLINY's signoff verifies it happened.

## A5 — Trailer format (DAEDALUS sub-decision)

The empirical anchor mentions `CAPTAIN_ADA_ariadne_core <captain-ada@ariadne-core.local>`. DAEDALUS picks the canonical format. Constraints:

- **Name field MUST include the seat mnemonic** (CAPTAIN_ADA, CAPTAIN_ARGUS, etc.) so seat is unambiguous.
- **Name field MUST distinguish per-project** so multi-project blame doesn't conflate seats (one ADA at ariadne-core ≠ one ADA at the-stoa). Suggested separator: underscore or hyphen, DAEDALUS picks.
- **Email field MUST be a `.local` or otherwise non-routing local-only domain** to prevent accidental email-list inclusion (no spam to a fake address).
- **Email field SHOULD use a lowercase-hyphen pattern** (`captain-ada@<project>.local`) for cleaner trailer rendering.

DAEDALUS sub-decision: exact name format (`CAPTAIN_ADA_the-stoa` vs `CAPTAIN_ADA_the_stoa` vs `CAPTAIN_ADA[the-stoa]` etc.); exact email format. Document rationale in `design.md`. If undecidable per DAEDALUS discretion, surface as PRINCIPAL-gate per §25 — do NOT proceed-then-flag.

**Worked example for design.md (use as illustration, not lock):**

```
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: CAPTAIN_CATO_the-stoa <captain-cato@the-stoa.local>
```

## A6 — Substrate canon insertion loci (DAEDALUS sub-decision)

The convention lands in three canon files. DAEDALUS picks the precise section number / heading for each; precedent is to mirror existing arc-section patterns (Arc 34's new sections are §5.11 in MAJOR_PLINY.md and §18 in MAJOR_POLYBIUS.md).

1. **`substrate/operating-disciplines.md`** — new top-level section, "Per-CAPTAIN git seat identity via Co-Authored-By trailer." Universal team-protocol canon. Encodes: the rule, the trailer format, why `Author:` is NOT touched (cross-ref to global CLAUDE.md), the squash-merge preservation property, scope (CAPTAINs only — explicit "PLINY + POLYBIUS NOT tagged"). Likely insertion: after §27 (Arc 33 mechanical/agent split), as new §28.
2. **`substrate/MAJOR_PLINY.md`** — new section under §5 (gauntlet dispatch) describing PLINY's responsibility at dispatch time: the brief to CAPTAIN_ADA (and other CAPTAINs) names the exact seat identity to use in the trailer. Suggested locus: §5.12 (after Arc 34's §5.11 paste-archival).
3. **`substrate/CAPTAIN_ADA.md`** + any other CAPTAIN envelope that commits — pre-commit discipline: "Before every commit you author inside an arc-build worktree, append a `Co-Authored-By: <your-seat-identity-from-brief>` trailer to the commit message." Update CAPTAIN_ADA.md authorship-discipline subsection (currently lines ~94 ff covering file-frontmatter `author:` discipline) to add the git-trailer discipline as a parallel concern, with explicit cite to `operating-disciplines.md` §28 (or whichever number DAEDALUS lands on).

If other CAPTAIN role files commit (DAEDALUS, DAEDALUS-built design artifacts, ARGUS / VERA verdicts) — DAEDALUS audits and updates as needed. Single source of truth for the rule is operating-disciplines.md §28; role files cite-comment to it.

## A7 — Implementation mechanism (DAEDALUS sub-decision)

DAEDALUS picks the trailer-insertion mechanism. Two credible shapes:

**(i) Manual in-commit-message trailer** — CAPTAIN_ADA's brief instructs: "Your commit message ends with `Co-Authored-By: <seat-identity>`." ADA writes the trailer as part of the commit body, same as ADA already does for any heredoc commit message. Zero tooling. Relies on agent discipline.

**(ii) Shell helper `substrate/scripts/git-coauthor.sh`** — a small wrapper script that takes the seat identity as arg and runs `git commit --trailer "Co-authored-by: ..."` under the hood. Installed by `install.sh`. CAPTAIN_ADA calls the helper instead of plain `git commit`.

DAEDALUS lean: (i) for Arc 35 (cheapest; no install.sh change; aligns with existing agent commit-message discipline; reversible if the discipline proves insufficient). If DAEDALUS picks (ii), document why (i) is insufficient and what (ii) buys.

## A8 — Read-discipline pairing (DAEDALUS sub-decision)

Co-Authored-By trailers address commit-LEVEL seat identity. They do NOT change git blame's line-level Author attribution (blame follows `Author:`, not trailers). The original empirical anchor was an ARGUS misattribution from `git blame` output — i.e., line-level. Arc 35's trailer convention is therefore necessary-but-not-sufficient for the read-discipline failure that motivated stoa--kjo.

DAEDALUS decides whether to ship a paired read-discipline section. Options:

**(a) Small subsection inside operating-disciplines.md §28** — "Reading git blame: line-level Author is PRINCIPAL-attributed by substrate convention; do NOT infer human authorship from blame. To learn who actually wrote a line, read the squash-merge commit body for Co-Authored-By trailers, or trace the ticket + PR history." Lightest. Composes with §19.6.

**(b) Standalone §29 in operating-disciplines.md** — same content, fuller treatment, own section + cross-refs.

**(c) Defer to follow-up arc** — Arc 35 ships only the write-side trailer; read-discipline ships separately. Risk: same empirical-gap-rediscovery pattern that surfaced stoa--jru (Arc 22) sitting paused 2 weeks (now fixed by Arc 34 / C4 HITL-paused queue sweep) — but stoa--kjo's read-discipline gap is well-named already, so this risk is low.

DAEDALUS lean: (a). Same-arc pairing makes the rationale self-contained ("we trailer the commit; here's why blame alone isn't enough").

## A9 — Self-application

**Arc 35's own build commits must apply the convention.** CAPTAIN_ADA's gauntlet build commits inside `.claude/worktrees/arc-35-build/` carry the Co-Authored-By trailer per the convention they ship. This is the same self-apply pattern as Arc 34 / C2 (paste-archival landed in the same gauntlet commit as the §5.11 canon edit), Arc 29 / §17 (base-vs-custom directory used by the arc that defines it), and Arc 33 (script/agent-split — the new skill ships in the same arc that defines the pattern).

Self-application is structurally important: if Arc 35 ships the convention but doesn't apply it to its own commits, the historical record will read "we made this rule on 2026-05-17 and started following it on 2026-05-N+1" — a discontinuity that complicates any future "when did this seat start authoring commits" question. Self-applying means: first commit that carries the convention IS the commit that adds the convention.

PLINY signoff verifies that Arc 35's own arc-build commits carry the trailer per §28 before PR-merging.

## A10 — Cite-comment discipline

Cross-references between the new operating-disciplines.md §28 + the global `~/.claude/CLAUDE.md` authorship section + MAJOR_PLINY.md dispatch-section update + CAPTAIN_ADA.md authorship-section update resolve via cite at every read-site. Same pattern as Arcs 26 / 28 / 29 / 30 / 31 / 32 / 33 / 34 cite-comments.

Specifically: every place where the substrate references "agent commit identity" or "git blame attribution" cite-comments to operating-disciplines.md §28. Every place where the global rule "never override Author:" appears in substrate canon (or per-project CLAUDE.md) cite-comments to global `~/.claude/CLAUDE.md` authorship-attribution section.

## A11 — Authorship attribution unchanged for file frontmatter

The Co-Authored-By trailer convention applies ONLY to git commit metadata. File-frontmatter `author:` fields (SKILL.md, marketplace.json, package.json, etc.) continue to name **Denson Smith** per substrate/CLAUDE.md and global ~/.claude/CLAUDE.md IMMUTABLE rule. CAPTAIN_ADA.md line 94 discipline ("any file with an author field... names the PRINCIPAL... never anyone else") stands. Arc 35 makes this explicit in the new §28 to prevent any reader from inferring "agents tag commits → agents also tag file frontmatter."

## A12 — Out-of-scope (HARD-LOCKED)

Arc 35 does NOT:

- Touch any file-frontmatter `author:` field discipline (immutable per A11).
- Override `Author:` for any commit (per global CLAUDE.md absolute rule + PRINCIPAL pick β).
- Tag PLINY or POLYBIUS commits (per PRINCIPAL pick — CAPTAINs only).
- Build per-agent identity for non-CAPTAIN seats (HERALD, CURATOR, BARTLEBY, STRABO, etc. — Arc 35 lists them in §28 as "future arcs may extend"; ships only the CAPTAINs that empirically commit).
- Build retroactive blame-attribution for past commits (Arc 35 is forward-only; the historical empirical anchor stays as-is).
- Build GitHub repo-side settings (commit signing, branch protection, CODEOWNERS, etc.) — substrate canon only.
- Build shell tooling beyond what A7 directly specifies — if DAEDALUS picks (i) manual, NO shell helper; if (ii), only the one helper.
- Touch substrate/install.sh beyond what A7 implementation choice requires.

Scope-creep guard: if DAEDALUS or any CAPTAIN surfaces a scope concern touching A12, treat as substance disagreement: confirm A12 wording from this directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

## A13 — §15 N=1 honesty per candidate

Per MAJOR_POLYBIUS.md §15 honest-scope and operating-disciplines.md §6.7.1: the trailer convention enters substrate canon off-gate on the empirical signal (one ARGUS misattribution incident, 2026-05-04) + PRINCIPAL project-direction declaration (2026-05-17 picks β + CAPTAINs-only + global cross-ref fold-in). N=1 bit-by-it (the original ARGUS misattribution); N=0 worked-when-applied (no prior arc has applied the convention; Arc 35's self-application is the first observation). Future-evidence accretion per §6.7.1 — promotion to "structural lesson" status accretes as future arcs ship under §28 and surface either successful application or fresh failure modes.

Same N=1 framing as Arc 27's MAJOR_POLYBIUS.md §16.6, Arc 28's operating-disciplines.md §22.3, Arc 29's §17.5, Arc 30's §5.9.3, Arc 31's §25.6, Arc 32's §5.9.4, Arc 33's §27, Arc 34's §18 + §5.11 + §9-step-3.

## A14 — Pre-branch + worktree convention self-applied

Per MAJOR_PLINY.md §5.9 + §5.9.4. PLINY runs the two-check rule before creating `arc-35/build`; builds in `.claude/worktrees/arc-35-build/` (NOT in main worktree). User-tier POLYBIUS confirmed at dispatch authoring: local main = origin/main at `244c1c3`; no orphan arc-build branches.

## A15 — Signoff-accuracy + attestation-honesty self-applied

Per MAJOR_PLINY.md §5.10 + operating-disciplines.md §19.6. PLINY's signoff live-verifies cleanup (arc-35/build local + remote deleted; worktree removed; PR merged; global CLAUDE.md edit landed and pushed). Attestations cite live-verified state, not dispatch-authoring SHA `244c1c3` echoed-from-context.

## A16 — Source-ticket closure

On Arc 35 ship: close `stoa--kjo` with cross-ref to the merge commit. Audit comment at close should explicitly note: (1) the original Option-A proposal was reframed to Option-β via PRINCIPAL pre-dispatch adjudication; (2) the cross-ref to operating-disciplines.md §28 (or whichever number DAEDALUS lands on) is where the convention now lives; (3) the global `~/.claude/CLAUDE.md` cross-ref is the compliance-with-spirit acknowledgment.

## Phase structure

**Phase 1 — Design (DAEDALUS + ARGUS).** DAEDALUS reads this directive + stoa--kjo + global CLAUDE.md authorship section + operating-disciplines.md §19.6 + §25 + §27 + MAJOR_PLINY.md §5.10 + §5.11 + CAPTAIN_ADA.md authorship-discipline section. Produces design.md covering: §28 wording draft, trailer format (A5 pick), insertion locus per file (A6 picks), implementation mechanism (A7 pick), read-discipline pairing (A8 pick), self-application plan (A9 — ensure arc-35 build commits will carry the trailer), cite-comment locations (A10), global CLAUDE.md edit wording (A4). ARGUS cold-audits; expected NEEDS_REVISION on at least one of {trailer format, read-discipline scope, global CLAUDE.md wording} given the architecture-sensitivity.

**Phase 2 — Build (ADA in `.claude/worktrees/arc-35-build/`).** ADA implements per approved design.md. Self-applies: ADA's commits in this worktree carry the trailer per the convention being shipped. The global CLAUDE.md edit happens via user-tier POLYBIUS direct commit on main (outside the arc-build worktree) AFTER the substrate canon ships — sequencing in design.md.

**Phase 3 — Verify (VERA + CATO + ZENO).** VERA exercises probes from design.md against the built deliverable (does CAPTAIN_ADA's brief now include identity? does a worked-example commit carry the trailer correctly? does GitHub render the trailer? does squash-merge preserve it?). CATO cold-reads the diff for craft + scope + wording. ZENO mechanical spec-vs-result.

**Phase 4 — Ship + close.** Smoke + PR + merge + cleanup + close. PLINY signoff per §5.10 live-verifies arc-35/build deleted local+remote + worktree removed + PR merged + global CLAUDE.md edit landed + Arc 35's own gauntlet build commits carry the trailer (self-application sanity check). Close stoa--kjo with audit comment per A16. Tag `[for: user-tier POLYBIUS]` on stoa--kjo inviting QA pass.

## DAEDALUS sub-decisions summary

- **A5** — trailer format (name + email exact shape)
- **A6** — insertion locus per file (section numbers + headings)
- **A7** — implementation mechanism (manual vs shell helper)
- **A8** — read-discipline pairing (subsection vs standalone §29 vs defer)

User-tier POLYBIUS leans: A5 underscore-separator with `<project>.local` email; A6 §28 + §5.12 + CAPTAIN_ADA.md authorship-section extension; A7 (i) manual; A8 (a) subsection inside §28.

If any pick exceeds DAEDALUS discretion, treat as PRINCIPAL-gate per §25 — halt + escalate immediately rather than proceed-then-flag.

## Read order for DAEDALUS

1. This directive (load-bearing spec).
2. `bw show stoa--kjo` (work-unit ticket; carries the original empirical anchor + Option-A original proposal — note PRINCIPAL pre-dispatch adjudication reframed to Option-β; this directive overrides the ticket on the fix-shape).
3. `~/.claude/CLAUDE.md` authorship-attribution section (the absolute rule β preserves; A4 edit lands cross-ref here).
4. `substrate/operating-disciplines.md` §19.6 (attestation-confabulation) + §25 (PRINCIPAL-gate) + §27 (mechanical/agent split — recent canon precedent for new top-level section shape).
5. `substrate/MAJOR_PLINY.md` §5.10 (signoff-accuracy) + §5.11 (Arc 34 archival; the most recent canon section shape).
6. `substrate/MAJOR_POLYBIUS.md` §18 (Arc 34 housekeeping discipline; recent canon section precedent; also the section that exempts POLYBIUS housekeeping commits from per-CAPTAIN tagging per A3).
7. `substrate/CAPTAIN_ADA.md` authorship-discipline section (currently file-frontmatter discipline only; A6 extends it with git-trailer discipline).
8. `substrate/CLAUDE.md` authorship section (project-tier rule; cross-ref to global; A4-adjacent edit may apply here too if DAEDALUS deems it warranted).
9. **Arc 33's `substrate/skills/inspect-script-output/`** — precedent for a small substrate component shipping with worked example.
10. **Arc 34's `substrate/arcs/arc-34-build-directive.md`** — bundling + self-application precedent.
