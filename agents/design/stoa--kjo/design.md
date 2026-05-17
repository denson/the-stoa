# Arc 35 design — Per-CAPTAIN git seat identity via Co-Authored-By trailer (stoa--kjo)

**Ticket:** `stoa--kjo`
**Branch:** `arc-35/build` (created by PLINY in separate worktree at `.claude/worktrees/arc-35-build/` per `MAJOR_PLINY.md` §5.9.4)
**Date:** 2026-05-17
**Status:** rev2 — folds 4 ARGUS rev1 findings (F1 path-citation; F2 §1.3 empirical reframing; F3 §3.4 audit-checklist pattern-break; F4 §9.2 N=1 honest citation). Architecture-layer picks (A5/A6/A7/A8) unchanged from rev1 (PASS-equivalent per ARGUS non-findings).
**Directive:** `substrate/arcs/arc-35-build-directive.md` (A1-A16 LOCKED; A5/A6/A7/A8 are DAEDALUS sub-decisions)
**Authored by:** CAPTAIN_DAEDALUS_the-stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §1 — Restatement and overview

### §1.1 What is being designed

Arc 35 ships a per-CAPTAIN git seat-identity convention. Every CAPTAIN commit landed inside an arc-build worktree (`.claude/worktrees/arc-N-build/`) during the gauntlet carries a `Co-Authored-By:` trailer that names the seat + project. The commit's `Author:` field stays PRINCIPAL's configured identity (`denson <densonsmith2@gmail.com>`); `git blame` line-level attribution stays PRINCIPAL. The trailer is the seat-identity signal; `Author:` is not touched. PLINY orchestrator commits and user-tier POLYBIUS housekeeping commits are NOT tagged — only CAPTAIN commits.

The convention lands as three coordinated substrate canon edits inside the gauntlet (new `operating-disciplines.md` §28; new `MAJOR_PLINY.md` §5.12; extension to `CAPTAIN_ADA.md` §5.5) PLUS one user-tier POLYBIUS direct-to-main edit OUTSIDE the gauntlet (cross-ref insertion in `~/.claude/CLAUDE.md` authorship-attribution section). Arc 35 self-applies: its own gauntlet build commits carry the trailer per the convention being shipped.

### §1.2 Why (the empirical anchor, restated)

The work-unit ticket `stoa--kjo` originates from a 2026-05-04 ARGUS misattribution on `ariadne--xft.4`. ARGUS read `git blame` and asserted "docstring authored by PRINCIPAL himself in commit `ebb9ecca`"; PRINCIPAL: "I am 100% sure I did not personally write that." The commit was a gauntlet-driven ADA build commit running under PRINCIPAL's git identity — the standard workspace pattern. The cost of the ARGUS mis-read was small (PRINCIPAL caught it immediately); the structural gap was that there was no commit-level signal of "which seat authored this commit" available to any future agent that walks git history. ARGUS inferred from `Author:` alone (the only signal git presented) and got it wrong.

The original `stoa--kjo` ticket proposed Option A (per-agent `Author:` override). PRINCIPAL's pre-dispatch adjudication (2026-05-17, captured in the directive header) reframed to Option β (Co-Authored-By trailer): preserves the `~/.claude/CLAUDE.md` absolute rule "Git commit `Author:` — always use the user's configured git identity, never override" literally; uses the same trailer shape global CLAUDE.md already uses for Claude (`Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`); GitHub renders the trailer as a contributor avatar AND preserves it in squash-merge commit bodies so the seat-identity signal survives `arc-N/build` branch deletion.

### §1.3 Imported assumptions (named per `CAPTAIN_DAEDALUS.md` §6.1)

- **GitHub squash-merge preservation of Co-Authored-By trailers (preservation property: reliable; write-side application: variable).** Confirmed via web search (2026-05-17): GitHub auto-populates Co-authored-by tags from squashed commits' authors AND appends/preserves existing trailers from squashed commit bodies into the squash-merge commit body. The *preservation property itself* — "if a trailer is in a squashed commit body, the squash-merge commit body preserves it" — is reliable, empirically confirmed on Arc 33 ship `789496b` which carries `Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>` exactly as ADA wrote it pre-squash. What is *variable* is ADA's write-side discipline: Arc 34 ship `244c1c3` has ZERO trailers (verified 2026-05-17 by `git log -1 --pretty='%(trailers:only)' 244c1c3`) because the pre-squash Arc 34 build commits `357e7635` (rev1) and `af815ebf` (rev2) BOTH had zero trailers — ADA omitted the standard Claude trailer on every Arc 34 build commit, so the preservation property had nothing to preserve. The convention's "seat trailers survive branch deletion via squash-merge" property therefore rests on TWO independent properties: (a) the preservation property (reliable on GitHub's side); (b) ADA's write-side discipline (must produce the trailer at commit time; empirically variable). Verification probe §4.5 covers (b); probe §4.6 covers (a). Self-assessed weak point §9.2 reframes the A7=(i) manual mechanism honestly against this Arc-34-witnessed write-side failure mode.
- **Sub-agent dispatch grounding.** PLINY brief to CAPTAIN_ADA already includes structured key-value fields per `MAJOR_PLINY.md` §5.2 (grounding-check enumeration). Adding a `seat-identity:` field is a parallel extension, not a structural change to the brief shape.
- **HEREDOC commit-message discipline already in place.** ADA's current commit pattern (Arc 32, Arc 33, Arc 34 build commits all visible in `git log`) uses HEREDOC bodies with the Claude trailer at the end. Adding the seat-identity trailer is an additional line in the same HEREDOC, not a new commit pattern. This is what makes A7 = (i) manual viable; an ADA-already-using-HEREDOC starting point makes the manual mechanism near-zero-cost.

### §1.4 What the design does NOT do (cite A12 verbatim — out-of-scope hard-lock)

Per the directive's A12 (HARD-LOCKED), Arc 35 does NOT:

- Touch any file-frontmatter `author:` field discipline (immutable per A11).
- Override `Author:` for any commit (per global CLAUDE.md absolute rule + PRINCIPAL pick β).
- Tag PLINY or POLYBIUS commits (per PRINCIPAL pick — CAPTAINs only).
- Build per-agent identity for non-CAPTAIN seats (HERALD, CURATOR, BARTLEBY, STRABO, etc. — Arc 35 lists them in §28 as "future arcs may extend"; ships only the CAPTAINs that empirically commit).
- Build retroactive blame-attribution for past commits (Arc 35 is forward-only; the historical empirical anchor stays as-is).
- Build GitHub repo-side settings (commit signing, branch protection, CODEOWNERS, etc.) — substrate canon only.
- Build shell tooling beyond what A7 directly specifies — if DAEDALUS picks (i) manual, NO shell helper; if (ii), only the one helper.
- Touch `substrate/install.sh` beyond what A7 implementation choice requires.

A7 picked = (i) manual (see §3 below) — therefore Arc 35 builds NO shell tooling and touches NO `install.sh`. The A12 boundary is met by the A7 pick.

---

## §2 — Sub-decisions (A5/A6/A7/A8)

All four DAEDALUS sub-decisions fall within discretion (no PRINCIPAL-gate escalation per `operating-disciplines.md` §25). Each pick aligns with the user-tier POLYBIUS lean recorded in the directive; rationale follows.

### §2.1 — A5: trailer format

**Pick:** `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>`.

Worked examples for the-stoa project-tier:

```
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
Co-Authored-By: CAPTAIN_CATO_the-stoa <captain-cato@the-stoa.local>
Co-Authored-By: CAPTAIN_VERA_the-stoa <captain-vera@the-stoa.local>
```

**Constraint mapping (directive A5):**

| Constraint (A5) | How this pick meets it |
|---|---|
| Name field MUST include the seat mnemonic | `CAPTAIN_<MNEMONIC>` segment — `CAPTAIN_ADA`, `CAPTAIN_DAEDALUS`, etc. |
| Name field MUST distinguish per-project | `_the-stoa` suffix in the name field; multi-project blame walking `Co-Authored-By` across repos will see `CAPTAIN_ADA_the-stoa` vs `CAPTAIN_ADA_ariadne-core` as distinct names |
| Email MUST be `.local` (non-routing) | `@the-stoa.local` — top-level `.local` is reserved by RFC 6762 for link-local mDNS, not routable on the public internet; no risk of accidental email to a fake address |
| Email SHOULD use lowercase-hyphen pattern | `captain-<mnemonic>@the-stoa.local` — all-lowercase, hyphen-separated local-part + hyphenated project domain |

**Rationale (separator choices).**

- **Seat-segment separator: underscore.** `CAPTAIN_ADA`, `CAPTAIN_DAEDALUS` — matches the existing on-disk role-file naming (`CAPTAIN_ADA.md`, `CAPTAIN_DAEDALUS.md` in `substrate/`; `CAPTAIN_DAEDALUS_the_stoa.md` in `.claude/agents/`) AND matches the empirical-anchor wording in the directive (`CAPTAIN_ADA_ariadne_core`). A reader walking `git log --pretty='%(trailers)'` who knows the seat names from substrate file paths sees the same casing in the trailer.
- **Seat-segment to project-segment separator: underscore.** Binds the two segments into a single "name token" — `CAPTAIN_ADA_the-stoa` reads as one identity. Empirical anchor uses underscore here too (`CAPTAIN_ADA_ariadne_core`). Using a hyphen instead (`CAPTAIN_ADA-the-stoa`) would make the boundary between seat-segment and project-segment ambiguous because hyphens already appear inside the project-segment (`the-stoa`). Underscore is unambiguous.
- **Project-segment: hyphenated canonical slug.** the-stoa's canonical slug across the repo is hyphenated: PR titles say "Arc 33: ..." not "Arc_33: ...", beadwork prefix is `stoa--`, the project directory is `the-stoa`. The empirical anchor uses `ariadne_core` (underscores) because ariadne-core's own canonical slug uses underscores; the-stoa's uses hyphens. Per-project, the project-segment matches the project's own canonical slug.
- **Email local-part: lowercase-hyphen.** `captain-<mnemonic>` — explicit per directive's A5 "SHOULD use a lowercase-hyphen pattern" hint. Matches the empirical anchor's email pattern (`captain-ada@ariadne-core.local`).
- **Email domain: `<project-slug>.local`.** Top-level `.local` is the canonical non-routing pseudo-TLD (RFC 6762). The project-slug as the second-level domain makes the email parse as "this is the project's local seat identity." The `.local` TLD also means GitHub will NOT match the email to any real GitHub user account, so the trailer renders as a name+email pair without an avatar — exactly the right shape (no fake user accounts; no avatar pollution; just a trailer-text record).

**Rejected alternatives (named per `CAPTAIN_DAEDALUS.md` §6.2).**

- **`CAPTAIN_ADA_the_stoa <captain-ada@the_stoa.local>` (all-underscore including project-segment).** Would match the on-disk envelope filename `CAPTAIN_DAEDALUS_the_stoa.md` exactly. Rejected because the project's canonical external slug is hyphenated (`the-stoa`, used in PR titles, branch names, GitHub URL, beadwork prefix); the trailer would diverge from every other place the project name appears externally. The envelope filename's underscore is a Windows-filename-safety legacy choice, not a canonical project-slug choice.
- **`CAPTAIN_ADA[the-stoa] <captain-ada@the-stoa.local>` (bracket-delimited project).** Rejected: brackets are not standard git-trailer name-field characters; some git-trailer parsers (and GitHub's contributor-extraction logic) may strip or mishandle the bracketed suffix. Less greppable (`grep 'CAPTAIN_ADA_the-stoa'` finds one match; `grep 'CAPTAIN_ADA\[the-stoa\]'` requires escaping). The underscore form is safer across tooling.
- **`ADA_the-stoa <captain-ada@the-stoa.local>` (drop CAPTAIN rank prefix).** Rejected: the rank prefix `CAPTAIN_` is what makes the trailer's seat-rank legible at read-time without consulting the substrate spec. A future MAJOR-rank seat that begins direct-committing (a hypothetical hotfix MAJOR) would need its own prefix; keeping the rank prefix preserves that future extensibility shape.

### §2.2 — A6: insertion loci per file

Three coordinated insertions inside the gauntlet, plus one cross-ref edit OUTSIDE the gauntlet (A4, user-tier POLYBIUS direct-commit).

| File | Insertion locus | Section heading |
|---|---|---|
| `substrate/operating-disciplines.md` | New top-level §28 after §27 ends (line 1357 in current arc-35-build worktree) | `## 28. Per-CAPTAIN git seat identity via Co-Authored-By trailer` |
| `substrate/MAJOR_PLINY.md` | New subsection §5.12 after §5.11 ends (line 516 in current arc-35-build worktree); inserted BEFORE the `---` separator at line 517 + `## 6. Communication` at line 519 | `### 5.12 Per-CAPTAIN seat-identity in the dispatch brief` |
| `substrate/CAPTAIN_ADA.md` | Extension to existing §5.5 "Authorship attribution (immutable)" at lines 92-94; appended new paragraph naming the trailer-discipline as a parallel concern with cite to op-disc §28 | (unchanged heading — `### 5.5 Authorship attribution (immutable)`) |
| `~/.claude/CLAUDE.md` (USER-TIER, outside gauntlet) | Insertion inside existing "Authorship attribution — never falsely credit someone else (CRITICAL)" section; new standalone subsection placed AFTER "Mandatory audit before committing or pushing" subsection closes and BEFORE the next existing subsection ("Naming references are NOT authorship claims"). The audit-checklist bullet list is UNCHANGED (per rev2 fix of ARGUS F3 audit-pattern-break). | `### Substrate seat-identity convention (compliance-with-spirit of "never override Author:", not exception)` |

**Confirmation of line numbers (live state in `.claude/worktrees/arc-35-build/` at design-time, 2026-05-17):**

- `substrate/operating-disciplines.md`: 1381 lines total; §27 closes at the cross-reference bullet list ending ~line 1356; line 1357 starts the `---` separator before `## Agent-regime inverses (the positive framing)` (line 1360). §28 inserts BETWEEN §27 close and the `---` separator at line 1358 (with appropriate blank line + `---` + blank line + new section heading sequencing).
- `substrate/MAJOR_PLINY.md`: 708 lines total; §5.11 closes at line 515 with `Same N=1 framing as ...`; line 516 is blank; line 517 is `---`; line 519 is `## 6. Communication`. §5.12 inserts BETWEEN line 515 (§5.11 close) and line 517 (`---`) — i.e., as a peer of §5.9, §5.10, §5.11 within the `## 5. The gauntlet pipeline` family.
- `substrate/CAPTAIN_ADA.md`: 173 lines total; §5.5 lives at lines 92-94. New paragraph appended at line 94+ as same-subsection extension; §5.6 (Heartbeat-and-read-before-write) at line 96 remains undisturbed.
- `~/.claude/CLAUDE.md`: the "Mandatory audit before committing or pushing" subsection runs lines 29-37 (heading at line 29; enumerated bullets at lines 33-37; the `Git commit Author:` bullet is at line 37). A "STOP and verify" closing paragraph immediately follows the bulleted list. The rev2 cross-ref insertion is a NEW standalone subsection placed AFTER that closing paragraph ends and BEFORE the next existing subsection ("Naming references are NOT authorship claims" — currently at approximately line 47 in PRINCIPAL's global file). The enumerated audit-checklist bullets at lines 33-37 are UNCHANGED. (Rev1 had appended a new bullet AT line 38; ARGUS F3 flagged the audit-pattern-break; rev2 restructures.)

**Locus rationale (per file).**

- **§28 in op-disc.** Universal-team protocol canon. Per `CAPTAIN_DAEDALUS.md` §6 the substrate-canonical home for universal disciplines is `operating-disciplines.md`. Arc 33's §27 (mechanical-script / agent-inspection split) is the most recent precedent for a new top-level section; its shape (PRINCIPAL declaration → discipline rule → per-seat behavior → cross-references → N=1 provenance) is what §28 follows. Per A6 directive lean: "Likely insertion: after §27 (Arc 33 mechanical/agent split), as new §28."
- **§5.12 in PLINY.** PLINY's responsibility is dispatch-time naming of the seat-identity each CAPTAIN should use in the trailer. The §5 family (gauntlet pipeline) is where dispatch-shape disciplines live: §5.1 (operating-mode in brief), §5.2 (ADA brief preamble — grounding-check enumeration), §5.9.4 (worktree convention), §5.10 (signoff-accuracy), §5.11 (paste archival). §5.12 (per-CAPTAIN seat-identity in brief) sits naturally after §5.11 as the most-recent canon-shaped peer.
- **CAPTAIN_ADA §5.5 extension (not a new §5.x subsection).** The directive A6 names "Update CAPTAIN_ADA.md authorship-discipline subsection (currently lines ~94 ff covering file-frontmatter `author:` discipline) to add the git-trailer discipline as a parallel concern." A NEW §5.x subsection would split the authorship-discipline material across two subsections — a reader landing at §5.5 would need to know to ALSO read §5.x for the trailer half. Extending §5.5 in place keeps both halves of "authorship signal at ADA's seat" in one read-locus. Pattern matches Arc 32 / C2 (which extended an existing template slot rather than creating a new sibling template).
- **`~/.claude/CLAUDE.md` cross-ref placement (rev2).** The "Mandatory audit before committing or pushing" subsection (lines 29-37) enumerates field-by-field what the audit checks. The last bullet (line 37) is `Git commit Author: — always use the user's configured git identity, never override.` Rev1 appended a new audit-checklist bullet after that one; ARGUS F3 flagged this as a pattern-break (the bullet describes a convention, not an audit target). Rev2 places the cross-ref as a NEW standalone subsection immediately after the "Mandatory audit" subsection closes (after its STOP-and-verify closing paragraph) and immediately before the next existing subsection. The new subsection's heading explicitly frames the relationship to the absolute rule ("compliance-with-spirit, not exception"), so a reader walking the section's subsection-shaped headings sees the convention as a peer of the absolute rule + its audit checklist, NOT as a member of the checklist. Per directive A4 ("a reader of global CLAUDE.md who operates in substrate workspaces sees both the absolute rule AND the substrate's compliant trailer convention, preventing drift in either direction") AND ARGUS F3's structural property (audit-checklist bullets enumerate audit targets only; complementary conventions live in their own subsection).

### §2.3 — A7: implementation mechanism

**Pick: (i) manual in-commit-message trailer.** No shell helper. No `install.sh` change.

**Rationale.**

ADA's existing commit-message discipline uses HEREDOC bodies with trailers when ADA applies the discipline correctly: Arc 33 build commits (visible via `git log --pretty='%(trailers)' 789496b`) show `Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>` written by ADA per the global CLAUDE.md commit-message convention; Arc 34 pre-squash build commits (`357e7635`, `af815ebf`) show ZERO trailers (verified 2026-05-17). The mechanism is "ADA writes the trailer line in the HEREDOC"; failure mode is "ADA forgets to include the trailer line." Arc 34 is the empirical witness that this manual mechanism HAS already failed once at this seat one arc ago. Arc 35 ships against the same mechanism, which is honest about both its empirical viability (Arc 33 worked) AND its known failure mode (Arc 34 didn't); §9.2 reframes the weak-point with this concrete witness. Adding a seat-identity trailer is one additional HEREDOC line in the exact same body shape:

```
git commit -m "$(cat <<'EOF'
<commit subject line>

<commit body prose>

Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

The two trailers compose as a coordinated pair — the seat-identity trailer above the Claude trailer (seat-identity is the substrate-tier signal; Claude trailer is the global-tier signal). Both render as separate contributor avatars on GitHub (the Claude trailer matches a known GitHub user; the seat trailer's `.local` domain doesn't match a real GitHub user, so it renders as text-only — the right shape).

**(ii) shell helper rejected.** A `substrate/scripts/git-coauthor.sh` wrapper would add: a new file under `substrate/scripts/` (a directory that does not exist today — would be Arc 35's introduction of a `scripts/` subdirectory under substrate), an `install.sh` modification to deploy it, agent role-file updates to call the helper instead of plain `git commit`, AND a new failure mode (the helper is forgotten or misconfigured, the trailer doesn't land, and the convention silently drifts). The cost of the helper exceeds its value: the manual mechanism is already what ADA does today for the Claude trailer; adding a second line is a one-token cognitive cost; the failure mode of forgetting the trailer is visible (VERA probe checks `git log --pretty='%(trailers)'`; if the trailer is missing, the probe fails).

The discipline is structural at the BRIEF level, not at the tooling level: PLINY's dispatch brief names the exact seat-identity string CAPTAIN_ADA writes into the HEREDOC; CAPTAIN_ADA writes it verbatim. This is the same shape as PLINY-names-the-ticket-ID, CAPTAIN-writes-it-into-commits — a discipline that has worked across 30+ arcs without a helper.

**Reversibility note (per directive A7).** If the manual mechanism proves insufficient at future arcs (e.g., ADA forgets the trailer on multiple consecutive arcs, VERA probe catches it after-the-fact too late to prevent the squash), a future arc may add the shell helper as a remediation. The (i) → (ii) migration is forward-compatible: the helper writes the same trailer the manual mechanism writes today; existing commits remain valid.

### §2.4 — A8: read-discipline pairing

**Pick: (a) small subsection inside operating-disciplines.md §28.** Title: "§28.5 — Reading git blame: line-level vs commit-level seat identity" (or §28.N depending on the §28 subsection numbering that lands; current draft uses §28.5).

**Rationale.**

The trailer convention is necessary-but-not-sufficient for the empirical-anchor failure mode. The original ARGUS misattribution was from `git blame` output (line-level), and `git blame` follows `Author:`, not trailers. So `git blame` on PRINCIPAL-committed files will STILL show PRINCIPAL — even after Arc 35 ships — for every line written by an agent. The read-discipline is: do not infer human authorship from `git blame`; to learn who actually wrote a line, walk the squash-merge commit body for `Co-Authored-By` trailers, or trace the ticket + PR + arc-build commit chain.

**Why (a) inside §28 rather than (b) standalone §29.** Pairing the read-discipline into the same section as the write-side convention makes the rationale self-contained: a reader landing at §28 sees "we ship the trailer (write side) AND here's why blame alone isn't enough (read side)." A separate §29 would force the reader to discover the pairing via cross-ref rather than read it as one coherent canon. The read-discipline is one paragraph; a full standalone section would over-weight it relative to the write-side rule (which is the main rule).

**Why not (c) defer.** The directive itself flags (c) as the riskier option: "Risk: same empirical-gap-rediscovery pattern that surfaced stoa--jru (Arc 22) sitting paused 2 weeks ... but stoa--kjo's read-discipline gap is well-named already, so this risk is low." Even with the risk low, the cost of pairing is one paragraph; the cost of deferring is the discoverability gap — a future ARGUS reads §28 (write-side) and proceeds to read git blame without the read-discipline cue. Same-arc pairing closes the gap without scope expansion.

The read-discipline subsection composes with `operating-disciplines.md` §19.6 (attestation-confabulation) — both are "cite live-verified state, not assumed-from-context state" disciplines. §19.6 fires at attestation time; §28's read-discipline fires at git-blame-reading time. Cross-reference §28's read-discipline to §19.6 so the reader sees the family.

---

## §3 — Per-target wording (the substantive build artifacts ADA will land)

### §3.1 — `substrate/operating-disciplines.md` §28 (new top-level section)

Insert at line 1358 (between §27 cross-references close and the `---` before `## Agent-regime inverses`). Insertion sequence:

```
<line 1357 = §27.7 cross-references close>
<blank line>
---
<blank line>
## 28. Per-CAPTAIN git seat identity via Co-Authored-By trailer
<full §28 body — see exact wording below>
<blank line>
---
<blank line>
<line 1360 = ## Agent-regime inverses (the positive framing)>
```

**Exact §28 body wording:**

```markdown
## 28. Per-CAPTAIN git seat identity via Co-Authored-By trailer

Every commit a CAPTAIN agent lands inside an arc-build worktree (`.claude/worktrees/arc-N-build/`) during a gauntlet carries a `Co-Authored-By:` trailer that names the seat + project. The trailer is the seat-identity signal; the commit `Author:` field stays PRINCIPAL's configured identity (`<user-name> <user-email>` from the PRINCIPAL's `git config user.*`) per global `~/.claude/CLAUDE.md`'s absolute rule "Git commit `Author:` — always use the user's configured git identity, never override." This section is the substrate-canonical home; per-seat application at `MAJOR_PLINY.md` §5.12 (dispatch-brief naming) and `CAPTAIN_ADA.md` §5.5 (pre-commit discipline).

### 28.1 The trailer format

```
Co-Authored-By: CAPTAIN_<MNEMONIC>_<project-slug> <captain-<mnemonic>@<project-slug>.local>
```

- **Name field** — `CAPTAIN_<MNEMONIC>_<project-slug>`. `<MNEMONIC>` is the seat's substrate name (`ADA`, `DAEDALUS`, `ARGUS`, `VERA`, `CATO`, `ZENO`, etc., per the `substrate/CAPTAIN_*.md` files). `<project-slug>` is the project's canonical slug (`the-stoa`, `ariadne-core`, etc. — hyphen-or-underscore-shaped per the project's own conventions). Underscore separator between the two segments binds them as a single name token.
- **Email field** — `captain-<mnemonic>@<project-slug>.local`. Lowercase-hyphen local-part. The `.local` TLD is reserved by RFC 6762 for link-local mDNS; it is non-routable on the public internet, so the trailer cannot accidentally generate email to a fake address. GitHub will not match the `.local` email to any real user account, so the trailer renders as a name+email text record without a fake-avatar pollution.

Worked examples for the-stoa project-tier:

```
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
Co-Authored-By: CAPTAIN_CATO_the-stoa <captain-cato@the-stoa.local>
```

### 28.2 Scope: CAPTAINs only

**Tagged (Co-Authored-By trailer required):**

- CAPTAIN_ADA build commits inside arc-build worktrees.
- CAPTAIN_DAEDALUS commits when DAEDALUS commits design artifacts directly (e.g., the design.md that opens a gauntlet).
- Any other CAPTAIN seat that direct-commits during the gauntlet (verdicts are usually committed as artifacts by ADA; if a CAPTAIN commits directly, tag it).

**Not tagged (Author = PRINCIPAL, no trailer required):**

- PLINY orchestrator commits (PLINY rarely direct-commits; merges via `gh pr merge` inherit PRINCIPAL identity).
- User-tier POLYBIUS direct-to-main housekeeping commits per `MAJOR_POLYBIUS.md` §18.1 (directive tracking, paste tracking, substrate-tool self-apply, orphan cleanup, retro docs, bw operations on the orphan beadwork branch).
- PRINCIPAL hand-authored commits.
- Squash-merge commits on main (created by `gh pr merge`; carry the trailers from squashed commits via GitHub's trailer-preservation property — see §28.3).

Rationale: PLINY + POLYBIUS commits are coordination + housekeeping, not authorial work. Tagging them adds noise without read-side signal. CAPTAIN commits ARE authorial work and ARE the empirical-anchor case (an ADA build commit was the misattributed source on the 2026-05-04 ariadne--xft.4 ARGUS git-blame incident).

### 28.3 Squash-merge preservation

GitHub's squash-merge behavior auto-populates a Co-Authored-By trailer from each squashed commit's author AND preserves any pre-existing Co-Authored-By trailers from the squashed commits' bodies into the squash-merge commit's body. The squash-merge commit on main therefore carries the trailer chain from every CAPTAIN commit that contributed to the arc, even after the `arc-N/build` branch is deleted. This is what makes the convention forward-compatible with the project's squash-merge convention (per `MAJOR_PLINY.md` §5.9 + §5.10 cleanup): seat identity survives branch deletion via the squash-merge commit body.

Verification: `git log --pretty='%(trailers)' main` walks squash-merge commit bodies and reveals the seat-identity trailers from each arc.

### 28.4 File-frontmatter author fields are NOT affected

This convention applies ONLY to git commit metadata. File-frontmatter `author:` fields (`SKILL.md`, `marketplace.json`, `package.json`, `LICENSE`, etc.) continue to name **Denson Smith** per the project-tier `CLAUDE.md` (at the project repo root) and global `~/.claude/CLAUDE.md` IMMUTABLE rule. The CAPTAIN_ADA.md §5.5 file-frontmatter discipline stands. This section makes the boundary explicit to prevent any reader from inferring "agents tag commits → agents also tag file frontmatter." Commit-trailer seat-identity is a metadata-layer signal; file-frontmatter author is a content-layer claim — different layers, different rules.

### 28.5 Read discipline: git blame is line-level; trailers are commit-level

The trailer convention addresses **commit-level** seat identity. `git blame` shows **line-level** Author attribution — and `git blame` follows the commit's `Author:` field, NOT its trailers. Because `Author:` stays PRINCIPAL by §28 design, `git blame` will show PRINCIPAL as the author of every line, even lines an agent wrote. **This is intended:** `Author:` preserves the workspace's identity uniformity; the trailer is the seat-identity signal layered on top.

The reading-side discipline that follows from this asymmetry:

> **Do NOT infer human authorship from `git blame` output.** A line attributed to the PRINCIPAL by blame may have been written by any seat (CAPTAIN or human) committing under PRINCIPAL's identity. To learn which seat actually wrote a line, walk the commit's trailers (`git log -1 --pretty='%(trailers)' <sha>`) or trace the ticket + PR + arc-build commit chain via `bw show <ticket>` + GitHub PR history.

This composes with §19.6 (attestation-confabulation): both disciplines are "cite live-verified state, not assumed-from-context state" — §19.6 at attestation time; §28.5 at git-blame-reading time. The 2026-05-04 ariadne--xft.4 ARGUS incident is an instance of the §28.5 failure mode: ARGUS read `git blame` output and asserted PRINCIPAL-authorship of a line an ADA build had written. The trailer convention does not prevent the same `git blame` output from appearing; the read discipline is what prevents the misattribution at the reading agent's end.

### 28.6 Future arcs may extend

This section enumerates CAPTAIN seats explicitly because they are the seats that empirically commit during the gauntlet today. The convention is shape-compatible with other seat ranks:

- A future paste-activated MAJOR seat that direct-commits (a hypothetical hotfix MAJOR, a long-running CURATOR session committing curator-tier artifacts) would carry `Co-Authored-By: MAJOR_<MNEMONIC>_<project-slug> <major-<mnemonic>@<project-slug>.local>` per the same shape.
- Currently-non-committing CAPTAINs (BARTLEBY, STRABO, HERALD, CURATOR per the substrate's `substrate/CAPTAIN_*.md` files) inherit §28 if-and-when they begin committing in future arcs.

Arc 35 does not pre-emptively extend the convention to non-committing seats — empirical-anchor surface today is gauntlet CAPTAINs only.

### 28.7 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL articulated this discipline (Option β fix-shape) on 2026-05-17 after the user-tier POLYBIUS audit surfaced the load-bearing tension between `stoa--kjo`'s original Option A (per-agent `Author:` override) and global `~/.claude/CLAUDE.md`'s absolute rule "never override `Author:`." §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

Supporting evidence at the time of this writing (2026-05-17):

- **N=1 bit-by-it (defect class: commit-level-seat-identity-absent):** 2026-05-04 ariadne--xft.4 ARGUS misattribution incident — ARGUS read `git blame` output and asserted "docstring authored by PRINCIPAL himself in commit `ebb9ecca`"; PRINCIPAL: "I am 100% sure I did not personally write that." The commit was an ADA build commit running under PRINCIPAL's git identity per standard workspace practice. Single observation today; defect class is "no commit-level seat-identity signal available to a reader walking git history."
- **N=0 worked-when-applied (controlled comparison):** no prior arc has applied the convention; Arc 35's self-application (A9) is the first instance. Accretes as future arcs ship under §28.

Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, Arc 31's `operating-disciplines.md` §25.6, Arc 32's family (§5.10.3 / §5.9.4.1 / §5.1.3 / §19.6.4), Arc 33's §27, and Arc 34's §18 + §5.11.

### 28.8 Cross-references

- Global `~/.claude/CLAUDE.md` — the absolute "never override `Author:`" rule §28 preserves; global CLAUDE.md authorship-attribution section carries a cross-ref bullet back to §28 acknowledging the substrate's compliant trailer convention.
- `MAJOR_PLINY.md` §5.12 — dispatch-brief responsibility (PLINY names the seat-identity each CAPTAIN should use in the trailer).
- `CAPTAIN_ADA.md` §5.5 — pre-commit discipline at the CAPTAIN seat (extension to the file-frontmatter authorship-discipline paragraph).
- §19.6 (attestation-confabulation) — sister discipline; both are "cite live-verified state, not assumed-from-context state" — §19.6 at attestation time; §28.5 at git-blame-reading time.
- §25 (PRINCIPAL-gate discipline) — the gate that adjudicated `stoa--kjo`'s original Option A to Option β.
- `MAJOR_POLYBIUS.md` §18 — the exempt-categories list (user-tier POLYBIUS housekeeping commits NOT tagged per §28.2).
- `MAJOR_PLINY.md` §5.10 (signoff-accuracy) + §5.11 (paste archival) — sibling arc-boundary disciplines; §28 fires throughout the arc-build (every CAPTAIN commit).
- `stoa--kjo` — work-unit ticket carrying the empirical-anchor + PRINCIPAL Option A → β adjudication.
- 2026-05-04 ariadne--xft.4 — the empirical-anchor incident (cross-repo reference).

---
```

### §3.2 — `substrate/MAJOR_PLINY.md` §5.12 (new subsection)

Insert at line 516 (between §5.11 close at line 515 and `---` at line 517). Insertion sequence:

```
<line 515 = §5.11.3 N=1 ... close>
<blank line>
### 5.12 Per-CAPTAIN seat-identity in the dispatch brief
<full §5.12 body — see exact wording below>
<blank line>
<line 517 = ---  unchanged>
<blank line>
<line 519 = ## 6. Communication  unchanged>
```

**Exact §5.12 body wording:**

```markdown
### 5.12 Per-CAPTAIN seat-identity in the dispatch brief

When you dispatch a CAPTAIN to a worktree-resident build (typically CAPTAIN_ADA inside `.claude/worktrees/arc-N-build/`, but applicable to any CAPTAIN that direct-commits during the gauntlet — DAEDALUS landing a design.md, a CAPTAIN landing a verdict artifact, etc.), the brief MUST name the exact seat-identity string the CAPTAIN writes into the `Co-Authored-By:` trailer of each commit per `operating-disciplines.md` §28. The brief carries the identity as a structured field; the CAPTAIN writes it verbatim into the commit's HEREDOC body.

**The dispatch-brief field shape:**

```
seat-identity: CAPTAIN_<MNEMONIC>_<project-slug> <captain-<mnemonic>@<project-slug>.local>
```

Worked example for an ADA dispatch in the-stoa project:

```
seat-identity: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
```

The CAPTAIN's commit message then writes the trailer verbatim:

```
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
```

PLINY names the project-slug per the project the gauntlet runs in (`the-stoa`, `ariadne-core`, etc. — the project's canonical slug; per-project convention recorded in that project's `CLAUDE.md` or substrate config). The CAPTAIN does NOT infer the slug; PLINY's brief is the source of truth.

**Why the brief carries the identity (not the CAPTAIN inferring it).** Two failure modes the brief-as-source-of-truth closes:

- **Per-project drift.** Without a brief-named identity, each CAPTAIN would have to infer the project-slug from the working directory path, the git remote, or the bw prefix — three different surfaces that may disagree (e.g., the working directory is `the-stoa` but the GitHub remote is `the-stoa.git`; the substrate project-slug convention may differ). Brief-named is unambiguous.
- **Cross-project CAPTAIN dispatches.** A future workflow might dispatch a CAPTAIN to operate against a different project's worktree (e.g., a CAPTAIN_ADA in `ariadne-core-workspace` dispatched from `the-stoa` PLINY). The brief names the seat-identity per the target project, not the dispatching PLINY's project.

**Cross-references:**

- `operating-disciplines.md` §28 — the substrate-canonical home for the trailer convention (the rule, the format, the scope, the squash-merge preservation property, the read-discipline pairing).
- §5.2 (ADA brief preamble — grounding-check enumeration) — the brief shape this section extends with the new `seat-identity:` field.
- `CAPTAIN_ADA.md` §5.5 — the per-seat application (CAPTAIN_ADA writes the trailer at commit time per the brief-supplied identity).
- §5.10 (signoff-accuracy) — verification that Arc N's own gauntlet commits carry the trailer per the convention being shipped (when an arc self-applies §28).
```

### §3.3 — `substrate/CAPTAIN_ADA.md` §5.5 extension

Existing §5.5 at lines 92-94 is unchanged. New paragraph appended IMMEDIATELY AFTER line 94 (before the blank line that precedes §5.6 at line 96). Insertion sequence:

```
<line 92 = ### 5.5 Authorship attribution (immutable)  unchanged>
<line 93 = blank  unchanged>
<line 94 = Any file with an author / owner / creator / maintainer / by / copyright field ... never anyone else. ...  unchanged>
<NEW blank line>
<NEW paragraph — see exact wording below>
<line 95 = blank  unchanged>
<line 96 = ### 5.6 Heartbeat-and-read-before-write via bw  unchanged>
```

**Exact NEW paragraph wording (appended to §5.5):**

```markdown
**Git-commit seat-identity trailer (commit-metadata layer, parallel to the file-frontmatter rule above).** Every commit you land inside an arc-build worktree carries a `Co-Authored-By:` trailer naming your seat + project per `operating-disciplines.md` §28. The trailer is dispatched in PLINY's brief as a structured `seat-identity:` field (per `MAJOR_PLINY.md` §5.12); write it verbatim at the end of the commit message HEREDOC, alongside the standard `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` trailer. The two trailers coexist; both are required. Example commit-message tail:

```
<commit body prose>

Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
```

The trailer is commit-metadata only — it does NOT touch the commit `Author:` field (which stays PRINCIPAL's configured identity per global `~/.claude/CLAUDE.md`'s absolute rule) and does NOT touch any file-frontmatter `author:` field (which stays Denson Smith per the paragraph above). The two disciplines are layered: file-frontmatter authorship is the content-layer claim; commit trailer is the metadata-layer seat-identity signal. Both apply independently; neither overrides the other.
```

### §3.4 — `~/.claude/CLAUDE.md` cross-ref (USER-TIER, OUTSIDE the gauntlet)

This edit lands as a user-tier POLYBIUS direct-to-main commit per `MAJOR_POLYBIUS.md` §18.1 (the user-tier housekeeping exception), NOT inside the arc-35-build worktree gauntlet. The sequencing is: gauntlet ships first (substrate canon §28 + §5.12 + CAPTAIN_ADA §5.5 extension); user-tier POLYBIUS then lands the cross-ref edit on PRINCIPAL's global CLAUDE.md AFTER the substrate canon merges.

**Insertion locus (rev2 — restructured per ARGUS F3 finding).** Inside the existing "Authorship attribution — never falsely credit someone else (CRITICAL)" section. The rev1 design placed the cross-ref as a NEW BULLET inside the "Mandatory audit before committing or pushing" enumerated checklist. ARGUS F3 flagged this as a structural pattern-break: the existing bullets enumerate *things to audit* (field names, file types, frontmatter lines, HTML meta tags, the Author rule); the new bullet describes a *complementary convention*, not a thing to audit. The pattern-break risks two miscategorizations by a cold reader: (a) the trailer is itself an audit-target field-of-its-own (false audit-discipline drift); (b) the bullet is a permitted *exception* to the absolute Author rule (the OPPOSITE of A4's intent). Rev2 corrects by inserting the cross-ref as a separate paragraph AFTER the "Mandatory audit" subsection closes — outside the enumerated checklist, with explicit framing.

**Current state of the "Mandatory audit before committing or pushing" subsection (lines 29-37 unchanged):**

```markdown
### Mandatory audit before committing or pushing

Before staging, committing, or pushing **any** file with an author-like field, check every one of:

- Field names: `author`, `authors`, `owner`, `creator`, `created_by`, `maintainer`, `maintainers`, `by`, `copyright`, `holder`, `vendor`, `publisher`
- Files that conventionally encode authorship: `plugin.json`, `marketplace.json`, `package.json`, `pyproject.toml`, `setup.py`, `Cargo.toml`, `Gemfile`, `composer.json`, `LICENSE`, `LICENSE.md`, `NOTICE`, `CITATION.cff`, `README.md` author/badge lines, skill `metadata.json`, `manifest.json`, anything under `.claude-plugin/`
- YAML frontmatter `author:` lines in skill files (`SKILL.md` and similar)
- HTML `<meta name="author">`, RSS `<author>`, sitemap author tags
- Git commit `Author:` — always use the user's configured git identity, never override

If any such field names a person other than Denson Smith, **STOP** and verify with the user in chat before proceeding. Do not assume that a name already present is correct just because it was there before — it may be a leftover from a fork, a template, an LLM-generated scaffold, or a previous error like the one being prevented here.
```

The audit checklist + its "STOP and verify" closing paragraph are UNCHANGED by rev2. The new cross-ref content lands as a standalone subsection AFTER the "Mandatory audit" subsection closes (immediately before the next existing subsection — currently "Naming references are NOT authorship claims").

**Post-edit state — NEW subsection inserted between "Mandatory audit before committing or pushing" subsection close and "Naming references are NOT authorship claims" subsection (verbatim wording for the new content):**

```markdown
### Substrate seat-identity convention (compliance-with-spirit of "never override Author:", not exception)

Projects that ship the Stoa substrate (`substrate/operating-disciplines.md` §28) add a `Co-Authored-By: CAPTAIN_<MNEMONIC>_<project-slug> <captain-<mnemonic>@<project-slug>.local>` trailer to CAPTAIN commits inside arc-build worktrees. The trailer is the seat-identity signal that lets a future agent or human reader walk `git log --pretty='%(trailers)'` and learn which agent seat authored a commit. The convention is the substrate's compliance mechanism for the "never override `Author:`" absolute rule above: `Author:` stays the PRINCIPAL's configured identity (unchanged); the seat-identity signal is layered on top via the Co-Authored-By trailer, which preserves through GitHub squash-merge into main.

This is NOT a permitted exception to the absolute Author rule and is NOT a new audit target. The "Mandatory audit" checklist above stands as-is; the Co-Authored-By trailer is metadata layered ON TOP of (not in place of) the audited Author field, and the file-frontmatter author-field discipline in the checklist is unchanged. Full canon home: `substrate/operating-disciplines.md` §28; per-seat application at `MAJOR_PLINY.md` §5.12 (dispatch-brief naming) and `CAPTAIN_ADA.md` §5.5 (pre-commit discipline at the writing seat).
```

**Wording rationale.** The standalone subsection cleanly separates the cross-ref from the audit checklist:

- The audit checklist enumerates things-to-check; this subsection describes a *complementary convention*. Different kind of content, different section.
- The heading "Substrate seat-identity convention (compliance-with-spirit of 'never override Author:', not exception)" makes the framing visible in the section heading itself — a reader walking the table-of-contents-shaped headings sees "compliance-with-spirit, not exception" before reading the body.
- The body opens with what the convention *is* (the trailer format + when it applies), then explicitly states the *compliance relationship* to the absolute rule ("`Author:` stays unchanged; signal is layered on top"), then explicitly closes the misread-as-exception door ("This is NOT a permitted exception ... and is NOT a new audit target").
- Cross-references to the substrate canon are at the end (the right shape — the heading + framing carry the load; the canon paths are the deep-read pointer).
- The closing sentence ("The 'Mandatory audit' checklist above stands as-is") explicitly defends the structural property ARGUS F3 protects: the audit checklist's enumerated bullets stay shaped as audit targets only.

This satisfies the directive A4 wording-property ("a reader of global CLAUDE.md who operates in substrate workspaces sees both the absolute rule AND the substrate's compliant trailer convention, preventing drift in either direction") AND ARGUS F3's structural property (the new content reads as compliance, NOT relaxation, AND must not be miscategorized as an audit target).

### §3.5 — Project-tier `CLAUDE.md` (at repo root) edit — DAEDALUS recommends NO edit

The directive's "Required reading" item 8 names the project-tier `CLAUDE.md` authorship section as A4-adjacent and notes "DAEDALUS picks whether to recommend." Reviewing the file at its actual on-disk location (`CLAUDE.md` at the the-stoa repo root — see "Path-citation correction" below): it already names the field-by-field audit list and the never-override discipline implicitly via reference to the global rule. Adding a §28 cross-ref here would duplicate the global-CLAUDE.md cross-ref without adding new signal — a reader of project `CLAUDE.md` who needs the trailer-convention canon is already routed (via the field-name list pattern) to the substrate's canonical home at `substrate/operating-disciplines.md` §28.

**Recommendation: NO edit to project-tier `CLAUDE.md` in Arc 35.** Reasoning:

1. Project `CLAUDE.md` authorship section talks about FILE-frontmatter authorship (`author:` field discipline + the "leftovers from forks" caveat). Commit-trailer seat-identity is a different layer (metadata, not content) and lives at `substrate/operating-disciplines.md` §28 — the right canonical home.
2. Adding a cross-ref bullet would expand the project `CLAUDE.md` authorship section into a two-discipline section, which over-weights commit-trailer-as-context-for-the-PRINCIPAL relative to the actual file-frontmatter discipline a project-tier reader needs.
3. The global `~/.claude/CLAUDE.md` cross-ref (per §3.4 above) IS the right surface for the trailer-convention acknowledgment, because the absolute "never override Author:" rule lives at the global tier — the cross-ref pairs naturally with the rule it complements.

If a future arc surfaces operational friction (e.g., a future CAPTAIN reads project-tier `CLAUDE.md` cold and doesn't know about the trailer convention because it's only cross-referenced from the global tier), revisit. For Arc 35, the global cross-ref alone is sufficient.

**Path-citation correction (sub-decision recorded for the build trail).** The directive (`substrate/arcs/arc-35-build-directive.md`) names this file as `substrate/CLAUDE.md` at lines 118 + 183 and in the polybius-activation paste at line 36. That path is wrong: there is no `substrate/CLAUDE.md` in this repo (verified 2026-05-17 by `ls` against the arc-35-build worktree). The project-tier `CLAUDE.md` is at the repo root (`/CLAUDE.md`); a separate app-tier `CLAUDE.md` exists at `/app/CLAUDE.md`; `substrate/` contains role files (`MAJOR_*.md`, `CAPTAIN_*.md`, `operating-disciplines.md`, etc.) but no `CLAUDE.md`. The directive's "project-tier rule" descriptor unambiguously refers to the project-tier CLAUDE.md (its content is the project-tier authorship/build rules ARGUS, ADA, and other CAPTAINs read on activation), which IS at repo-root `/CLAUDE.md`. Per the verify-then-execute discipline (`operating-disciplines.md` §7.2 / §19), this design corrects the citation in every shipped wording (§28.4 body above uses "project-tier `CLAUDE.md` (at the project repo root)"; this §3.5 uses "project-tier `CLAUDE.md`" without the broken `substrate/` prefix) rather than propagating the directive's path-error into permanent substrate canon. The broken path SHOULD also be cleaned up in a future-arc directive cleanup (P5 hygiene; not Arc 35 scope per A12) to prevent the same error reappearing in future arc directives that copy-paste from arc-35's; flagged to the §10 residual-questions list for ARGUS's call on whether to surface as an out-of-scope follow-up ticket.

---

## §4 — Verification probes (the spec VERA exercises)

The probes are runnable assertions VERA exercises against the built deliverable per `CAPTAIN_DAEDALUS.md` §3 + §6.6. Each probe specifies: what to check, the command to run, the expected output, and what failure means.

### §4.1 — §28 substrate canon section landed correctly

**Check:** `substrate/operating-disciplines.md` contains a new top-level `## 28. Per-CAPTAIN git seat identity via Co-Authored-By trailer` section between §27 close and the `## Agent-regime inverses` section.

**Command:**

```bash
grep -n "^## 28\. Per-CAPTAIN git seat identity via Co-Authored-By trailer" substrate/operating-disciplines.md
```

**Expected output:** Exactly one match line; line number > current §27 end (line 1356) AND < current "Agent-regime inverses" line (1360 + offset for §28 body).

**Failure interpretation:** Section missing (ADA didn't land it) OR section duplicated (ADA inserted twice) OR section heading misformatted (different casing, different separator).

### §4.2 — §28 subsections present

**Check:** §28 body has all required subsections (28.1 trailer format, 28.2 scope, 28.3 squash-merge preservation, 28.4 file-frontmatter NOT affected, 28.5 read discipline, 28.6 future arcs, 28.7 N=1 provenance, 28.8 cross-references).

**Command:**

```bash
grep -n "^### 28\." substrate/operating-disciplines.md
```

**Expected output:** Eight lines matching `### 28.1` through `### 28.8` in that order.

**Failure interpretation:** Missing subsection (incomplete build) OR mis-numbered subsection (numbering drift from design.md spec).

### §4.3 — §5.12 in MAJOR_PLINY.md landed correctly

**Check:** `substrate/MAJOR_PLINY.md` contains a new `### 5.12 Per-CAPTAIN seat-identity in the dispatch brief` subsection between §5.11 close and `## 6. Communication`.

**Command:**

```bash
grep -n "^### 5\.12 Per-CAPTAIN seat-identity in the dispatch brief" substrate/MAJOR_PLINY.md
```

**Expected output:** Exactly one match line; line number > current §5.11.3 line and < current `## 6. Communication` line (519 + offset).

**Failure interpretation:** Subsection missing OR mis-titled.

### §4.4 — CAPTAIN_ADA.md §5.5 extension landed

**Check:** `substrate/CAPTAIN_ADA.md` §5.5 contains the new "Git-commit seat-identity trailer" paragraph cross-referencing `operating-disciplines.md` §28 and `MAJOR_PLINY.md` §5.12.

**Command:**

```bash
grep -nE "Git-commit seat-identity trailer|operating-disciplines\.md.*§?28|MAJOR_PLINY\.md.*§?5\.12" substrate/CAPTAIN_ADA.md
```

**Expected output:** At least three matches inside the §5.5 region (between line 92 `### 5.5` heading and line 96 `### 5.6` heading + new-paragraph offset).

**Failure interpretation:** Extension paragraph missing OR cross-refs missing OR wrong target sections.

### §4.5 — Arc 35's own gauntlet build commits carry the trailer (self-application per A9)

**Check:** Every commit on `arc-35/build` authored by a CAPTAIN seat carries a `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` trailer.

**Command (run from the arc-35-build worktree):**

```bash
git log arc-35/build --pretty='%H %s%n  TRAILERS:%n%(trailers:only)' main..arc-35/build
```

**Expected output:** Every commit reachable from `arc-35/build` but not from `main` carries at least one `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` trailer line (plus the standard Claude trailer if present).

**Failure interpretation:** A CAPTAIN commit is missing the seat-identity trailer — Arc 35 has shipped the convention but not self-applied it. Per directive A9, this is a structural failure; ADA must rev2-rewrite the missing commits before VERA can pass.

**Edge case:** the design.md commit (this commit, by CAPTAIN_DAEDALUS_the-stoa) is the FIRST commit that carries the convention; it MUST be self-applied at commit time. ADA's gauntlet build commits follow — each must carry its own seat-identity trailer.

### §4.6 — Squash-merge preservation property holds (post-merge probe; VERA executes after PR-merge or via dry-run check)

**Check:** A squash-merge of the `arc-35/build` PR preserves the Co-Authored-By trailers from squashed commits into the squash-merge commit's body on main.

**Command (dry-run — verify the property on a PRIOR squash-merge to baseline expected behavior):**

```bash
git log main -1 --pretty='%(trailers:only)' 789496b  # Arc 33 ship commit
```

**Expected baseline output:** `Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>` (the Claude trailer ADA wrote into per-arc-build commits IS preserved in the squash-merge commit body — established behavior on Arc 33 ship `789496b`). Note: Arc 34 ship `244c1c3` has ZERO trailers, but this is NOT a refutation of the preservation property — it is a write-side failure (pre-squash Arc 34 commits `357e7635` and `af815ebf` had zero trailers themselves; the preservation property had nothing to preserve). Arc 33 is the deliberately-chosen baseline because it exercises the preservation path; Arc 34 is the deliberately-named counter-example for the write-side discipline path (probe §4.5 catches that failure mode).

**Command (post-merge — verify the Arc 35 squash-merge carries the seat trailers):**

```bash
git log main -1 --pretty='%(trailers:only)' <arc-35-squash-merge-sha>
```

**Expected post-merge output:** Trailer body includes at least one `Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` line per CAPTAIN that contributed to the arc.

**Failure interpretation:** If the Arc 33 dry-run baseline fails (returns empty), the GitHub squash-merge preservation property is not what design.md §1.3 asserts — re-investigate (web search for GitHub behavior changes; the preservation-side of §1.3's imported assumption is wrong). If the Arc 35 post-merge probe fails after CAPTAIN commits on `arc-35/build` DID carry the trailers (verified by §4.5), the trailers were written but not preserved — investigation needed (per-commit trailer formatting issue; GitHub Web UI vs CLI merge difference). If §4.5 already shows missing trailers on `arc-35/build`, the write-side mechanism failed (the Arc 34 failure mode recurring), and this probe's failure is downstream of that — fix at the write side (interactive rebase + amend per §5 remediation) before re-running this probe.

### §4.7 — Global `~/.claude/CLAUDE.md` cross-ref landed (user-tier POLYBIUS direct-commit, OUTSIDE gauntlet)

**Check:** The global CLAUDE.md authorship-attribution section contains the NEW standalone subsection "Substrate seat-identity convention (compliance-with-spirit of 'never override Author:', not exception)" placed between the "Mandatory audit" subsection close and the next existing subsection ("Naming references are NOT authorship claims"). The audit-checklist enumerated bullets are UNCHANGED from pre-edit state.

**Command (run from PRINCIPAL's filesystem; PLINY signoff verifies per §5.10):**

```bash
# Probe 4.7.a — new subsection heading lands at the right place
grep -nE "^### Substrate seat-identity convention" ~/.claude/CLAUDE.md

# Probe 4.7.b — cross-ref to substrate §28 present in the new subsection body
grep -nE "substrate/operating-disciplines\.md.*§?28" ~/.claude/CLAUDE.md

# Probe 4.7.c — audit-checklist bullets are UNCHANGED (no new audit-target bullet)
grep -nE "^- Git commit \`Co-Authored-By\`" ~/.claude/CLAUDE.md
```

**Expected outputs:**

- 4.7.a returns exactly one match inside the authorship-attribution section (after the "Mandatory audit" subsection close, before the "Naming references are NOT authorship claims" subsection).
- 4.7.b returns at least one match inside the new subsection's body (cross-ref to canon home).
- 4.7.c returns ZERO matches (the rev1 audit-checklist bullet pattern-break is NOT present; the cross-ref lives as a standalone subsection, not as an audit-checklist bullet).

**Failure interpretation:**

- 4.7.a empty: cross-ref subsection missing — user-tier POLYBIUS direct-commit didn't fire OR fired with wrong heading.
- 4.7.b empty: cross-ref subsection present but body doesn't link back to the substrate canon home — wording bug.
- 4.7.c non-empty: rev1's audit-checklist bullet pattern-break has landed — F3 not fixed (the post-edit shape regressed back to rev1).

Per Arc 35 sequencing, the global edit lands AFTER the substrate ships; PLINY signoff (per §5.10) verifies BOTH the substrate ship AND the global edit before declaring arc-close.

### §4.8 — Out-of-scope guard (A12 compliance probe)

**Check:** Arc 35's diff does NOT touch any of the A12-out-of-scope surfaces.

**Commands:**

```bash
# Probe 4.8.a: no file-frontmatter author: field edits
git diff main..arc-35/build -- '*.md' '*.json' '*.toml' '*.yml' '*.yaml' | grep -E "^[+-]\s*author:|^[+-]\s*\"author\""

# Probe 4.8.b: no commit Author: overrides (every commit on arc-35/build has Author = PRINCIPAL)
git log main..arc-35/build --pretty='%H %an <%ae>' | grep -v "denson <densonsmith2@gmail.com>"

# Probe 4.8.c: no install.sh changes
git diff main..arc-35/build -- substrate/install.sh

# Probe 4.8.d: no new substrate/scripts/ directory (A7 = manual mechanism, no shell helper)
git diff main..arc-35/build -- substrate/scripts/

# Probe 4.8.e: no PLINY-or-POLYBIUS commit tagging (only CAPTAIN seats in trailers)
git log main..arc-35/build --pretty='%(trailers:only)' | grep -E "Co-Authored-By: (MAJOR_PLINY|MAJOR_POLYBIUS)"
```

**Expected outputs:** All five commands return empty output (no matches).

**Failure interpretation per probe:**

- 4.8.a non-empty: ADA edited a file-frontmatter `author:` field (A11 IMMUTABLE violation).
- 4.8.b non-empty: ADA overrode commit `Author:` on some commit (global CLAUDE.md absolute rule violation).
- 4.8.c non-empty: ADA modified `install.sh` (A12 violation — only A7=ii mechanism authorizes install.sh changes; A7 picked = i).
- 4.8.d non-empty: ADA created a shell helper or other script under substrate/scripts/ (A7 = i forbids).
- 4.8.e non-empty: ADA tagged a PLINY or POLYBIUS commit (A3 scope violation — CAPTAINs only).

### §4.9 — Credential-discipline non-applicability (per `CAPTAIN_DAEDALUS.md` §6.6)

This design does NOT involve credentialed operations against any third-party API or cloud service. The build is pure substrate canon edits (markdown files in `substrate/`) plus a user-tier markdown edit (`~/.claude/CLAUDE.md`); no credentials, no CI, no third-party calls. §6.6's "design's verification probes section MUST include at least one probe that confirms the design's CI-mediated structure" requirement does not bind because the design has no credentialed-ops surface to mediate. The N/A is stated explicitly per §6.6's discipline rather than left implicit.

---

## §5 — Self-application plan (A9)

Per directive A9, Arc 35's own gauntlet build commits MUST carry the Co-Authored-By trailer per the convention being shipped. The first commit that carries the convention IS the commit that adds the convention (the design.md commit by DAEDALUS — this commit). Subsequent commits (ADA build, VERA verdict if committed, CATO verdict if committed, ZENO verdict if committed) carry their respective seat-identity trailers.

**Commit-by-commit plan for Arc 35:**

| Commit (by seat) | Trailer the commit carries | Notes |
|---|---|---|
| DAEDALUS design.md commit (this commit) | `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>` + `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` | The originating self-application instance. |
| ARGUS verdict commit (if committed as artifact) | `Co-Authored-By: CAPTAIN_ARGUS_the-stoa <captain-argus@the-stoa.local>` + Claude trailer | Verdict typically commented to bw, not committed; if ADA absorbs the verdict into the build commit as commentary, no separate ARGUS commit needed. |
| ADA build commit(s) — substrate canon edits per §3.1, §3.2, §3.3 | `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` + Claude trailer | Single commit preferred (substrate canon ships as one cohesive unit); multiple acceptable if scope warrants. |
| VERA verdict commit (if committed as artifact) | `Co-Authored-By: CAPTAIN_VERA_the-stoa <captain-vera@the-stoa.local>` + Claude trailer | Verdict typically commented to bw; commit only if scope warrants. |
| CATO verdict commit (if committed as artifact) | `Co-Authored-By: CAPTAIN_CATO_the-stoa <captain-cato@the-stoa.local>` + Claude trailer | Same as VERA. |
| ZENO verdict commit (if committed as artifact) | `Co-Authored-By: CAPTAIN_ZENO_the-stoa <captain-zeno@the-stoa.local>` + Claude trailer | Same as VERA. |
| PLINY squash-merge to main (via `gh pr merge`) | NOT a CAPTAIN commit; carries all preserved trailers from squashed CAPTAIN commits via GitHub's preservation property | The §28.3 squash-merge preservation property is what makes the seat-identity signal survive the merge. |
| User-tier POLYBIUS direct-to-main commit on `~/.claude/CLAUDE.md` (OUTSIDE gauntlet, AFTER substrate ships) | NO seat trailer (POLYBIUS not tagged per A3); standard PRINCIPAL Author per §18.1 housekeeping convention | The cross-ref edit is housekeeping per §18.1, not authorial work. |

**Self-application probe** (per §4.5): VERA runs `git log arc-35/build --pretty='%(trailers:only)' main..arc-35/build` and verifies every CAPTAIN commit has its seat trailer.

**Failure remediation:** if a CAPTAIN commit forgets the trailer, that commit must be re-authored (interactive rebase + amend OR new commit with corrected trailer + drop of the bad commit) BEFORE PLINY merges the PR. Shipping un-self-applied would create the discontinuity the directive A9 calls out: "we made this rule on 2026-05-17 and started following it on 2026-05-N+1." Per §9.2, the Arc 34 empirical witness (`244c1c3` ship has 0 trailers because pre-squash `357e7635` + `af815ebf` had 0 trailers — ADA omitted the standard Claude trailer on every Arc 34 build commit) is the concrete evidence that the manual mechanism HAS already failed once at this seat for the simpler one-trailer case; Arc 35's two-trailer convention runs the same operator-dependent risk. The verification gate (§4.5 probe + PLINY signoff per §5.10) is the structural safety net Arc 34 lacked; it must catch the failure BEFORE merge, when remediation is cheap.

---

## §6 — Cite-comment locations (A10)

Per directive A10, every place that references "agent commit identity" or "git blame attribution" carries a cite-comment to `operating-disciplines.md` §28. Every place that references the global "never override Author:" rule carries a cite-comment to global `~/.claude/CLAUDE.md` authorship-attribution section.

**Cite-comment enumeration (the places Arc 35 plants the cites):**

| Site | Cite to | Already covered by §3 wording? |
|---|---|---|
| `operating-disciplines.md` §28.8 cross-references | global `~/.claude/CLAUDE.md`, `MAJOR_PLINY.md` §5.12, `CAPTAIN_ADA.md` §5.5, §19.6, §25, `MAJOR_POLYBIUS.md` §18, `MAJOR_PLINY.md` §5.10 + §5.11, `stoa--kjo`, ariadne--xft.4 | Yes (§3.1 §28.8 wording above) |
| `MAJOR_PLINY.md` §5.12 cross-references | `operating-disciplines.md` §28, §5.2, `CAPTAIN_ADA.md` §5.5, §5.10 | Yes (§3.2 §5.12 wording above) |
| `CAPTAIN_ADA.md` §5.5 extension | `operating-disciplines.md` §28, `MAJOR_PLINY.md` §5.12, global `~/.claude/CLAUDE.md` | Yes (§3.3 extension wording above) |
| Global `~/.claude/CLAUDE.md` new standalone subsection ("Substrate seat-identity convention") | `substrate/operating-disciplines.md` §28 (canon home); `MAJOR_PLINY.md` §5.12; `CAPTAIN_ADA.md` §5.5 | Yes (§3.4 rev2 wording above) |
| `MAJOR_POLYBIUS.md` §18.1 (existing — A3 exempts POLYBIUS commits) | NOT EDITED by Arc 35 (Out-of-scope per A12 — no edits to §18 prose); the existing §18 prose already enumerates "user-tier POLYBIUS direct-commit ... may direct-commit to main for a bounded set of housekeeping operations" which IS the A3 exemption rationale. No NEW cite required from §18 into §28 — the §28 cross-reference list points BACK to §18 instead. | N/A (no edit to §18) |
| Other CAPTAIN role files (DAEDALUS, ARGUS, VERA, CATO, ZENO, BARTLEBY, STRABO, HERALD, CURATOR) | NOT EDITED by Arc 35; single source of truth at op-disc §28; per A6 directive: "single source of truth for the rule is operating-disciplines.md §28; role files cite-comment to it." | N/A (no edits to non-ADA CAPTAIN role files in Arc 35; CAPTAIN_ADA is the one CAPTAIN that empirically commits in the gauntlet today, and its envelope gets the explicit extension; other CAPTAINs inherit §28 via universal-team read of operating-disciplines.md per §23) |

**Cite-comment-not-cross-ref distinction.** Per Arc 33 / Arc 34 precedent, "cite-comment" means an inline citation in the section's prose pointing to the canonical home, not a separate cross-references list (though the cross-references list IS one form of cite-comment). The §3 wording above plants inline cites in the prose AND populates a `Cross-references` subsection at the end of each new section, mirroring the §27 + §5.11 precedent shape.

---

## §7 — Worked-example commit message (the ADA reference)

ADA's substrate-canon build commit for Arc 35 will look like this (full reference for ADA to copy + adapt):

```bash
git commit -m "$(cat <<'EOF'
Arc 35: per-CAPTAIN git seat identity via Co-Authored-By trailer — substrate canon (stoa--kjo)

Ships three coordinated substrate canon edits per arc-35-build-directive.md A2-A11 + agents/design/stoa--kjo/design.md §3:

- substrate/operating-disciplines.md: new §28 "Per-CAPTAIN git seat identity via Co-Authored-By trailer" (universal-team canon home; trailer format §28.1; CAPTAINs-only scope §28.2; squash-merge preservation §28.3; file-frontmatter unchanged §28.4; read discipline for git blame §28.5; future-extension §28.6; N=1 provenance §28.7; cross-references §28.8)
- substrate/MAJOR_PLINY.md: new §5.12 "Per-CAPTAIN seat-identity in the dispatch brief" (PLINY's dispatch-time responsibility; seat-identity carried as structured field; cross-refs to §28 + §5.2 + CAPTAIN_ADA §5.5 + §5.10)
- substrate/CAPTAIN_ADA.md: §5.5 extension paragraph naming the commit-trailer discipline as a parallel concern to file-frontmatter authorship; cross-refs to §28 + §5.12 + global CLAUDE.md

Self-application per A9: this commit and every CAPTAIN commit on arc-35/build carries the trailer per the convention being shipped. The first commit that carries the convention IS the commit that adds the convention.

Out-of-scope per A12 (HARD-LOCKED): no file-frontmatter author: field edits; no Author: overrides; no PLINY/POLYBIUS commit tagging; no non-CAPTAIN seat identity; no retroactive blame; no GitHub repo settings; no shell tooling beyond A7=i (manual); no install.sh changes.

Empirical anchor: 2026-05-04 ariadne--xft.4 ARGUS git-blame misattribution. PRINCIPAL Option A → β reframing 2026-05-17.

Cross-refs: substrate/operating-disciplines.md §28 (canonical home); §19.6 (attestation-confabulation sister discipline); §25 (PRINCIPAL-gate adjudication); MAJOR_POLYBIUS.md §18 (exempt-categories list); MAJOR_PLINY.md §5.10 (signoff verifies self-application); ~/.claude/CLAUDE.md authorship section (cross-ref edit lands user-tier post-merge).

Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

The two trailers at the end are load-bearing:

1. `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` — the new convention being shipped (per §28.1).
2. `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>` — the standard Claude trailer per global CLAUDE.md commit-message convention.

Both must be present on every CAPTAIN gauntlet commit on `arc-35/build`. VERA's probe §4.5 checks both.

**DAEDALUS's own design.md commit** (this commit, landing immediately after design.md write) uses the same HEREDOC pattern with DAEDALUS's seat-identity trailer:

```bash
git commit -m "$(cat <<'EOF'
Arc 35: DAEDALUS design.md for stoa--kjo — per-CAPTAIN git seat identity via Co-Authored-By trailer

Design covers all four sub-decisions per arc-35-build-directive.md (A5 trailer format CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>; A6 §28 + §5.12 + CAPTAIN_ADA §5.5-extension; A7 manual mechanism (i); A8 read-discipline subsection (a) inside §28.5) plus exact wording for each canon insertion (§28 body in op-disc; §5.12 in PLINY; §5.5 extension paragraph in CAPTAIN_ADA; cross-ref bullet in global ~/.claude/CLAUDE.md). Verification probes §4.1-§4.9 specified. Self-application per A9: this commit IS the first commit that carries the convention being shipped.

Cross-refs: substrate/arcs/arc-35-build-directive.md (LOCKED spec); ~/.claude/CLAUDE.md authorship-attribution section (absolute Author: rule preserved); substrate/operating-disciplines.md §19.6 + §25 + §27 (precedent shapes); MAJOR_PLINY.md §5.9.4 + §5.10 + §5.11 (sibling family); MAJOR_POLYBIUS.md §18 (A3 exemption rationale); CAPTAIN_ADA.md §5.5 (extension target).

Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## §8 — Out-of-scope (cite A12 verbatim)

Per directive A12 (HARD-LOCKED), Arc 35 does NOT:

- Touch any file-frontmatter `author:` field discipline (immutable per A11).
- Override `Author:` for any commit (per global CLAUDE.md absolute rule + PRINCIPAL pick β).
- Tag PLINY or POLYBIUS commits (per PRINCIPAL pick — CAPTAINs only).
- Build per-agent identity for non-CAPTAIN seats (HERALD, CURATOR, BARTLEBY, STRABO, etc. — Arc 35 lists them in §28 as "future arcs may extend"; ships only the CAPTAINs that empirically commit).
- Build retroactive blame-attribution for past commits (Arc 35 is forward-only; the historical empirical anchor stays as-is).
- Build GitHub repo-side settings (commit signing, branch protection, CODEOWNERS, etc.) — substrate canon only.
- Build shell tooling beyond what A7 directly specifies — if DAEDALUS picks (i) manual, NO shell helper; if (ii), only the one helper. **A7 picked = (i) manual; therefore NO shell helper, NO new substrate/scripts/ directory.**
- Touch `substrate/install.sh` beyond what A7 implementation choice requires. **A7 picked = (i); therefore NO install.sh changes.**

Scope-creep guard per directive A12: if DAEDALUS or any CAPTAIN surfaces a scope concern touching A12, treat as substance disagreement: confirm A12 wording from this directive, file follow-up ticket if the concern has merit, do NOT expand this arc.

---

## §9 — Self-assessed weak points (per `CAPTAIN_DAEDALUS.md` §6.2)

Per the post-work gate at §6.2, the design's brittle spots are flagged here for ARGUS's critique pass. Each entry: weak point + why this shape anyway.

### §9.1 — Trailer-format `.local` domain may surprise readers expecting routable emails

**Weak point.** `captain-<mnemonic>@<project-slug>.local` uses the RFC 6762 `.local` pseudo-TLD. A reader of git history who is unfamiliar with `.local` may think the email is malformed or unintentionally fake-looking; a future tool that parses Co-Authored-By trailers and tries to resolve the email (e.g., looking up GitHub user by email) will fail to match. Some git platforms (Gitea, GitLab) may render the trailer slightly differently than GitHub does — the design has not been tested against non-GitHub renderers.

**Why this shape anyway.** The directive A5 constraint is explicit: "Email field MUST be a `.local` or otherwise non-routing local-only domain to prevent accidental email-list inclusion." Routable email addresses risk spam to a fake address; the `.local` TLD is the canonical non-routing pseudo-TLD per RFC 6762. Alternatives (`@example.com` per RFC 2606, `@invalid` per RFC 6761) are semantically equivalent for non-routability but less common in git seat-identity conventions. `.local` is the empirically-anchored choice in the directive's worked example. The "tool that parses trailers" concern is a future-tool concern, not a today concern; the design ships the convention that meets today's stated constraint.

### §9.2 — Manual mechanism (A7=i) has a documented past-failure mode at THIS seat one arc ago (Arc 34)

**Weak point (rev2 — reframed with concrete N=1 citation per ARGUS F4 finding and A13 / `operating-disciplines.md` §6.7.1 N=1-honesty discipline).** A7=i (manual in-commit-message trailer) has no mechanical enforcement. The failure mode is not hypothetical: it has already materialized once at this seat one arc ago, for the standard `Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>` trailer convention this seat-identity trailer composes with.

**Concrete witnesses (verified 2026-05-17 by `git log -1 --pretty='%(trailers:only)' <sha>`):**

| Arc | Ship SHA | Pre-squash SHAs | Trailers on ship | Trailers on pre-squash |
|---|---|---|---|---|
| Arc 33 | `789496b` | (single ADA commit) | 1 (`Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>` preserved) | 1 |
| Arc 34 | `244c1c3` | `357e7635` (rev1) + `af815ebf` (rev2) | **0** (squash had nothing to preserve) | **0 + 0** |
| Arc 35 (this) | (TBD) | `16b09e1` (DAEDALUS design.md rev1, this seat self-applied) + DAEDALUS rev2 of this commit + ADA build commit(s) | (TBD) | rev1 = 2 (self-applied per A9) |

Arc 34 is the empirical witness that ADA omitted the standard Claude trailer on EVERY pre-squash build commit one arc ago at this exact seat. The convention being shipped in Arc 35 has a meaningfully higher cognitive load (TWO trailers per commit instead of one — the seat-identity trailer + the Claude trailer), AND the same operator (CAPTAIN_ADA in this project's gauntlet) who already missed the simpler one-trailer case once. If the manual mechanism (A7=i) fails again on Arc 35's ADA build commit, the SHIP commit would carry zero seat-identity trailers (preservation property has nothing to preserve), Arc 35 would not have self-applied per A9, and the convention would ship as canon-without-self-application — the discontinuity the directive A9 explicitly forbids ("we made this rule on 2026-05-17 and started following it on 2026-05-N+1"). VERA probe §4.5 + PLINY signoff per §5.10 are the safety net; the remediation (interactive rebase + amend, or new commit + drop) is operationally awkward and creates additional git history noise.

**Why this shape anyway (rev2 — the deliberate justification per A13 + ARGUS F4 framing "default to manual; the manual mechanism has already failed once at this seat one arc ago for the Claude trailer convention; this design accepts that risk with deliberate justification").** Three deliberate reasons:

1. **Cost-asymmetry favors manual at Arc 35's scale.** A7=ii (shell helper) buys mechanical enforcement at the cost of: new tooling surface (`substrate/scripts/`), `install.sh` change to deploy the helper, agent role-file updates to call the helper, AND a new failure mode (the helper is misconfigured or its location varies across worktrees). The helper itself has a known failure mode (Arc 34 showed ADA can forget conventions); replacing one manual convention with a helper-mediated one does not eliminate the discipline gap, it RELOCATES it (now ADA must remember to call the helper). The helper IS recoverable surface to lose ("did I call git-coauthor.sh?" is the same question as "did I include the trailer line?" — both at HEREDOC-authoring time).

2. **The Arc 34 failure was a single-trailer omission; the Arc 35 mitigation is verification-mediated, not enforcement-mediated.** §4.5 (probe: every CAPTAIN commit on `arc-35/build` has the seat trailer) + §5.10 (PLINY signoff verifies this before PR-merge) form a verification gate at the place the convention's failure manifests (the commit-already-exists, not-yet-merged state — the same state where amend/drop remediation is cheap). The verification gate is the structural safety net Arc 34 lacked (no probe ran on Arc 34 for the Claude trailer because no probe existed to run). Arc 35 ships the probe AND the convention as one cohesive unit; the probe IS the answer to "what about the Arc 34 failure mode."

3. **Reversibility (A7 directive escape hatch).** If Arc 35's gauntlet PLUS the probe still fails — i.e., ADA-forgets-trailer AND VERA-misses-it OR PLINY-signoff-misses-it — the next arc may add the shell helper (A7=ii) as remediation. The (i) → (ii) migration is forward-compatible: the helper writes the same trailer the manual mechanism writes today; existing commits remain valid. The deferral is to evidence-from-Arc-35 itself: if Arc 35 ships clean and self-applies clean, the manual mechanism is empirically viable; if Arc 35 ships with the failure mode recurring, the next arc has the empirical anchor for adding the helper.

**Honest scoping of the risk.** The Arc 34 instance is N=1 at this exact seat for the trailer-omission failure mode; Arc 33 is N=1 at the same exact seat for trailer-application success. The mechanism's reliability is not "untested" or "robust" — it is "1-of-2 at this seat across the immediately preceding two arcs," which is exactly the evidence-density Arc 35's design must own. If Arc 35 ships with the trailers present (probe §4.5 PASS, PLINY signoff per §5.10 verifies), the count moves to 2-of-3 (one near-miss recovered by the new probe — exactly the value the verification gate adds); if Arc 35 ships with the trailers missing (probe §4.5 catches at gauntlet time, remediation succeeds), the count moves to 2-of-3 with the catch credited to the new probe (proving the safety-net works); if Arc 35 ships with the trailers missing AND the probe fails to catch, the design has a structural defect and the next arc must add A7=ii. Per `operating-disciplines.md` §6.7.1, this is honest at the structural-lesson tier: the mechanism is named, the failure mode is empirically anchored, the safety net is named, the escape hatch is named.

### §9.3 — Read-discipline §28.5 may underplay the persistent gap

**Weak point.** The trailer convention is necessary-but-not-sufficient for the empirical-anchor failure mode (`git blame` line-level attribution still follows `Author:`, not trailers). §28.5 names this asymmetry but the rule is "do not infer human authorship from blame" — which depends on the reader (every future ARGUS, CATO, etc.) actually applying the discipline at every blame-read site. The discipline carries no mechanical enforcement; the structural gap (blame is line-level, trailers are commit-level) persists. A future ARGUS that reads §28.5 cold and asserts "PRINCIPAL wrote this line per blame" is the same failure shape as the 2026-05-04 incident.

**Why this shape anyway.** The full fix for the asymmetry is Option A from the original `stoa--kjo` ticket (per-agent `Author:` override) — which PRINCIPAL explicitly rejected on 2026-05-17 because it violates the global "never override `Author:`" rule. Given Option β is the chosen fix-shape, the read-discipline at §28.5 IS the structural complement: the trailer adds the commit-level seat-identity signal AND the read-discipline tells agents how to USE it. The remaining gap (agents must apply the discipline at every blame-read site) is shared with every other operating-disciplines.md canon — none of which has mechanical enforcement; they all rely on agent-reading-and-following. The §28.5 rule is named explicitly to maximize discoverability; future arcs may add inspection-agent-layer enforcement (per `operating-disciplines.md` §27 mechanical/agent split) if the persistent gap surfaces empirically.

### §9.4 — Cross-project trailer-format extensibility is asserted, not tested

**Weak point.** §28.1 names the format as `CAPTAIN_<MNEMONIC>_<project-slug>` with per-project slug; the design asserts this works for any project's canonical slug shape (hyphenated like `the-stoa`, underscored like `ariadne_core`, etc.). Arc 35 self-applies the convention ONLY at the-stoa project-tier; no cross-project validation is done. If a future project's canonical slug shape (CamelCase? slashed? dotted?) doesn't compose cleanly into the trailer format, the convention would need a project-specific adjustment.

**Why this shape anyway.** Arc 35's scope is shipping the convention at the-stoa; cross-project extensibility is a future-arc concern (per A6 directive: "ships only the CAPTAINs that empirically commit"). The format's extensibility is asserted on the principle that ASCII-hyphen-and-underscore covers known project slug shapes (the-stoa, ariadne-core, ariadne_core); CamelCase and other exotic shapes would surface as future-arc concerns when a new project adopts the substrate. The design's worked examples (the-stoa explicit; ariadne-core implicit via empirical anchor reference) cover the two project-slug shape families relevant today.

### §9.5 — Sequencing of substrate ship vs global CLAUDE.md edit is operator-dependent

**Weak point.** The global `~/.claude/CLAUDE.md` cross-ref edit (per §3.4) lands as a user-tier POLYBIUS direct-to-main commit OUTSIDE the arc-35-build gauntlet, AFTER the substrate canon merges. PLINY signoff (per §5.10) verifies both happened. But the sequencing depends on user-tier POLYBIUS being available to execute the global edit between substrate-merge and signoff-post — if user-tier POLYBIUS is unavailable, PLINY signoff would have to either (a) wait, blocking arc close, or (b) post a signoff that honestly names "substrate shipped; global CLAUDE.md edit pending — open ticket filed for the edit."

**Why this shape anyway.** The global CLAUDE.md is PRINCIPAL's personal config; only PRINCIPAL and user-tier POLYBIUS have legitimate authority to edit it. A gauntlet CAPTAIN editing the global file would cross a tier boundary inappropriately. The sequencing dependency is a property of the tier-separation, not a design weakness; option (b) (honest-fallback signoff per §5.10's existing discipline) is the structural fallback the directive already authorizes. If the dependency surfaces operationally (PLINY signoff blocked waiting for user-tier POLYBIUS too often), a future arc can revise — but Arc 35's two-tier sequencing is the right shape for today's tier model.

---

## §10 — Residual questions for ARGUS

These are explicit questions for the ARGUS plan-critique pass (per `CAPTAIN_DAEDALUS.md` §7 verdict-format `residual_questions_for_argus:`). They are NOT weak points (those are §9); they are places where ARGUS's cold-read perspective is specifically requested.

1. **Is §28.5's read-discipline subsection sufficient, or does it warrant standalone-section treatment (Option (b)) given the persistent gap §9.3 names?** DAEDALUS picked (a) per same-arc-pairing rationale; ARGUS may surface a different perspective. (rev1 non-finding per ARGUS — preserved as residual for completeness.)
2. **Is the rev2 §3.4 wording for the global `~/.claude/CLAUDE.md` standalone subsection structurally correct?** Rev1 had the cross-ref as an audit-checklist bullet; ARGUS F3 flagged it as pattern-breaking. Rev2 restructures as a standalone subsection AFTER the "Mandatory audit" subsection closes, with the heading "Substrate seat-identity convention (compliance-with-spirit of 'never override Author:', not exception)". ARGUS rev2 should re-verify: (a) the new content reads as compliance, NOT relaxation; (b) the audit-checklist enumerated bullets are confirmed UNCHANGED; (c) the new subsection's heading conveys the framing without requiring the reader to descend to body prose; (d) the body's closing sentence ("The 'Mandatory audit' checklist above stands as-is") is sufficient to close the audit-target-misread door.
3. **Does the §3.5 recommendation to NOT edit project-tier `CLAUDE.md` hold?** DAEDALUS reasoned that the global cross-ref is sufficient + project-tier authorship section is FILE-frontmatter focused; ARGUS may have a different view on whether project-tier readers need the trailer-convention surface too. (Note: rev2 corrects the rev1 path-error per ARGUS F1 — the project-tier CLAUDE.md is at repo-root `/CLAUDE.md`, not `substrate/CLAUDE.md` which does not exist; the recommendation-not-to-edit applies to the actual project-tier `/CLAUDE.md`.)
4. **Is the trailer-format pick (A5 = `CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>`) the right balance of empirical-anchor alignment vs. the-stoa's canonical slug shape?** Specifically: should the seat-segment-to-project-segment separator be underscore (as picked) or hyphen? (rev1 non-finding per ARGUS PASS on §2.1 — preserved as residual for completeness.)
5. **Are VERA probes §4.1-§4.9 sufficient coverage, or are there structural properties of the convention (e.g., CI/PR-bot rendering, GitHub API behavior) that warrant additional probes?** DAEDALUS specified what felt complete; ARGUS may surface gaps. (Note rev2 adds three sub-probes 4.7.a-4.7.c for the global CLAUDE.md edit shape per F3 fix; the structural property "audit-checklist bullets are UNCHANGED" is now mechanically checkable.)
6. **Future-arc directive cleanup (per F1 fix sub-decision recorded at §3.5).** This design corrects the `substrate/CLAUDE.md` path-citation in every shipped wording rather than propagating the directive's path-error into permanent canon. The directive itself (`substrate/arcs/arc-35-build-directive.md` lines 118 + 183 + activation paste line 36) still carries the broken path. ARGUS should adjudicate whether this warrants a follow-up ticket (P5 hygiene; not Arc 35 scope per A12) to scrub the directive's path-error and any other future arc directive that copy-pastes from it, or whether the design.md's correction is sufficient (since the substrate canon is what readers cite forward).

---

## §11 — Authorship attribution (per `CAPTAIN_DAEDALUS.md` §8)

This design document is authored by CAPTAIN_DAEDALUS_the-stoa on behalf of the PRINCIPAL (Denson Smith). The synthesis, structural choices, sub-decision picks (A5/A6/A7/A8), exact wording for each canon insertion, verification probes, weak-point self-assessment, and residual questions are the PRINCIPAL's per `CAPTAIN_DAEDALUS.md` §8. The empirical anchor (2026-05-04 ariadne--xft.4 ARGUS misattribution) is cited as historical context. The PRINCIPAL's Option A → β adjudication (2026-05-17) is captured in the directive header and reflected throughout this design.

No file-frontmatter `author:` field is touched by this design or by Arc 35's build. The Co-Authored-By trailer convention shipped by Arc 35 is metadata-layer; it does NOT override the file-frontmatter authorship rule.
