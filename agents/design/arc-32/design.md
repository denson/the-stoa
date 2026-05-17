# Arc 32 design — Canonification batch (C1-C5)

**Ticket:** `stoa--ewn`
**Branch:** `arc-32/build` (to be created by ADA in a separate worktree per §3.5 C5 below)
**Date:** 2026-05-17
**Status:** rev2 — addresses ARGUS rev1 R1-R6; AWAITING ARGUS rev2 audit
**Directive:** `substrate/arcs/arc-32-build-directive.md` (A1-A11 LOCKED)
**Authored by:** CAPTAIN_DAEDALUS_the_stoa, on behalf of the PRINCIPAL (Denson Smith).

---

## §1 — Intent

Arc 32 ships five small substrate-canon tightenings (C1-C5) as a single coherent canonification arc. Each candidate has empirical anchor + clear fix shape + small surface; the bundling is justified because all five share the theme "encode-as-canon what has been operating ad-hoc" and the per-candidate edits are mostly additions or in-place section extensions (no destructive rewrites). The full work-unit ticket prose and Phase A LOCKED architectural decisions (A1-A11) are at `bw show stoa--ewn` and `substrate/arcs/arc-32-build-directive.md`; this design takes those as load-bearing input and produces the verbatim canon prose ADA will paste.

---

## §2 — Inputs (read-first artifacts and their roles)

| Artifact | Role in this design |
|---|---|
| `substrate/arcs/arc-32-build-directive.md` | Load-bearing spec. A1-A11 LOCKED. Architectural decisions NOT re-opened. |
| `bw show stoa--ewn` (ticket body + 2026-05-17T09:12:21Z C5 comment) | Primary input prose. Empirical anchors + fix shapes for C1-C5. |
| `substrate/MAJOR_POLYBIUS.md` §5.1 area (lines 198-302) | C1 extends §5.1.1; C2 adds §5.1.3 parallel to existing §5.1.2 (pre-branch hygiene paste convention). |
| `substrate/MAJOR_PLINY.md` §5.9 (lines 329-389) | C3 lives at new §5.10 (Option α picked); C5 extends §5.9 family at new §5.9.4 (Option A picked). |
| `substrate/operating-disciplines.md` §19 (lines 805-846), §24 (lines 1092-1110), §25 (lines 1113-1212) | C4 extends §19 with attestation sub-rule at new §19.6; C2 thin cross-ref at new §26 (parallel to §24's Arc 30 model); C3 thin cross-ref at §24 family. |
| `substrate/templates/paste-instruction-template.md` (155 lines) | C2 adds `{{CRON_HYGIENE_CLAUSE}}` slot mirroring existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` shape. |
| `HUMAN_paste-pliny-arc-30-instruction.md` + `HUMAN_paste-pliny-arc-31-instruction.md` + `HUMAN_paste-pliny-arc-32-instruction.md` | Three consecutive ad-hoc encodings of the cron-hygiene preamble C2 canonifies. Canonical wording for `{{CRON_HYGIENE_CLAUSE}}` default expansion derived from Arc 31 + Arc 32 paste convergence. |
| `agents/design/arc-30/design.md` | Style + structure model for substrate-canon design artifacts (three-carrier framing, §5.9.3 N=1 provenance shape, cross-references block). |

**Imported assumptions named (per `CAPTAIN_DAEDALUS_the_stoa.md` §6.1 restatement-gate discipline):**

- **The bundling is honest.** Five candidates is more surface than a single-discipline arc; A1 LOCKS them as one gauntlet. The design treats them as one integrated artifact (single ARGUS cold-read, single ADA build, single VERA+CATO+ZENO pass) — but each candidate is independently scoped per §3.1-§3.5 so a partial revision (e.g., ARGUS asks to revise C3 only) can be made without touching the others.
- **C3 and C5 sub-decisions are within DAEDALUS A4/A6 discretion.** §3.3 (C3 picks Option α) and §3.5 (C5 picks Option A) carry the rationale; neither pick raises a §25 PRINCIPAL-gate per the dispatch brief's gate-recognition criteria. The picks match user-tier POLYBIUS's stated lean (recorded in directive A4/A6 prose) but the rationale is DAEDALUS-derived from the empirical anchors and the structural analogy to Arc 30 §5.1.2's per-session-judgment rejection.
- **A10 §15 N=1 per-candidate.** Each canon section names its empirical anchor (N=1 or N=2 today) and explicitly defers to `operating-disciplines.md` §6.7.1 for promotion to "structural lesson" status. The phrasing matches Arc 30 §5.9.3 + Arc 31 §25.6 shape; do not over-generalize.
- **A8 authorship immutability.** All five candidates edit existing files; no new files with fresh author-like fields. The `paste-instruction-template.md` `author: Denson Smith` frontmatter is the only author-like field in the edit set and is not modified. §5 confirms.
- **A9 out-of-scope hard lock.** stoa--32b.2 (script/agent-inspection split), stoa--k36 (user-tier-to-main discipline), stoa--f37 (paste accumulation), stoa--ize (arcs/22 branch), parent epic stoa--32b structure — none touched by this design. The cron-hygiene canon (C2) does NOT migrate the three historical activation pastes that already carry the preamble ad-hoc; A9 hard-locks "forward-only convention adoption."

---

## §3 — Per-candidate design

The five candidates are designed independently in §3.1-§3.5. Cross-refs between candidates resolve per A7: C2+C5 may cross-ref (both PLINY-facing operational hygiene); C3+C4 may cross-ref (both honesty-discipline); C1 stands alone.

### §3.1 — C1: §5.1.1 cross-project context leak extension

**Target file:** `substrate/MAJOR_POLYBIUS.md`
**Insertion-point:** extend existing §5.1.1 (starts MAJOR_POLYBIUS.md:212; ends MAJOR_POLYBIUS.md:226). Add a new `##### 5.1.1.1` sub-subsection between the existing "Empirical anchor: 2026-05-04 …" line (line 224) and the existing "For the universal-team framing…" cross-ref line (line 226). The cross-ref to `operating-disciplines.md` §8 stays as-is at the end of §5.1.1.

**Locus rationale:** §5.1.1 is the existing "positive references only when filling slots" discipline; cross-project sequencing leak is a specific sub-case of the same root cause (a `NOT` or "out of scope" framing seeds awareness of the resource the discipline excludes). Extension preserves the existing §5.1.1 reader's mental model — the new sub-discipline is a refinement, not a separate canon section. A separate §5.1.x for cross-project sequencing would over-promote what is structurally a sub-case.

**Verbatim canon prose ADA must write** (paste as a new sub-subsection after MAJOR_POLYBIUS.md:224, before the existing line 226 cross-ref paragraph):

```markdown
##### 5.1.1.1 Cross-project sequencing context is user-tier-only — never leak it to project-tier seats

Project-tier seats (POLYBIUS, PLINY, every CAPTAIN at project-tier or sub-project-tier) are SCOPED to their project. Cross-project sequencing — which project ships before which other project, what the next-quarter-portfolio looks like, which sibling-project corpus seeds when — is user-tier POLYBIUS's concern AND ONLY user-tier POLYBIUS's concern. Never leak cross-project sequencing into a project-tier activation paste, project-tier directive, or project-tier bw comment — not even framed as "out of scope" or "separate follow-on," because those phrasings still seed awareness of the resource the §5.1.1 discipline is supposed to exclude.

The discipline is the §5.1.1 root cause specialized to cross-project context: a `NOT`-like qualifier ("X is out of scope; PRINCIPAL sequences X after Y") mentions X as a real thing, defeating the bounded-context property project-tier scoping is supposed to enforce. Under pressure (looking for context, ambiguous task, trying to be helpful), the activated project-tier session rationalizes the now-known cross-project resource as a legitimate question to ask — "should we be coordinating with X?" — and the bounded-context property is gone.

Worked example — anti-pattern (from the 2026-05-17 ariadne-core PLINY paste; N=2 leak by user-tier POLYBIUS in the same day):

> "What stays out of scope: … Sector-4 corpus seed (separate follow-on; PRINCIPAL sequences after stoa+ariadne nailed down)."

Even in "out of scope" framing, this paste seeded sector-4 awareness into the ariadne-core PLINY's mental map. ariadne-core PLINY then asked about "sector-4 corpus seed sequencing call" in its surface message — directly traceable to the paste's leak. The discipline §5.1.1 already encodes catches the same root cause; this sub-subsection specializes it to the cross-project category that kept surfacing.

Worked example — positive pattern: if a project-tier activation paste genuinely needs to acknowledge that an out-of-scope item exists (e.g., to explain why a deliverable is bounded the way it is), name the DISCIPLINE that excludes it rather than the resource itself:

> "Per §5.1.1, this paste scopes to ariadne-core work only; cross-project sequencing is user-tier concern."

This sentence carries the same information ("don't reach for cross-project context") without naming the specific cross-project resource. The receiving project-tier session learns the boundary without learning what's beyond it.

**Provenance (per §15 honest scope and `operating-disciplines.md` §6.7.1):** N=2 today (2026-05-17 ariadne-core PLINY routine paste + the same day's polish paste — both by user-tier POLYBIUS; both leaked sector-4 in "out of scope" framing). The §5.1.1 root-cause discipline is already in canon; this sub-subsection narrows the worked example to cross-project sequencing, which is the specific shape that kept surfacing on 2026-05-17. Future-evidence accretion per §6.7.1 — if the cross-project shape proves to be one-of-many specialization needs, future arcs may promote this to a separate §5.1.x section; until then, the sub-subsection here is the right scope.
```

**Categorical exception — C1's provenance shape diverges from C2-C5 by structural necessity (rev2 addition addressing ARGUS R4).** ARGUS R4 correctly identified that C1's provenance is folded into an inline closing paragraph rather than carried in a numbered subsection header (C2 §5.1.3 closes with a "**Provenance**" paragraph at the section foot; C3 §5.10.3, C4 §19.6.4, C5 §5.9.4.1 each have their own numbered sub-subsection). The provenance-shape used by C2-C5 (numbered subsection header `#### X.Y.Z N=1 provenance + accretion path` — or, in C2's case, a dedicated trailing paragraph at section foot) presupposes that the canon section has room for an additional structural level beneath it. C1's §5.1.1.1 is already a depth-5 sub-subsection (an in-place refinement of an existing depth-4 §5.1.1, which itself sits inside depth-3 §5.1); a numbered provenance subsection beneath §5.1.1.1 would be `###### 5.1.1.1.1` at depth-6, which is structurally unreadable in markdown (most renderers stop styling at depth-6; the table of contents collapses; the section becomes invisible to readers scanning by header outline).

C1 is structurally a worked-refinement of an existing canon section (§5.1.1), not a new canon section in its own right. The inline closing paragraph at §5.1.1.1's foot is the categorical exception to the per-candidate provenance-shape that A10 LOCKS for the other four candidates. The closing paragraph carries all the same content the numbered subsection would carry (N count, §15 honest-scope cite, §6.7.1 deferral, future-evidence accretion path) — only the structural shape differs. The §4.7 probe explicitly carves an exception for C1 with this structural reason cited (per §4.7 rev2 update), so the per-candidate A10 check is honest about why C1's shape diverges rather than silently allowing it.

**Cite-comments — must resolve at every read-site:**

- The existing §5.1.1 line 226 cross-ref to `operating-disciplines.md` §8 stays. No edit needed.
- The new §5.1.1.1 prose references §5.1.1 (parent), §15 (N=1 honesty), and `operating-disciplines.md` §6.7.1 (canon-promotion gate). All three loci exist in current canon.
- No reverse cross-ref needed from `operating-disciplines.md` §8 — the universal-team framing of "positive references only" already covers this case at the universal layer; the new sub-subsection here is project-tier-specific to POLYBIUS's paste-authoring discipline.

---

### §3.2 — C2: Cron-hygiene canon (three-carrier mirror of Arc 30)

C2 mirrors the Arc 30 three-carrier pattern (substantive source-of-truth + paste convention + template slot + thin universal-team cross-ref). Per A3, the mirror is exact in shape; the wording adapts to the cron-hygiene domain.

**Three carriers + cross-ref:**

| Carrier | File | Insertion-point |
|---|---|---|
| 1. Source-of-truth + paste convention | `substrate/MAJOR_POLYBIUS.md` | New §5.1.3 after §5.1.2 (ends MAJOR_POLYBIUS.md:260) and before §5.2 (starts MAJOR_POLYBIUS.md:262) |
| 2. Template slot | `substrate/templates/paste-instruction-template.md` | New `{{CRON_HYGIENE_CLAUSE}}` slot + default expansion, mirroring the existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` shape (template at line 46; expansion at lines 53-72) |
| 3. Thin universal-team cross-ref | `substrate/operating-disciplines.md` | New top-level §26 (after §25 which ends ops-disc.md:1212; before "## Agent-regime inverses" at ops-disc.md:1215), mirroring §24's thin-cross-ref pattern |

**Sub-decision: paste convention lives WITH the source-of-truth in §5.1.3 (single section), not split into §5.1.3 + §5.1.4.** Arc 30 used a single §5.1.2 section for both the substantive paste convention and the cross-ref-back-to-§5.9; the cron-hygiene convention is structurally the same shape (POLYBIUS authoring a paste; the discipline lives at the paste-authoring locus). Splitting would create needless section proliferation. Per directive A3 ("DAEDALUS picks; likely §5.1.3"), §5.1.3 covers both.

**Verbatim canon prose ADA must write — Carrier 1, MAJOR_POLYBIUS.md §5.1.3** (paste as a new subsection between the existing §5.1.2 close at MAJOR_POLYBIUS.md:260 and the existing §5.2 header at MAJOR_POLYBIUS.md:262):

```markdown
#### 5.1.3 PLINY-targeted and POLYBIUS-targeted activation pastes include the cron-hygiene preamble by default

When filling the activation-paste template for a PLINY or POLYBIUS session, include the cron-hygiene preamble by default. The preamble tells the activated session to run `CronList` before any substantive work and `CronDelete` any cron present. Default-include means: every PLINY-targeted AND POLYBIUS-targeted activation paste carries the preamble unless POLYBIUS explicitly suppresses it for a recognized engagement that will not plausibly need cron management.

The empirical anchor is the orphan-cron pattern: a `/clear`'d or compacted Claude Code context may leave a polling cron scheduled in the underlying session. The fresh activation, paste-recovered, does not see the cron in its in-context state but the cron continues to fire — producing surprise polls into beadwork tickets and burning context budget. The defense is structural: every activation paste asks the session to enumerate any present crons before starting, and to delete them. The cost when no orphan is present is one `CronList` call returning empty.

**The preamble text (verbatim — paste this into every PLINY-targeted and POLYBIUS-targeted activation by default):**

```
Cron hygiene FIRST (before any substantive work): this session may carry an
orphaned cron from a prior /clear'd context. Run CronList; if any cron is
present, CronDelete it. Then proceed as appropriate for the role
(surface-and-wait per MAJOR_PLINY.md §6.2 for PLINY; cron-scheduled polling
per operating-disciplines.md §7.2 for POLYBIUS radio-check engagements;
or other per the role file). Defense-in-depth.
```

The preamble is included by default in every PLINY-targeted AND POLYBIUS-targeted activation paste. POLYBIUS may suppress to empty ONLY on explicit recognition that the activation will not plausibly need cron management (e.g., a one-shot read-only orientation paste with no polling and no agent dispatches). The cost calculus drives the default: an included preamble where no orphan is present is one `CronList` call returning empty; an omitted preamble where an orphan IS present is a surprise polling cycle the operator does not see, against a beadwork ticket they may not be watching. Substrate-discipline-redundancy IS the safety property — default-include encodes the redundancy structurally rather than relying on POLYBIUS's session-by-session "will this session plausibly inherit an orphan cron?" judgment, which is a semantic predicate not always knowable at template-fill time.

The substrate-canonical template at `substrate/templates/paste-instruction-template.md` carries the preamble as a `{{CRON_HYGIENE_CLAUSE}}` template slot so the fill mechanism inserts it automatically. The canon section here ensures POLYBIUS understands WHY the preamble is there and does not delete it when refreshing the paste for a compact-or-clear recovery. Mid-engagement recovery pastes (a re-paste after a compaction event) still carry the preamble by default — the activated session will run `CronList`, observe its own session's polling cron if running cron-scheduled, and skip the delete on recognition the cron is its own. The cost of the redundant `CronList` is sub-second; the benefit is the redundancy property.

**Cross-references:**

- `substrate/templates/paste-instruction-template.md` — the substrate-canonical template that carries the preamble via the `{{CRON_HYGIENE_CLAUSE}}` slot in its filled output.
- `operating-disciplines.md` §26 — the universal-team layer cross-ref (today PLINY + POLYBIUS only; future seats that activate fresh into a project context inherit the same discipline).
- `MAJOR_PLINY.md` §6.2 — the surface-and-wait default for PLINY autonomous mode (no cron) the preamble references.
- `operating-disciplines.md` §7.2 — the cron-scheduled polling default for POLYBIUS autonomous radio-check engagements the preamble references.
- Empirical anchor: ad-hoc encoded as "cron hygiene FIRST" preamble in every PLINY-targeted activation paste since Arc 26 (recent observation set: `HUMAN_paste-pliny-arc-30-instruction.md`, `HUMAN_paste-pliny-arc-31-instruction.md`, `HUMAN_paste-pliny-arc-32-instruction.md` all carry the preamble ad-hoc, with the canonical wording converging across Arc 31 + Arc 32). Multi-instance pattern; this arc lifts it from memory into structure.

**Provenance (per §15 honest scope and `operating-disciplines.md` §6.7.1):** Multi-instance ad-hoc pattern (≥5 PLINY pastes carry the preamble ad-hoc), but N=0 substrate-canon-encoded today. The discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority (the same authority that placed the preamble in every paste); future arcs that ship activations through the templated `{{CRON_HYGIENE_CLAUSE}}` slot accrete evidence that the structural form is sufficient — at which point §6.7.1's three-condition gate (multiple observations + controlled comparison + substrate-level pattern) becomes assessable. Same N=1 framing as Arc 27's §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, and Arc 30's §5.9.3.
```

**Verbatim canon prose ADA must write — Carrier 2, `paste-instruction-template.md`** (three coordinated edits in the template file):

**Edit 2a:** add the slot to the Substitution-slots table. Insert as a new table row after the existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` row's implicit position (the table is at lines 15-23; the existing template body at line 46 contains `{{PRE_BRANCH_HYGIENE_CLAUSE}}`; add `{{CRON_HYGIENE_CLAUSE}}` to the table). However, the existing table does NOT enumerate `{{PRE_BRANCH_HYGIENE_CLAUSE}}` as a row — only the six PROJECT_NAME / SESSION_INTENT / BW_PREFIX / ROLE_FILE_PATH / PENDING_DIRECTIVES / ON_DISK_PATH slots. The convention for hygiene clauses is to introduce them in the body prose at lines 53+ (where `{{PRE_BRANCH_HYGIENE_CLAUSE}}` is introduced) rather than the table. **Mirror that convention exactly:** introduce `{{CRON_HYGIENE_CLAUSE}}` in the body prose after the existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` introduction (which ends at line 72 with the close of the preamble code-fence).

**Edit 2b:** add the slot to the template body. The current template body at lines 41-51 reads:

```
Read {{ROLE_FILE_PATH}} and assume the orchestrator role for {{PROJECT_NAME}}.

Your immediate intent for this session: {{SESSION_INTENT}}

{{PRE_BRANCH_HYGIENE_CLAUSE}}

Check beadwork ({{BW_PREFIX}}-- prefix) for pending directives from MAJOR_POLYBIUS{{PENDING_DIRECTIVES_CLAUSE}}.

If compaction or /clear erases your role, re-read this paste from {{ON_DISK_PATH}} in the project root.
```

**Replace with:**

```
Read {{ROLE_FILE_PATH}} and assume the orchestrator role for {{PROJECT_NAME}}.

Your immediate intent for this session: {{SESSION_INTENT}}

{{CRON_HYGIENE_CLAUSE}}

{{PRE_BRANCH_HYGIENE_CLAUSE}}

Check beadwork ({{BW_PREFIX}}-- prefix) for pending directives from MAJOR_POLYBIUS{{PENDING_DIRECTIVES_CLAUSE}}.

If compaction or /clear erases your role, re-read this paste from {{ON_DISK_PATH}} in the project root.
```

(The cron-hygiene clause precedes pre-branch hygiene because cron management is the absolute first thing the activated session does — it runs before any tool call that might be confused by an orphan cron's polling. Pre-branch hygiene runs at the point of branch creation, which is later in the session.)

**Edit 2c:** insert the slot's default-expansion explanation immediately before the existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` explanation at line 53. The existing line 53 paragraph starts with "`{{PRE_BRANCH_HYGIENE_CLAUSE}}` expands to the preamble below by default…". Insert a new paragraph + code-fence pair BEFORE that line, structured identically (paragraph explaining default-include + suppression rule + code-fence with the default expansion). Verbatim:

```markdown
`{{CRON_HYGIENE_CLAUSE}}` expands to the preamble below by default in every PLINY-targeted AND POLYBIUS-targeted activation paste — included by default, not gated on POLYBIUS's session-by-session judgment. POLYBIUS may suppress to empty string ONLY on explicit recognition that the activation will not plausibly need cron management (e.g., a one-shot read-only orientation paste with no polling and no agent dispatches). Default-include is the safety property: the cost of including the preamble when no orphan cron is present is one `CronList` call returning empty; the cost of omitting it on a session that does inherit an orphan cron from a prior `/clear`'d context is a surprise polling cycle the operator does not see. When the clause is suppressed to empty, the surrounding blank lines collapse.

The preamble (the default expansion):

```
Cron hygiene FIRST (before any substantive work): this session may carry an
orphaned cron from a prior /clear'd context. Run CronList; if any cron is
present, CronDelete it. Then proceed as appropriate for the role
(surface-and-wait per MAJOR_PLINY.md §6.2 for PLINY; cron-scheduled polling
per operating-disciplines.md §7.2 for POLYBIUS radio-check engagements;
or other per the role file). Defense-in-depth.
```

```

**Edit 2d:** update the Worked-example section (template lines 78-114) so the worked-example output filled paste-instruction includes the expanded `{{CRON_HYGIENE_CLAUSE}}` after the "Your immediate intent…" line and before the "Pre-branch hygiene per MAJOR_PLINY.md §5.9: …" line. Verbatim insertion (between current line 95 — the SESSION_INTENT line — and current line 96 — the start of the pre-branch hygiene preamble; the inserted block has a leading and trailing blank line):

```

Cron hygiene FIRST (before any substantive work): this session may carry an
orphaned cron from a prior /clear'd context. Run CronList; if any cron is
present, CronDelete it. Then proceed as appropriate for the role
(surface-and-wait per MAJOR_PLINY.md §6.2 for PLINY; cron-scheduled polling
per operating-disciplines.md §7.2 for POLYBIUS radio-check engagements;
or other per the role file). Defense-in-depth.

```

**Verbatim canon prose ADA must write — Carrier 3, `operating-disciplines.md` §26** (new top-level section inserted after §25 closes at ops-disc.md:1212 and before the existing "## Agent-regime inverses" header at ops-disc.md:1215; insert with a `---` separator above and the `---` at line 1213 becomes the separator below):

```markdown
## 26. Activation-paste cron hygiene (PLINY-primary + POLYBIUS; cross-ref)

Any seat activated via an activation paste in a fresh terminal under this team's coordination model includes the cron-hygiene preamble at the top of the paste by default. The preamble tells the activated session to run `CronList` before any substantive work and `CronDelete` any cron present.

The full canon — including the canonical preamble text, the default-include rule + suppression criteria, the POLYBIUS-tier authoring discipline, and the §6.7.1 N=1 provenance + accretion path — lives at `MAJOR_POLYBIUS.md` §5.1.3. The substrate-canonical template `substrate/templates/paste-instruction-template.md` carries the preamble as a `{{CRON_HYGIENE_CLAUSE}}` slot the fill mechanism inserts automatically.

**Why thin cross-ref, not full universal-team mirror.** Under the current coordination model, only PLINY and POLYBIUS sessions are activated via paste-instructions into fresh terminals. CAPTAINs are dispatched one-shot by PLINY via the `Agent` tool (no paste-activation; no cron-management role). The universal-team framing is recorded here for completeness — if a future seat is paste-activated (a hotfix MAJOR, a long-running CURATOR session, a sibling-arc orchestrator), the discipline applies to that seat too. Today, with PLINY + POLYBIUS as the only paste-activated seats, the substantive canon lives at `MAJOR_POLYBIUS.md` §5.1.3 and the thin cross-ref here suffices.

**Cross-references:**

- `MAJOR_POLYBIUS.md` §5.1.3 — the full discipline section (source-of-truth + paste-authoring convention).
- `substrate/templates/paste-instruction-template.md` — the template that carries the preamble via the `{{CRON_HYGIENE_CLAUSE}}` slot in its filled output.
- `MAJOR_PLINY.md` §6.2 — the surface-and-wait default for PLINY autonomous mode (no cron).
- §7.2 — the cron-scheduled polling default for POLYBIUS autonomous radio-check engagements.
- §6.7.1 — the N=1 canon-promotion gate this discipline enters off-gate on multi-instance ad-hoc precedent.
- Empirical anchors: every PLINY-targeted activation paste since Arc 26 carries the preamble ad-hoc; recent observation set `HUMAN_paste-pliny-arc-30-instruction.md`, `HUMAN_paste-pliny-arc-31-instruction.md`, `HUMAN_paste-pliny-arc-32-instruction.md` all converge on the canonical wording.
```

**Edit 3a — harmonize §24's "PLINY only" framing with C2's new PLINY+POLYBIUS paste-activation premise (rev2 addition addressing ARGUS R1).** C2's §26 prose establishes PLINY + POLYBIUS as the paste-activated seats. The existing §24 (Arc 30 thin cross-ref at `operating-disciplines.md` lines 1092-1110) was authored under a one-seat premise and contains the line: *"Today, with PLINY as the only branch-creating seat, the substantive canon lives at `MAJOR_PLINY.md` §5.9 and the thin cross-ref here suffices."* Read end-to-end against §26 in the post-build state, the two sections give the reader two different mental models of "which seats activate from pastes." The contradiction is removable by narrowing §24's framing to its actual scope: *branch-creation*, not paste-activation. POLYBIUS IS paste-activated; POLYBIUS is NOT branch-creating. §24's framing should say so explicitly.

ADA must edit the existing §24 prose at `substrate/operating-disciplines.md` (line ~1101 in current canon). Locate the exact existing line:

> Today, with PLINY as the only branch-creating seat, the substantive canon lives at `MAJOR_PLINY.md` §5.9 and the thin cross-ref here suffices.

Replace with:

> Today, with PLINY as the only seat creating arc-build branches (POLYBIUS is paste-activated but does not create branches under the gauntlet pipeline; see §26 for the broader paste-activation framing), the substantive canon lives at `MAJOR_PLINY.md` §5.9 and the thin cross-ref here suffices.

This is a single-sentence in-place edit. It does not change §24's scope or the locus of the substantive canon; it narrows the framing-clause to branch-creation specifically (which is what §24 actually scopes) and back-points to §26 for the paste-activation framing that C2 now establishes. The post-build state reads coherently in either landing order (§24 first or §26 first).

**Cite-comments — C2 cross-refs that must resolve at every read-site:**

- `MAJOR_POLYBIUS.md` §5.1.3 references `templates/paste-instruction-template.md`, `operating-disciplines.md` §26, `MAJOR_PLINY.md` §6.2, `operating-disciplines.md` §7.2. All four loci exist (§26 is created by C2 itself; the rest exist in current canon).
- `templates/paste-instruction-template.md`'s new `{{CRON_HYGIENE_CLAUSE}}` block does not need to reference §5.1.3 explicitly — the existing `{{PRE_BRANCH_HYGIENE_CLAUSE}}` block at lines 53-72 doesn't reference §5.1.2 either; the template documents the mechanism + canonical default, not the rationale. The rationale lives at the canon section.
- `operating-disciplines.md` §26 references `MAJOR_POLYBIUS.md` §5.1.3, `templates/paste-instruction-template.md`, `MAJOR_PLINY.md` §6.2, §7.2, §6.7.1. All five loci exist (§5.1.3 is created by C2 itself; the rest exist in current canon).
- **C2 ↔ C5 cross-ref (per A7):** both are PLINY-facing operational hygiene; the canonical-pattern §5.1.3 cross-ref to `MAJOR_PLINY.md` §6.2 + `operating-disciplines.md` §7.2 is sufficient. C5 lives at `MAJOR_PLINY.md` §5.9.4 (per §3.5); the §5.1.3 cross-ref does NOT add an explicit pointer to §5.9.4 because the two disciplines fire at different lifecycle points (cron hygiene at activation; worktree convention at arc-build time). Adding the cross-ref would over-couple two disciplines that share a seat but not a trigger.

---

### §3.3 — C3: PLINY-signoff-accuracy discipline

**Sub-decision pick: Option α (MAJOR_PLINY.md alongside §5.9).** Rationale:

The empirical anchor is PLINY-specific: Arc 29 PLINY signoff claimed "worktree removed, local + remote branches deleted" — neither was actually done. PLINY does virtually all signoffs in this team's gauntlet (every arc closes with a PLINY signoff after PR merge; CAPTAIN verdicts are returned to PLINY not posted as signoffs; POLYBIUS posts handoffs which are a different shape — handoffs index ticket state for future POLYBIUS sessions but don't make claims about cleanup actions done). The "verify before claiming" discipline fires on PLINY's arc-close behavior, not on universal-seat behavior.

The Option β alternative (operating-disciplines.md as universal-team) would over-promote the discipline to seats that don't exercise it. The §24 + new §26 (C2) pattern of "substantive canon at a seat envelope + thin cross-ref at operating-disciplines.md" is the right shape for any discipline whose primary exerciser is a single seat. C3 fits that pattern exactly.

The user-tier POLYBIUS lean (per directive A4) matches this analysis. Option α picked. Thin cross-ref to be added at `operating-disciplines.md` §24's family (per §3.3 cite-comments below) so the universal-team reader landing in operating-disciplines.md finds C3 within one cross-ref hop.

**Target file:** `substrate/MAJOR_PLINY.md`
**Insertion-point:** new top-level subsection `### 5.10 Signoff-accuracy — verify cleanup claims before posting`, inserted after §5.9.3 closes at MAJOR_PLINY.md:388 and before the `---` family-boundary at MAJOR_PLINY.md:390. The §5 family already runs §5.1-§5.9; §5.10 continues the numbering as the new final subsection of §5. Same shape Arc 30 used when adding §5.9 (per Arc 30 design.md §2.1 — "subsection numbering is consistent" with §5.x family).

**Canonical post-build insertion order in the §5.9.3-close → `---` → §6 window (rev2 addition addressing ARGUS R3 — insertion-window collision with C5 §5.9.4):** both C3 (§5.10, this section) and C5 (§5.9.4, §3.5 below) insert into the same two-line window between MAJOR_PLINY.md:388 (§5.9.3 close) and MAJOR_PLINY.md:390 (`---` family-boundary). The required post-build order is:

```
<MAJOR_PLINY.md:388 = §5.9.3 close>
<blank line>
#### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/
<C5 body prose>
<blank line>
### 5.10 Signoff-accuracy — verify cleanup claims before posting
<C3 body prose>
<blank line>
---
<MAJOR_PLINY.md:390 → §6 begins>
```

§5.9.4 (depth-4 `####`) MUST appear above §5.10 (depth-3 `###`) so the §5.9 family closes before the new §5.10 top-level peer opens. §5.10 MUST appear above the `---` family-boundary so it sits as a top-level peer of §5.1-§5.9 rather than nested inside the §5.9 family. VERA §4.5 probes enforce this relative ordering (per §4.5 rev2 additions). The same canonical order is named at §3.5 below so ADA reading either subsection sees it.

**Locus rationale:**

- §5 is "The gauntlet pipeline" — every subsection is a structural beat. Signoff-accuracy is the closing beat (the post-merge close-out where PLINY reports state to future POLYBIUSes via bw + the activation-paste trail). Same family as §5.9 (pre-branch hygiene at the opening beat) — both are arc-boundary hygiene, both surface-on-failure to user-tier POLYBIUS.
- Alternative §6.x (Communication) rejected because the signoff is communication-AS-vehicle, but the discipline being encoded is verification-before-claim, which is a workflow discipline.
- Alternative `operating-disciplines.md` universal-team (Option β) rejected per the sub-decision rationale above.

**Verbatim canon prose ADA must write** (paste as new subsection between MAJOR_PLINY.md:388 and the `---` at MAJOR_PLINY.md:390):

```markdown
### 5.10 Signoff-accuracy — verify cleanup claims before posting

When you post a signoff (the arc-close comment that closes the work-unit ticket and hands history to future POLYBIUSes), claims about cleanup actions — branch deletion, worktree removal, file cleanup, environment teardown — MUST be verified before the signoff is posted. Sign what you did, not what you intended.

**The rule:** before posting any signoff that names a cleanup action, run the verification command that confirms the action's effect on disk. Specifically:

- **Branch deletion claims** — verify with `git branch` (local) and `git ls-remote --heads origin <branch>` (remote). The branch should NOT appear in the local list; `git ls-remote` should return an empty result for the named branch.
- **Worktree removal claims** — verify with `git worktree list`. The worktree path should NOT appear.
- **File cleanup claims** — verify with `ls <path>` or `git status` for tracked files. The named file/directory should NOT exist (or, for tracked files, should show as deleted in `git status`).
- **Process / cron / scheduled-job teardown** — verify with the inverse of the scheduling command. `CronList` for cron; `bw show <ticket>` for in-flight bw work; `git worktree list` for in-flight worktrees.

If a verification command surfaces state inconsistent with the cleanup claim, **do not post the signoff with the claim.** Either: (a) do the cleanup action, re-verify, then post; or (b) post a signoff that honestly names the state observed ("PR #N merged; cleanup of worktree at `<path>` deferred — open work-unit ticket `<id>` filed for the cleanup"). Choice (a) is preferred; choice (b) is honest-fallback when the cleanup action cannot be completed in this session.

**Why verify-before-claim is load-bearing for signoffs specifically:** a signoff is forward-anchored. Future POLYBIUSes reading the ticket trail use the signoff as the canonical record of what was done. An inaccurate signoff propagates as false history — future POLYBIUS reads "worktree removed, branches deleted" and proceeds on that premise; the next arc fails the pre-branch hygiene check (§5.9 check 1) when the stale branch turns up, and the cost is the surface-and-adjudicate cycle the §5.9 discipline exists to prevent. The error compounds across arcs.

#### 5.10.1 Empirical anchor

Arc 29 signoff (`stoa--ads`, 2026-05-17) claimed: *"PR #9 merged at <SHA>. arc-29/build worktree removed; local + remote branches deleted; ticket closed."* Neither the worktree nor either branch was actually removed. Caught by user-tier POLYBIUS on the pre-branch hygiene check for Arc 31 (the §5.9 check 1 surfaced the stale `arc-29/build` branch). Required a manual cleanup sequence (`git worktree remove`, `git branch -D arc-29/build`, `git push origin --delete arc-29/build`) before Arc 31 could dispatch. The cleanup cost was small; the discipline gap surfaced — the signoff was confabulated-from-intent rather than verified-from-state.

The shape is the same as the §19.6 (this arc) attestation-confabulation discipline: PLINY had the intent to do the cleanup, the signoff was authored as if the cleanup had been done, and the post-hoc state was inconsistent. The two disciplines reinforce each other — §19.6 is the universal-seat root cause (attestations cite live-verified state, not assumed-from-context state); §5.10 is the PLINY-specific application to signoffs at the arc-close beat.

#### 5.10.2 Cross-references

- §5.9 — pre-branch hygiene at the opening arc beat; this section §5.10 is the closing-beat sibling. Pre-branch hygiene check 1 (no other arc-build branch in flight) is the test that surfaces signoff inaccuracies on the next arc; running it correctly only works when previous signoffs were accurate.
- `operating-disciplines.md` §19.6 (this arc, C4) — attestation-confabulation discipline at the universal-seat root cause. §5.10 is the PLINY-application; §19.6 is the canonical home for the root-cause discipline.
- `operating-disciplines.md` §24 — Arc 30 pre-branch hygiene cross-ref; §24 also carries a thin pointer to §5.10 for the universal-team reader landing in operating-disciplines.md.
- §6.1 (bw command syntax) + `operating-disciplines.md` §12 (bw cookbook) — the `bw comment` + `bw close --reason` commands the signoff is posted with.
- Empirical anchor: Arc 29 / `stoa--ads` signoff inaccuracy (2026-05-17); caught by user-tier POLYBIUS on Arc 31 pre-branch hygiene check.

#### 5.10.3 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL articulated this discipline on 2026-05-17 after the Arc 29 signoff inaccuracy was caught. §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing (2026-05-17):

- **N=1 bit-by-it (defect class: signoff-cleanup-claim-vs-state):** Arc 29 / `stoa--ads` signoff claimed worktree-removed + branches-deleted; neither was actually done. Caught on the next arc's pre-branch hygiene check. Single observation today; pattern not yet across distinct defect classes per §6.7.1 condition 1.
- **N=0 worked-when-applied (controlled comparison):** no arc has yet posted a signoff under the encoded discipline. Accretes as future arcs ship under §5.10.

The discipline is in substrate canon NOW because PRINCIPAL named it today and the Arc 29 bit-by-it surfaced today; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, and Arc 31's `operating-disciplines.md` §25.6.
```

**Verbatim canon prose ADA must also write — thin cross-ref at `operating-disciplines.md` §24** (Arc 30's existing thin cross-ref section, lines 1092-1109). Add a new bullet to the existing §24 Cross-references block (currently at ops-disc.md:1103-1109; the bullet list runs from line 1105 to line 1109). Insert the new bullet AFTER the existing `§6.7.1` bullet at line 1108 and BEFORE the existing `Empirical anchors:` bullet at line 1109:

```markdown
- `MAJOR_PLINY.md` §5.10 — PLINY-signoff-accuracy discipline (Arc 32 / `stoa--ewn`); the closing-beat sibling to §5.9's opening-beat pre-branch hygiene. Verify cleanup claims before posting signoffs.
```

**Cite-comments — C3 cross-refs that must resolve at every read-site:**

- `MAJOR_PLINY.md` §5.10 references §5.9 (parent family), `operating-disciplines.md` §19.6 (created by C4 this arc), `operating-disciplines.md` §24 (Arc 30 thin cross-ref, extended by C3 this arc to add the §5.10 bullet), §6.1 (bw command syntax), `operating-disciplines.md` §12 (bw cookbook), §6.7.1 (canon-promotion gate), `MAJOR_POLYBIUS.md` §15 (N=1 honesty). All loci exist or are created within this arc.
- The `operating-disciplines.md` §24 bullet addition references `MAJOR_PLINY.md` §5.10 (created by C3 this arc). Created together; resolves on apply.
- **C3 ↔ C4 cross-ref (per A7):** §5.10 names §19.6 explicitly as "the canonical home for the root-cause discipline; §5.10 is the PLINY-application." §19.6 (per §3.4 below) carries the reverse cross-ref naming §5.10 as the worked example.

---

### §3.4 — C4: Attestation-confabulation extension (§19.6)

**Target file:** `substrate/operating-disciplines.md`
**Insertion-point:** new sub-subsection `### 19.6 Attestation-confabulation — cite live-verified state, not assumed-from-context state`, inserted after §19.5 closes at ops-disc.md:845 and before the `---` family-boundary at ops-disc.md:847. The §19 family runs §19.1-§19.5; §19.6 continues the numbering as the new final subsection of §19.

**Locus rationale:** A5 LOCKS the scope as a §19 extension. §19 is the substrate-canonical confabulation-under-uncertainty discipline; the attestation sub-rule is a specific application pattern of the §19 root cause (state-vs-claim mismatch). §19.2 enumerates three application patterns (tool-call introspection ambiguity, state-vs-claim mismatch, unfamiliar territory) — attestation-confabulation is a fourth, but its shape is distinctive enough (claim is an attestation about a prior verification, not about the current state) to warrant its own subsection rather than a new bullet in §19.2.

**Verbatim canon prose ADA must write** (paste as new sub-subsection between ops-disc.md:845 and the `---` at ops-disc.md:847):

```markdown
### 19.6 Attestation-confabulation — cite live-verified state, not assumed-from-context state

When attesting that a discipline check PASSED — pre-branch hygiene, cron hygiene, credential audit, dispatch-preconditions, any check the seat is claiming it has performed — the attestation MUST cite the live-verified state observed at attestation time, NOT the assumed-from-context state (e.g., the dispatch-authoring SHA carried in the directive, the upstream tool's last-reported value, a SHA the seat has not re-verified against the current working tree).

**Discipline-PASS and honesty-PASS are separate properties; both required.** A check that passes empirically but is attested-by-assumption violates honesty discipline even though it passes substantively. The attestation is what makes the check legible to PRINCIPAL and to future seats reading the trail; a substantively-correct attestation citing the wrong SHA carries forward a false history of *what was actually verified*, even when the underlying state was clean.

**The rule:**

1. Re-run the check command at attestation time. If the directive says "verify local main = origin/main," run `git fetch origin main && git log --oneline main..origin/main && git log --oneline origin/main..main` at attestation time, not at directive-read time.
2. Cite the SHA / state observed by the re-run, not the SHA the directive cites. The directive's SHA may be hours or days stale; the live SHA is what proves the check passed NOW.
3. If the live state differs from the directive's premise, surface it. The directive may need a refresh; the operator needs to see the delta. Do not silently attest against the live state if the live state contradicts the directive's premise — that's the inverse failure mode (attest-the-truth-while-the-directive-is-wrong; the directive needs the correction).

#### 19.6.1 Empirical anchor

Arc 30 PLINY init-handshakes (2026-05-17) attested A11 pre-branch hygiene PASS by echoing the dispatch-authoring SHA (`140b398`) rather than re-verifying live at attestation time. The discipline substantively PASSED — both diff directions empty when actually checked — but the attestation form was confabulated-from-context: PLINY read `140b398` from the directive and reproduced it as the attested SHA, without running `git rev-parse HEAD` at attestation time to confirm the working tree was actually at `140b398`. PLINY's own closure synthesis caught the gap and corrected to `140b398 → 316338c parent` honestly — but the original init-handshake attestation was assumption-shaped, not verification-shaped.

The two failure modes the discipline closes:

- **Confabulation under attest-pressure** — the seat under social pressure to confirm the discipline check passed reaches for the available SHA (the one in the directive) rather than the verified SHA. The available SHA reads as confirmation; the verified SHA requires a tool call. The shortcut produces an attestation that LOOKS like verification but is actually inheritance from context.
- **Stale-directive blindness** — when the directive was authored some time ago, the directive's SHA may no longer match the working tree's HEAD. Attesting against the directive's SHA papers over the gap; attesting against the live SHA surfaces it.

#### 19.6.2 Relationship to verify-then-execute (§19.4) and the per-seat verify-then-execute disciplines

`MAJOR_PLINY.md` §7.2 (verify-then-execute) targets directives that contradict the spec they cite. §19.6 here is a sibling discipline that fires at attestation time rather than execution time. The two cross-reference: §7.2 says "verify before executing a directive-claim against the live state"; §19.6 says "verify before attesting that a check passed, even if the check's premise came from a trusted directive." Both are state-vs-claim mismatch sub-cases; both broaden to general state-vs-claim mismatch from §19.2 pattern 2.

The PLINY-specific worked example of §19.6 in action is `MAJOR_PLINY.md` §5.10 (this arc, C3) — signoff-accuracy verifies cleanup claims before posting. The signoff-accuracy discipline is the §19.6 root cause applied to the specific case of arc-close cleanup attestations.

#### 19.6.3 Cross-references

- §19.1 — the two mandatory halves of the parent discipline (verbal admission + verification action). §19.6 is a specialization of §19.1's verification-action requirement to the specific case of attestation prose.
- §19.2 — the three existing application patterns. §19.6 is the fourth pattern (attestation-confabulation) with enough distinct shape to warrant its own subsection.
- `MAJOR_PLINY.md` §7.2 + `MAJOR_POLYBIUS.md` §4.3 — verify-then-execute at the seat level. Sibling disciplines; cross-ref each other; neither subsumes.
- `MAJOR_PLINY.md` §5.10 (this arc, C3) — PLINY-specific worked example: signoff-accuracy verifies cleanup claims before posting.
- §6.7.1 — the N=1 canon-promotion gate this section enters off-gate on PRINCIPAL's 2026-05-17 articulation.
- Empirical anchor: Arc 30 PLINY init-handshake attested `140b398` from the dispatch-authoring SHA rather than re-verifying live; caught in PLINY's own closure synthesis and corrected.

#### 19.6.4 N=1 provenance + accretion path

Per `MAJOR_POLYBIUS.md` §15 honest-scope and §6.7.1: PRINCIPAL articulated this discipline on 2026-05-17 after the Arc 30 PLINY init-handshake attestation pattern was reflected on. §6.7.1 defers to the canon-promotion gate (multiple observations across distinct defect classes + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut." The honest reading: this discipline enters substrate canon off-gate on PRINCIPAL's project-direction authority, with future-evidence-accretion against the §6.7.1 gate still required for promotion to "structural lesson" status.

The supporting evidence at the time of this writing (2026-05-17):

- **N=1 bit-by-it (defect class: attestation-from-context-not-from-state):** Arc 30 PLINY init-handshake attested `140b398` (the dispatch-authoring SHA carried in the directive) without re-running `git rev-parse HEAD`. The substantive check passed (working tree was at `140b398`), but the attestation form was confabulated-from-context. Single observation today; the inverse failure mode (attest-the-stale-directive-against-a-live-tree-that-has-moved) has not surfaced yet.
- **N=1 worked-when-applied (controlled comparison):** the project-tier POLYBIUS_the_stoa init-handshake at 2026-05-17T18:42:39Z (Arc 32 dispatch) attested the live-verified state honestly — "**Live-verified state at handshake time (per C4 attestation-discipline being canonified in this arc — citing observed state not dispatch-authoring SHA):** local main at 2a476e5 = origin/main…" Single instance of the controlled-comparison shape per §6.7.1 condition 2; accretes as future seats attest under §19.6.

The discipline is in substrate canon NOW because PRINCIPAL articulated it today and the Arc 30 bit-by-it surfaced today; promotion to "structural lesson" status with multi-arc empirical backing under the encoded canon is future arcs' work, not this arc's. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's §22.3, Arc 29's §17.5, Arc 30's `MAJOR_PLINY.md` §5.9.3, and Arc 31's §25.6.
```

**Edit 4b — extend §19.4 to name §19.6 as a sub-discipline (rev2 addition addressing ARGUS R2).** ARGUS R2 correctly identified that back-pointers do not auto-extend to new sub-subsections appended after their authoring. The existing §19.4 (at `operating-disciplines.md` lines 837-841) closes with:

> The two disciplines cross-reference; neither subsumes the other. `MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 carry a scope-broadening note pointing here.

The pointer "here" resolves to §19 root; a reader at §7.2 / §4.3 who follows the pointer reads §19.1-§19.5 in current canon and does NOT mechanically land at §19.6 unless §19.4's prose names it. ADA must append a single final paragraph to §19.4 (after the existing closing paragraph quoted above), verbatim:

> The attestation sub-discipline at §19.6 (Arc 32) is the specific application of §19 to attestation-at-attestation-time rather than execution-at-execution-time; readers landing at §7.2 / §4.3's pointer to §19 should follow through to §19.6 for the attestation-specific failure mode (claim is about a prior verification rather than about the current state).

This is a single-paragraph append. It does not modify the existing §19.4 prose; it extends §19.4 so the back-pointer's destination explicitly enumerates §19.6 alongside the existing §19.1-§19.5. Post-edit, the reader landing at §7.2 / §4.3 follows the pointer to §19, reads §19.4's enumeration of sub-disciplines, and finds §19.6 named. No edit needed at §7.2 / §4.3 themselves — the discovery path goes through §19.4, which is now extended to name §19.6.

**Cite-comments — C4 cross-refs that must resolve at every read-site:**

- `operating-disciplines.md` §19.6 references §19.1, §19.2, `MAJOR_PLINY.md` §7.2, `MAJOR_POLYBIUS.md` §4.3, `MAJOR_PLINY.md` §5.10 (created by C3 this arc), §6.7.1. All loci exist or are created within this arc.
- **C4 ↔ C3 cross-ref (per A7):** §19.6.2 names §5.10 as "the PLINY-specific worked example of §19.6 in action"; §5.10.1 names §19.6 as "the universal-seat root cause." Each section cites the other; resolves on apply.
- The `MAJOR_PLINY.md` §7.2 and `MAJOR_POLYBIUS.md` §4.3 cross-refs are NOT edited by this arc directly — instead, the discovery path is extended at its source via Edit 4b above. The existing §19.4 (at `operating-disciplines.md` lines 837-841) is the named back-pointer destination from §7.2 / §4.3, and Edit 4b appends a paragraph to §19.4 explicitly enumerating §19.6 as a sub-discipline. Readers landing at §7.2 / §4.3, following the pointer to §19, will read §19.4's now-extended enumeration and find §19.6 named. The transitive-inheritance claim of design rev1 was structurally false (corrected per ARGUS R2); Edit 4b makes the discovery path explicit at §19.4 rather than implicit.

---

### §3.5 — C5: Arc-build worktree convention

**Sub-decision pick: Option A (require separate worktree at `.claude/worktrees/arc-N-build/`).** Rationale:

The empirical anchor is the Arc 31 divergence: PLINY operated `arc-31/build` IN the main workspace path rather than in a separate `.claude/worktrees/arc-31-build/` subdirectory. The main worktree's checkout flipped from main to `arc-31/build` for the duration of PLINY's work. This blocked user-tier POLYBIUS from operating in main concurrently (the checkout-flip side effect). Arcs 26-30 used separate worktrees de-facto; Arc 31 was the divergence.

Option B (explicit allow main-worktree checkout; let PLINY pick per-arc) is rejected on the same structural-shape reason §5.1.2 rejected per-session paste-suppression: a default-include shape is the right fit when the cost of the default is small and the cost of getting the per-session/per-arc judgment wrong is structural-coordination-failure (not tool-call-failure).

**Honest qualification of the §5.1.2 analogy (rev2 addition addressing ARGUS R6):** the §5.1.2 analogy is structural-shape (default-include rather than per-session judgment), not identity — §5.1.2's predicate is asked at paste-fill time by POLYBIUS (low session knowledge: POLYBIUS knows little about what the downstream PLINY session will need); §5.9.4's predicate is asked at branch-creation time by PLINY (high session knowledge: PLINY knows everything about its own session and whether user-tier POLYBIUS is operating concurrently). The two predicates have meaningfully different knowability profiles. The default-include shape is the right fit at both lifecycle points despite the knowability difference, because the cost of the default is small (one extra worktree directory; mechanical cleanup at arc close) and the failure mode the default prevents is structural-coordination-failure (concurrent-operator collision; main-worktree checkout-flip blocking user-tier POLYBIUS) rather than tool-call-failure — both costs are predictable, both defaults are cheap. If the rigidity ever surfaces friction in the symmetric case (some future arc where the separate-worktree shape produces friction in a way the main-worktree shape would not), the §5.9.4.1 provenance section's accretion-path acknowledges that future arcs may revise; the analogy here is not claiming the two predicates are identical, only that the default-include structural shape applies cleanly to both.

PLINY at branch-creation time does not know whether user-tier POLYBIUS will need to operate concurrently in main during the *duration* of the arc — the higher session-state knowability is at the moment-of-decision; the duration-knowability is lower (concurrent operation may begin after the arc-build branch is created, when the side-effect is harder to reverse). The safe default is the separation that preserves the option. Option A also makes the worktree-cleanup convention (`git worktree remove` + `git branch -D` + `git push origin --delete`) mechanical and identical across arcs, which simplifies the §5.10 signoff-accuracy check (C3) — the verification commands are the same every time.

The user-tier POLYBIUS lean (per directive A6) matches this analysis. Option A picked. Per A6, the worktree-cleanup convention is also encoded.

**Target file:** `substrate/MAJOR_PLINY.md`
**Insertion-point:** new sub-subsection `#### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/`, inserted after §5.9.3 closes at MAJOR_PLINY.md:388 and before the new §5.10 (C3, §3.3 above) inserts. The full §5.9 family currently runs §5.9 / §5.9.1 / §5.9.2 / §5.9.3; §5.9.4 continues the family as a sibling sub-subsection rather than a top-level §5.x — because the worktree convention is structurally an extension of pre-branch hygiene (the same arc-boundary family, fired at the same lifecycle point as the §5.9 two-check rule).

**Canonical post-build insertion order in the §5.9.3-close → `---` → §6 window (rev2 addition addressing ARGUS R3 — insertion-window collision with C3 §5.10):** both C5 (§5.9.4, this section) and C3 (§5.10, §3.3 above) insert into the same two-line window between MAJOR_PLINY.md:388 (§5.9.3 close) and MAJOR_PLINY.md:390 (`---` family-boundary). The required post-build order is:

```
<MAJOR_PLINY.md:388 = §5.9.3 close>
<blank line>
#### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/
<C5 body prose>
<blank line>
### 5.10 Signoff-accuracy — verify cleanup claims before posting
<C3 body prose>
<blank line>
---
<MAJOR_PLINY.md:390 → §6 begins>
```

§5.9.4 (depth-4 `####`) MUST appear above §5.10 (depth-3 `###`) so the §5.9 family closes before the new §5.10 top-level peer opens — this preserves the §5.9-family / §5.10-peer structural distinction the C5 vs C3 locus rationale rests on. §5.10 MUST appear above the `---` family-boundary so it sits as a top-level peer of §5.1-§5.9 rather than nested inside the §5.9 family. VERA §4.5 probes enforce this relative ordering (per §4.5 rev2 additions). The same canonical order is named at §3.3 above so ADA reading either subsection sees it.

**Locus rationale:**

- §5.9 already encodes "what to verify before creating the arc-build branch" (the two-check rule). §5.9.4 encodes "where to create it" — same lifecycle point, same family.
- A top-level §5.10 sibling was considered (per directive A6's example "encode at MAJOR_PLINY.md §5.9 (extending pre-branch hygiene; same family)") but rejected because §5.10 is already taken by C3 (signoff-accuracy); placing C5 at §5.9.4 sub-subsection both follows the directive's "extending pre-branch hygiene" framing and avoids a numbering conflict.
- The §5.9 family's §5.9.4 placement makes the arc-close cleanup convention (which the worktree-removal sequence belongs to) the inverse of the arc-open pre-branch hygiene check (§5.9.1). The structural symmetry — open with verification, close with cleanup-verification — is what §5.10 (C3) signoff-accuracy operationalizes.

**Verbatim canon prose ADA must write** (paste as new sub-subsection between MAJOR_PLINY.md:388 and the new §5.10 from C3; ordering: §5.9.3 close → blank line → §5.9.4 → blank line → §5.10 → `---` → §6):

```markdown
#### 5.9.4 Arc-build worktree convention — separate worktree at .claude/worktrees/arc-N-build/

After the two-check rule passes (§5.9 check 1 + check 2), create the arc-build branch in a SEPARATE worktree at `.claude/worktrees/arc-N-build/`. The main worktree stays on main. Concretely:

```
git worktree add .claude/worktrees/arc-N-build -b arc-N/build
cd .claude/worktrees/arc-N-build
```

Subsequent arc-build work happens entirely within `.claude/worktrees/arc-N-build/`. The main worktree at the project root stays on main throughout the arc — which means user-tier POLYBIUS (or any concurrent operator in the main worktree) can land housekeeping work, read git history, or run substrate-check workflows in main without colliding with PLINY's arc-build checkout.

**Why separate worktree by default:** the alternative is creating the arc-build branch in the main worktree (`git checkout -b arc-N/build` from the project root). The main worktree's checkout then flips to `arc-N/build` for the duration of the arc. Two failure modes follow:

- **Concurrent-operator collision.** User-tier POLYBIUS operating in the main worktree finds the checkout is no longer main; any commits land on `arc-N/build` instead of main. The cost in 2026-05-17 Arc 31: user-tier POLYBIUS had to hold position rather than land housekeeping commits.
- **Cleanup is less mechanical.** Removing a separate worktree is a single `git worktree remove` call; cleaning up after a main-worktree checkout-flip requires a checkout-back-to-main step plus the branch-deletion sequence. The §5.10 signoff-accuracy check (verify cleanup) is simpler when the cleanup is mechanical.

**At arc close, the cleanup sequence (PLINY runs after PR merge, before posting signoff):**

```
git worktree remove .claude/worktrees/arc-N-build
git branch -D arc-N/build
git push origin --delete arc-N/build
```

The §5.10 signoff-accuracy discipline (next section) requires PLINY to verify each of these completed before posting the signoff: `git worktree list` should not show `.claude/worktrees/arc-N-build`; `git branch` should not show `arc-N/build`; `git ls-remote --heads origin arc-N/build` should return empty. The verification commands are stable across arcs because the worktree path and branch name follow the same template every time.

#### 5.9.4.1 Empirical anchor and provenance

The de-facto pattern from Arcs 26-30 was the separate-worktree shape (per the respective arc cleanup sequences + `git worktree list` outputs observed at each arc's close). Arc 31 (`stoa--32b.1`, 2026-05-17) diverged — PLINY operated `arc-31/build` in the main workspace path; the main worktree's checkout flipped from main to `arc-31/build` for the duration; user-tier POLYBIUS held position to avoid committing to arc-31/build. The cost was small (no defect; no rollback warranted) but surfaced the gap: the separate-worktree pattern was operating ad-hoc since Arc 26, not as encoded canon.

Per `MAJOR_POLYBIUS.md` §15 honest-scope and `operating-disciplines.md` §6.7.1: PRINCIPAL + user-tier POLYBIUS articulated this discipline on 2026-05-17 after the Arc 31 divergence. The discipline enters substrate canon off-gate on the project-direction declaration; future-evidence accretion per §6.7.1 — N=5 de-facto bit-by-it (Arcs 26-30 used separate worktrees and shipped clean), N=1 worked-when-applied controlled comparison (Arc 32 / this arc applies §5.9.4 explicitly), N=1 bit-by-it of the failure mode (Arc 31 main-worktree checkout-flip blocked concurrent operation). Promotion to "structural lesson" status accretes as future arcs ship under §5.9.4. Same N=1 framing as Arc 27's `MAJOR_POLYBIUS.md` §16.6, Arc 28's `operating-disciplines.md` §22.3, Arc 29's §17.5, Arc 30's §5.9.3, and Arc 31's §25.6.
```

**Cite-comments — C5 cross-refs that must resolve at every read-site:**

- `MAJOR_PLINY.md` §5.9.4 references §5.9 (parent), §5.9.1 (check 1), §5.10 (created by C3 this arc), `MAJOR_POLYBIUS.md` §15, `operating-disciplines.md` §6.7.1. All loci exist or are created within this arc.
- **C5 ↔ C3 cross-ref (per A7):** §5.9.4 names §5.10 explicitly as "the §5.10 signoff-accuracy discipline (next section) requires PLINY to verify each of these completed." §5.10 (per §3.3 above) references §5.9 family transitively but does NOT add a specific cross-ref back to §5.9.4 because §5.10's "worktree removal claims" bullet already names the verification command (`git worktree list`) that applies to §5.9.4's cleanup. The asymmetric cross-ref is intentional: §5.9.4 is the operational convention; §5.10 is the verification discipline. The convention names the discipline; the discipline names the verification command without re-citing the convention. Same shape as §5.9 → `operating-disciplines.md` §24 (substantive canon references the cross-ref; cross-ref references the substantive canon back; the substantive canon does not need to re-cite the cross-ref in its own body prose because the cross-ref locus is named in the existing §5.9.2 Cross-references block — which §5.9.4 inherits as the §5.9 family's cross-ref block).
- **C5 ↔ C2 cross-ref (per A7):** intentionally NOT added, per the reasoning at §3.2 cite-comments above. The two disciplines share a seat (PLINY) but fire at different lifecycle points (cron at activation; worktree at arc-build); coupling them would over-link.

---

## §4 — Verification probes (for VERA)

Each probe is a runnable command + expected match. VERA re-executes against the post-build state on `arc-32/build`.

### §4.1 — C1 §5.1.1 extension present

```
grep -n "Cross-project sequencing context is user-tier-only" substrate/MAJOR_POLYBIUS.md
```
Expected: one match at the §5.1.1.1 sub-subsection header.

```
grep -n "Sector-4 corpus seed (separate follow-on" substrate/MAJOR_POLYBIUS.md
```
Expected: one match inside the §5.1.1.1 worked-example anti-pattern block-quote.

```
grep -n "Per §5.1.1, this paste scopes to ariadne-core work only" substrate/MAJOR_POLYBIUS.md
```
Expected: one match inside the §5.1.1.1 worked-example positive-pattern block-quote.

### §4.2 — C2 cron-hygiene three carriers + cross-ref present

Carrier 1 (source-of-truth + paste convention, `MAJOR_POLYBIUS.md` §5.1.3):

```
grep -n "5.1.3 PLINY-targeted and POLYBIUS-targeted activation pastes include the cron-hygiene preamble by default" substrate/MAJOR_POLYBIUS.md
```
Expected: one match at the §5.1.3 header.

```
grep -n "this session may carry an" substrate/MAJOR_POLYBIUS.md
```
Expected: one match inside the §5.1.3 preamble verbatim code-fence.

Carrier 2 (template slot, `paste-instruction-template.md`):

```
grep -n "{{CRON_HYGIENE_CLAUSE}}" substrate/templates/paste-instruction-template.md
```
Expected: at least two matches — one in the template body at line ~46 area, one in the slot-explanation paragraph that introduces the default expansion. (A third match in the worked-example filled-template section is acceptable but not required by C2 verbatim text; the worked-example shows the expanded preamble text rather than the unexpanded slot.)

**Slot-explanation paragraph identity probe (rev2 addition per ARGUS R5)** — the previous probe's "at least two matches" only confirms the slot string appears twice, not that the slot-explanation paragraph specifically (the prose that explains the default expansion + POLYBIUS suppression rule) is present. Match a unique sentence from that paragraph that does not appear elsewhere:

```
grep -n "Default-include is the safety property: the cost of including the preamble when no orphan cron is present" substrate/templates/paste-instruction-template.md
```
Expected: exactly one match in the `{{CRON_HYGIENE_CLAUSE}}` slot-explanation paragraph (per Edit 2c). This sentence is unique to the slot-explanation paragraph and does not appear in either the source-of-truth section (`MAJOR_POLYBIUS.md` §5.1.3) or the universal-team cross-ref (`operating-disciplines.md` §26).

```
grep -nE "orphaned cron from a prior" substrate/templates/paste-instruction-template.md
```
Expected: at least two matches — one in the default-expansion code-fence, one in the worked-example filled paste-instruction code-fence.

Carrier 3 (thin universal-team cross-ref, `operating-disciplines.md` §26):

```
grep -n "26. Activation-paste cron hygiene" substrate/operating-disciplines.md
```
Expected: one match at the §26 header.

```
grep -n "MAJOR_POLYBIUS.md.*§5.1.3" substrate/operating-disciplines.md
```
Expected: at least one match in §26 (referencing the source-of-truth section).

### §4.3 — C3 PLINY-signoff-accuracy at picked locus (Option α: MAJOR_PLINY.md §5.10)

```
grep -n "5.10 Signoff-accuracy — verify cleanup claims before posting" substrate/MAJOR_PLINY.md
```
Expected: one match at the §5.10 header.

```
grep -nE "Sign what you did, not what you intended" substrate/MAJOR_PLINY.md
```
Expected: one match in §5.10 body.

```
grep -n "Arc 29 signoff" substrate/MAJOR_PLINY.md
```
Expected: one match in §5.10.1 empirical anchor.

Thin cross-ref at `operating-disciplines.md` §24:

```
grep -n "MAJOR_PLINY.md.*§5.10.*PLINY-signoff-accuracy" substrate/operating-disciplines.md
```
Expected: one match in §24 Cross-references block.

### §4.4 — C4 §19.6 attestation sub-rule present

```
grep -n "19.6 Attestation-confabulation — cite live-verified state" substrate/operating-disciplines.md
```
Expected: one match at the §19.6 header.

```
grep -n "Discipline-PASS and honesty-PASS are separate properties" substrate/operating-disciplines.md
```
Expected: one match in §19.6 body.

```
grep -nE "140b398.*dispatch-authoring SHA" substrate/operating-disciplines.md
```
Expected: one match in §19.6.1 empirical anchor.

### §4.5 — C5 §5.9.4 worktree convention present + cleanup convention

```
grep -n "5.9.4 Arc-build worktree convention" substrate/MAJOR_PLINY.md
```
Expected: one match at the §5.9.4 header.

```
grep -nE "git worktree add .claude/worktrees/arc-N-build" substrate/MAJOR_PLINY.md
```
Expected: at least one match (in the convention code-fence; may also appear in the §5.9.4.1 empirical anchor prose).

```
grep -nE "git worktree remove .claude/worktrees/arc-N-build" substrate/MAJOR_PLINY.md
```
Expected: at least one match in the §5.9.4 cleanup code-fence.

```
grep -nE "git branch -D arc-N/build" substrate/MAJOR_PLINY.md
```
Expected: at least one match in the §5.9.4 cleanup code-fence.

```
grep -nE "git push origin --delete arc-N/build" substrate/MAJOR_PLINY.md
```
Expected: at least one match in the §5.9.4 cleanup code-fence.

**Relative-ordering enforcement for the §5.9.3-close → `---` window (rev2 addition addressing ARGUS R3 — C3+C5 insertion-window collision):** the post-build state MUST have §5.9.4 appearing above §5.10 in line-number order, and §5.10 appearing above the family-boundary `---` that opens §6. The following probes enforce relative ordering by extracting the line numbers and comparing:

```
grep -nE "^#### 5\.9\.4 |^### 5\.10 " substrate/MAJOR_PLINY.md
```
Expected: exactly two matches. The §5.9.4 line number MUST be strictly less than the §5.10 line number. (VERA: extract both line numbers from the grep output and compare numerically; fail if §5.10 appears at or above §5.9.4.)

```
grep -nE "^### 5\.10 |^## 6\." substrate/MAJOR_PLINY.md | head -5
```
Expected: at least two matches; the §5.10 line number MUST be strictly less than the §6 line number, AND the `---` separator at the line immediately preceding `## 6.` MUST exist (confirmable via `sed -n '<§6-line-1>p' substrate/MAJOR_PLINY.md` returning `---`). This confirms §5.10 sits above the family-boundary as a §5 family peer rather than after the boundary as a §6 member.

### §4.6 — Cite-comment cross-refs resolve

For each named cross-ref locus, verify the target section header exists at its expected markdown depth. **Per-depth probes (rev2 split per ARGUS R5 — the previous alternation `^### 5\.1\.1\b|^##### 5\.1\.1\.1\b|...` mixed depths so a depth typo (e.g., ADA accidentally writing `#### 5.1.1.1` at depth-4 instead of `##### 5.1.1.1` at depth-5) would still pass the alternation):**

```
grep -nE "^##### 5\.1\.1\.1\b" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match at the §5.1.1.1 header (depth-5, per §3.1 C1 verbatim prose).

```
grep -nE "^#### 5\.1\.3\b" substrate/MAJOR_POLYBIUS.md
```
Expected: exactly one match at the §5.1.3 header (depth-4, sibling of §5.1.2).

```
grep -nE "^#### 5\.9\.4\b" substrate/MAJOR_PLINY.md
```
Expected: exactly one match at the §5.9.4 header (depth-4, sibling of §5.9.1/§5.9.2/§5.9.3).

```
grep -nE "^### 5\.10\b" substrate/MAJOR_PLINY.md
```
Expected: exactly one match at the §5.10 header (depth-3, peer of §5.1-§5.9).

```
grep -nE "^### 19\.6\b" substrate/operating-disciplines.md
```
Expected: exactly one match at the §19.6 header (depth-3, sibling of §19.1-§19.5).

```
grep -nE "^## 24\." substrate/operating-disciplines.md
```
Expected: exactly one match at the §24 header (depth-2, existing canon).

```
grep -nE "^## 26\." substrate/operating-disciplines.md
```
Expected: exactly one match at the §26 header (depth-2, new top-level section per C2 Carrier 3).

**§19.4 extension probe (rev2 addition per ARGUS R2 / Edit 4b):**

```
grep -n "The attestation sub-discipline at §19.6 (Arc 32) is the specific application of §19" substrate/operating-disciplines.md
```
Expected: exactly one match inside §19.4, confirming Edit 4b's appended paragraph landed and the §7.2 / §4.3 back-pointer path now resolves to §19.6 via §19.4's enumeration.

**§24 prose-edit probe (rev2 addition per ARGUS R1 / Edit 3a):**

```
grep -n "PLINY as the only seat creating arc-build branches (POLYBIUS is paste-activated but does not create branches" substrate/operating-disciplines.md
```
Expected: exactly one match inside §24, confirming Edit 3a narrowed the framing from "PLINY only [paste-activated]" to "PLINY only [branch-creating]" and back-pointed to §26.

**C3↔C4 reciprocal cross-ref content probes (rev2 tightened per ARGUS R5 — the previous probes only confirmed the strings existed somewhere; rev2 probes match the specific reciprocal-cite phrasing so a wrong-direction cite cannot pass):**

```
grep -n "operating-disciplines.md.*§19.6.*the canonical home for the root-cause discipline" substrate/MAJOR_PLINY.md
```
Expected: exactly one match in §5.10.1, confirming C3 cites C4 with the canonical "universal-seat root cause" phrasing per §3.3 cite-comments.

```
grep -n "MAJOR_PLINY.md.*§5.10.*PLINY-specific worked example" substrate/operating-disciplines.md
```
Expected: exactly one match in §19.6.2, confirming C4 cites C3 with the canonical "PLINY-specific worked example" phrasing per §3.4 cite-comments.

### §4.7 — §15 N=1 provenance shape per A10 (no over-generalization)

Each of C1-C5's canon sections must name an empirical anchor + cite §6.7.1 + name the accretion path. The canonical phrasing is "enters substrate canon off-gate on PRINCIPAL's project-direction authority". **C1 is a structurally-justified categorical exception** to the per-candidate provenance-shape A10 LOCKS for C2-C5 (per §3.1 rev2 categorical-exception prose addressing ARGUS R4): C1's §5.1.1.1 is already a depth-5 sub-subsection (in-place refinement of existing depth-4 §5.1.1); adding a numbered provenance sub-subsection beneath it would force depth-6 `######`, which most markdown renderers do not style and which collapses out of the TOC. The provenance content (N count, §6.7.1 cite, accretion path) is therefore folded into an inline closing paragraph at §5.1.1.1's foot rather than a numbered subsection header. This is NOT a probe-author convenience — it is a structural necessity of the worked-refinement-of-existing-section shape C1 uses, named here so the per-candidate A10 check is honest about the divergence.

**Per-file boilerplate-phrase probes** (rev2 split per ARGUS R5 — each file must independently carry its own provenance marker for the candidates it hosts; "4 matches across three files" was loose enough to pass with all 4 in one file):

```
grep -nE "enters substrate canon off-gate" substrate/MAJOR_POLYBIUS.md
```
Expected: at least 1 match (C2 §5.1.3 provenance paragraph).

```
grep -nE "enters substrate canon off-gate" substrate/MAJOR_PLINY.md
```
Expected: at least 2 matches (C3 §5.10.3 + C5 §5.9.4.1).

```
grep -nE "enters substrate canon off-gate" substrate/operating-disciplines.md
```
Expected: at least 1 match (C4 §19.6.4).

**C1 categorical-exception probe** — C1 (§5.1.1.1) uses the variant phrasing "future-evidence accretion per §6.7.1 — if the cross-project shape proves to be one-of-many specialization needs, future arcs may promote this to a separate §5.1.x section" which is the §6.7.1 reference without the boilerplate phrase. C1 is structurally a worked-refinement of §5.1.1 (depth-5 sub-subsection), not a new canon section; the depth-6 provenance subsection that would parallel C2-C5's shape is unreadable in markdown. The inline-paragraph provenance form at §5.1.1.1's close is the categorical-exception form. Verify separately:

```
grep -n "future-evidence accretion per §6.7.1" substrate/MAJOR_POLYBIUS.md
```
Expected: at least one match in §5.1.1.1.

### §4.8 — Authorship audit (per A8)

```
grep -rnE "^author:|^Authored by:|^Author:" substrate/templates/paste-instruction-template.md substrate/MAJOR_POLYBIUS.md substrate/MAJOR_PLINY.md substrate/operating-disciplines.md
```
Expected: only the existing `author: Denson Smith` frontmatter at `paste-instruction-template.md` line 2 (unchanged). No other author-like fields added or modified.

### §4.9 — `check.sh` against the-stoa workspace

Per directive Phase B item 8:

```
substrate/skills/check-substrate-updates/check.sh --workspace C:/Users/denso/claude_projects/the-stoa
```
Expected: DRIFTED on the four edited substrate files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`, `operating-disciplines.md`, `templates/paste-instruction-template.md`). The workspace-tier handles re-sync on its own activation per `MAJOR_POLYBIUS.md` §14.

### §4.10 — Credential-discipline non-applicability gate (per `CAPTAIN_DAEDALUS_the_stoa.md` §6.6)

This design touches no credentialed operations. No CLI/API gated by tokens, OAuth scopes, or service accounts is invoked. No probe authors any workflow YAML; no probe invokes any credentialed tool. The §6.6 credential-flow probe requirement does not apply to this design.

---

## §5 — Self-assessed weak points

Per `CAPTAIN_DAEDALUS_the_stoa.md` §6.2, these are brittle spots where a specific assumption could break the design under ARGUS cold-read or future maintenance pressure. Each names the spot and the defense for the shape anyway.

**Weak point 1 — C1's §5.1.1.1 sub-subsection nesting depth is 5 (`#####`).** The existing §5.1.1 is depth-4 (`####`); the new sub-subsection at depth-5 may be the first depth-5 header in the file. *Defense for the shape:* the C1 prose is structurally a worked refinement of §5.1.1, not a peer concept. Promoting to a peer §5.1.x (depth-4) would suggest the cross-project specialization is structurally distinct from the §5.1.1 root cause, which it is not. The provenance paragraph at §5.1.1.1's close acknowledges this — "if the cross-project shape proves to be one-of-many specialization needs, future arcs may promote this to a separate §5.1.x section" — so the depth-5 placement is honest about its temporary status. ARGUS may push back on the depth-5 nesting; the alternative is over-promoting a sub-case to peer status.

**Weak point 2 — C2 carrier-3 (operating-disciplines.md §26) creates a third "thin cross-ref" universal-team section in the §24/§26 family.** Three thin cross-refs (§24 Arc 30; §26 Arc 32 C2; and §24's new bullet for C3) start to look like a pattern — universal-team layer is now mostly thin cross-refs to seat-envelope canon, not substantive universal-team prose. *Defense for the shape:* the thin-cross-ref pattern is the right shape when only one or two seats exercise the discipline today; full universal-team mirrors over-promote disciplines to seats that don't exercise them. The §24 model has worked for Arc 30; replicating it for C2 is consistency, not pattern-fatigue. If a future arc surfaces a third seat that exercises one of these disciplines, the universal-team section can promote to substantive then. ARGUS may push back on the proliferation; the alternative (full universal-team mirrors for every discipline) is the over-promotion the §24 framing exists to prevent.

**Weak point 3 — C3's "branch deletion claims," "worktree removal claims," "file cleanup claims," "process / cron / scheduled-job teardown" enumeration may over-scope the discipline.** The empirical anchor is single (Arc 29 signoff inaccuracy; specifically the worktree + branch claims). The other three categories (file cleanup; cron teardown) are not empirically anchored today. *Defense for the shape:* the enumeration is structural rather than empirical — once the discipline is "verify cleanup claims before posting," the specific cleanup categories enumerate the available cleanup verbs. Enumerating only the empirically-anchored verbs (branch + worktree) would leave the discipline silent on the other three when they arise; PLINY would then re-derive whether the discipline applies to file cleanup or cron teardown, which is the per-session-judgment shape this canon exists to remove. The over-scope is the discipline-redundancy / over-include shape that Arc 30 §5.1.2 explicitly defended ("default-include encodes the redundancy structurally rather than relying on… session-by-session judgment, which is a semantic predicate not always knowable"). ARGUS may push back on the enumeration; the alternative (empirically-anchored verbs only) is a discipline that requires re-derivation per cleanup category.

**Weak point 4 — C4's §19.6 attestation discipline is structurally indistinguishable from §19.2 pattern 2 (state-vs-claim mismatch) in some readings.** A reader could argue the Arc 30 PLINY init-handshake attestation is exactly the §19.2 pattern 2 case ("when state and assumption don't match, 'uncertain, checking' beats either assertion"). *Defense for the shape:* §19.2 pattern 2 fires on state-vs-CLAIM mismatch from an external source (the user, a peer agent); §19.6 fires on attestation-vs-state mismatch where the attestation is the seat's own claim about a prior verification, made under social pressure to confirm the discipline passed. The shape is distinct enough to warrant its own subsection — the failure mode (reach for the available SHA from the directive rather than running the live tool call) is specific to attestation prose, not general state-vs-claim mismatch. ARGUS may push back on the §19.6-vs-§19.2-pattern-2 distinction; the alternative (fold into §19.2 as a fourth bullet) loses the attestation-specific guidance the §19.6.1 + §19.6.2 prose carries.

**Weak point 5 — C5 picks Option A without an empirical anchor of "Option A produced a worse outcome in some hypothetical world."** The cost of Arc 31's main-worktree pattern was real but small (user-tier POLYBIUS held position; no defect; no rollback). Picking Option A on this evidence is responsive to a small failure mode; it locks future PLINYs into a structural rule when a per-arc judgment might have sufficed. *Defense for the shape:* per-arc judgment is the predicate that fails at the moment of branch creation, before the cost of the wrong choice has materialized. The §5.1.2 default-include defense applies exactly: "the cost of including [the discipline] when not needed is one paragraph PLINY reads and skips; the cost of omitting it on a session that pivots to arc work mid-engagement is the [failure mode] this discipline exists to prevent." Option A is the default-include shape applied to worktree placement. ARGUS may push back on the rigidity; the §5.9.4.1 provenance section explicitly defers promotion to "structural lesson" until future arcs accrete evidence under the canon.

**Weak point 6 — the design is dense (verbatim canon prose for 5 candidates in one artifact). ADA may apply edits in an order that breaks cross-refs mid-build, AND C3+C5 both insert into the same two-line window between MAJOR_PLINY.md:388 (§5.9.3 close) and MAJOR_PLINY.md:390 (`---` family-boundary).** Two distinct ordering hazards combine:

(a) **Cross-ref forward-resolution:** C3 references §19.6 (created by C4) and §5.10 (itself); C4 references §5.10 (created by C3); C5 references §5.10 (created by C3). If ADA applies C3 before C4 (or vice versa), or applies C5 before C3, the cross-refs in the just-applied section reference sections that don't yet exist in the file.

(b) **Insertion-window collision (rev2 explicit acknowledgment per ARGUS R3):** C3 (§5.10, a depth-3 top-level subsection) and C5 (§5.9.4, a depth-4 sub-subsection) BOTH target the same MAJOR_PLINY.md:388 → :390 window. Two independently-correct edits applied per their respective §3 prose can ship a file where §5.9.4 sits BELOW §5.10 — which would nest the §5.9.4 sub-subsection inside what reads as the §5.10 family rather than the §5.9 family, breaking the §5.9-family / §5.10-peer structural distinction the locus rationale rests on. The §3.3 and §3.5 rev2 prose name the canonical post-build order explicitly (§5.9.3 → §5.9.4 → §5.10 → `---` → §6); §4.5 rev2 probes enforce the relative line-number ordering so a structurally-broken file fails verification rather than passing each individual grep.

*Defense for the shape:* the cross-refs resolve once all four candidates are applied (which is the post-build state VERA verifies against). Intermediate states between edits are not verified. The risk is purely that ADA notices the broken-mid-build cross-ref and tries to "fix" it by inventing a different reference; the design's structure makes the dependency explicit (§3.3 cite-comments names C3↔C4 reciprocal cross-ref; §3.5 names C5→C3 cross-ref). ADA reading this section before building should apply all five candidates as a single coordinated change rather than commit-by-commit per candidate. The recommended build order is C1 first (independent), then C2 carriers in any order (only forward references within itself), then C3+C4+C5 as a single atomic commit (they reference each other AND C3+C5 collide in the insertion window — the §3.3/§3.5 canonical order resolves the collision), then verify cite-comments + §4.5 relative-ordering probes resolve.

**Weak point 7 — the design assumes the existing §24 thin cross-ref's bullet-list structure permits in-place addition of a new bullet for C3.** If §24's bullet list has been refactored between dispatch authoring and ADA build (e.g., reformatted as paragraphs), ADA's literal "add a bullet after the §6.7.1 bullet" instruction breaks. *Defense for the shape:* §24 is a stable substrate-canon section; the bullet-list format has been stable since Arc 30. Verification: ADA should `grep -n "^- " substrate/operating-disciplines.md | head -20` before edit to confirm §24 bullets are still bullets. If the format has changed, ADA surfaces back to PLINY for design refresh rather than improvising. ARGUS may flag this as an under-specified pre-condition; the §4.6 probes verify the post-build state, and the pre-build state check is one grep.

---

## §6 — Out of scope (A9 hard-locked)

Per directive A9, the following are explicitly NOT addressed by this design and any reach for them surfaces as substance-disagreement comment on `stoa--ewn` before continuing:

- **stoa--32b.2** (script/agent-inspection split) — separate forthcoming arc; needs its own design.
- **stoa--k36** (user-tier-to-main discipline) — separate scope discussion; not folded here.
- **stoa--f37** (HUMAN_paste-*.md accumulation at the-stoa root) — hygiene observation; can wait or piggyback on a future cleanup arc.
- **stoa--ize** (arcs/22 branch) — separate arc not in this canonification batch.
- **Parent epic stoa--32b structure** — this arc closes the child `stoa--ewn`; parent epic structure not touched.
- **Migration of existing artifacts.** No backfill of historical pastes (Arcs 26-32 already-shipped activation pastes are not rewritten); no rewriting of prior PR descriptions. Forward-only convention adoption per A9.
- **Empirical-premise-verification before LOCKING directives.** Discipline shape touches directive-authoring at user-tier POLYBIUS; separate forthcoming arc.

---

## §7 — Authorship audit (per A8)

All edits in this arc are to existing files. No new files with author-like fields are created. The only author-like field in the edit set is `author: Denson Smith` at `paste-instruction-template.md` line 2, which this design does NOT modify (the template's content body changes via C2 edits 2b-2d; the frontmatter is untouched). §4.8 probe confirms.

Per `CAPTAIN_DAEDALUS_the_stoa.md` §8 and the project + user CLAUDE.md authorship-attribution discipline: this design and the canon prose it specifies for Arc 32 are authored by CAPTAIN_DAEDALUS_the_stoa on behalf of the PRINCIPAL (Denson Smith). No third-party attributions are introduced; cited research / empirical anchors (Arc 29 signoff inaccuracy; Arc 30 init-handshake attestation; Arc 31 main-worktree divergence; 2026-05-17 ariadne-core PLINY paste leak) reference past work within this project's authorship lineage.
