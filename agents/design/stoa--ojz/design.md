# Arc 38 design — Substrate architecture batch (TIRO + bj5 + gq1)

**Authored by:** CAPTAIN_DAEDALUS_the-stoa (one-shot dispatch from MAJOR_PLINY, autonomous mode, 2026-05-17 → 2026-05-18).
**Work-unit:** `stoa--ojz` (parent; C1). Source tickets closing alongside per directive A19: `stoa--ojz` (C1) + `stoa--bj5` (C2) + `stoa--gq1` (C3).
**Directive:** `substrate/arcs/arc-38-build-directive.md` (A1-A20 LOCKED at dispatch; sub-decisions inside A5/A8/A11/A13 are DAEDALUS-discretion).
**Branch:** `arc-38/build` (worktree at `.claude/worktrees/arc-38-build/`).
**Spec-state at dispatch:** SPECIFICATION.md HEAD `68c0c12` (post-R4 audit-iteration cadence converged); main HEAD `4d65a4e`.

---

## §0. Problem restatement (pre-work gate per CAPTAIN_DAEDALUS §6.1)

Arc 38 ships three substrate-architecture canon items in one gauntlet:

1. **C1 — CAPTAIN_TIRO** is a new substrate-specialist seat (bw substrate specialist) that absorbs the "generalist forgets the `--all` flag during completeness audits" failure mode (empirical anchor: user-tier POLYBIUS conducted three audits 2026-05-17 each citing truncated bw output as live state). TIRO is **read-direct** (delegated bw queries return structured answers with correct completeness flags) + **write-advisory** (suggests syntax for the asking seat to execute). Split is PRINCIPAL-LOCKED per SPECIFICATION.md §4.6.
2. **C2 — User-tier substrate drift detection** extends `substrate/skills/check-substrate-updates/` to cover user-tier (`~/.claude/`). The blocker since 2026-05-14 is that user-tier deployed files carry install.sh substitutions (`{{USER_TIER_DIR}}` → real path, `{{NAME_SUFFIX}}` → empty) that can't be cleanly reversed for the diff. A per-file-marker scheme (DAEDALUS sub-decision A8) records substitutions per-deploy so check.sh can normalize.
3. **C3 — Substrate-component design principles** lands new substrate canon (`operating-disciplines.md` §31, per the A11 pick below) covering the agent-installable distribution model + composability framing surfaced by the Ariadne distribution-shaping work (HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13).

**What this design does NOT cover** (out-of-scope hard-locks per directive A20):

- Additional candidates beyond C1+C2+C3 (no bundling).
- Widening TIRO to execute writes for another seat (PRINCIPAL-LOCKED split per SPECIFICATION.md §4.6).
- Extending TIRO to non-bw subsystems (git/cron/worktree are noted candidates if pattern proves valuable; future arcs).
- Restructuring check-substrate-updates beyond what bj5 requires (project-tier scope unchanged + extended; not rewritten).
- Touching install.sh beyond what TIRO + bj5 require.
- Touching the stellation workspace.
- Proposing NC8 (Arc 38 PRINCIPAL accepted option (b) per spec §13.10 bullet 4).

**Imported assumptions** (named per CAPTAIN_DAEDALUS §6.1 honest-restatement discipline):

- The bw substitutions set is THIN at user-tier — only `MAJOR_POLYBIUS.md` gets a non-trivial substitution (`{{USER_TIER_DIR}}` → real path). `MAJOR_PLINY.md` and CAPTAINs get only `{{NAME_SUFFIX}}` (which is empty-string at user-tier). Templates and skills are deployed verbatim (no substitution). This shape directly informs the A8 choice; if a future arc adds new substitutions, the manifest design (§A8 below) absorbs them by adding entries — no schema change.
- The directive's "operating-disciplines.md §17 (base-vs-custom)" reference (A12 cross-refs list) is a numbering-shift artifact: in `operating-disciplines.md` the base-vs-custom canon is `§23`; in `MAJOR_POLYBIUS.md` it is `§17`. The two sections are **co-equal canon at their respective tiers** (universal-team cut + POLYBIUS-tier cut), both anchored at their §X.1 source-of-truth subsections to the same 2026-05-17 PRINCIPAL declaration captured at `stoa--ads` — NOT a base canon + derivative refinement. The design cross-refs the correct loci for each file and cites them paired (matching the existing install.sh cite-comment precedent at lines 836-837 / 865-866 / 893-894).
- "stoa--uly precedent" cited in the directive A5 refers to Arc 27 (POLYBIUS session lifecycle); the precedent shape inherited is "new substrate role file shipping" + author-frontmatter discipline. Confirmed by reading `substrate/arcs/arc-27-build-directive.md`.
- Arc 37 squash-merge `bb12806` regression (per `stoa--6wp` ticket body) is OUT of Arc 38's direct scope per A20 (NOT in candidate list), but Arc 38 self-applies §28 trailer discipline + the §15.10 squash-merge-body convention preemptively per A15 — "first arc that should ship trailer-clean on the squash-merge body forward of bb12806."

**Residual ambiguity surfaced for ARGUS** (none load-bearing; named for completeness):

- Whether `WebSearch`/`WebFetch` should be added to TIRO's toolset for live bw upstream docs lookup. Per directive A3, default is NOT included; DAEDALUS may surface as PRINCIPAL-gate. **DAEDALUS recommendation: do NOT add.** Rationale: bw is a local subsystem; the cookbook + `bw <command> --help` cover the documented surface; live upstream docs lookup is rare AND when it surfaces, the asking seat can dispatch STRABO (the external-research specialist) per spec §4.4. Adding WebSearch/WebFetch to TIRO would scope-creep the seat. Listed as `residual_question_for_argus` in the verdict, NOT escalated as PRINCIPAL-gate (the default in A3 is unchanged).

---

# PART 1 — C1: CAPTAIN_TIRO bw substrate specialist seat (stoa--ojz)

## §1.1. Approach

CAPTAIN_TIRO is authored as a standard CAPTAIN sub-agent envelope at `substrate/CAPTAIN_TIRO.md`, mirroring the structural shape of `CAPTAIN_BARTLEBY.md` (the closest precedent: bounded-toolset specialist that returns structured answers to the dispatching seat). Install.sh deploy wiring adds `TIRO` to the `CAPTAIN_NAMES` array. Cross-refs land in 4 existing substrate files per A6.

The file's primary load-bearing content is the **bw subcommand reference with documented gotchas** — this is what makes the seat's whole-context priming on bw mechanics fix the "generalist forgets the gotcha" failure mode. The reference is NOT a copy of `operating-disciplines.md` §12 (the cookbook); it is a TIRO-specific synthesis pointing back to §12 at every read-site (cite-comment discipline per A17), plus the worked-example dispatch patterns that show seats HOW to ask TIRO and how to read TIRO's structured return.

### §1.1.1. The role file structure

`substrate/CAPTAIN_TIRO.md` follows the standard CAPTAIN envelope (compare CAPTAIN_BARTLEBY.md as the closest analogue):

```
---
name: CAPTAIN_TIRO{{NAME_SUFFIX}}
description: "bw substrate specialist; delegated reads (with correct completeness flags) and write-advisory (returns syntax, never executes writes for another seat)."
tools: Bash, Read, Grep, Glob
model: opus
author: Denson Smith
---

# CAPTAIN_TIRO — bw substrate specialist

[role-table block — Rank/Mnemonic/Descriptive role/Lives at/Activation/Tool restrictions]

[Mnemonic origin paragraph — Marcus Tullius Tiro, Cicero's secretary, inventor of Tironian shorthand,
the literal records-keeper of antiquity.]

## 1. Your one job
   [Read-direct + write-advisory split, with the rationale paragraph from SPECIFICATION.md §4.6.]

## 2. The brief you receive
   [What MAJOR_PLINY dispatches with: bw query (read) OR write-syntax question; ticket ID;
    operating-mode flag.]

## 3. What you produce
   [Structured answer for reads; syntax-advice block for writes; no write execution on
    behalf of another seat — refuse and return.]

## 4. What you do NOT do
   [Write tickets/comments/closes/deps for another seat; design or architecture decisions;
    interpret findings beyond surfacing the bw data; widen scope beyond bw.]

## 5. Voice
   [Workmanlike + cookbook-clean. Cite the documented gotcha when it applies; do not paraphrase
    the cookbook.]

## 6. Disciplines specific to this seat
   ### 6.1 The --all flag discipline (load-bearing for completeness audits)
   ### 6.2 Read-direct vs write-advisory boundary (PRINCIPAL-LOCKED)
   ### 6.3 bw subcommand reference (with documented gotchas)
   ### 6.4 Worked-example dispatch patterns (read-query / completeness-audit / write-syntax-advice)
   ### 6.5 Heartbeat-and-read-before-write via bw (standard CAPTAIN comm contract)
   ### 6.6 Credential discipline (bw doesn't touch credentials — cross-ref only)

## 7. Verdict format
   [Structured return block: status / ticket / verdict / query / answer / cookbook_cite /
    summary / gap_or_blocker]

## 8. Authorship attribution (immutable)
   [Standard CAPTAIN paragraph — file-frontmatter `author: Denson Smith` per A18 IMMUTABLE.]

## 9. When this file is wrong
   [Standard CAPTAIN paragraph — field notes, not doctrine; surface via verdict follow-ups.]
```

**Sizing target:** ~280-320 LOC (envelope + the bw subcommand reference + 3 worked-example dispatches). Comparable to CAPTAIN_BARTLEBY.md (170 LOC) plus the bw subcommand reference (~50 LOC for the 10-row table + gotcha rows) and the 3 worked-example dispatches (~80 LOC; BARTLEBY does not carry these). Honest math per §5.5: envelope (~170) + table (~50) + 3 examples (~80) = ~300 LOC, with ±20 LOC tolerance for the §6.x discipline sections (heartbeat, credential cross-ref, role-table block, voice paragraph, mnemonic-origin paragraph). Staying within the 280-320 band keeps the seat dense-but-focused; trimming below 280 erodes load-bearing content (§5.5 names what is load-bearing vs trimmable).

### §1.1.2. The §6.3 bw subcommand reference — exact content

Per directive A4, this is the load-bearing-for-the-seat content. The reference is structured around the documented gotchas that motivated TIRO's existence (cite-comments point back to `operating-disciplines.md` §12 + the bw `--help` output for each subcommand):

| Subcommand | Read/Write | Canonical syntax | Documented gotcha |
|---|---|---|---|
| `bw list` | Read | `bw list [--status STATUS] [-t TYPE] [-p N] [--grep TEXT] [--all]` | **Default-truncates.** Without `--all`, output is silently capped. For completeness audits this IS the canon-relevant failure mode TIRO exists to absorb. <!-- cite: operating-disciplines.md §12.1 → "Reading: bw list — open tickets, default truncated"; SPECIFICATION.md §4.6 + §9.1 empirical anchor (2026-05-17 three-audit confabulation) --> |
| `bw show <id>` | Read | `bw show <id>` | Returns full body + every comment. Safe at any size; pipe through `tail -<N>` if only the recent comments are wanted. <!-- cite: operating-disciplines.md §12.1 --> |
| `bw history <id>` | Read | `bw history <id>` | Chronological audit of status changes, comments, close reasons. Reconstructs ticket lifecycle after session loss. <!-- cite: operating-disciplines.md §12.1 --> |
| `bw prime` | Read (mandatory for top-level seats) | `bw prime` | Mandatory for POLYBIUS/PLINY/pair-programmer Majors; optional for CAPTAINs (the dispatch brief carries the context). TIRO itself does NOT need `bw prime` — its brief carries the query. <!-- cite: operating-disciplines.md §12.4 (per-role specifics) --> |
| `bw create` | Write (advisory only) | `bw create "<title>" --priority P0-P4 --description "<body>"` | Title is **positional**; `--priority` + `--description` are flags. Multi-line description uses HEREDOC pattern. <!-- cite: operating-disciplines.md §12.1 (Filing tickets) + §12.2 --> |
| `bw comment` | Write (advisory only) | `bw comment <id> "<body>"` | **Text is POSITIONAL; `-m` does NOT exist.** Writing `bw comment <id> -m "text"` lands `-m` as the literal comment body. The single most-reported gotcha. <!-- cite: operating-disciplines.md §12.1 (Commenting + closing) + §12.2 + MAJOR_PLINY.md §6.1 + MAJOR_POLYBIUS.md §7.3 --> |
| `bw close` | Write (advisory only) | `bw close <id> --reason "<text>"` | `--reason` is the flag (not `-m`). Reason lands in `bw history`; substantive close-out goes in a comment. <!-- cite: operating-disciplines.md §12.1 --> |
| `bw dep add` | Write (advisory only) | `bw dep add <X> blocks <Y>` | **Direction matters:** `blocked-by` is NOT valid syntax. To reverse direction, swap args. <!-- cite: operating-disciplines.md §12.1 (Dependencies) + §12.2 (canonical error table) --> |
| `bw dep remove` | Write (advisory only) | `bw dep remove <X> blocks <Y>` | Symmetric to add. <!-- cite: operating-disciplines.md §12.1 --> |
| `bw sync` | Write (advisory only) | `bw sync` | Push to orphan `beadwork` branch. Idempotent. Run before closing a session with local-only writes. <!-- cite: operating-disciplines.md §12.1 (Sync) --> |

**Documented gotchas that recur and warrant inline naming:**

- **`worktreeconfig` recovery.** Historically the 3-command promote-and-drop fix at `operating-disciplines.md` §9. Structurally fixed in bw rebuild 2026-05-08; if still seen on a fresh worktree, the local bw install predates the fix — surface to POLYBIUS rather than improvising. <!-- cite: operating-disciplines.md §12.2 + §9 -->
- **"no prime detected" warnings.** Top-level seats run `bw prime`. CAPTAINs ignore (the brief carries context). <!-- cite: operating-disciplines.md §12.2 + §12.4 -->
- **HEREDOC pattern for multi-line input.** Required for `bw create --description` with multi-line body; same shape works for `bw comment` if a structured comment is needed. <!-- cite: operating-disciplines.md §12.1 (Filing tickets — HEREDOC example) -->

### §1.1.3. The §6.4 worked-example dispatch patterns

Three concrete worked examples to show seats how to dispatch TIRO and how to read the return:

**Example 1 — read query (completeness audit):**

> **Brief from PLINY:** "TIRO, list all open P2 tickets at the-stoa for context on Arc 39 sequencing. Completeness audit; apply `--all`."
>
> **TIRO action:** `cd <repo> && bw list --status open -p 2 --all`
>
> **TIRO return shape:**
> ```
> status: completed
> ticket: <dispatch-ticket-id>
> verdict: pass
> query: "all open P2 tickets at the-stoa (completeness audit)"
> answer:
>   - stoa--abc — <title> (P2, opened YYYY-MM-DD)
>   - stoa--def — <title> (P2, opened YYYY-MM-DD)
>   - [N more entries]
> cookbook_cite: operating-disciplines.md §12.1 (bw list --all for completeness)
> summary: <N> open P2 tickets; <K> blocked; <M> with open dependencies.
> ```

**Example 2 — comment-history read (audit trail):**

> **Brief from POLYBIUS:** "TIRO, comment history on stoa--y14 — I need the full timeline for cross-tier coordination context."
>
> **TIRO action:** `cd <repo> && bw show stoa--y14` (full body + all comments; do NOT use `tail` for an audit trail).
>
> **TIRO return:** structured `answer:` block with each comment timestamped + author-tag-parsed per §7.7.

**Example 3 — write syntax advisory (asking seat executes):**

> **Brief from POLYBIUS:** "TIRO, what's the canonical command to close stoa--y14 with an audit comment naming PR #N merged at sha X?"
>
> **TIRO return:**
> ```
> status: completed
> ticket: <dispatch-ticket-id>
> verdict: pass
> query: "canonical close syntax for stoa--y14 with audit comment + PR cross-ref"
> answer:
>   1. bw comment stoa--y14 "PR #N merged at <sha>. <substantive close-out body>"
>   2. bw close stoa--y14 --reason "<one-line ship summary>"
>   3. bw sync
> cookbook_cite: operating-disciplines.md §12.1 (Commenting + closing; Sync) + §12.3 (Close comment vs --reason)
> summary: Three commands; comment + close + sync. Asking seat executes; TIRO does not.
> ```

The asking seat (POLYBIUS in this example) then runs the commands itself, preserving authorship attribution per A2.

## §1.2. A5 — TIRO install.sh wiring (DAEDALUS sub-decision)

**Pick: add `TIRO` to the existing `CAPTAIN_NAMES` array at all 3 tiers (user / project / subproject), uniform with other CAPTAINs. No per-tier filtering.**

**Concrete edit:** `substrate/install.sh:122-133` — append `TIRO` to the `CAPTAIN_NAMES` array.

```bash
# Before:
CAPTAIN_NAMES=(
  DAEDALUS
  ARGUS
  ADA
  VERA
  CATO
  STRABO
  BARTLEBY
  HERALD
  CURATOR
  ZENO
)

# After (insertion locus: after ZENO; alphabetical-within-group is NOT a current invariant
# — the existing order is "gauntlet pipeline first then support seats"; TIRO is a SUPPORT
# specialist seat, lands in the support cluster after ZENO):
CAPTAIN_NAMES=(
  DAEDALUS
  ARGUS
  ADA
  VERA
  CATO
  STRABO
  BARTLEBY
  HERALD
  CURATOR
  ZENO
  TIRO
)
```

**Rationale for uniform-across-tiers deploy:**

- **Universal-team framing wins.** TIRO is a substrate-specialist seat per SPECIFICATION.md §4.6; the pattern generalizes (future arcs may add similar specialists for git/cron/worktree). Per-tier-conditional deploy would be a one-off scope, contrary to the substrate's universal-team-default discipline (e.g., operating-disciplines.md is deployed at all 3 tiers).
- **User-tier POLYBIUS dispatches TIRO too.** Per directive A6, cross-tier or cross-project bw queries are exactly the case where user-tier POLYBIUS most benefits from TIRO. Per the empirical anchor (2026-05-17 three-audit confabulation), it was USER-TIER POLYBIUS that demonstrated the failure mode. Refusing TIRO at user-tier would lock TIRO away from the seat that surfaced the need.
- **install.sh's existing per-tier asymmetries are MAJOR-specific, not CAPTAIN-specific.** install.sh lines 437-521 show that the per-tier branching is on MAJOR file suffixing + CLAUDE.md modification + USER_TIER_DIR substitution; CAPTAIN deploy is uniform across all 3 tiers (lines 653-676). TIRO inherits the existing uniform-CAPTAIN-deploy mechanism with no new code path.

**Verification step ADA must run before commit:**

```bash
./substrate/install.sh --target user --dry-run 2>&1 | grep -c "CAPTAIN_TIRO"
# Must return: 1 (TIRO listed in the dry-run plan)

./substrate/install.sh --target project --project-dir /tmp/dummy-proj --dry-run 2>&1 | grep -c "CAPTAIN_TIRO"
# Must return: 1 (with _<slug> suffix in the dry-run output)

./substrate/install.sh --target subproject --parent-dir /tmp/dummy-proj --subproject sub1 --dry-run 2>&1 | grep -c "CAPTAIN_TIRO"
# Must return: 1 (with _sub1 suffix)
```

The 3 dry-runs are non-destructive; they verify the install.sh deploy plan lists TIRO at every target mode without writing anything.

**Validation step VERA must run as a Phase 3 probe:** see §1.5 below.

## §1.3. A6 — Cross-refs (LOCKED scope, DAEDALUS picks exact wording + insertion points)

Four cross-ref edits across existing substrate files. Each carries a cite-comment per A17 so future readers can verify the cite resolves at the read site.

### §1.3.1. `substrate/MAJOR_POLYBIUS.md` §7

**Insertion locus:** new paragraph at the END of `§7.3 Working with beadwork — command syntax` (i.e., after line 433, before the `### 7.4` heading). §7.3 already cross-refs `operating-disciplines.md §12` as the canonical cookbook; the new paragraph adds the TIRO specialist-delegation note.

**Exact wording:**

```markdown
**Specialist delegation — CAPTAIN_TIRO.** For read queries (especially completeness audits across cross-tier or cross-project bw stores), dispatch CAPTAIN_TIRO per `operating-disciplines.md` §12 + `substrate/CAPTAIN_TIRO.md`. TIRO's whole-context priming on bw mechanics absorbs the "generalist forgets `--all`" failure mode that motivated the seat (2026-05-17 empirical anchor: three POLYBIUS audits on a single day each citing truncated bw output as live state). Writes (create, comment, close, dep add, sync) stay with this seat; TIRO advises on syntax when asked but never executes writes on POLYBIUS's behalf. <!-- cite: SPECIFICATION.md §4.6 (TIRO scope-lock) + operating-disciplines.md §19.6 (attestation-confabulation root cause) -->
```

### §1.3.2. `substrate/MAJOR_PLINY.md` §6

**Insertion locus:** new paragraph at the END of `§6.1 Working with beadwork — command syntax` (i.e., after line 605, before the `### 6.2` heading). §6.1 already cross-refs `operating-disciplines.md §12`; the new paragraph adds the TIRO specialist-delegation note.

**Exact wording:**

```markdown
**Specialist delegation — CAPTAIN_TIRO.** During arc execution, dispatch CAPTAIN_TIRO for bw read queries (ticket lookups, comment histories, completeness audits across the parent epic's child set) per `operating-disciplines.md` §12 + `substrate/CAPTAIN_TIRO.md`. Consult TIRO for write syntax when uncertain (the `-m`-isn't-real / dep-direction / HEREDOC / `--reason`-flag gotchas all live in TIRO's whole context). Writes stay with the seat that owns the work; TIRO returns syntax, you execute. <!-- cite: SPECIFICATION.md §4.6 + operating-disciplines.md §12 -->
```

### §1.3.3. `substrate/operating-disciplines.md` §12 (bw cookbook)

**Insertion locus:** new paragraph at the END of `§12.4 Per-role specifics` (i.e., after line 795 — the existing per-role-specifics section ends at "Pair-programmer Majors" bullet; new paragraph before the "Empirical anchor:" paragraph at line 797).

**Exact wording:**

```markdown
- **CAPTAIN_TIRO (bw substrate specialist; new Arc 38):** the cookbook above is reference material; TIRO is the dispatched specialist seat agents delegate to for the read use cases the cookbook covers — completeness audits (apply `--all`), comment-history reads, cross-tier ticket lookups. TIRO does NOT execute writes on another seat's behalf (per PRINCIPAL-locked split at SPECIFICATION.md §4.6); TIRO advises on write syntax when asked + the asking seat executes the commands itself. Full envelope: `substrate/CAPTAIN_TIRO.md`. <!-- cite: SPECIFICATION.md §4.6 + §9.1 -->
```

### §1.3.4. Gauntlet-seat CAPTAINs (DAEDALUS picks WHICH need cross-refs)

Per directive A6: "DAEDALUS picks which need cross-refs; ADA + ARGUS + VERA + CATO + ZENO commonly use bw for ticket reads + verdict writes."

**Pick: add a thin cross-ref note to TWO seats: CAPTAIN_ADA and CAPTAIN_CATO.** Rationale:

- **ADA** runs verdict writes routinely + reads ticket bodies for grounding during builds. The `bw show <ticket>` read for grounding is the most-empirically-exercised bw operation across the gauntlet (every ADA dispatch starts with one). ADA benefits from knowing TIRO is the delegated seat for any multi-ticket read.
- **CATO** runs cross-ticket reads during review (verifying cite-comments resolve, tracing prior-arc tickets for craft consistency). CATO's review work is the second-largest bw-read consumer after ADA.

**Why NOT all gauntlet seats:**

- ARGUS reads the design + the dispatch brief; ARGUS rarely needs cross-ticket bw context (the design carries it). Adding a TIRO note risks scope-creep on ARGUS's plan-critique work.
- VERA exercises probes; the probes name what to verify. VERA does not typically run multi-ticket bw reads.
- ZENO mechanical-checks spec-vs-result; reads tickets named in the deliverables list. Same low-bw-read load as VERA.
- DAEDALUS is the design seat (this very seat); DAEDALUS reads tickets + research input the dispatch brief names. The CAPTAIN_DAEDALUS.md envelope already cross-refs operating-disciplines.md §12 + §18 (bw heartbeat); adding a TIRO note here would create a recursion artifact (the design seat references the specialist seat the design ships).

**Insertion locus for ADA:** at the end of CAPTAIN_ADA.md's "What you do NOT write" or equivalent section — DAEDALUS leaves the exact section pick to ADA (the ADA envelope is the seat ADA is implementing AGAINST; DAEDALUS does not arbitrate ADA's own envelope structure preemptively). Reference text:

```markdown
**For bw audits across multiple tickets, dispatch CAPTAIN_TIRO** per `operating-disciplines.md` §12 + `substrate/CAPTAIN_TIRO.md`. TIRO returns structured ticket-lists with correct completeness flags; you read the answer and proceed. Single-ticket `bw show <id>` for grounding stays inline at this seat. <!-- cite: SPECIFICATION.md §4.6 -->
```

**Insertion locus for CATO:** at the end of CATO's "tools/scope" or equivalent section. Reference text:

```markdown
**For cross-ticket review (verifying cite-comments resolve, tracing prior-arc context for craft consistency), dispatch CAPTAIN_TIRO** per `operating-disciplines.md` §12 + `substrate/CAPTAIN_TIRO.md`. TIRO returns the multi-ticket read in one structured answer; review continues with the answer in-context. <!-- cite: SPECIFICATION.md §4.6 -->
```

ADA implements per the wording above; ADA picks the exact insertion section header in each envelope based on the current section structure (which may have rotated since the dispatch).

## §1.4. A18 — Authorship attribution (IMMUTABLE per CLAUDE.md)

`substrate/CAPTAIN_TIRO.md` MUST carry `author: Denson Smith` in YAML frontmatter per Arc 27 stoa--uly convention. ADA verifies pre-commit; ZENO mechanical-checks in Phase 3.

**Exact frontmatter shape:**

```yaml
---
name: CAPTAIN_TIRO{{NAME_SUFFIX}}
description: "bw substrate specialist; delegated reads (with correct completeness flags) and write-advisory (returns syntax, never executes writes for another seat)."
tools: Bash, Read, Grep, Glob
model: opus
author: Denson Smith
---
```

**Pre-commit verification command for ADA:**

```bash
head -10 substrate/CAPTAIN_TIRO.md | grep -c "^author: Denson Smith$"
# Must return: 1
```

## §1.5. Verification probes (VERA exercises in Phase 3)

Three probes for C1. Probe #1 is structural (file shape conforms to CAPTAIN envelope); Probe #2 is install.sh dry-run; Probe #3 is the load-bearing "TIRO is dispatchable + returns a sensible answer" smoke.

### §1.5.1. Probe 1 — TIRO role file structural conformance

```bash
# Must return: 1 (file exists)
test -f substrate/CAPTAIN_TIRO.md && echo 1

# Must return: 1 (YAML frontmatter present)
head -1 substrate/CAPTAIN_TIRO.md | grep -c "^---$"

# Must return: 1 (author field correct per A18 IMMUTABLE)
head -10 substrate/CAPTAIN_TIRO.md | grep -c "^author: Denson Smith$"

# Must return: 1 (toolset matches A3 LOCKED)
head -10 substrate/CAPTAIN_TIRO.md | grep -c "^tools: Bash, Read, Grep, Glob$"

# Must return: 0 (no Write/Edit in toolset — TIRO is read-direct + write-advisory)
head -10 substrate/CAPTAIN_TIRO.md | grep -cE "tools:.*\b(Write|Edit)\b"

# Must return: at least 1 of each (the load-bearing sections exist)
grep -c "## 1\. Your one job" substrate/CAPTAIN_TIRO.md
grep -c "Read-direct" substrate/CAPTAIN_TIRO.md
grep -c "write-advisory" substrate/CAPTAIN_TIRO.md
grep -c "PRINCIPAL-locked" substrate/CAPTAIN_TIRO.md       # the split-discipline cite
grep -c "operating-disciplines.md.*§12" substrate/CAPTAIN_TIRO.md   # cookbook cite
```

### §1.5.2. Probe 2 — install.sh dry-run lists TIRO at all 3 tiers

```bash
# At user-tier (filename unsuffixed)
./substrate/install.sh --target user --dry-run 2>&1 | grep -c "CAPTAIN_TIRO\.md"
# Must return: at least 1

# At project-tier (filename suffixed with _<slug>)
mkdir -p /tmp/tiro-install-probe
./substrate/install.sh --target project --project-dir /tmp/tiro-install-probe --dry-run 2>&1 \
  | grep -c "CAPTAIN_TIRO_tiro_install_probe\.md"
# Must return: at least 1
rm -rf /tmp/tiro-install-probe

# At subproject-tier (filename suffixed with _<subproject-slug>)
mkdir -p /tmp/tiro-parent-probe
./substrate/install.sh --target subproject --parent-dir /tmp/tiro-parent-probe --subproject testsub --dry-run 2>&1 \
  | grep -c "CAPTAIN_TIRO_testsub\.md"
# Must return: at least 1
rm -rf /tmp/tiro-parent-probe
```

### §1.5.3. Probe 3 — TIRO dispatchable + returns sensible structured answer

VERA dispatches TIRO with a known-good query and inspects the structured return.

```
[VERA brief to TIRO]
operating-mode: hitl
ticket: <Arc 38 probe ticket; VERA picks or PLINY supplies>
query: "list all closed tickets in the-stoa bw store filed before 2026-05-01"
expected verdict: pass
expected answer shape: structured list of {ticket-id, title, close-date}
```

**Pass criteria:**

- TIRO's verdict block parses as a valid CAPTAIN return (status / ticket / verdict / query / answer / cookbook_cite / summary fields present per §1.1.1 step 7).
- TIRO does NOT attempt to write any tickets / comments / closes / deps.
- TIRO's `cookbook_cite:` resolves to `operating-disciplines.md §12.1` (the closed-status filtering surface).
- TIRO's `answer:` is structurally consistent with `bw list --status closed --all` output for the named query.

**Anti-pass criteria (fail flags):**

- TIRO writes to bw on another seat's behalf (toolset enforcement + envelope discipline should both prevent this; if it happens, structural failure).
- TIRO returns the answer WITHOUT applying `--all` (truncation hidden — the empirical-anchor failure mode TIRO exists to absorb).
- TIRO refuses the query as "not a read" (false negative; the query is paradigmatically a TIRO read).

## §1.6. Cite-comment plan for C1

Per A17, every cross-ref TIRO ships carries a cite-comment at the read site. Concretely, the cite-comments ADA writes are:

| File | Read-site (approx line) | Cite-comment content |
|---|---|---|
| `substrate/CAPTAIN_TIRO.md` | top of §6.2 (read-direct/write-advisory boundary) | `<!-- cite: SPECIFICATION.md §4.6 (PRINCIPAL-locked split, 2026-05-17) + operating-disciplines.md §19.6 (attestation-confabulation root cause) -->` |
| `substrate/CAPTAIN_TIRO.md` | top of §6.3 (bw subcommand reference) | `<!-- cite: operating-disciplines.md §12 (the cookbook this seat operationalizes) -->` |
| `substrate/CAPTAIN_TIRO.md` | top of §6.5 (heartbeat-and-read-before-write) | `<!-- cite: operating-disciplines.md §18 (universal-team framing) + MAJOR_PLINY.md §5.8 (Monitor + bw-poll bridge) -->` |
| `substrate/MAJOR_POLYBIUS.md` | end of §7.3 | `<!-- cite: SPECIFICATION.md §4.6 (TIRO scope-lock) + operating-disciplines.md §19.6 (attestation-confabulation root cause) -->` |
| `substrate/MAJOR_PLINY.md` | end of §6.1 | `<!-- cite: SPECIFICATION.md §4.6 + operating-disciplines.md §12 -->` |
| `substrate/operating-disciplines.md` | end of §12.4 | `<!-- cite: SPECIFICATION.md §4.6 + §9.1 -->` |
| `substrate/CAPTAIN_ADA.md` | (ADA picks section) | `<!-- cite: SPECIFICATION.md §4.6 -->` |
| `substrate/CAPTAIN_CATO.md` | (ADA picks section) | `<!-- cite: SPECIFICATION.md §4.6 -->` |

## §1.7. Self-application per A14 (chicken/egg surfaced)

DAEDALUS observed during this design: when researching the directive's "open ticket sequencing" reference (looking at `stoa--ojz`, `stoa--bj5`, `stoa--gq1` plus implicit cross-refs), `bw list --all` was used directly per `operating-disciplines.md` §12.1 — TIRO does not exist yet. Friction observed: NONE; the cookbook surfaced the right flag and the read was clean. This is **NEGATIVE empirical-anchor reinforcement** — for a 3-ticket read with the cookbook at hand, the failure mode does NOT surface. The failure-mode anchor (2026-05-17 three-audit confabulation) was a COMPLETENESS AUDIT (`bw list --status open` at large N where truncation matters); the design-research read was a SMALL TARGETED LOOKUP. Both are valid TIRO use cases, but the failure mode is asymmetric across them. ADA may observe the same asymmetry during build; if so, surface in build-commit message as forward audit-feedback. If ADA hits a multi-ticket completeness read during build and the failure mode DOES surface, document inline as POSITIVE empirical-anchor reinforcement.

---

# PART 2 — C2: User-tier substrate drift detection (stoa--bj5)

## §2.1. Approach

Extend `substrate/skills/check-substrate-updates/` to handle user-tier (`~/.claude/`) workspaces. The blocker since 2026-05-14 is that user-tier deployed files carry install.sh substitutions that can't be cleanly reversed for the diff against canon source.

Two coordinated extensions per directive A8/A9/A10:

1. **Per-file-marker scheme (A8)** — install.sh writes a manifest at user-tier that records substitutions per-deployed-file; check.sh reads the manifest to normalize the deployed file before diffing.
2. **Registry shape (A9)** — extend `consumer-workspaces.txt` to register the user-tier path (or add a separate user-tier registry / tier-tag annotation; DAEDALUS picks below).
3. **Per-script changes (A10)** — check.sh / apply.sh / revert.sh each absorb the user-tier path with minimal divergence from the existing project-tier code path.

### §2.1.1. Spike findings (Phase 1, completed before A8 finalized)

Per the dispatch brief Phase 1 requirement:

- `ls substrate/skills/check-substrate-updates/` → `SKILL.md`, `check.sh`, `apply.sh`, `revert.sh`. **Unchanged since bj5 was filed (2026-05-14).**
- `cat substrate/consumer-workspaces.txt` → 4 project-tier workspaces registered; user-tier explicitly out-of-scope per the comment block ("v0 scope: project-tier and subproject-tier only. User-tier check is future work").
- No new bw 0.14.0 substitution-tracking primitive in evidence (none cited in install.sh or check.sh; no bw subcommand for substitution-tracking exists per `bw --help`). **A8 stays inside the α/β/γ/δ candidate space** — no need to surface as PRINCIPAL-gate per §25.

Confirms the spike: the bj5 design space is unchanged. A8 picks below.

### §2.1.2. The substitution surface (load-bearing for A8 sizing)

Reading install.sh lines 614-628 + 660-672 confirms the user-tier substitution surface is THIN:

| Deployed file | Substitution at user-tier | Substitution token |
|---|---|---|
| `~/.claude/MAJOR_POLYBIUS.md` | YES — non-trivial | `{{USER_TIER_DIR}}` → real path (e.g., `/c/Users/denso/claude_projects`) |
| `~/.claude/MAJOR_POLYBIUS.md` | YES — trivial (empty replacement) | `{{NAME_SUFFIX}}` → `` (empty string) |
| `~/.claude/MAJOR_PLINY.md` | YES — trivial only | `{{NAME_SUFFIX}}` → `` (empty string) |
| `~/.claude/agents/CAPTAIN_*.md` (all 10, including new TIRO) | YES — trivial only | `{{NAME_SUFFIX}}` → `` (empty string) |
| `~/.claude/operating-disciplines.md` | NO — verbatim cp | (none) |
| `~/.claude/templates/*.md` | NO — verbatim cp | (none) |
| `~/.claude/skills/**/*` | NO — verbatim cp | (none) |

**The only substitution that creates a real diff problem at user-tier is `{{USER_TIER_DIR}}` in `MAJOR_POLYBIUS.md`.** The `{{NAME_SUFFIX}}` substitution is empty-string at user-tier, so the deployed file is byte-equal to the source-after-`sed-s///g`-on-empty-pattern. (Verify: the source `MAJOR_POLYBIUS{{NAME_SUFFIX}}.md` after `sed s/{{NAME_SUFFIX}}//g` returns `MAJOR_POLYBIUS.md` for the title block; no other `{{NAME_SUFFIX}}` references at line-content level.)

**Implication:** the per-file-marker scheme's load-bearing fixture is ONE substitution (`{{USER_TIER_DIR}}` in one file). The manifest's value as single-source-of-truth is in being FORWARD-COMPATIBLE: future substrate changes that introduce new substitutions absorb into the manifest by adding entries; check.sh reads the manifest without schema change.

## §2.2. A8 — Per-file-marker scheme (DAEDALUS sub-decision)

**Pick: γ — Manifest file per workspace.** Per directive A8 + user-tier POLYBIUS lean. Concrete shape below.

### §2.2.1. Manifest file shape

**Path:** `<workspace>/.claude/.substrate-manifest`

**Format:** simple key-value lines, one substitution per line, file-scoped via a leading filename token:

```
# Stoa substrate deploy manifest — substitutions applied to deployed files.
# Written by install.sh at deploy time. Read by check.sh + apply.sh to normalize.
# Format: <deployed-relative-path>\t<token>\t<replacement>
# DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run.
#
# tier=user
# deployed_at=2026-05-18T03:30:00Z
# substrate_sha=<sha at deploy>

.claude/MAJOR_POLYBIUS.md	{{USER_TIER_DIR}}	/c/Users/denso/claude_projects
.claude/MAJOR_POLYBIUS.md	{{NAME_SUFFIX}}	
.claude/MAJOR_PLINY.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_DAEDALUS.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_ARGUS.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_ADA.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_VERA.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_CATO.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_STRABO.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_BARTLEBY.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_HERALD.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_CURATOR.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_ZENO.md	{{NAME_SUFFIX}}	
.claude/agents/CAPTAIN_TIRO.md	{{NAME_SUFFIX}}	
```

**Design choices:**

- **Tab-separated (TSV-style)** so substitution values can contain spaces, paths with slashes, etc. without escaping. Tabs are nearly absent from filesystem paths + tokens, so collision risk is near-zero. (Defensive guard: install.sh refuses to write a manifest entry where the substitution value contains a literal tab character; reported as an error.)
- **Empty replacement values are valid lines** (`{{NAME_SUFFIX}}` at user-tier is empty). Parser must distinguish "empty replacement" from "missing entry."
- **Header block (3 lines starting with `# tier=` / `# deployed_at=` / `# substrate_sha=`)** carries the per-manifest metadata. Reading these unblocks: tier-detection without re-walking install.sh logic; deploy-time forensics; substrate-sha comparison without a separate state file.
- **File-class scope inherited from install.sh.** Only the file classes that install.sh sed-substitutes get manifest entries (MAJORs + CAPTAINs). Templates + skills are deployed verbatim by install.sh and require NO manifest entries; check.sh continues to byte-compare them directly per the existing project-tier path.

### §2.2.2. Why γ over α / β / δ

Per directive A8 candidate space:

- **(α) Embedded marker in each deployed file.** REJECTED: pollutes every deployed file with non-canon comment lines. Future install.sh re-runs would have to parse + strip the marker before comparing; the marker becomes a load-bearing source-side feature. Worse for substrate hygiene than a sidecar.
- **(β) Sidecar `.substrate-state` per deployed file.** REJECTED: 2-file pairs to maintain; sidecar can be deleted independently of file (creating drift between the substitution record and the file it records); doubles the filesystem footprint. The single-source-of-truth invariant collapses.
- **(γ) Manifest file per workspace.** PICKED. Single source of truth per workspace. Survives file moves/renames within the workspace because the manifest path is relative to workspace root, not relative to file. install.sh rewrites the manifest on every re-run, so it cannot drift from the actual deploy state UNDER substrate-tool operations; manual edits of deployed files are the operator's responsibility (and surface as DRIFTED via check.sh — the existing detection path). Matches the rest of the substrate's design (one canon source; one deployed manifest per workspace).
- **(δ) Reverse-substitution attempt.** REJECTED: heuristic; fails when substitution patterns are ambiguous. The `{{USER_TIER_DIR}}` case is the load-bearing fixture (path like `/c/Users/denso/claude_projects` could appear in canon source for unrelated reasons — e.g., a doc-comment example path); reverse-substitution can't distinguish "this path is a substitution-replacement" from "this path is canon-literal." Probabilistic correctness is not acceptable for a drift-detection tool.

### §2.2.3. Manifest failure modes (named for ARGUS scrutiny)

- **Manifest missing at check time.** check.sh treats a missing `.substrate-manifest` at user-tier as "workspace was deployed before manifest support shipped" — falls back to the existing v0 friendly message ("user-tier check is out of v0 scope; re-run install.sh to deploy the manifest"). Existing project-tier workspaces don't need a manifest (substitutions there are derivable from the workspace's basename per check.sh's `detect_tier` function); the manifest is user-tier-ADDITIVE, not project-tier-REQUIRED.
- **Manifest stale (deployed-substrate sha differs from registered).** Surface as a check.sh warning (not an error): "manifest registered against substrate sha X; current substrate at sha Y; re-deploy via install.sh." The DRIFTED detection itself still works (manifest's substitution-token/value pairs are still the right normalization input); the warning prompts operator action.
- **Manifest manually edited.** Same as the project-tier "deployed file manually edited" case — surfaces as DRIFTED. The manifest is install.sh's output; operator should not edit. Header comment names this explicitly: "DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run."
- **Manifest entry references a deployed file that no longer exists.** Stale manifest entry; check.sh ignores (the file-not-present case is handled by the existing MISSING-detection path). install.sh rewrites the manifest on next deploy and stale entries drop out.

### §2.2.4. install.sh wiring for manifest write

Insertion locus: NEW step in install.sh after step 7 (staleness detection, line 805) and before step 7b (custom-files visibility, line 949). The manifest write is the LAST step before the final "install.sh: done" line (other than the optional next-step guidance in step 8).

**New function in install.sh helpers section (after `scaffold_user_tier`, ~line 370):**

```bash
# write_substrate_manifest <dest-dir> <tier> <slug>
#
# Writes <dest-dir>/.substrate-manifest recording every substitution applied to
# deployed files in this run. Used by check.sh + apply.sh at user-tier (where
# the {{USER_TIER_DIR}} substitution can't be reliably reverse-derived; A8 bj5).
# Project-tier + subproject-tier workspaces also get the manifest written
# (uniform behavior; check.sh continues to derive substitutions from workspace
# basename at those tiers and the manifest is informational).
#
# Format: tab-separated triples (deployed-rel-path \t token \t replacement),
# preceded by a header block.
write_substrate_manifest() {
  local dest="$1"
  local tier="$2"
  local slug="$3"
  local manifest="${dest}/.substrate-manifest"
  local name_suffix=""

  case "$tier" in
    project|subproject) name_suffix="_${slug}" ;;
  esac

  local now sha
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  sha="$(cd "$SCRIPT_DIR" && git rev-parse --short HEAD 2>/dev/null || echo unknown)"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] write: $manifest (tier=$tier, deployed_at=$now, substrate_sha=$sha)"
    return 0
  fi

  {
    echo "# Stoa substrate deploy manifest — substitutions applied to deployed files."
    echo "# Written by install.sh at deploy time. Read by check.sh + apply.sh to normalize."
    echo "# Format: <deployed-relative-path>\\t<token>\\t<replacement>"
    echo "# DO NOT EDIT MANUALLY. install.sh rewrites this file on every re-run."
    echo "#"
    echo "# tier=${tier}"
    echo "# deployed_at=${now}"
    echo "# substrate_sha=${sha}"
    echo ""
    # MAJOR_POLYBIUS.md: NAME_SUFFIX always; USER_TIER_DIR at user-tier only.
    if [ "$tier" = "subproject" ]; then
      printf ".claude/MAJOR_POLYBIUS%s.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}" "${name_suffix}"
      printf ".claude/MAJOR_PLINY%s.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}" "${name_suffix}"
    else
      printf ".claude/MAJOR_POLYBIUS.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}"
      printf ".claude/MAJOR_PLINY.md\t{{NAME_SUFFIX}}\t%s\n" "${name_suffix}"
      if [ "$tier" = "user" ] && [ -n "$USER_TIER_DIR" ]; then
        printf ".claude/MAJOR_POLYBIUS.md\t{{USER_TIER_DIR}}\t%s\n" "$USER_TIER_DIR"
      fi
    fi
    # CAPTAINs (always NAME_SUFFIX — empty at user-tier; _<slug> at project/subproject).
    if [ "$WITH_CAPTAINS" -eq 1 ]; then
      for name in "${CAPTAIN_NAMES[@]}"; do
        printf ".claude/agents/CAPTAIN_%s%s.md\t{{NAME_SUFFIX}}\t%s\n" "$name" "${name_suffix}" "${name_suffix}"
      done
    fi
  } > "$manifest"
  echo "wrote manifest: $manifest"
}
```

**Insertion site of the call** (after step 7 staleness scan, before step 7b custom-files visibility):

```bash
# 7c. Write substrate manifest (Arc 38 / bj5 / A8). Records substitutions applied
# to deployed files so check.sh can normalize before diffing. Universal across all
# 3 tiers (the load-bearing user-tier case is the {{USER_TIER_DIR}} substitution
# in MAJOR_POLYBIUS.md; project-tier + subproject-tier write informational manifests).
write_substrate_manifest "$DEST_DIR" "$TARGET" "$PROJECT_SLUG"
```

### §2.2.5. check.sh changes for manifest read

The existing `apply_substitutions()` function (check.sh:107-130) is FILE-CLASS-SCOPED — it sed-substitutes only MAJOR + CAPTAIN files based on hard-coded path patterns. For the user-tier extension, the function rewrites to be MANIFEST-DRIVEN: it reads the workspace's `.substrate-manifest`, looks up the relevant substitutions for the deployed file at hand, and applies them.

**The new `apply_substitutions_from_manifest()` function** (replaces or augments the existing `apply_substitutions()` at check.sh:107-130 and apply.sh:87-104 — DAEDALUS picks REPLACE for the user-tier path with FALLBACK to the existing hard-coded path when no manifest is present):

```bash
# apply_substitutions_from_manifest <source-file> <deployed-rel-path> <workspace-abs>
#
# Manifest-driven substitution for user-tier (bj5; A8). Falls back to the existing
# hard-coded apply_substitutions for project-tier + subproject-tier (where the
# substitution surface is derivable from the workspace basename + the file path).
#
# Reads <workspace-abs>/.substrate-manifest if present; for the named deployed-rel-path,
# applies every (token, replacement) entry via sed. If no manifest present, falls back
# to apply_substitutions (legacy code path; project-tier + subproject-tier behavior is
# unchanged from pre-Arc-38).
apply_substitutions_from_manifest() {
  local source_file="$1"
  local dep_rel="$2"
  local ws_abs="$3"
  local manifest="${ws_abs}/.substrate-manifest"

  if [ ! -f "$manifest" ]; then
    # No manifest — fall back to legacy hard-coded substitution (project-tier
    # path is unchanged from pre-Arc-38; the legacy function takes tier+slug).
    local tier_line tier slug
    tier_line="$(detect_tier "$ws_abs")"
    tier="${tier_line%% *}"
    slug="${tier_line#* }"; slug="${slug# }"
    apply_substitutions "$source_file" "$dep_rel" "$tier" "$slug"
    return 0
  fi

  # Manifest present — read every (token, replacement) entry for this deployed-rel-path
  # and apply them via sed pipeline.
  local sed_expr=""
  while IFS=$'\t' read -r entry_path token replacement; do
    # Skip comments + blanks
    case "$entry_path" in
      ""|\#*) continue ;;
    esac
    if [ "$entry_path" = "$dep_rel" ]; then
      # Append a -e expression. Use | as delimiter (avoid / collision with paths).
      # Defensive: refuse to substitute if either token or replacement contains | literal.
      case "$token$replacement" in
        *"|"*)
          # Fall back to legacy substitution — manifest entry can't safely sed.
          # Defensive; the install.sh writer should reject these at write time.
          continue
          ;;
      esac
      sed_expr="${sed_expr} -e s|${token}|${replacement}|g"
    fi
  done < "$manifest"

  if [ -z "$sed_expr" ]; then
    # No substitution entries for this file — verbatim passthrough.
    cat "$source_file"
  else
    eval "sed ${sed_expr} \"$source_file\""
  fi
}
```

**Update sites in check.sh** (the existing call at check.sh:691 `apply_substitutions "$src_abs" "$dep" "$tier" "$slug"` rewrites to `apply_substitutions_from_manifest "$src_abs" "$dep" "$ws_abs"`).

**Update sites in apply.sh** (the existing call at apply.sh:308 same pattern).

### §2.2.6. check.sh user-tier detection rewrite

The existing check.sh:624-631 user-tier branch bails with the friendly out-of-scope message. The Arc 38 rewrite: detect user-tier, look for `.substrate-manifest`, if present proceed with manifest-driven substitution; if absent, fall back to the existing friendly message (telling the operator to re-run install.sh to deploy the manifest).

```bash
if [ "$tier" = "user" ]; then
  # Arc 38 (bj5; A8) — user-tier check support via manifest-driven substitution.
  # If no manifest at the workspace, fall back to the pre-Arc-38 friendly message.
  local manifest="${ws_abs}/.substrate-manifest"
  if [ ! -f "$manifest" ]; then
    printf "%-40s USER-TIER (manifest missing — re-run install.sh --target user to deploy)\n" "$label"
    echo "  The Arc 38 bj5 extension uses a manifest at <workspace>/.substrate-manifest"
    echo "  to record substitutions applied by install.sh. The current deploy predates"
    echo "  the manifest. Re-run install.sh --target user to write the manifest, then"
    echo "  re-run check.sh."
    return 0
  fi
  # Manifest present — proceed with normal check pass (Pass 1 DRIFTED + MISSING,
  # Pass 2 OBSOLETE, Pass 3 uncommitted) using manifest-driven substitution.
  # The existing code path falls through here; the only changed call site is
  # apply_substitutions -> apply_substitutions_from_manifest.
fi
```

Note: at user-tier the `detect_tier` function already returns `"user "` and the rest of check.sh's Pass 1/2/3 logic works against `~/.claude/` as workspace root. The only change is the substitution path. Existing project-tier behavior is unchanged.

## §2.3. A9 — User-tier registry (DAEDALUS picks shape)

**Pick: extend the existing `consumer-workspaces.txt` registry to include the user-tier path; no new file; no tier-tag annotation.**

**Concrete edit to `substrate/consumer-workspaces.txt`:**

```
# Consumer workspaces for the stoa substrate-update check skill.
# One absolute path per line. Comments (#) and blank lines are ignored.
#
# Used by substrate/skills/check-substrate-updates/check.sh to know which
# workspaces to scan for drift between deployed substrate files and the
# current the-stoa source. Add a new workspace by appending its absolute
# path here.
#
# As of Arc 38 (stoa--bj5): user-tier workspaces (~/.claude/) are supported
# via the per-deploy manifest written by install.sh (.substrate-manifest);
# previously user-tier was friendly-no-op'd per the {{USER_TIER_DIR}}
# substitution-tracking blocker. Add the user-tier workspace by appending
# the absolute path to ~/.claude (NOT to ~/; tier-detection looks for
# .claude/MAJOR_POLYBIUS*.md to confirm a stoa deploy).

/c/Users/denso/claude_projects/ariadne-core-workspace
/c/Users/denso/claude_projects/railway_stoa
/c/Users/denso/claude_projects/sector-4
/c/Users/denso/claude_projects/the-stoa
/c/Users/denso/.claude
```

**Rationale for "extend existing file vs new file vs annotation":**

- **Extend existing file (PICKED).** Single registry; check.sh's existing file-walk continues to work; tier-detection inside check.sh (`detect_tier`) already distinguishes user-tier from project-tier from subproject-tier (the `$ws_abs = $HOME/.claude` test, check.sh:251). NO change to the registry's parse logic; NO change to check.sh's file-walk; only the tier-branched HANDLING changes (which is the A8 / A10 work above).
- **New file (REJECTED).** Two registries to keep in sync; check.sh would need a second file-walk loop; the user-tier "workspace" is a different shape (path is `~/.claude`, not `<parent>/<project-name>`) but check.sh's tier-detection already absorbs that asymmetry. Splitting the registry doubles the failure surface for no gain.
- **Tier-tag annotation (REJECTED).** E.g., `/c/Users/denso/.claude  # tier:user`. Adds a parse step (extract tag) for what `detect_tier` already derives from the path. Annotations drift from reality if tier-detection rotates; the derivation IS the source of truth. Annotation would be ornamental.

**For the the-stoa repo specifically** (the registry seed shipped at the substrate-source layer): the user-tier path is PRINCIPAL-machine-specific (`/c/Users/denso/.claude` on Denson's machine; other users would have different absolute paths). The shipped registry adds the line as a worked-example with a comment noting it's PRINCIPAL-specific:

**Actually, REVISED RECOMMENDATION** (per ARGUS scrutiny consideration): the shipped registry should NOT include the absolute user-tier path as canon (it's machine-specific). Instead, the comment block above DOCUMENTS how to add a user-tier line at install time, and the registry file SHIPS WITH the 4 project-tier lines unchanged. PRINCIPAL (or POLYBIUS) appends the user-tier line per-machine. The Arc 38 build does NOT modify the shipped registry's line content; it only updates the comment block.

This is the conservative read; the alternative (ship the user-tier line as the 5th entry) would be the demo-friendly read but creates a substrate-tier vs PRINCIPAL-machine coupling. **DAEDALUS picks the conservative read.** ADA's commit modifies the comment block only; PRINCIPAL or POLYBIUS appends the user-tier path manually (or via the opportunistic self-application path described in §2.6 below).

**Updated `substrate/consumer-workspaces.txt` (canonical shape ADA ships):**

```
# Consumer workspaces for the stoa substrate-update check skill.
# One absolute path per line. Comments (#) and blank lines are ignored.
#
# Used by substrate/skills/check-substrate-updates/check.sh to know which
# workspaces to scan for drift between deployed substrate files and the
# current the-stoa source. Add a new workspace by appending its absolute
# path here.
#
# Tiers supported as of Arc 38 (stoa--bj5):
#   - project-tier (e.g., /path/to/some-project, containing .claude/MAJOR_POLYBIUS.md)
#   - subproject-tier (e.g., /path/to/parent/sub, containing .claude/MAJOR_POLYBIUS_<slug>.md)
#   - user-tier (~/.claude/ — supported via the .substrate-manifest written by install.sh)
#
# For user-tier check support, append the absolute path to ~/.claude. The path
# is PRINCIPAL-machine-specific (it varies per OS + per user), so it is not
# shipped as a default entry; PRINCIPAL or POLYBIUS appends per-machine after
# install.sh --target user has been run (which writes the .substrate-manifest
# the check depends on).

/c/Users/denso/claude_projects/ariadne-core-workspace
/c/Users/denso/claude_projects/railway_stoa
/c/Users/denso/claude_projects/sector-4
/c/Users/denso/claude_projects/the-stoa
```

## §2.4. A10 — Per-script changes (DAEDALUS picks per-script changes)

### §2.4.1. check.sh changes (4 sites)

1. **Replace `apply_substitutions` with `apply_substitutions_from_manifest` at the call site** (line 691). Existing `apply_substitutions` stays in the file as the FALLBACK called from inside `apply_substitutions_from_manifest` for the project-tier no-manifest case (or for transient state during install.sh re-run).
2. **Add the new `apply_substitutions_from_manifest` function** in the helpers section (after `apply_substitutions` at line 130).
3. **Rewrite the user-tier branch in `check_workspace`** (lines 624-631) per §2.2.6 above.
4. **Cite-comment block** at the top of the new function citing the A8 design + bj5 ticket per A17:

```bash
# CITE: manifest-driven substitution per Arc 38 / bj5 / design.md §2.2 (A8 γ pick).
# The manifest at <workspace>/.substrate-manifest is written by install.sh at deploy
# time (substrate/install.sh write_substrate_manifest function). If a future install.sh
# change rotates the manifest format, this function must update its parser to match.
# Companion cite at the install.sh writer site references this read-site for the
# format invariant.
```

### §2.4.2. apply.sh changes (3 sites)

1. **Same `apply_substitutions` → `apply_substitutions_from_manifest` swap** at apply.sh:308.
2. **Same new function** (DRY: the function defined in check.sh is duplicated in apply.sh because the two scripts intentionally share-via-inline rather than via a shared lib per the existing convention at check.sh:74-80). Cite-comment per §2.4.1 step 4.
3. **Rewrite the user-tier refusal in apply.sh** (lines 201-204):

```bash
if [ "$TIER" = "user" ]; then
  # Arc 38 (bj5; A8) — user-tier apply supported via .substrate-manifest. If no manifest,
  # fall back to the pre-Arc-38 refusal (telling the operator to re-run install.sh).
  if [ ! -f "${WORKSPACE}/.substrate-manifest" ]; then
    echo "apply.sh: error: user-tier workspace missing .substrate-manifest; re-run install.sh --target user to deploy the manifest, then re-run apply.sh." >&2
    exit 2
  fi
  # Manifest present — proceed with normal apply (per-file consent + diff + git
  # pre-commit safety + running-agent warning); the only changed call site is
  # apply_substitutions -> apply_substitutions_from_manifest.
fi
```

### §2.4.3. revert.sh changes (1 site)

Per the existing revert.sh:50-53 design, revert uses `git checkout <parent-of-apply-commit>` for git-tracked workspaces and `cp` from `.substrate-backups/<timestamp>/` for non-git workspaces. **Neither code path involves substitutions**, so revert.sh works at user-tier IF and ONLY IF the workspace is git-tracked (e.g., user-tier `~/.claude/` would need `git init` + `.claude/` under tracking for the git path; otherwise the backup-dir path kicks in).

**Required change to revert.sh** (small):

- Add the same user-tier detection branch (currently revert.sh has NO tier detection — it just operates on the workspace passed via `--workspace`). The friendly message: "user-tier revert is supported as of Arc 38; the workspace's git status determines the recovery path (git revert vs backup-dir restore). Either path requires a prior apply.sh run."

**Actually, simpler**: revert.sh is GENERIC (doesn't care about tier — it operates on whatever path was passed). The change is to UPDATE the documentation comment at the top of revert.sh to remove any implicit "project-tier only" framing if present (currently there's none; revert.sh comments say "auto-detect git path or backup-dir" without tier-restriction language). NO code change needed; revert.sh works at user-tier transparently.

**For the cite-discipline**: add a comment to revert.sh confirming user-tier is in-scope as of Arc 38:

```bash
# CITE: as of Arc 38 (bj5; A8), user-tier workspaces are in-scope for revert.sh.
# The script is tier-agnostic — it operates on the --workspace path regardless of
# tier; the existing git/backup-dir detection handles both. The user-tier
# substitution-tracking (manifest at <workspace>/.substrate-manifest) is not
# involved at revert-time (revert restores byte-for-byte from git or backup-dir).
# Cross-ref: agents/design/stoa--ojz/design.md §2.4.3 (this design).
```

### §2.4.4. SKILL.md changes

The skill's `SKILL.md` carries a "v0 scope" section that explicitly bills user-tier as OUT OF SCOPE. Rewrite to v1.

**Edits to `substrate/skills/check-substrate-updates/SKILL.md`:**

1. Line 31-32: change "v0 scope and limitations" → "Scope and limitations".
2. Lines 33-41 (the user-tier paragraph): rewrite to reflect Arc 38 support:

```markdown
## Scope and limitations

The skill supports **project-tier**, **subproject-tier**, AND **user-tier** consumer workspaces.

User-tier support (Arc 38, bj5) operates via the `.substrate-manifest` written by `install.sh` at deploy time. The manifest records every substitution `install.sh` applied to the deployed file (notably `{{USER_TIER_DIR}}` in `MAJOR_POLYBIUS.md`); `check.sh` and `apply.sh` read the manifest to normalize deployed files before diffing.

A user-tier workspace whose manifest is missing (e.g., the workspace was deployed before Arc 38 shipped) friendly-no-ops with a message instructing PRINCIPAL to re-run `install.sh --target user` to deploy the manifest. The fallback path is non-destructive.
```

3. Lines 43-49 (the "Other v0 simplifications" bullet list): keep the "no attribution within DRIFTED" / "explicit registry" / "no marker insertion" bullets but rephrase from "v0 simplifications" to "Conscious scope limits". The Arc 38 work doesn't change those scope choices; the only change is user-tier support.

## §2.5. Verification probes (VERA exercises in Phase 3)

Three probes for C2.

### §2.5.1. Probe 1 — manifest written by install.sh dry-run at user-tier

```bash
# Run install.sh --target user --dry-run (non-destructive)
./substrate/install.sh --target user --dry-run 2>&1 | grep -c "write: .*\.substrate-manifest"
# Must return: at least 1 (the manifest write is announced in dry-run)
```

### §2.5.2. Probe 2 — manifest round-trip on a synthetic user-tier deploy

```bash
# Create a throwaway user-tier-shaped deploy in a temp dir (per operating-disciplines.md
# §25.5: probes that mutate real workspaces require explicit PRINCIPAL authorization;
# this probe deliberately operates on a temp dir so no real ~/.claude/ is touched).
TMPDIR_FAKE_USER=$(mktemp -d)
HOME_ORIG="$HOME"
HOME="$TMPDIR_FAKE_USER"
mkdir -p "$HOME/.claude/agents"

# Deploy via install.sh (non-dry-run; against the temp HOME).
./substrate/install.sh --target user --user-tier-dir "$TMPDIR_FAKE_USER/projects"

# Verify manifest exists + has the expected USER_TIER_DIR entry.
test -f "$HOME/.claude/.substrate-manifest" && echo "manifest present"
grep -c "{{USER_TIER_DIR}}" "$HOME/.claude/.substrate-manifest"
# Must return: 1 (the MAJOR_POLYBIUS.md USER_TIER_DIR substitution entry)

# Run check.sh; verdict should be CURRENT (no drift from a fresh deploy).
echo "$HOME/.claude" > /tmp/probe-registry.txt
./substrate/skills/check-substrate-updates/check.sh --registry /tmp/probe-registry.txt 2>&1 \
  | grep -c "CURRENT"
# Must return: 1

# Mutate a deployed file (synthetic drift).
echo "drift line" >> "$HOME/.claude/MAJOR_POLYBIUS.md"
./substrate/skills/check-substrate-updates/check.sh --registry /tmp/probe-registry.txt 2>&1 \
  | grep -c "DRIFTED"
# Must return: 1 (drift detected via manifest-normalized comparison)

# Cleanup
HOME="$HOME_ORIG"
rm -rf "$TMPDIR_FAKE_USER"
rm -f /tmp/probe-registry.txt
```

### §2.5.3. Probe 3 — fallback path when manifest is missing

```bash
# Create a user-tier-shaped deploy without manifest (simulate pre-Arc-38 deploy).
TMPDIR_FAKE_USER2=$(mktemp -d)
mkdir -p "$TMPDIR_FAKE_USER2/.claude/agents"
# Drop MAJOR_POLYBIUS.md without manifest write
cp substrate/MAJOR_POLYBIUS.md "$TMPDIR_FAKE_USER2/.claude/MAJOR_POLYBIUS.md"

# Run check.sh; should friendly-no-op with the manifest-missing message.
echo "$TMPDIR_FAKE_USER2/.claude" > /tmp/probe-registry2.txt
./substrate/skills/check-substrate-updates/check.sh --registry /tmp/probe-registry2.txt 2>&1 \
  | grep -c "manifest missing"
# Must return: at least 1

# apply.sh on the same workspace should also refuse with the helpful message.
./substrate/skills/check-substrate-updates/apply.sh --workspace "$TMPDIR_FAKE_USER2/.claude" --all-differing 2>&1 \
  | grep -c "missing \.substrate-manifest"
# Must return: at least 1

# Cleanup
rm -rf "$TMPDIR_FAKE_USER2"
rm -f /tmp/probe-registry2.txt
```

## §2.6. Self-application per A14 (partial; opportunistic)

The dispatch brief authorizes ADA to opportunistically self-apply the C2 build during Phase 3 against the-stoa's own user-tier substrate (`~/.claude/` on the build machine), IF ADA decides the smoke is informative. Non-required; the verification probes (§2.5) already exercise the round-trip on synthetic user-tier deploys.

If ADA does self-apply against real `~/.claude/`:

- BEFORE running install.sh --target user against PRINCIPAL's real `~/.claude/`, surface to POLYBIUS for explicit consent per operating-disciplines.md §25.5 (probes-mutating-real-workspaces). The install.sh write IS a real mutation (writes the new manifest file to PRINCIPAL's `~/.claude/`).
- If consent given, run install.sh, then check.sh; observe any DRIFTED entries unrelated to Arc 38 (would be drift the 2026-05-14 empirical anchor surfaced — currently no drift detection covers user-tier).
- Surface DRIFTED entries as Pass 8 spec-recon scope or as new follow-up tickets per directive A14.

## §2.7. Cite-comment plan for C2

| File | Read-site | Cite-comment content |
|---|---|---|
| `substrate/install.sh` | top of `write_substrate_manifest()` function | `# CITE: manifest-write per Arc 38 / bj5 / design.md §2.2.4 (A8 γ pick). Format invariant: tab-separated <dep-rel-path>\t<token>\t<replacement>; header block carries tier + deployed_at + substrate_sha. Companion read-sites at substrate/skills/check-substrate-updates/check.sh + apply.sh.` |
| `substrate/skills/check-substrate-updates/check.sh` | top of `apply_substitutions_from_manifest()` | `# CITE: manifest-read per Arc 38 / bj5 / design.md §2.2.5. Format invariant maintained at substrate/install.sh write_substrate_manifest. If install.sh rotates manifest format, this parser must update. Fallback path: legacy apply_substitutions() for project-tier no-manifest case (pre-Arc-38 behavior preserved).` |
| `substrate/skills/check-substrate-updates/apply.sh` | top of `apply_substitutions_from_manifest()` | (same as check.sh — duplicate per existing share-via-inline convention) |
| `substrate/skills/check-substrate-updates/check.sh` | user-tier branch in `check_workspace()` | `# CITE: Arc 38 (bj5; A8) — user-tier check via manifest. Fall back to friendly out-of-scope message if manifest absent (pre-Arc-38 deploy detected).` |
| `substrate/skills/check-substrate-updates/apply.sh` | user-tier branch | (same) |
| `substrate/skills/check-substrate-updates/revert.sh` | top of file or near tier-handling comment | `# CITE: as of Arc 38 (bj5; A8), user-tier workspaces in-scope for revert.sh. Tier-agnostic by design; no manifest involvement at revert time.` |
| `substrate/skills/check-substrate-updates/SKILL.md` | "Scope and limitations" section | (prose, not cite-comment per se; the section itself cross-refs Arc 38 + bj5 + design.md §2.4.4) |
| `substrate/consumer-workspaces.txt` | header comment block | (prose, not cite-comment per se; describes the Arc 38 user-tier support + the PRINCIPAL-machine-specific append convention) |

---

# PART 3 — C3: Substrate-component design principles (stoa--gq1)

## §3.1. Approach

Land new substrate canon at `operating-disciplines.md` as `§31. Substrate-component design principles for agent-installable distribution` (per A11 pick below). Two principles surfaced by the Ariadne distribution-shaping work (HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 Findings 2 + 3):

1. **Principle 1 — Agent-installable distribution model.** The 7-step user-experience flow for any agent-installable substrate component.
2. **Principle 2 — Composability framing.** AI is the primary reader at the repo; the human is the decision-authority who acts on the AI's recommendation. Breadth-through-composability over breadth-through-demo-multiplication.

Plus worked example (Ariadne Core as the originating empirical anchor) plus cross-refs to existing canon per A12.

The directive A12 also names a new template at `substrate/templates/agent-installable-component-template.md`. **DAEDALUS pick: defer the template to a future arc, NOT Arc 38.** Rationale below at §3.3.

## §3.2. A11 — gq1 insertion locus (DAEDALUS sub-decision)

**Pick: α — new top-level §31 in `operating-disciplines.md`, inserted after §30 (four-layer identity model).** Per directive A11 + user-tier POLYBIUS lean.

**Concrete insertion locus:** `substrate/operating-disciplines.md` line 1932 (immediately after §30.6 cross-refs end at line 1930; immediately before the "## Agent-regime inverses (the positive framing)" closing material at line 1934).

**Why α over β / γ:**

- **(α — new §31 after §30) PICKED.** Clean separation; consistent with prior new-section additions in recent arcs (§27 Arc 33 mechanical/agent split; §28 Arc 35 trailer canon; §29 Arc 37 multi-team interop; §30 Arc 37 four-layer identity). The substrate canon's structure is "numbered sections accumulated by arc"; new canon → new numbered section is the most-empirically-followed pattern. ARGUS-discoverable: walk `grep -n "^## " operating-disciplines.md` to see the cadence of section additions.
- **(β — subsection of §29 multi-team interop) REJECTED.** Substrate components ARE artifacts that flow between teams (the multi-team interop is the WHERE; design-principles are the HOW-they're-shaped), but folding design-principles into the §29 subsection structure inverts the dependency: §29 describes the runtime topology; gq1's principles are about the SHAPE of the artifact before it enters the topology. Subsection-of-§29 would make the §29 reader infer the design-principle direction from the artifact-flow direction — adjacent concerns conflated.
- **(γ — new top-level section BEFORE §29) REJECTED.** Argument: design-principles are upstream of multi-team interop, so they should sit upstream in the file. Counter-argument: section numbering in operating-disciplines.md is CHRONOLOGICAL by arc-add, not LOGICAL by dependency direction (e.g., §6.7 N=1 honest-scope is logically upstream of §28 trailer canon but lands at §6.7 because Arc N added it where it was added). Slotting gq1 before §29 would introduce a NUMBERING REBASE: §29 → §30, §30 → §31, plus a renumber of every cross-ref in the codebase. Substantial cost for ornamental gain.

## §3.3. A12 — gq1 content shape (DAEDALUS picks exact wording)

Per directive A12, new section body covers principles + worked example + cross-refs. Exact section structure + prose follows.

### §3.3.1. Section header + intro paragraph

```markdown
## 31. Substrate-component design principles for agent-installable distribution

A substrate component is any artifact a peer workspace consumes from a producer workspace via `install.sh`-style or skill-copy-style deploy. The Stoa substrate itself (deployed from `the-stoa` via `install.sh`) is the canonical instance; Ariadne Core (the semantic-search infrastructure originated by ariadne-core-workspace) is the second. Future substrate components — Railway-deploy skills produced by `railway_stoa`; the inspection-agent pattern per §27; component-author skills per future arcs — follow the same shape.

This section names two design principles that apply to any agent-installable substrate component: the agent-installable distribution model (Principle 1) + the composability framing (Principle 2). Both surfaced empirically — Principle 1 from PRINCIPAL's 2026-05-13 Ariadne distribution-shaping conversation (HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 Findings 2 + 3); Principle 2 from the same conversation's "many wirings of one substrate" framing. Stoa-substrate-as-shipped-via-install.sh is a parallel empirical instance (N=2 per A13 ii pick); the principles abstract across both.
```

### §3.3.2. §31.1 Principle 1 — agent-installable distribution model

```markdown
### 31.1 Principle 1 — Agent-installable distribution model

The user-experience flow for any agent-installable substrate component:

1. **User encounters component** (URL via word-of-mouth, a published demo, a shared link).
2. **User pastes URL to their AI** (Claude Code, ChatGPT, etc.).
3. **User asks the AI: "do I need this?"** (the diagnostic question — fit-to-domain, not feature-tour).
4. **AI fetches the repo's README + AGENTS.md + skills/ materials** (the agent-facing landing surface).
5. **AI evaluates against the user's domain** (cross-checking the user's accumulated memories — see §30 four-layer identity — against the component's stated fit criteria).
6. **AI returns yes / no / try-the-demo recommendation** (with rationale citing fit-vs-domain or domain-mismatch).
7. **If yes + user consent: AI installs + runs demo** (the consent moment is a §25 PRINCIPAL-gate; the install + demo are bounded mechanical operations the agent runs once authorized).

The AI is the primary reader at the component's repo; the human is the decision-authority who acts on the AI's recommendation. Repo-shape implications follow from this primary-reader inversion: README stays human-readable but adds a top-of-page pointer routing agents to AGENTS.md (or equivalent agent-facing landing file); AGENTS.md is the canonical agent-facing decision-support landing (fit criteria, install cost, skill inventory, recommendation templates, hard rules); an invitation-style skill handles the "do I need this?" diagnostic conversation; a walkthrough skill handles post-install hands-on demo.

**Worked instance — Stoa substrate-as-component.** The Stoa substrate (this very deployable) follows the same flow: a user encounters the-stoa via the canonical URL; pastes it to their AI; asks "do I need this?"; the AI fetches `SKILL.md` + `CLAUDE.md` + the case-study materials; evaluates against the user's domain (substrate-team-coordination work? AI-agent-as-collaborator pattern in active use?); returns yes / no / try-the-visual-tour; on yes + consent, runs `install.sh --target user` or `--target project`. The repo-shape implication: `SKILL.md` at repo root routes agents to `skills/stoa-intro/SKILL.md` (visual tour) or `skills/install-stoa/SKILL.md` (guided install) or the case study — exactly the 7-step shape.

**Worked instance — Ariadne Core distribution.** Ariadne Core's distribution flow at the ariadne-core-workspace produces the same shape: user-encounters; paste-URL; ask-fit; AI-fetches AGENTS.md + the skills/ materials; AI-evaluates against domain (factory-manager? healthcare? SRE? legal?); AI-returns recommendation; consent + install + demo. The HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 thread is the load-bearing source.
```

### §3.3.3. §31.2 Principle 2 — composability framing

```markdown
### 31.2 Principle 2 — Composability framing

Breadth of a substrate component is composability, not demo-inventory.

The claim "this substrate supports many projects" is a COMPOSABILITY claim — one substrate, many wirings — NOT a BREADTH-OF-DEMOS claim — "look, here are five demos showing five separate use cases." The first claim is what makes a substrate component valuable to a new user (their use case can be a NEW wiring, not a copy of a demonstrated one); the second claim ages out the moment the user's use case differs from any demo.

Concretely: **Ariadne Core** supports the factory-manager demo but ALSO supports healthcare / SRE / legal / journalism / audit / cyber by the same substrate WIRED DIFFERENTLY. **One install, many shapes.** The right way to surface breadth is to demonstrate the wiring surface (e.g., the per-domain skills + the per-domain memory accumulation patterns); the wrong way is to ship five demos and let the reader infer composability from coverage.

**Concretely for the Stoa substrate** (the parallel instance): one install of the substrate supports many project shapes — the-stoa's own substrate-meta work, ariadne-core's semantic-search domain, railway_stoa's deploy-tooling domain, sector-4's future domain. The substrate composes across project shapes via the base-vs-custom convention (§23 + `MAJOR_POLYBIUS.md` §17) plus the two-team forge/shop architecture (`MAJOR_POLYBIUS.md` §19). The breadth claim for the Stoa substrate is "one substrate, deploys via install.sh, wires to your domain through customization conventions" — NOT "see, we have N demo projects."

**Architectural implication for substrate-component authoring:** when authoring substrate-component marketing/onboarding materials (READMEs, AGENTS.md, skills/, demo links), frame breadth as composability (one substrate, many wirings) not as demo inventory (here are five demos). The composability framing both ages slower (a new domain composes without new demos) and signals correctly (the substrate IS the breadth, not the demos).
```

### §3.3.4. §31.3 A13 N-evidence framing (DAEDALUS sub-decision)

**Pick: ii — Cite Ariadne + Stoa substrate as parallel empirical instances (N=2).** Per directive A13 + user-tier POLYBIUS lean.

**Rationale:**

- **(i) Ariadne only (N=1)** — Technically honest, but UNDER-reports the existing evidence. The Stoa substrate's distribution flow (install.sh + the README routing pattern at `SKILL.md`) is a sibling-shaped instance that PRECEDES the Ariadne distribution shape on the repo. Reporting N=1 when N=2 is observable in the substrate itself would be reverse-confabulation (§19.6 mirror).
- **(ii) Ariadne + Stoa substrate-deploy (N=2) — PICKED.** Both observable; both follow the 7-step flow; both honor the composability framing. N=2 is the honest count; calling out both lets future readers walk both instances when looking for the pattern. Lower friction than (iii); higher honesty than (i).
- **(iii) Ariadne + Stoa + Railway speculation (N=2 + 1 anticipated)** — REJECTED. Adding Railway as "anticipated future instance" would speculate about a workspace that has not shipped its first substrate-component publicly. The §6.7.1 N=1 honest-scope discipline cuts strongly against forward-projecting empirical anchors; speculation lands as canon and ages badly.

**Exact §31.3 wording:**

```markdown
### 31.3 Empirical anchors — N=2 honest scope

Per §6.7.1 honest-scope: this section enters substrate canon off-gate on PRINCIPAL's project-direction authority (2026-05-13 Ariadne distribution-shaping conversation, captured at HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 Findings 2 + 3). §6.7.1 defers to the canon-promotion gate (multiple observations + controlled comparison + substrate-level pattern); §6.7.1 does not carve out a separate "PRINCIPAL-declaration shortcut."

Supporting evidence at the time of this writing:

- **N=1 — Ariadne Core distribution (originating empirical anchor).** PRINCIPAL's 2026-05-13 conversation surfaced both principles in the context of authoring Ariadne Core's distribution materials. The 7-step agent-installable flow + composability-over-demo-multiplication framing are PRINCIPAL's verbatim formulations (per the HUMAN_relay file).
- **N=2 — Stoa substrate distribution (parallel empirical anchor).** The Stoa substrate itself follows the same shape, observable at the the-stoa repo: `SKILL.md` at repo root routes agents to invitation skills + install skill; `install.sh` provides the bounded mechanical install per Principle 1 step 7; the substrate composes across projects via base-vs-custom + two-team architecture per Principle 2. The Stoa-substrate instance PRE-DATES the Ariadne instance (the-stoa shipped install.sh in earlier arcs; Ariadne adopted the agent-installable shape after observing the-stoa's pattern), making it an INDEPENDENT instance rather than a derivative of the Ariadne anchor.

N=2 is the honest count. Both instances are observable in the current ecosystem; the principles abstract across both. Promotion to "structural lesson" status with multi-instance + controlled-comparison + substrate-level-pattern evidence remains future-arc work; future substrate components (Railway-deploy skills + future component-author skills) accrete additional N as they ship.

Same N=1/N=2 framing as Arc 35's §28.7, Arc 34's `MAJOR_POLYBIUS.md` §18.5, Arc 29's §23.4, and Arc 37's §29.6 + §30.5.
```

### §3.3.5. §31.4 cross-references

Per directive A12, cross-refs to §29 (multi-team interop), §23 + `MAJOR_POLYBIUS.md` §17 (co-equal base-vs-custom canon at universal-team + POLYBIUS-tier cuts respectively; cited paired per the install.sh precedent), §27 (mechanical/agent split), §28 (Co-Authored-By trailer):

```markdown
### 31.4 Cross-references

- **§29 (Multi-team interoperation)** — substrate components ARE the artifacts that flow between teams per §29.2. §31 names the design principles; §29 names the runtime topology those principles operate within.
- **§23 (Base vs custom agents — universal-team framing)** + **`MAJOR_POLYBIUS.md` §17 (POLYBIUS-tier statement of the same canon)** — co-equal canon for the base-vs-custom architectural model, both anchored at their respective §X.1 source-of-truth subsections to PRINCIPAL's 2026-05-17 declaration captured at `stoa--ads`. The two are paired cuts of one canon (universal-team cut + POLYBIUS-tier cut), not a base + derivative; cite both together per the established install.sh cite-comment precedent (install.sh lines 836-837 / 865-866 / 893-894). Substrate components ship a BASE that consumers can CUSTOMIZE per the per-class path convention. The composability framing (§31.2) leans on the base-vs-custom split: substrate component = the base; per-project wiring = the custom.
- **§27 (Mechanical-script / agent-inspection split)** — the script-then-agent pattern IS a substrate-component pattern; the inspection-agent layer (per §27.5) is itself a deliverable that ships in `substrate/skills/inspect-script-output/`. Principle 2 composability framing applies: the pattern composes across script-based workflows (substrate-update flow today; future flows as the pattern proves out).
- **§28 (Co-Authored-By trailer — substrate-component attribution)** — substrate-component authorship attribution at the commit-trailer layer follows §28; file-frontmatter attribution per §28.4 stays Denson Smith (or per-project PRINCIPAL).
- **§30 (Four-layer identity model)** — substrate components ship the **role file** layer (the universal substrate identity layer); the **memories** layer is PRINCIPAL-accumulated per-deployment; the **handoff** layer is per-engagement; the **bw substrate** layer is per-project. Principle 1's 7-step flow operates against all four layers (the AI evaluating "do I need this?" at step 5 reads against the user's accumulated memories per §30.2).
- **HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13** (the load-bearing source; ariadne-core-workspace) — Findings 2 + 3 carry PRINCIPAL's verbatim formulations of both principles.
- **`stoa--gq1`** (this section's originating ticket).
- **`stoa--vmc`** (Arc 23, closed) — sibling substrate-canon principle (bw-fit matrix); related shape (which substrate for which use-case).
- **`SPECIFICATION.md` §13.5** (the Pass 4 / Arc 38 enumeration) — this section's place in the workplan.
```

## §3.4. A14 self-application for C3 — none

Per directive A14: "gq1 self-application — none. Design-principles canon doesn't have obvious self-application within the arc that ships it. Acceptable." DAEDALUS confirms: nothing for ADA to self-apply at C3. PLINY-signoff is the only post-ship verification; ZENO mechanical-checks the §31 cross-refs resolve.

## §3.5. Out-of-scope for C3: the proposed template

Per directive A12, the gq1 ticket body names a new template at `substrate/templates/agent-installable-component-template.md`. **DAEDALUS pick: defer the template to a future arc; Arc 38 ships §31 prose only.**

**Rationale:**

- The template's load-bearing user is "future arcs that ship substrate components." Arc 38 does NOT ship a new substrate component (it ships substrate-canon work for the EXISTING components). The template's first real consumer is not in Arc 38; the empirical anchor for "what shape does the template need" comes from the first future-arc component-shipping work, not from a speculative blueprint authored before any consumer exists.
- The §6.7.1 honest-scope discipline cuts against authoring scaffolding ahead of consumer demand. Authoring a template "in case a future component-author needs it" is exactly the make-script-comprehensive failure mode §27 names (scaffolding accumulates without a consumer; consumer eventually arrives with a different shape; scaffolding ages out).
- Arc 38 is already medium-large (3 candidates of different shapes). Adding a 4th deliverable (template) widens scope.

**Forward path:** when a future arc ships its first NEW substrate-component (e.g., a Railway-deploy skill packaged for agent-installation), the directive for that arc dispatches a DAEDALUS pass that authors the template in-context alongside the component. The template's shape will be informed by the actual component's shape — not by a speculative shape inferred from the §31 prose alone.

ARGUS may scrutinize this defer-decision. Listed as `residual_question_for_argus` in the verdict.

## §3.6. Verification probes (VERA exercises in Phase 3)

Two probes for C3.

### §3.6.1. Probe 1 — §31 lands at the expected locus

```bash
# Must return: 1 (§31 header present)
grep -c "^## 31\. Substrate-component design principles for agent-installable distribution$" substrate/operating-disciplines.md

# Must return: 1 (§31 lands immediately after §30 — verify by line ordering)
# (Find the line number of §30, find the line number of §31, confirm §31 > §30 and no other ## section between.)
awk '/^## 30\./{n30=NR} /^## 31\./{n31=NR} END{print (n31 > n30 ? "ok" : "FAIL")}' substrate/operating-disciplines.md
# Must return: "ok"

# Must return: 1 (Principle 1 subsection present)
grep -c "^### 31\.1 Principle 1 — Agent-installable distribution model$" substrate/operating-disciplines.md

# Must return: 1 (Principle 2 subsection present)
grep -c "^### 31\.2 Principle 2 — Composability framing$" substrate/operating-disciplines.md

# Must return: 1 (N=2 honest-scope subsection present)
grep -c "^### 31\.3 Empirical anchors — N=2 honest scope$" substrate/operating-disciplines.md

# Must return: 1 (cross-refs subsection present)
grep -c "^### 31\.4 Cross-references$" substrate/operating-disciplines.md
```

### §3.6.2. Probe 2 — §31 cross-refs resolve

```bash
# Each cross-ref named in §31.4 must point to a real section that exists.
for ref in "§29" "§23" "§27" "§28" "§30"; do
  cnt=$(grep -c "^## ${ref#§}\." substrate/operating-disciplines.md)
  if [ "$cnt" -ne 1 ]; then
    echo "FAIL: cross-ref ${ref} from §31 does not resolve in operating-disciplines.md"
    exit 1
  fi
done
echo "all operating-disciplines.md cross-refs from §31 resolve"

# MAJOR_POLYBIUS.md §17 must resolve.
grep -c "^## 17\." substrate/MAJOR_POLYBIUS.md
# Must return: 1

# HUMAN_relay file must be cited (presence check on the cross-ref text itself).
grep -c "HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13" substrate/operating-disciplines.md
# Must return: at least 1 (the §31.4 cross-ref)

# §31.4's §27 cross-ref bullet names substrate/skills/inspect-script-output/ as
# the deliverable skill — verify the skill directory exists at the cited path.
# (If a future arc renames the skill, this probe catches the dangling cross-ref.)
test -d substrate/skills/inspect-script-output && echo "inspect-script-output skill path resolves"
# Must print: "inspect-script-output skill path resolves"
```

## §3.7. Cite-comment plan for C3

| File | Read-site | Cite-comment content |
|---|---|---|
| `substrate/operating-disciplines.md` | top of §31 intro paragraph | `<!-- cite: HUMAN_relay_user_polybius_ariadne_distribution_and_mcp_2026-05-13 (ariadne-core-workspace) Findings 2 + 3; stoa--gq1 ticket body; SPECIFICATION.md §13.5 Pass 4 / Arc 38 enumeration -->` |
| `substrate/operating-disciplines.md` | top of §31.1 Principle 1 | `<!-- cite: HUMAN_relay file (verbatim 7-step formulation) -->` |
| `substrate/operating-disciplines.md` | top of §31.2 Principle 2 | `<!-- cite: HUMAN_relay file (verbatim composability framing) -->` |
| `substrate/operating-disciplines.md` | top of §31.3 N=2 honest scope | `<!-- cite: §6.7.1 N=1 canon-promotion gate; sibling §29.6 + §30.5 N=1/N=2 framing precedent -->` |

---

# PART 4 — Universal / cross-candidate concerns

## §4.1. A15 — Co-Authored-By trailer + signoff + paste archival self-application

Per Arc 35 §28 + Arc 36 §7.7 + MAJOR_PLINY.md §5.10 + §5.11 + operating-disciplines.md §19.6.

### §4.1.1. Trailer discipline for every commit in arc-38/build

Every CAPTAIN commit inside the `arc-38/build` worktree carries:

```
Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>
```

DAEDALUS's own commits in this worktree (the design.md commit; any subsequent design-rev commits) carry `Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>`. ADA's build commits carry the ADA trailer. Per directive A15.

### §4.1.2. Squash-merge body discipline (preempts the Arc 37 bb12806 regression)

Per `stoa--6wp` (the Arc 37 regression ticket): PLINY's Phase 4 PR merge MUST NOT use `gh pr merge --squash --body "<custom>"` because the custom `--body` OVERRIDES GitHub's default body (which would concatenate source commits + their trailers).

**Two valid shapes for PLINY:**

1. **Omit `--body` entirely** — `gh pr merge <N> --squash --delete-branch`. GitHub auto-populates the squash-merge body from the source commits' bodies, preserving every trailer.
2. **Include `--body` with trailers explicitly in the HEREDOC** — `gh pr merge <N> --squash --delete-branch --body "$(cat <<EOF ... Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local> Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local> EOF )"`.

**DAEDALUS recommendation: shape 1 (omit `--body`).** Lower-friction; auto-preserves any future CAPTAIN trailers without ad-hoc HEREDOC maintenance; matches what GitHub's UI-driven squash-merge would produce; eliminates the regression class.

The directive A15 already names this requirement; this section reiterates so ADA does NOT inadvertently land any `--body` in the build commit message (the regression was in PLINY's `gh pr merge` invocation; ADA's commit messages are separate). Per A15: "This is the first arc that should ship trailer-clean on the squash-merge body forward of the Arc 37 bb12806 regression (Arc 40 ships the canon fix; Arc 38 should apply the discipline ahead of that)."

### §4.1.3. §5.10 signoff-accuracy

PLINY's signoff at arc close verifies cleanup claims live (arc-38/build local + remote deleted; worktree removed; PR merged; main fast-forwarded). Verification commands per `MAJOR_PLINY.md` §5.10. **Critical: re-run `git rev-parse HEAD` at attestation time; do NOT echo the dispatch-authoring SHA `68c0c12` as verified-at-attestation state.**

### §4.1.4. §5.11 paste archival

Activation pastes (`HUMAN_paste-{polybius,pliny}-arc-38-instruction.md`) at workspace root move into `substrate/arcs/arc-38/pastes/` on arc close, via `git mv` per §5.11. PLINY-driven.

## §4.2. A16 — `[from: <self>]` author-tag convention + cron hygiene

Per Arc 36 §7.1 5th beat + §7.7 + §11 step 1.5.

- POLYBIUS coordination heartbeats on `stoa--ojz` carry `[from: polybius-the-stoa]`.
- PLINY heartbeats carry `[from: pliny-the-stoa]` (over-compliance per A2.5; acceptable).
- DAEDALUS / ADA / CATO / VERA / ZENO comments classified §7.7 case 4 (non-POLYBIUS substance comments; do not enter timeline-arithmetic).

DAEDALUS this dispatch: `[from: daedalus-the-stoa]` on every heartbeat (already applied).

## §4.3. A17 — Cite-comment discipline summary

All cite-comments collated per Part section:
- §1.6 (C1 — 8 cite sites)
- §2.7 (C2 — 8 cite sites)
- §3.7 (C3 — 4 cite sites)

Total: 20 cite-sites ADA writes. ZENO mechanical-checks at Phase 3 that each cite resolves (the cited section/file/line actually exists).

## §4.4. A18 — Authorship attribution immutable per CLAUDE.md

`substrate/CAPTAIN_TIRO.md` frontmatter: `author: Denson Smith`. Verified at §1.4 above.

No other file Arc 38 touches has `author:` frontmatter that needs the discipline applied; install.sh, check.sh, apply.sh, revert.sh, consumer-workspaces.txt, operating-disciplines.md, MAJOR_POLYBIUS.md, MAJOR_PLINY.md, CAPTAIN_ADA.md, CAPTAIN_CATO.md, SKILL.md (check-substrate-updates) — all are either un-frontmattered or already correctly attributed.

## §4.5. A19 — Source-ticket closure (PLINY-driven, post-ship)

On Arc 38 ship:

- **stoa--ojz** (C1 + work-unit parent) closes with cross-ref + audit comment naming new CAPTAIN_TIRO.md role file + install.sh wiring + cross-refs landed.
- **stoa--bj5** (C2) closes with cross-ref + audit comment naming the per-file-marker scheme (manifest) + user-tier registry extension (comment block only) + check.sh/apply.sh/revert.sh extensions landed.
- **stoa--gq1** (C3) closes with cross-ref + audit comment naming new operating-disciplines.md §31.

Tag `[for: user-tier-polybius]` on stoa--ojz inviting QA pass.

## §4.6. A20 — Out-of-scope hard-locks (re-affirmed)

DAEDALUS confirms: this design honors every A20 hard-lock. NO additional candidates bundled; NO widening of TIRO; NO non-bw subsystems; NO restructure of check-substrate-updates beyond bj5; NO install.sh changes beyond TIRO + bj5; NO stellation touches; NO NC8.

---

# §5. Self-assessed weak points (per CAPTAIN_DAEDALUS §6.2)

This section pairs with ARGUS's plan-critique: DAEDALUS names the brittle spots; ARGUS names the risks DAEDALUS missed.

## §5.1. Weak point: the manifest's "format invariant" creates a future-coupling surface

**Description:** The A8 γ manifest scheme introduces a NEW format invariant (`<dep-rel-path>\t<token>\t<replacement>`) that lives at install.sh's writer site AND at check.sh's reader site AND at apply.sh's reader site. Any future change to install.sh's substitution behavior (new tokens; new file classes; per-tier asymmetries) must update the manifest writer AND every reader to match. The cite-comments at every site (§2.7) are the only mitigation — there is no schema enforcement, no parser validation against a published schema, no version field in the manifest header.

**Why this shape anyway:** Schema enforcement at this scale would be ceremony for a 5-substitution surface (one non-trivial substitution: `{{USER_TIER_DIR}}` at user-tier MAJOR_POLYBIUS.md). Substrate convention per the existing check.sh:74-80 comment is "live-parse from install.sh, with cite-comments at every reader site"; the manifest scheme is the SAME shape (live-write from install.sh, with cite-comments at every reader site). Adding a parser-validation layer would invert the relationship — readers would have to know the schema before knowing the substitution; the cite-at-read-site discipline already covers the drift surface.

**ARGUS scrutiny invitation:** if you see a less coupled shape that doesn't require N readers to update on every install.sh substitution change, surface it. The fallback path I considered: passing the substitution map AS A FUNCTION CALL between install.sh and check.sh via an exported bash function or sourced library — REJECTED because it creates a same-runtime-context coupling that violates the install.sh / check.sh independence (check.sh runs days/weeks after install.sh wrote the deployed files; the function-call shape requires both to run in the same process).

## §5.2. Weak point: TIRO chicken/egg has no organic adoption mechanism

**Description:** Arc 38 ships TIRO but does NOT mechanically enforce "future seats dispatch TIRO for bw queries" (per A20 hard-lock). The cross-refs in MAJOR_POLYBIUS.md §7.3 + MAJOR_PLINY.md §6.1 + CAPTAIN_ADA.md + CAPTAIN_CATO.md + operating-disciplines.md §12.4 are PROSE; they require the seat reading them to recognize the dispatch opportunity. The empirical-anchor failure mode (2026-05-17 three-audit confabulation) was a HUMAN-cognitive failure (operator-under-context-pressure forgets the flag); same cognitive failure could result in "operator-under-context-pressure forgets the TIRO dispatch path AND forgets the `--all` flag," replicating the anchor under TIRO availability.

**Why this shape anyway:** Mechanical enforcement (pre-comment hook, lint, pre-dispatch check) is a future-arc deliverable per the directive A20 + §27 mechanical/agent split. The current arc establishes the SEAT; observation across multiple future arcs informs whether mechanical enforcement is needed. Same shape as Arc 33's `inspect-script-output` skill (the skill exists; the §27 A7 boundary explicitly does NOT mechanically enforce its use across every relevant discipline; per-discipline integration is incremental future-arc work). The TIRO seat AT LEAST makes the alternative path EXIST; pre-Arc-38, the operator's options were "remember the flag" or "audit fails." Post-Arc-38, the alternative is "dispatch TIRO," which removes the per-operator cognitive load. The cognitive failure of forgetting BOTH the flag AND the dispatch is possible but less likely than the single cognitive failure of forgetting just the flag.

**ARGUS scrutiny invitation:** does the cross-ref text in §1.3 above make the dispatch path discoverable enough? Specifically: a POLYBIUS or PLINY in the middle of an arc, doing a bw audit, who lands at MAJOR_POLYBIUS.md §7.3 — does the "Specialist delegation — CAPTAIN_TIRO" paragraph register as "I should dispatch TIRO," or does it register as "informational"? If informational, the cross-ref might need a sharper "DO X" framing rather than the descriptive framing I picked.

## §5.3. Weak point: §31 N=2 cite of the-stoa as parallel instance is partially self-referential

**Description:** §3.3.4 (A13 ii pick) cites "Stoa substrate distribution" as the N=2 instance for Principles 1 + 2. But the Stoa substrate is THE SAME SUBSTRATE that the §31 canon ships from. There's a circularity: "Principle X holds across N=2 instances, one of which is the substrate that's encoding Principle X." A reader could legitimately ask: is this N=2 honest evidence, or is it bootstrapping (one PRINCIPAL-articulated principle + one example artificially constructed to satisfy the canon-promotion gate)?

**Why this shape anyway:** The Stoa substrate's distribution flow PRE-DATES the Ariadne distribution-shaping conversation. The substrate shipped install.sh + the `SKILL.md`-at-repo-root routing pattern + the composability-via-base-vs-custom in Arcs 27/29/etc., before PRINCIPAL articulated the principles. The N=2 claim is HONEST in temporal order (the substrate observably exemplified the pattern before PRINCIPAL named the pattern); the N=2 claim is HONEST in pattern-shape (Principle 1's 7-step flow is observable in the substrate; Principle 2's composability framing is observable in §17/§23 + §19 + the existing breadth of consumer-workspaces). The self-reference is a TEMPORAL artifact of the canon being authored INSIDE the substrate it describes; not a bootstrapping circularity.

**Mitigation:** §31.3 (the N=2 honest-scope paragraph) names "the Stoa-substrate instance PRE-DATES the Ariadne instance" explicitly, so the temporal honesty is visible to the reader. Future arcs that ship NEW substrate-components (Railway-deploy skill packaged for agent-installation; future component-author skill) accrete N=3+ and dilute the self-reference concern.

**ARGUS scrutiny invitation:** does the temporal-honesty framing in §31.3 read as sufficient, or does the self-reference need to be either (a) called out more explicitly as a known artifact ("the Stoa substrate is both the encoder AND an instance; the encoder property does not invalidate the instance property because the substrate exemplified the pattern before encoding it"), or (b) hedged toward N=1 + "the Stoa substrate parallels the shape"?

## §5.4. Weak point: A8 manifest scheme adds a NEW file at every install — operator may not expect it

**Description:** `<workspace>/.claude/.substrate-manifest` is a NEW file introduced by Arc 38. Operators who run `install.sh` will see a new file appear in their `.claude/` directory; if they're git-tracking `.claude/` (common — per the apply.sh git-tracking discipline), the manifest appears as an untracked file requiring a commit. The header comment ("DO NOT EDIT MANUALLY") signals intent, but the OPERATOR-side surprise is non-zero.

**Why this shape anyway:** The manifest IS the load-bearing fix for the user-tier drift-detection blocker. The operator-side surprise is bounded: one new file per workspace; documented intent; survives git-tracking the way every other `.claude/` file does. The alternative (no manifest) keeps the user-tier blocker open; the alternative (sidecar per file) creates N new files instead of 1.

**Mitigation:** The install.sh log line `wrote manifest: <path>` announces the new file at deploy time so operators see it appear. The `consumer-workspaces.txt` header comment block (per §2.3) names the manifest's role.

**ARGUS scrutiny invitation:** is the manifest as a NEW file the right shape, or should it live ELSEWHERE (e.g., embedded as a hidden block in CLAUDE.md? as a section of `.substrate-last-check`?). Hidden-block in CLAUDE.md would couple to CLAUDE.md's `--modify-claude-md` consent flag (not always given). Extension of `.substrate-last-check` would conflate the per-deploy substitution record (manifest) with the per-check state record (timestamp + sha); the two have different lifecycles (manifest changes per deploy; state changes per check). Keeping the manifest as its own file aligns lifecycle with content.

## §5.5. Weak point: TIRO's ~280-320 LOC sizing target may run long

**Description:** §1.1.1 sizes the TIRO role file at ~280-320 LOC. The closest precedent (CAPTAIN_BARTLEBY.md) is 170 LOC. TIRO adds the bw subcommand reference (§6.3 — table with 10 subcommands + gotchas; estimated ~50 LOC) + worked-example dispatches (§6.4 — 3 examples each with brief + action + structured return; estimated ~80 LOC). The math comes to ~300 LOC, which sits mid-band of the 280-320 target. If the §6.x discipline sections accrete more than ±20 LOC over the envelope baseline (e.g., the heartbeat-and-read-before-write §6.5 ends up needing a worked example for TIRO-specific bw introspection), the file pushes above 320.

**Why this shape anyway:** The bw subcommand reference + worked examples ARE the load-bearing differentiating content of the seat (vs the generic CAPTAIN envelope). Trimming the worked examples would erode the seat's "how to dispatch me" signal. Trimming the subcommand reference would push the seat into "see the cookbook" which DOES NOT solve the empirical-anchor failure mode (the operator forgot the flag DESPITE the cookbook existing; TIRO's whole-context priming is the differentiator).

**Mitigation:** ADA may trim individual examples or table entries if line-budget pressure surfaces during build; the load-bearing content is the table + at-least-one-example-per-shape (read query, completeness audit, write-syntax advisory). Trimming below 280 LOC erodes the differentiating content; landing in the 280-320 band is the target; staying slightly above 320 is acceptable if the content is load-bearing and the §6.x discipline sections justify their lines. If the file pushes meaningfully above 350 LOC, surface to PLINY before commit (potential scope-creep signal).

**ARGUS scrutiny invitation:** is the worked-examples count of 3 right? Could it be 2 (one read, one write-advisory) with the completeness-audit example folded into the §6.1 cookbook-discipline paragraph? Or should it be 4-5 to cover the full surface (read query + completeness audit + comment-history + write-syntax + dep-direction)? My pick of 3 is calibrated to "show the asking seat the dispatch shape and the return shape; let the cookbook cover the long tail."

---

# §6. Out of scope (out-of-scope-for-this-design list)

Per CAPTAIN_DAEDALUS §3 step 5 — concerns this design deliberately does not address, with one-line reasons:

- **TIRO write enforcement.** No pre-comment hook / lint / cron / sentinel preventing TIRO from writing for another seat. Discipline-layer only. Future-arc work IF non-compliance recurs per Arc 33 §27 pattern.
- **TIRO toolset extension to WebSearch/WebFetch.** Surfaced in §0 as residual question for ARGUS; default per A3 stays NOT included.
- **Multi-shot TIRO dispatches (one TIRO call answering N queries).** The one-shot CAPTAIN dispatch shape is universal; TIRO inherits it; multi-query batching is out-of-scope.
- **TIRO at non-stoa projects.** TIRO ships via install.sh and lands at every install (user-tier; project-tier; subproject-tier) — but its bw-specific priming is only valuable at projects that USE bw. Ariadne-core-workspace + railway_stoa + sector-4 all use bw; future workspaces that don't use bw inherit TIRO without using it. The seat doesn't actively refuse non-bw projects; it just isn't dispatched. No build action needed.
- **bj5 manifest version field.** No schema-versioning of the manifest. If a future arc rotates the manifest format incompatibly, that arc's directive will include the migration step (rewrite all deployed manifests at first install.sh re-run). Speculative versioning ahead of the rotation is scope-creep.
- **bj5 manifest in subproject-tier as load-bearing.** Subproject-tier writes the manifest too (per install.sh uniform behavior), but the substitution surface is the same as project-tier (NAME_SUFFIX from project-slug, derivable from workspace path); the manifest at subproject-tier is informational, not load-bearing for check.sh's correctness. No additional design here.
- **gq1 template (`substrate/templates/agent-installable-component-template.md`).** Deferred to first future-arc that ships a NEW substrate-component (per §3.5). Not Arc 38.
- **gq1 §31 mechanical extraction into a separate file.** §31 stays in operating-disciplines.md per A11 α pick; no separate `agent-installable-components.md` file.
- **Squash-merge bb12806 retroactive fix.** Per `stoa--6wp` ticket body: NOT in scope. Arc 38 applies the §28 + §15.10 discipline PREEMPTIVELY (per A15); the canon fix for §28.3 (subsection naming the trailer-preservation pitfall) is Arc 40 / §13.7 work.
- **Mechanical bw-CLI dispatch routing (auto-dispatch TIRO when a bw command is detected in a seat's planned action).** Not Arc 38. Future-arc IF organic adoption is insufficient.

---

# §7. Phase 3 verification probe summary (for VERA)

Three candidates × multiple probes:

| Candidate | Probe ID | Probe summary | Pass criteria |
|---|---|---|---|
| C1 / TIRO | 1.5.1 | Role file structural conformance | YAML frontmatter + author field + toolset + section headers all present |
| C1 / TIRO | 1.5.2 | install.sh dry-run lists TIRO at 3 tiers | grep for `CAPTAIN_TIRO[_slug]?.md` returns ≥1 at each tier |
| C1 / TIRO | 1.5.3 | TIRO dispatchable + sensible structured answer | VERA dispatches TIRO; verdict block parses; cookbook_cite resolves; no writes attempted |
| C2 / bj5 | 2.5.1 | install.sh dry-run announces manifest write at user-tier | grep for `write:.*\.substrate-manifest` returns ≥1 |
| C2 / bj5 | 2.5.2 | Manifest round-trip on synthetic user-tier deploy | CURRENT verdict on fresh deploy; DRIFTED detected after intentional file mutation |
| C2 / bj5 | 2.5.3 | Fallback path when manifest is missing | check.sh + apply.sh friendly-no-op with manifest-missing message |
| C3 / gq1 | 3.6.1 | §31 lands at expected locus | Header + 4 subsections grep-pass; §31 line-number > §30 line-number |
| C3 / gq1 | 3.6.2 | §31 cross-refs resolve | §29, §23, §27, §28, §30, MAJOR_POLYBIUS.md §17, HUMAN_relay file references all present; `substrate/skills/inspect-script-output/` directory exists |

All probes are mechanical (grep / dry-run / synthetic-clone). Probe 2.5.2 + 2.5.3 use `mktemp -d` for isolation per operating-disciplines.md §25.5 (probes mutating real workspaces require explicit operator authorization; synthetic-temp-dir is the canonical pattern).

---

# §8. Verdict (DAEDALUS-side)

Per CAPTAIN_DAEDALUS §7 verdict format. The full verdict block is returned in the dispatch return; the bw comment + this design.md are the artifacts.

- **status:** completed
- **ticket:** stoa--ojz (work-unit parent; C1 + C2 + C3 bundle)
- **verdict:** pass
- **design_artifact_path:** `agents/design/stoa--ojz/design.md` (this file)
- **restatement:** Arc 38 ships three substrate-architecture canon items in one gauntlet — CAPTAIN_TIRO (new bw substrate specialist seat with read-direct + write-advisory split, install.sh deploy wiring at all 3 tiers, cross-refs in 4 substrate files), user-tier drift detection (per-deploy manifest at .substrate-manifest, registry comment-block extension, check.sh/apply.sh manifest-driven substitution + revert.sh tier-agnostic verification, friendly fallback when manifest absent), and substrate-component design principles (new operating-disciplines.md §31 codifying the agent-installable distribution model + composability framing with N=2 honest scope across Ariadne + Stoa substrate).
- **sub-decision picks:**
  - **A5 (TIRO install.sh wiring):** add `TIRO` to `CAPTAIN_NAMES` at install.sh:122-133, uniform deploy across all 3 tiers; no per-tier filtering. Rationale at §1.2.
  - **A8 (bj5 per-file-marker scheme):** γ — manifest file per workspace at `<workspace>/.claude/.substrate-manifest`. Tab-separated `<dep-rel-path>\t<token>\t<replacement>` triples with metadata header block. Rationale at §2.2.
  - **A9 (bj5 user-tier registry):** extend existing `consumer-workspaces.txt` with new comment block describing user-tier support; do NOT ship user-tier path as default entry (PRINCIPAL-machine-specific). Rationale at §2.3.
  - **A11 (gq1 §31 insertion locus):** α — new top-level §31 in operating-disciplines.md, after §30. Rationale at §3.2.
  - **A13 (gq1 N-evidence framing):** ii — Ariadne (N=1 originating anchor) + Stoa substrate distribution (N=2 parallel anchor). Rationale at §3.3.4.

---

(end of design.md — 750+ lines covering 3 candidates + universal section + weak-points + out-of-scope + probes + verdict.)
