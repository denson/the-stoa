# Arc 41 — Pass 7 substrate bundle: integrated design

**Ticket:** `stoa--utn` (dispatch); candidates `stoa--n2e` + `stoa--58b` + `stoa--3ml` + `stoa--pqn` LOCKED.
**Author (substrate edits):** Denson Smith.
**Designed by:** CAPTAIN_DAEDALUS_the_stoa, 2026-05-18 (rev1 at commit 56c0b97; rev2 folds ARGUS-rev1 R1+R2+R3 HIGH/MEDIUM probe-grounding fixes + R4+R5+R6+R8 LOW dispositions; R7 LOOSE adjudicated — no rev).
**Inputs consumed:** `substrate/arcs/arc-41-build-directive.md` (A1-A16 LOCKED); ticket bodies for all 4 candidates via `bw show` (n2e + 58b + 3ml + pqn); ticket body for `stoa--jru` (Arc 36 v2 parent EPIC) for VERA 5-item probe-regex source; ticket body for `stoa--myd` (multi-checker convergence accretion P4) for A5 Item 3 routing target; `substrate/arcs/arc-40-build-directive.md` + Arc 40 ship commit `dbb5b81` (recent precedent — squash-merge canon shipped Arc 40); `substrate/MAJOR_POLYBIUS.md` §13.1 lines 818-833 (n2e target — "Universal escalation triggers (autonomous mode)" bullet list); `substrate/MAJOR_PLINY.md` §5 + §5.2 lines 116-136 (58b target — dispatch-brief authoring locus) + §5.10 lines 424-434 (Arc 40 squash-merge canon) + §5.11 lines 465-507 (paste archival) + §5.12 lines 520-557 (seat-identity dispatch-brief naming) + §6.1 lines 576-608 (Communication routing); `substrate/operating-disciplines.md` line 13 (Thesis sentence — 3ml target) + §11 lines 478-490 step 1.5 (pqn Item 2 target) + §20 lines 1236-1305 (58b cross-ref target; §20.1 + §20.3) + §28 lines 1699-1786 (trailer canon); section-count audit `grep -nE '^## [0-9]+\.' substrate/operating-disciplines.md` (§1 through §31 confirmed — 31 numbered top-level sections; the Thesis at line 11, Agent-regime inverses at line 2040, Empirical lineage at line 2051 are unnumbered); `agents/design/arc-36/design.md` lines 169-606 (pqn Item 1 — locating the 5 VERA probe sites: §4.1.2 line 183, §4.1.6b probe site, §4.2.2 line 300, §4.5.3 line 557, §4.6.1 line 573, §4.8 line 599); arc-36 ZENO verdict via `bw show stoa--jru` (the 5 probe-regex items enumerated by VERA + ZENO at the arc-36 v2 close).

---

## 1. Frame

### 1.1 Four candidates; one bundle; the final canon-edit arc before validate-spec

Arc 41 is Pass 7 of `SPECIFICATION.md` §13 workplan — the FINAL canon-edit arc in the make-the-team-meet-the-spec sequence (Arcs 39+40+41), before Pass 8 reconciliation + Pass 9 validate-spec mechanical-check (Arc 42). Per §13.8 theme: cross-references + audits + Arc 36 follow-ups; a tight bundle of small canon-edits.

The four LOCKED candidates are all 1-line-to-1-paragraph-class changes:

- **C1 (stoa--n2e)** — add `operating-disciplines.md` §20.3 (refusal-as-signal) cross-ref to `MAJOR_POLYBIUS.md`'s "Universal escalation triggers" bullet list (§13.1 lines 826-833).
- **C2 (stoa--58b)** — add `operating-disciplines.md` §20 (credential discipline) cross-ref to `MAJOR_PLINY.md`'s dispatch-brief authoring locus (§5 / §5.2).
- **C3 (stoa--3ml)** — update `operating-disciplines.md` Thesis line 13 stale section-count reference (`§1-§17` → `§1-§31`).
- **C4 (stoa--pqn)** — three Arc 36 v2 follow-ups (VERA probe-regex tightening on `agents/design/arc-36/design.md` for 5 items; bug #40228 surveillance one-liner at op-disc §11 step 1.5; organic `[from:]` adoption observation comment routed per A5 Item 3 pick).

The arc carries no novel structural property (in contrast to Arc 40's A20 recursive-shape surveillance which made PLINY edit PLINY's own role-file mid-arc); it is the smallest arc in the sequence, mostly 1-line cross-refs. The directive's self-application observation #2 frames the question: does tight scope produce clean PASS-first reflecting tighter directive design? The design must not over-build to defeat that observation.

### 1.2 Pre-work: restatement-gate (CAPTAIN_DAEDALUS.md §6.1)

The dispatch brief asked: ship one design.md covering 4 LOCKED candidates; pick A5 sub-decisions (Item 1 lane ε/ζ; Item 2 placement; Item 3 routing) at design time; surface PRINCIPAL-gate per §25 if any pick exceeds DAEDALUS discretion band.

My restatement: **codify three small substrate cross-references (n2e adds §20.3 cite to POLYBIUS escalation triggers; 58b adds §20 cite to PLINY dispatch-brief site; 3ml updates the stale Thesis section-count to current `§1-§31`); land Arc 36 follow-ups across three sub-shapes (5 VERA probe-regex tightening edits to `agents/design/arc-36/design.md` riding this gauntlet under lane ε; a 1-line bug #40228 surveillance observation at op-disc §11 step 1.5; a `[from:]` organic-adoption observation comment on `stoa--myd`).** Every change is content-narrow; no structural restructuring of any target section per A14 hard-locks.

**Imported assumptions named** (per §6.1 honest-restatement requirement):

1. **The Thesis-line section-count "§1-§N" is a sentence-level reference to the count of NUMBERED top-level sections** (`^## N. Title` headings — §1 through §31 as confirmed by `grep -nE '^## [0-9]+\.' substrate/operating-disciplines.md` returning 31 matches at design time). The unnumbered top-level headings — "The thesis these disciplines express" (line 11), "Agent-regime inverses (the positive framing)" (line 2040), "Empirical lineage" (line 2051) — are framing material, not disciplines in the enumeration, and are not counted. The Thesis sentence currently reads "§1-§17 plus the autonomous-mode setup checklist" — that parenthetical "plus the autonomous-mode setup checklist" was authored when the setup checklist lived OUTSIDE the §1-§17 enumeration (pre-Arc 25 / pre-§20). Post-Arc 38, the autonomous-mode setup checklist is §11 — already INSIDE the §1-§31 range. The update therefore removes the "plus the autonomous-mode setup checklist" parenthetical along with the range update, since §11 is now subsumed by the enumeration. Final wording recommendation in §4.C3 below; ADA voice latitude per §5.

2. **The 5 VERA probe-regex tightening items are bounded by the explicit enumeration in `bw show stoa--jru`** ZENO verdict close (2026-05-18T00:04:44Z) + CATO verdict (2026-05-18T00:02:52Z). Items per `bw show stoa--jru` quote: (a) §4.1.2 'cross-tier upward' over-broad — tighten to anchored UPWARD-only pattern; (b) §4.2.2 'no.*watchdog' case-sensitive — add -i; (c) §4.1.6b slot-table shell-escape brittleness; (d) §4.5.3 watcher-cron grep matches anti-pattern's rejection prose — needs context-aware exclusion; (e) §4.6.1/§4.8 whole-file grep — needs git-diff-+-line scoping variant. Spike-revealing-more-than-5 risk is acknowledged in §6 weak-points; if ADA's read of arc-36/design.md surfaces a sixth item that needs the same tightening discipline, ADA folds it under "VERA discipline-extension consistency" rather than punting — but the bounded enumeration is the contract.

3. **Bug #40228 surveillance is observation-only.** The bug (`anthropics/claude-code#40228` — `CronCreate durable: true` doesn't persist to `~/.claude/scheduled_tasks.json` despite documented schema; OPEN since 2026-03-28) is already named in op-disc §11 step 1.5 via the existing `durable: true` discipline (line 322 cite) + Arc 36 design.md §10 follow-up. Arc 41 adds an explicit observation surface so a future operator scanning §11 step 1.5 knows the watch is in place. Per A14 hard-lock: NO recovery-discipline canon change baked in (the discipline is "watch the bug; reassess when Anthropic ships a fix").

4. **Item 3 (`[from:]` organic-adoption observation) is comment-routing, not canon-promotion.** A14 hard-locks A2.5 scope expansion intentionally; pqn ticket Item 3 explicitly frames as "low priority, observation-deferred-until-pattern-confirms." The Arc 36 v2 close-out evidence (93 `[from:]`-tagged comments on stoa--jru across 9 seat-slugs per POLYBIUS_the_stoa standdown) + the Arcs 37-40 informal continuation is genuine N-evidence; routing the observation to `stoa--myd` (multi-checker convergence accretion P4) co-locates it with the existing N=1 multi-checker observation rather than spawning a new ticket.

The restatement converges with the brief; no `refused` gate fires. All three A5 sub-decisions land within DAEDALUS discretion band; no PRINCIPAL-gate-eligible picks surface at design time.

---

## 2. Cross-cutting universal disciplines (apply to all candidates)

### 2.1 §28 Co-Authored-By trailers on every ADA + DAEDALUS commit

Every commit landed inside `.claude/worktrees/arc-41-build/` by ADA or DAEDALUS carries:

```
Co-Authored-By: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>
```

Worked examples (verbatim per `substrate/operating-disciplines.md` §28.1 lines 1714-1718):

```
Co-Authored-By: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa.local>
Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
```

Use HEREDOC body. Per A6 LOCKED. The trailer is the seat-identity signal; `Author:` stays PRINCIPAL's `git config user.*` per global `~/.claude/CLAUDE.md` immutable rule.

### 2.2 §5.10 signoff with live-verified state

PLINY's Phase 4 signoff cites live-verified state per §19.6 attestation-honesty — never echoes dispatch-authoring SHAs without re-verification. The cleanup-verification commands per `MAJOR_PLINY.md` §5.10 lines 428-434 are mandatory before the signoff comment is posted: `git branch` + `git ls-remote --heads origin arc-41/build` (branch); `git worktree list` (worktree); `ls substrate/arcs/arc-41/pastes/` + `ls HUMAN_paste-*arc-41*` (paste archival per §5.11 lines 485-487).

### 2.3 §5.10 squash-merge — Arc 40 canon ENFORCED

Phase 4 squash-merge MUST follow the `MAJOR_PLINY.md` §5.10 line 434 canon shipped in Arc 40 (`dbb5b81`, 2026-05-18). The discipline is now substrate canon, not convention:

- **Option (a) PREFERRED:** `gh pr merge <N> --squash --delete-branch --subject "..."` — OMIT `--body`. GitHub's default squash body auto-concatenates the source commits' bodies, preserving all `Co-Authored-By:` trailers per `operating-disciplines.md` §28.3 (lines 1737-1741).
- **Option (b) acceptable:** include `--body` HEREDOC with `Co-Authored-By:` trailers explicitly listed in the body so the override does not strip them.

Anti-pattern (Arc 37 regression at `bb12806` — empirically tested + canonized at op-disc §28.3.1 in Arc 40): `--body "<clean summary without trailers>"` silently strips every seat-identity signal from the squash-merge commit on main.

### 2.4 §5.11 paste archival on arc close (A16 wording-clarification)

Per A16 LOCKED + Arc 40 POLYBIUS observation folded into the Arc 41 directive: archival is **only** the 2 HUMAN_paste-*.md activation files (git-mv'd to `substrate/arcs/arc-41/pastes/`). The directive itself stays at `substrate/arcs/arc-41-build-directive.md` flat path; NO directive moved to `pastes/` subdir.

Concretely, at arc-close PLINY runs:

```
mkdir -p substrate/arcs/arc-41/pastes
git mv HUMAN_paste-pliny-arc-41-instruction.md   substrate/arcs/arc-41/pastes/
git mv HUMAN_paste-polybius-arc-41-instruction.md substrate/arcs/arc-41/pastes/
git commit -m "Arc 41: archive activation pastes to substrate/arcs/arc-41/pastes/"
git push
```

`git mv` preserves the file's git-log --follow continuity per §5.11 line 480; plain `mv` + `git rm` + `git add` would break this. Note for ARGUS: same precedent-versus-wording question raised at Arc 39 / Arc 40 closes is now resolved by directive A16 wording-clarification; PLINY follows the clarified wording.

### 2.5 A15 CATO MANDATORY

Pass 9 validate-spec is imminent in Arc 42; cumulative craft scrutiny matters across canon-edit arcs even when individual diffs are small. CATO PASS required before Phase 4 ship per directive A15.

### 2.6 ADA brief preamble (per MAJOR_PLINY.md §5.2 — reproduce verbatim in §2)

ADA: ground-check every concrete example in the design against the shipped code, specifically:

- JSON example shapes (response bodies, request bodies)
- Function/method signatures (parameter names, types, return types)
- Error message text (exact string match)
- Line ranges in path:line citations
- HTTP response codes
- Wire-protocol constants (header names, status codes, envelope keys)

If a design example contradicts the shipped code, the shipped code is canon — flag the design drift but build to ship reality.

For Arc 41 specifically, the candidates most at risk for ground-check are:

- **C3's section-count claim** (`§1-§31` — verified at design time via `grep -nE '^## [0-9]+\.' substrate/operating-disciplines.md` returning 31 matches; ADA re-verifies before writing the edit; if the count differs at ADA's read time, ADA writes the live count and flags the design drift in the build commit body).
- **C4 Item 1's 5 probe-site line numbers** in `agents/design/arc-36/design.md` (cited as §4.1.2 line 183, §4.2.2 line 300, §4.5.3 line 557, §4.6.1 line 573, §4.8 line 599, and the §4.1.6b probe-site whose exact line ADA locates fresh — directive cited "5 items" not 5 lines; the bounded enumeration is the contract, not the lines).
- **C4 Item 2's existing op-disc §11 step 1.5 bug #40228 mention** at line 322 (`grep -nE '40228' substrate/operating-disciplines.md` at design time confirmed; ADA re-verifies the line and inserts the new surveillance line at the structurally right place).

### 2.7 A13 author frontmatter — not triggered

Arc 41 introduces no new substrate-canon files with YAML frontmatter. n2e + 58b + 3ml are inline canon edits; pqn Item 1 edits `agents/design/arc-36/design.md` (already exists; no new file); pqn Item 2 is a 1-line addition at op-disc §11 step 1.5; pqn Item 3 is a bw comment on `stoa--myd` (no file). A13 is therefore not triggered; the `author: Denson Smith` global rule applies if any file with such a frontmatter is touched, but no such file is in Arc 41's scope. ARGUS to confirm the trigger remains untriggered if A5 picks shift during revision.

### 2.8 §20 credential discipline NON-APPLICABLE

Arc 41 touches no credentialed third-party API or cloud service. All edits are local substrate canon (markdown) + one design.md edit + one bw comment. No CI workflow authored; no API token, OAuth scope, or service account in scope. §6.6 credential discipline (per `CAPTAIN_DAEDALUS.md`) is NON-APPLICABLE to this arc. Probe §3.7 below makes this explicit.

---

## 3. Per-candidate scopes

### 3.C1 — stoa--n2e: cross-ref MAJOR_POLYBIUS.md escalation triggers → op-disc §20.3 (refusal-as-signal)

**Target site:** `substrate/MAJOR_POLYBIUS.md` §13.1 "Universal escalation triggers (autonomous mode)" bullet list (lines 826-833). The current list reads:

```
**Universal escalation triggers (autonomous mode).** Every seat surfaces to PRINCIPAL on:

- Substance disagreement after one round-trip with peer.
- Authorship/copyright/PRINCIPAL-final-say content.
- Irreducible ambiguity that blocks progress.
- Peer silence > 60 minutes on an open coordination ticket.

Routine technical/operational decisions stay at the seat.
```

**Recommended edit shape (DAEDALUS picks per A2):** add a fifth bullet naming refusal-as-signal violations as a universal escalation trigger, AND add a cite-comment immediately after the list resolving the cross-ref to op-disc §20.3.

```
**Universal escalation triggers (autonomous mode).** Every seat surfaces to PRINCIPAL on:

- Substance disagreement after one round-trip with peer.
- Authorship/copyright/PRINCIPAL-final-say content.
- Irreducible ambiguity that blocks progress.
- Peer silence > 60 minutes on an open coordination ticket.
- Refusal-as-signal: any tool call refused by PRINCIPAL or by a credentialed
  step the agent attempts (1Password biometric refused, gcloud/gh/aws auth
  refused, MCP-server-denied scope). Halt immediately, do NOT retry, do
  NOT improvise a fallback. Per `operating-disciplines.md` §20.3, a refusal
  is the substrate telling the agent the design is wrong, not a transient
  failure to route around.

Routine technical/operational decisions stay at the seat.

(Cross-ref: `operating-disciplines.md` §20.3 — refusal-as-signal canon.)
```

**Out-of-scope per A14 hard-lock:** no other restructuring of MAJOR_POLYBIUS.md §13.1 or surrounding §13.x; the bullet add + cite-comment is the entire edit.

**Reciprocation:** the cite-comment is one-directional (POLYBIUS → op-disc §20.3). op-disc §20.3's existing prose at lines 1283-1291 names the rule generally enough that a back-reference is not load-bearing; the §20.3 cross-ref body at lines 1305-1306 boundary-marker against §20.4 is the cross-team-readable surface. If ARGUS surfaces that a back-reference IS needed for cite-completeness, the back-ref can be one additional cite-comment at op-disc §20.3 close ("Cross-ref: `MAJOR_POLYBIUS.md` §13.1 enumerates refusal-as-signal in the universal escalation triggers list").

### 3.C2 — stoa--58b: cross-ref MAJOR_PLINY.md dispatch-brief site → op-disc §20 (credential discipline)

**Target site:** `substrate/MAJOR_PLINY.md` §5.2 (ADA brief preamble — lines 116-136). DAEDALUS picks §5.2 over §6 (Communication) because §5.2 is the *dispatch-brief authoring locus*: it is the section that already names the ADA brief preamble verbatim and is the structural surface PLINY consults when authoring a dispatch brief. §6 is a Communication channel-routing table, not a brief-authoring surface. Per 58b ticket: "the brief should point CAPTAINs at operating-disciplines.md §20" — §5.2 is where the brief is composed.

**Recommended edit shape (DAEDALUS picks per A3):** add a new subsection at §5.2's tail (after the empirical anchor at line 136), naming the credential-discipline cross-ref as a brief-composition discipline.

```
### 5.2.1 Credential-discipline cite for credentialed-operations dispatches

When the dispatch brief involves credentialed operations against any
third-party API or cloud service (Railway, gcloud, gh, op, aws, azure,
kubectl, vercel, fly — any CLI or HTTP API gated by an API token, OAuth
scope, or service account), the brief MUST point the CAPTAIN at
`operating-disciplines.md` §20 (Credential discipline) so the CI-mediated
canon is structurally surfaced at the dispatch moment rather than left for
the CAPTAIN to rediscover. The cite is one line in the brief's preamble:

> See `operating-disciplines.md` §20 (Credential discipline) for the
> CI-mediated canonical pattern (§20.1), the five rejected anti-patterns
> (§20.2), and the universal rule (§20.4). Agents author CI workflows;
> agents do NOT hold credentials.

The brief's credential-flow section MUST specify a CI-mediated path
(workflow YAML the agent authors; CI runs the workflow). Any per-call
credentialed-CLI dispatch in the brief is a §20.2 anti-pattern — refuse
back to POLYBIUS for re-scope rather than dispatch.

(Cross-ref: `operating-disciplines.md` §20 — full credential discipline
canon. §20.3 refusal-as-signal is the responsive sibling — when an external
refusal has already happened mid-dispatch, halt immediately per
`MAJOR_POLYBIUS.md` §13.1 universal escalation triggers + §20.3.)
```

**Out-of-scope per A14 hard-lock:** no restructuring of §5 or §6 beyond the 5.2.1 subsection add; existing §5.2 prose unchanged; §6 (Communication) unchanged.

**Reciprocation:** op-disc §20 already names PLINY as a universal-seat at line 1238 ("Universal-seat — POLYBIUS, PLINY, every CAPTAIN..."); a back-reference at §20 to MAJOR_PLINY.md §5.2.1 is one cite-comment if ARGUS surfaces that cite-completeness needs it. The cross-ref pair (POLYBIUS → §20.3 via §13.1, PLINY → §20 via §5.2.1) leaves op-disc §20 with two upstream POLYBIUS-tier + PLINY-tier read-sites, which is the substantive property the n2e+58b pair-ticket-shape produces.

### 3.C3 — stoa--3ml: op-disc Thesis line 13 stale section-count

**Target site:** `substrate/operating-disciplines.md` line 13 — the Thesis paragraph's enumeration parenthetical.

**Current text (verified at design time):**

```
The disciplines below (§1-§17 plus the autonomous-mode setup checklist) are not a flat list of operational rules. They are expressions of one underlying design thesis about how agentic systems align with human goals on complex projects.
```

**Recommended edit (DAEDALUS picks per A4):**

```
The disciplines below (§1-§31) are not a flat list of operational rules. They are expressions of one underlying design thesis about how agentic systems align with human goals on complex projects.
```

**Two simultaneous changes in one sentence-level edit:**

1. **Range:** `§1-§17` → `§1-§31`. Verified at design time: `grep -nE '^## [0-9]+\.' substrate/operating-disciplines.md` returns 31 matches; current file has §1-§31 numbered top-level sections post-Arc 38's §31 add. (Unnumbered headings at line 11 "The thesis these disciplines express", line 2040 "Agent-regime inverses", line 2051 "Empirical lineage" are framing material, not disciplines — correctly excluded.)

2. **Parenthetical drop:** "plus the autonomous-mode setup checklist" is REMOVED. The autonomous-mode setup checklist is `operating-disciplines.md` §11 (line 478), which is INSIDE the §1-§31 range. The parenthetical was load-bearing pre-Arc-25 when the setup checklist lived outside the §1-§N enumeration. Post-Arc 38 it is redundant + reader-misleading (suggests the checklist is NOT counted when it IS).

**Out-of-scope per A14 hard-lock:** no other editing of Thesis prose beyond this single-sentence section-count update; surrounding paragraphs (lines 15-31) untouched; voice unchanged.

**Re-verification at ADA build time:** if the section count differs from `§31` at ADA's read time (e.g., a substrate edit in flight raises the count), ADA writes the live count and flags the design drift in the build commit body. The "current at ship time" property matters more than the design-time count.

### 3.C4 — stoa--pqn: Arc 36 v2 follow-ups (3 items)

#### 3.C4.1 — Item 1: VERA probe-regex tightening on agents/design/arc-36/design.md (A5 Item 1 = ε in-arc-build)

**A5 Item 1 pick: ε in-arc-build.** Rationale: the 5 probe-regex items are wording-tight enough to benefit from ARGUS pre-gate + CATO meta-verify rather than direct-to-main; lower risk to bundle through the gauntlet since they're inside `agents/design/` (design archive, not substrate canon). User-tier weakly leans ε for craft scrutiny; honored. ζ direct-to-main would have been the lower-friction lane consistent with mn3 routing, but mn3's framing is structurally different (mn3 is design.md probe-spec fixes that PLINY-leans α direct-to-main per the mn3 ticket body itself; pqn Item 1 has no such ticket-body lane lean and benefits from the redundant-checker property).

**Target sites in `agents/design/arc-36/design.md`** (5 items, per VERA + ZENO enumeration in `bw show stoa--jru` at 2026-05-18T00:04:44Z; lines verified at design time):

**(a) §4.1.2 over-broad regex — line 186-187:**

Current:
```bash
awk '/^### 7\.4/,/^### 7\.5/' substrate/operating-disciplines.md | grep -iE 'upward[- ]only|cross-tier upward|UPWARD requests only'
# Expected: zero matches (old wording fully replaced)
```

Issue: `cross-tier upward` matches intentional use-case prose elsewhere in §7.4 replacement text. The probe was meant to detect *legacy UPWARD-only* framing, not the bidirectional-prose mention of upward use cases.

Tightened replacement:
```bash
awk '/^### 7\.4/,/^### 7\.5/' substrate/operating-disciplines.md | grep -E 'upward[- ]only|UPWARD requests only|^[^a-zA-Z]*upward\.only'
# Expected: zero matches (anchored to old wording shape; case-sensitive to avoid bidirectional-prose hits)
```

The pattern is anchored to the literal legacy phrases (`upward-only` / `upward only` hyphen-or-space; `UPWARD requests only`; `upward.only` only when preceded by non-letter context). Removes `cross-tier upward` (over-broad) and drops `-i` flag (the legacy framing was case-explicit).

**(b) §4.2.2 case-sensitive regex — line 306:**

Current:
```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -cE 'no.*watchdog|no additional'
# Expected: ≥1 (explicitly accepts the failure mode rather than mitigating via watcher cron)
```

Issue: shipped prose capitalizes `No`; the probe's `no.*watchdog` doesn't match `No.*watchdog`. Add `-i` flag.

Tightened replacement:
```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md | grep -ciE 'no.*watchdog|no additional'
# Expected: ≥1 (case-insensitive to match 'No' / 'no' prose variants)
```

**(c) §4.1.6 slot-table shell-escape brittleness (R2 rev2 spike resolution):**

VERA's informal "§4.1.6b" label in the `bw show stoa--jru` ZENO close (2026-05-18T00:04:44Z) was a sub-issue annotation for the slot-table-regex brittleness WITHIN the §4.1.6 probe block — NOT a separate heading. `agents/design/arc-36/design.md` carries §4.1.1 through §4.1.10 only; no §4.1.6b heading exists. Interpretation (ii) per PLINY R2 spike — sub-probe relocated under §4.1.6 with awk pattern grounded against the LIVE heading shape.

**Target site:** `agents/design/arc-36/design.md` §4.1.6 (line 232 — "Substitution-slot table extended with SLUG slots"), specifically the second awk-grep pipeline at line 238:

```bash
awk '/^## Substitution slots/,/^---$/' substrate/templates/polling-cron-prompt-template.md | grep -cE '\| \`\{\{SELF_SEAT_SLUG\}\}\`|\| \`\{\{PEER_SEAT_SLUG\}\}\`'
```

Issue: the regex carries backslash-escaped backticks (`\``) inside a single-quoted argument; while POSIX-safe in practice, the backslash-before-backtick shape is shell-escape brittle (double-quote re-evaluation would interpret the backtick as command substitution; the design surfaced this as a probe-precision item rather than a substrate defect). VERA's tightening rec: simplify to bare-backtick-equipped pattern that survives shell-quoting unambiguously.

Tightened replacement (DAEDALUS recommendation; ADA voice latitude):
```bash
awk '/^## Substitution slots/,/^---$/' substrate/templates/polling-cron-prompt-template.md \
  | grep -cE '\{\{SELF_SEAT_SLUG\}\}|\{\{PEER_SEAT_SLUG\}\}'
# Expected: 2 (both new slots present in the slot table itself; pattern drops
# the table-row-pipe + backtick anchors — the slot-name match alone is
# unambiguous within the slot-table awk-bracketed region, no shell-escape
# fragility)
```

ADA refines the exact tightening wording if the live brittleness has shifted from the design-time read; the discipline is "the probe's regex must survive shell-quoting at execution time without `bash -c`-style re-evaluation."

**(d) §4.5.3 watcher-cron grep matches anti-pattern's rejection prose — line 560:**

Current:
```bash
grep -rE 'watcher cron|watchdog cron|separate watcher' substrate/operating-disciplines.md substrate/templates/
# Expected: zero matches in NEW content (existing references in arc-22 directive at substrate/arcs/ are reference material and excluded)
```

Issue: the probe's pattern matches anti-pattern's REJECTION prose in §11 / §C.1 ("Option 2 watcher cron was rejected because..."). The probe was meant to detect *new* watcher-cron prose, not the rejection-citation.

Context-aware exclusion replacement:
```bash
# Search for NEW watcher-cron prose, excluding rejection-context lines:
grep -rnE 'watcher cron|watchdog cron|separate watcher' substrate/operating-disciplines.md substrate/templates/ \
  | grep -vE 'rejected|anti-pattern|Option 2|not the substrate|do NOT'
# Expected: zero matches (rejection-context lines excluded; only NEW watcher-cron prose surfaces)
```

**(e) §4.6.1 / §4.8 whole-file grep needs git-diff-+-line scoping — lines 576, 605:**

Current §4.6.1:
```bash
grep -rE '\b[Cc]olonel\b|\bthe user\b' substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md | grep -vE 'template-slot|arcs/' | head -10
# Expected: zero non-template hits
```

Issue: whole-file grep catches pre-existing legacy `the user` references unrelated to the arc's new content; the probe should scope to ADDED lines only (`git diff main...arc-36/build` `+` lines).

Tightened replacement (variant; ADA picks the equivalent that runs on the build target):
```bash
# Scope to git-diff +-lines added by arc-36/build relative to main:
git diff main...arc-36/build -- substrate/operating-disciplines.md substrate/MAJOR_POLYBIUS.md substrate/templates/polling-cron-prompt-template.md substrate/templates/autonomous-mode-activation-template.md \
  | grep -E '^\+' | grep -vE '^\+\+\+' | grep -E '\b[Cc]olonel\b|\bthe user\b'
# Expected: zero non-template +-line hits in new arc-36 content
```

Same shape applied to §4.8 credential-discipline probe at line 605 (whole-file grep → git-diff +-line scoping).

**Out-of-scope per A14 hard-lock:** no broader probe-spec reorganization; no new §4.x subsections; no edits to the design.md beyond the 5 enumerated tightening sites; no edits to the substrate Arc 36 shipped at fcd68c0.

**Self-application note:** the 5 probes' tightening discipline matches the new `CAPTAIN_VERA.md` §5.11 probe-spec regex anchoring canon shipped in Arc 40 — each tightening converges with the canon's "every regex anchored; every install.sh-flag citation grounded; every bw-output grep grounded" rule. This is N-evidence for the §5.11 canon's worked-when-applied gate (Arc 40 N=0 at ship; pqn Item 1 contributes the first worked-when-applied data point under the new canon).

#### 3.C4.2 — Item 2: bug #40228 surveillance line at op-disc §11 step 1.5 (A5 Item 2 pick)

**A5 Item 2 pick: insert one observation line at op-disc §11 step 1.5, immediately after the existing bug #40228 reference at the `durable: true` discipline site.** Rationale: the existing bug citation at op-disc:322 (per §4.2.2a probe in arc-36 design) already names the bug as the empirical-anchor provenance for the `durable: true` honest-intent encoding. Adding the surveillance line at the same site groups the watch-and-honest-intent prose for any future operator scanning §11 step 1.5; placing it elsewhere (e.g., a new sub-bullet at §11 step 1.5 tail) would scatter the bug-related prose. Observation-only per pqn ticket Item 2 + A14 hard-lock — no recovery-discipline canon promotion.

**Recommended edit shape (DAEDALUS picks per A5 Item 2):** append one observation line to op-disc §11 step 1.5's existing `durable: true` discipline paragraph. ADA locates the precise insertion point by grepping for the existing `40228` citation:

```bash
grep -n '40228' substrate/operating-disciplines.md
```

then insert the surveillance line immediately after the existing citation paragraph (target: at the close of the `durable: true` discipline, before the next discipline beat).

**Surveillance line wording (DAEDALUS recommendation; ADA voice latitude):**

```
**Bug #40228 surveillance state.** The `durable: true` parameter encoded above
is honest-intent: it works when the bug is fixed without canon revision (the
parameter is documented schema; the persistence is the runtime defect). Watch
state as of Arc 41 (2026-05-18): bug #40228 remains OPEN at
anthropics/claude-code; no recovery-discipline canon change is baked in at
§11 step 1.5; recovery rests on `MAJOR_POLYBIUS.md` §9 step 7 PRINCIPAL-consent
re-setup. If the bug is fixed in a Claude Code release, the canon does NOT
need revision — `durable: true` becomes load-bearing-as-documented rather than
honest-intent-only. No reassessment ticket required until bug closure.
```

**Out-of-scope per A14 hard-lock:** no recovery-discipline canon change; no Option-2 watcher-cron prose (the existing prose at §11 step 1.5 has the anti-pattern rejection in place — surveillance line does NOT touch the anti-pattern boundary); no new §11.x subsection; no change to the `durable: true` parameter or its place in the renewal-cron prompt body.

#### 3.C4.3 — Item 3: `[from:]` organic-adoption observation comment on stoa--myd (A5 Item 3 pick)

**A5 Item 3 pick: file observation comment on `stoa--myd` (multi-checker convergence accretion P4).** Rationale: `stoa--myd` already exists as the accretion store for N-evidence on multi-checker / multi-seat substrate-property observations (filed by user-tier POLYBIUS at the-stoa MAJOR_POLYBIUS Arc 25 standdown recommendation; the ticket-body's accretion mechanism is precisely "when a future arc surfaces a similar convergent finding, add a comment on this ticket"). The `[from:]` organic-adoption across Arcs 36-37-38-39-40 (93 + ongoing tagged comments across 9 seat-slugs as of Arc 36 v2 close per POLYBIUS_the_stoa standdown) is a multi-seat substrate-property observation in exactly the shape myd accretes — NOT a discrete observation needing a fresh ticket. User-tier weakly leans comment-on-myd; honored. A14 hard-lock confirmed — NOT canon-promotion in this arc per pqn Item 3 framing + the A2.5 intentional hard-lock.

**Observation comment text (DAEDALUS recommendation; ADA voice latitude):**

```
[from: daedalus-the-stoa] Arc 41 organic-adoption N-evidence entry per pqn Item 3.

**Property observed:** the `[from: <self-seat-slug>]` author-tag convention shipped
by Arc 36 v2 (§7.1 fifth-beat, A2.5-scoped to POLYBIUS-on-POLYBIUS only) has
organically extended beyond A2.5 scope across all CAPTAINs + PLINY across Arcs
36, 37, 38, 39, 40.

**N-tally as of 2026-05-18:**
- Arc 36 v2 close (stoa--jru): 93 [from:]-tagged comments across 9 seat-slugs
  (POLYBIUS_the_stoa standdown, 2026-05-18T00:13:31Z).
- Arcs 37-40: continued informal organic use by every seat that comments on bw
  during gauntlet execution.

**Gauntlet-property frame (per myd ticket-body accretion thesis):** the
adoption is not multi-checker convergence on a finding — it is multi-seat
convergence on a substrate convention. Different shape than the N=1 Arc 25
observation (which was four checkers converging on the same P10 finding); same
shape in that organic convergence across independent seats is what the
substrate is observed to produce.

**A2.5 scope frame:** the convention was intentionally A2.5-scoped to
POLYBIUS-on-POLYBIUS to bound the timeline-arithmetic surface (§7.7 case 4 in
op-disc only consumes POLYBIUS-attributed comments). The organic wider use is
style-not-substance per pqn ticket Item 3 — informative but doesn't ship a
substrate need yet. Future arc may codify wider adoption as A2.5 scope
expansion if/when gauntlet-pacing failure modes surface that would benefit
from PLINY/CAPTAIN timeline contribution.

**Disposition:** N-evidence accretion only per pqn Item 3 + Arc 41 A14
hard-lock (no canon promotion in Arc 41). Add this comment as the multi-seat
substrate-convention adoption data point on myd's accretion thread.

Cross-refs:
- pqn ticket Item 3 (Arc 36 v2 follow-up, "Convention adoption beyond A2.5 scope")
- Arc 36 v2 close (stoa--jru, POLYBIUS_the_stoa standdown 2026-05-18T00:13:31Z)
- op-disc §7.1 beat 5 + §7.7 (the shipped convention)
- Arc 41 design.md §3.C4.3
```

**Out-of-scope per A14 hard-lock:** no canon promotion (A2.5 scope expansion is hard-locked); no new ticket; no extension of `[from:]` to non-POLYBIUS seats in any substrate doc; no mechanical-parser enforcement.

---

## 4. Verification probes (for VERA)

Per the recently-shipped `CAPTAIN_VERA.md` §5.11 probe-spec regex anchoring discipline (Arc 40) + the VERA m1+m2 / stoa--mn3 teaching moment: every regex anchored, every install.sh-flag citation grounded, every bw-output grep grounded.

### §4.1 — A6 trailer check (universal)

**§4.1.1 — DAEDALUS design commit carries §28 trailer**

```bash
git log arc-41/build --pretty='%H %s%n%(trailers:key=Co-Authored-By)' -n 20 \
  | grep -cE '^Co-authored-by: CAPTAIN_DAEDALUS_the-stoa <captain-daedalus@the-stoa\.local>$'
# Expected: ≥1 (DAEDALUS design.md commit on arc-41/build carries the trailer; case-insensitive header per git's lowercase normalization)
```

**§4.1.2 — ADA build commit(s) carry §28 trailer**

```bash
git log arc-41/build --pretty='%H %s%n%(trailers:key=Co-Authored-By)' -n 20 \
  | grep -cE '^Co-authored-by: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa\.local>$'
# Expected: ≥1 (ADA build commit on arc-41/build carries the trailer)
```

### §4.2 — A2 n2e: MAJOR_POLYBIUS.md cross-ref to op-disc §20.3 resolves

**§4.2.1 — refusal-as-signal bullet added to §13.1 Universal escalation triggers**

```bash
awk '/^### 13\.1/,/^### 13\.2/' substrate/MAJOR_POLYBIUS.md \
  | grep -cE '^- Refusal-as-signal:|^- \*\*Refusal-as-signal'
# Expected: ≥1 (the new bullet present in the §13.1 Universal-escalation-triggers list)
```

**§4.2.2 — cross-ref cite-comment resolves to op-disc §20.3**

```bash
awk '/^### 13\.1/,/^### 13\.2/' substrate/MAJOR_POLYBIUS.md \
  | grep -cE 'operating-disciplines\.md.*§20\.3|§20\.3 — refusal-as-signal'
# Expected: ≥1 (cite-comment names the §20.3 target)
```

**§4.2.3 — op-disc §20.3 read-site resolves the back-pointer (no edit; just citation surface)**

```bash
awk '/^### 20\.3/,/^### 20\.4/' substrate/operating-disciplines.md \
  | grep -cE 'refusal-as-signal|refused by PRINCIPAL'
# Expected: ≥1 (op-disc §20.3 prose intact; cite-comment back-pointer is optional per §3.C1 reciprocation note)
```

### §4.3 — A3 58b: MAJOR_PLINY.md cross-ref to op-disc §20 resolves

**§4.3.1 — new §5.2.1 subsection present**

```bash
grep -nE '^### 5\.2\.1' substrate/MAJOR_PLINY.md
# Expected: one match (the new §5.2.1 subsection header)
```

**§4.3.2 — credential-discipline cite-comment resolves to op-disc §20**

```bash
awk '/^### 5\.2\.1/,/^### 5\.3/' substrate/MAJOR_PLINY.md \
  | grep -cE 'operating-disciplines\.md.*§20|§20\.1|§20\.2|§20\.4'
# Expected: ≥1 (cite-comment names the §20 target with at least one specific subsection cite)
```

**§4.3.3 — §5.2.1 names the CI-mediated structural property**

```bash
awk '/^### 5\.2\.1/,/^### 5\.3/' substrate/MAJOR_PLINY.md \
  | grep -ciE 'CI-mediated|agents author.*CI workflows|agents do NOT hold credentials'
# Expected: ≥1 (the structural property — CI-mediated path; case-insensitive for prose-style tolerance)
```

### §4.4 — A4 3ml: Thesis line 13 sentence count updated

**§4.4.1 — Thesis sentence references current section-count range (extracted literal must equal §4.4.3 live count — R4 rev2 coherence check)**

```bash
# R4 rev2: hard-coded `§1-§31` removed; replaced with coherence check between
# the Thesis-literal and §4.4.3's live count. The previous probe coupled to
# a design-time count that could drift between design and ship; the coherence
# pair (§4.4.1 extracts; §4.4.3 counts; equality verified at probe time)
# eliminates the drift surface entirely.

# §4.4.1 — extract the Thesis-line section-count upper-bound integer:
THESIS_HIGH=$(sed -n '13p' substrate/operating-disciplines.md \
  | grep -oE '§1-§[0-9]+' | grep -oE '[0-9]+$')
echo "Thesis-line claim: §1-§${THESIS_HIGH}"
# Expected: prints "Thesis-line claim: §1-§N" with N matching §4.4.3's live count
```

**§4.4.2 — stale §1-§17 + parenthetical "plus the autonomous-mode setup checklist" both removed**

```bash
sed -n '13p' substrate/operating-disciplines.md \
  | grep -cE '§1-§17|plus the autonomous-mode setup checklist'
# Expected: 0 (both stale fragments removed)
```

**§4.4.3 — Thesis-line literal equals live section count (R4 rev2 coherence)**

```bash
# Live section count at probe time:
LIVE_COUNT=$(grep -cE '^## [0-9]+\.' substrate/operating-disciplines.md)
# Thesis-line extracted literal from §4.4.1:
THESIS_HIGH=$(sed -n '13p' substrate/operating-disciplines.md \
  | grep -oE '§1-§[0-9]+' | grep -oE '[0-9]+$')
# Coherence check: both probes pass when consistent; either fails if substrate
# drifts mid-run.
test "${THESIS_HIGH}" = "${LIVE_COUNT}" && echo "PASS: Thesis ${THESIS_HIGH} = live ${LIVE_COUNT}" || echo "FAIL: drift Thesis=${THESIS_HIGH} live=${LIVE_COUNT}"
# Expected: "PASS: Thesis N = live N" (where N is the current section count;
# the design's §3.C3 re-verification clause fires at ADA build time if the
# count differs from design-time §31, and ADA writes the live count — but
# this probe verifies coherence at the same run regardless of the absolute
# number, eliminating the hard-coded `Expected: 31` brittleness)
```

### §4.5 — A5 Item 1: pqn VERA probe-regex tightening (ε in-arc-build)

**§4.5.1 — design.md §4.1.2 probe pattern tightened (no longer includes over-broad `cross-tier upward`)**

```bash
awk '/^\*\*§4\.1\.2/,/^\*\*§4\.1\.3/' agents/design/arc-36/design.md \
  | grep -cE 'cross-tier upward'
# Expected: 0 (the over-broad pattern fragment removed from the §4.1.2 probe block)
```

**§4.5.2 — design.md §4.2.2 probe carries `-i` (or `grep -ci`) flag**

```bash
awk '/^\*\*§4\.2\.2 /,/^\*\*§4\.2\.2a/' agents/design/arc-36/design.md \
  | grep -cE 'grep -[a-z]*i[a-z]* '
# Expected: ≥1 (case-insensitive flag added; allows `grep -ciE` / `grep -iE` / similar)
# Note (R1 rev2 fix): live §4.2.2 heading uses em-dash (U+2014) not three ASCII
# hyphens; pattern drops the literal `---` and uses trailing space to
# disambiguate from §4.2.2a/§4.2.2b siblings. Verified against live file:
# the corrected pattern brackets a non-empty range (~17 lines including the
# probe code block); the previous `---` pattern bracketed zero lines (false-PASS).
```

**§4.5.3 — design.md §4.5.3 probe excludes rejection-context lines**

```bash
awk '/^\*\*§4\.5\.3/,/^\*\*§4\.5\.4/' agents/design/arc-36/design.md \
  | grep -cE 'rejected|anti-pattern|Option 2'
# Expected: ≥1 (the rejection-context exclusion clause present in the tightened probe)
```

**§4.5.4 — design.md §4.6.1 or §4.8 probe uses git-diff +-line scoping variant (R3 rev2 fix)**

```bash
# R3 rev2 fix: re-cast as structural property check (two literal-anchored
# checks; previous combined-alternation `grep -E .\^\+` was malformed —
# `.` matched any char where a quote was intended; `\^` only matches
# literal `^` outside a character class). Concretely: the §4.6-or-§4.8
# region must contain BOTH the git-diff invocation against arc-36/build
# AND the ^+ line-prefix filter idiom.
awk '/^### §4\.6/,/^### §4\.7/' agents/design/arc-36/design.md \
  | grep -cF 'git diff main...arc-36/build'
# Expected: ≥1 (git-diff invocation present in §4.6 range)

awk '/^### §4\.8/,/^---$/' agents/design/arc-36/design.md \
  | grep -cF 'git diff main...arc-36/build'
# Expected: ≥1 (git-diff invocation present in §4.8 range; the §4.5.4 contract
# is OR semantics — either §4.6 or §4.8 carries the +-line scoping; tighten
# to AND by summing both probes if pqn Item 1 applies to both per §5.4.e)

# Structural sub-check: the ^+ line-prefix filter idiom appears in at least
# one §4.6 or §4.8 probe block (the git-diff output is then scoped to added
# lines only via this filter):
{ awk '/^### §4\.6/,/^### §4\.7/' agents/design/arc-36/design.md ; \
  awk '/^### §4\.8/,/^---$/' agents/design/arc-36/design.md ; } \
  | grep -cF "grep -E '^\\+'"
# Expected: ≥1 (the +-line filter present in at least one tightened probe;
# fgrep literal-match avoids the previous malformed-regex hazard)
```

**§4.5.5 — design.md §4.1.6 slot-table sub-probe rewritten to survive shell-quoting (R2 rev2 locator correction)**

```bash
# R2 spike: "§4.1.6b" was VERA's informal sub-issue label, not a separate
# heading; live arc-36/design.md carries §4.1.1 through §4.1.10 only. Probe
# retargeted to the real §4.1.6 heading. Discipline: "no $VAR-shaped shell
# substitution in the regex; no backslash-escaped-backtick fragility; no
# unescaped backticks." Probe shape (post-tightening structural property):
awk '/^\*\*§4\.1\.6 /,/^\*\*§4\.1\.7/' agents/design/arc-36/design.md \
  | grep -cE '\$\(|\$\{|\\`'
# Expected: 0 (no shell-substitution / backslash-escaped-backtick patterns
# remain in the tightened §4.1.6 probe block; the bare-slot-name pattern
# survives shell-quoting unambiguously per §3.C4.1.c)
```

### §4.6 — A5 Item 2: bug #40228 surveillance line at op-disc §11 step 1.5

**§4.6.1 — surveillance line present at §11 step 1.5**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md \
  | grep -cE 'surveillance|surveillance state|Bug #40228 surveillance|watch state'
# Expected: ≥1 (surveillance-line wording present in §11 step 1.5)
```

**§4.6.2 — surveillance line preserves the existing #40228 citation (observation-only, no canon change)**

```bash
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md \
  | grep -cE '40228'
# Expected: ≥2 (the existing citation at line ~322 PLUS the new surveillance line both cite #40228; if this returns <2 the canon was edited in a way that removed the existing citation — A14 hard-lock violation)
```

**§4.6.3 — no recovery-discipline canon change (anti-pattern boundary preserved; R8 rev2 git-diff +-line scoping for "no new affirmative use" half)**

```bash
# §4.6.3a — existing rejection-context prose preserved (whole-file presence):
awk '/^\*\*1\.5/,/^\*\*2\./' substrate/operating-disciplines.md \
  | grep -ciE 'watcher cron|watchdog cron|separate watcher|Option 2'
# Expected: ≥1 (existing Option-2-rejection prose preserved in §11 step 1.5)

# §4.6.3b — R8 rev2: scope to git-diff +-lines (NEW arc-41 content only) to
# verify no new affirmative use of these patterns surfaces in the surveillance
# line addition. Mirrors the §4.5.4 + §4.12.2 git-diff +-line scoping pattern
# this arc ships. Per VERA §5.11 self-application: whole-file grep above does
# NOT prove "no new affirmative use"; +-line scoping closes that half.
git diff main...arc-41/build -- substrate/operating-disciplines.md \
  | grep -E '^\+' | grep -vE '^\+\+\+' \
  | grep -ciE 'watcher cron|watchdog cron|separate watcher|Option 2' \
  | xargs -I{} test {} -le 0 && echo "PASS: no new affirmative use in arc-41 +-lines" || \
  { echo "FAIL: new affirmative use surfaced — A14 hard-lock violation" ; \
    git diff main...arc-41/build -- substrate/operating-disciplines.md \
      | grep -E '^\+' | grep -vE '^\+\+\+' \
      | grep -iE 'watcher cron|watchdog cron|separate watcher|Option 2' ; }
# Expected: "PASS: no new affirmative use in arc-41 +-lines" (the surveillance
# line at §3.C4.2 must not introduce affirmative-use prose; existing rejection
# citations in unrelated context lines stay invisible because they're not in
# the +-line scope. If ADA's surveillance prose accidentally cites one of
# these patterns AFFIRMATIVELY rather than as the existing anti-pattern
# rejection, the probe fires and ARGUS surfaces A14 hard-lock violation.)
```

### §4.7 — A5 Item 3: organic-adoption observation comment on stoa--myd

**§4.7.1 — comment posted on stoa--myd carrying Arc 41 organic-adoption observation**

```bash
bw show stoa--myd 2>&1 | grep -cE 'Arc 41 organic-adoption N-evidence|pqn Item 3'
# Expected: ≥1 (the observation comment landed on myd carrying Arc 41 organic-
# adoption N-evidence anchor or pqn-Item-3 anchor)
# Note (R6 rev2): dropped dead first alternative `\[from: daedalus-the-stoa\].*Arc 41`
# — the `[from:]` author-tag and "Arc 41" sit on different lines in bw-comment
# output (tag on the first comment line, content body following); `.*` does
# not match across newlines without `grep -Pzo` multi-line mode. The two
# remaining alternatives are body-content anchors that DO appear on the same
# line as themselves.
```

**§4.7.2 — myd ticket still OPEN (accretion store, not closed by this observation)**

```bash
bw show stoa--myd 2>&1 | head -1 | grep -c '○ stoa--myd'
# Expected: 1 (open-circle glyph in title line confirms ticket is open; comment is an accretion entry, not a closure)
```

### §4.8 — §5.11 paste archival (A16 wording-clarification)

**§4.8.1 — 2 activation pastes at substrate/arcs/arc-41/pastes/**

```bash
ls substrate/arcs/arc-41/pastes/HUMAN_paste-pliny-arc-41-instruction.md \
   substrate/arcs/arc-41/pastes/HUMAN_paste-polybius-arc-41-instruction.md 2>&1 \
  | grep -cE 'HUMAN_paste-(pliny|polybius)-arc-41-instruction\.md$'
# Expected: 2 (both archived to the canonical path)
```

**§4.8.2 — workspace root absent of arc-41 paste files**

```bash
ls HUMAN_paste-pliny-arc-41-instruction.md HUMAN_paste-polybius-arc-41-instruction.md 2>/dev/null
# Expected: empty stdout (workspace root carries no arc-41 pastes post-archival)
```

**§4.8.3 — directive itself stays at flat path (A16 wording-clarification)**

```bash
ls substrate/arcs/arc-41-build-directive.md substrate/arcs/arc-41/pastes/arc-41-build-directive.md 2>&1 \
  | grep -cE 'arc-41-build-directive\.md$'
# Expected: 1 (the directive is at substrate/arcs/ flat; NOT inside pastes/)
```

### §4.9 — §5.10 cleanup post-arc

**§4.9.1 — arc-41/build worktree removed**

```bash
git worktree list | grep -c 'arc-41-build'
# Expected: 0 (worktree removed post-merge; verified at PLINY signoff time per §5.10)
```

**§4.9.2 — arc-41/build branch deleted local + remote**

```bash
git branch | grep -c 'arc-41/build'
# Expected: 0 (local branch deleted)

git ls-remote --heads origin arc-41/build | wc -l
# Expected: 0 (remote branch deleted)
```

### §4.10 — A12 source-ticket closures (4 tickets)

**§4.10.1 — n2e + 58b + 3ml + pqn all CLOSED**

```bash
for t in stoa--n2e stoa--58b stoa--3ml stoa--pqn; do
  bw show "$t" 2>&1 | head -1 | grep -cE '^# ✓ '"$t"
done
# Expected: each iteration prints 1 (the ✓ glyph indicates closed status; per Arc 40 ZENO precedent)
```

**§4.10.2 — `[for: user-tier-polybius]` tag on stoa--utn carried through**

```bash
bw show stoa--utn 2>&1 | grep -cE '\[for: user-tier-polybius\]'
# Expected: ≥1 (dispatch ticket carries the user-tier-POLYBIUS QA-pass tag per A12)
```

### §4.11 — A15 CATO MANDATORY

**§4.11.1 — CATO verdict present in the gauntlet history**

```bash
bw show stoa--utn 2>&1 | grep -cE '\[from: cato-the-stoa\]'
# Expected: ≥1 (CATO posted at least one verdict comment per A15 CATO MANDATORY)
```

### §4.12 — Author/voice/credential-discipline universal gates

**§4.12.1 — Author preserved as PRINCIPAL on every arc-41/build commit**

```bash
git log arc-41/build --pretty='%an <%ae>' main..arc-41/build \
  | grep -cvE '^(denson|Denson|Denson Smith) <(densonsmith2@gmail\.com|denson@users\.noreply\.github\.com)>$'
# Expected: 0 (every commit's Author is PRINCIPAL per CLAUDE.md absolute rule; if any non-PRINCIPAL Author surfaces, A6/§28 was violated by Author-override rather than trailer-add)
```

**§4.12.2 — voice grep clean on arc-41 NEW content (git-diff +-line scoped)**

```bash
git diff main...arc-41/build -- substrate/ agents/design/arc-41/ \
  | grep -E '^\+' | grep -vE '^\+\+\+' \
  | grep -cE '\b[Cc]olonel\b|\bthe user\b'
# Expected: 0 (no voice violations in NEW content; +-line scoping per the §4.5.4 discipline this arc ships)
```

**§4.12.3 — credential-discipline non-applicability (§2.8 gate)**

```bash
git diff main...arc-41/build -- substrate/ agents/design/arc-41/ \
  | grep -E '^\+' | grep -vE '^\+\+\+' \
  | grep -cE 'op (read|run)|gcloud |gh auth |aws |kubectl |vercel |railway |fly '
# Expected: 0 (no credentialed-CLI invocation in arc-41 edits; the §20 cite in §3.C2 is a REFERENCE to the discipline, not an invocation)
```

---

## 5. Deliverables — file-by-file edit specs

ADA may refine voice/phrasing inside the structural constraint each spec sets.

### 5.1 — substrate/MAJOR_POLYBIUS.md (C1 n2e)

**§5.1.a — §13.1 "Universal escalation triggers" bullet add + cite-comment** (lines 826-833 currently; ADA re-verifies at build).

Replace the existing bullet list + closing line per §3.C1's recommended edit shape. Two additions: the fifth bullet (refusal-as-signal) + the cite-comment paragraph immediately after the list. No other §13.1 prose changes; no §13.2 boundary disturbed.

### 5.2 — substrate/MAJOR_PLINY.md (C2 58b)

**§5.2.a — new §5.2.1 subsection** inserted at the close of §5.2 (after the existing empirical anchor at line 136), before §5.3 header at line 138.

Subsection text per §3.C2's recommended edit shape: opening sentence ("When the dispatch brief involves credentialed operations..."), the credentialed-services enumeration, the cite-comment quote-block, the structural-path imperative, and the closing cross-ref paragraph. ADA voice latitude inside the structural shape.

### 5.3 — substrate/operating-disciplines.md (C3 3ml + C4 Item 2)

**§5.3.a — Thesis line 13 sentence-level edit** per §3.C3's recommended edit. One sentence; two changes (range update + parenthetical drop). No other Thesis paragraph (lines 11-33) prose touched.

**§5.3.b — §11 step 1.5 surveillance line addition** per §3.C4.2's recommended insertion at the close of the existing `durable: true` discipline paragraph at op-disc:~322 (ADA grep-locates the exact insertion point per the §4.6.2 probe contract — the existing #40228 citation is the anchor, surveillance line goes immediately after).

### 5.4 — agents/design/arc-36/design.md (C4 Item 1)

**§5.4.a-e — 5 probe-regex tightening edits** per §3.C4.1's enumerated sites:

- (a) §4.1.2 line 186-187: drop `cross-tier upward`; drop `-i` flag; restructure pattern per recommended shape.
- (b) §4.2.2 line 306: add `-i` flag (or change to `grep -ciE`).
- (c) §4.1.6 line 238 (second awk-grep pipeline): replace backslash-escaped-backtick regex with bare-slot-name pattern per §3.C4.1.c (R2 spike resolution — VERA's "§4.1.6b" label was a sub-issue annotation within §4.1.6, not a separate heading).
- (d) §4.5.3 line 560: add rejection-context exclusion clause to the grep pipeline.
- (e) §4.6.1 line 576 / §4.8 line 605: rewrite to git-diff +-line scoping variant.

ADA preserves the surrounding probe-block prose intact; only the regex/grep command + its `# Expected:` line change. The "Expected" counts may need updating if the tightened pattern materially changes match-count semantics; ADA judges.

### 5.5 — bw comment on stoa--myd (C4 Item 3)

**§5.5.a — observation comment** per §3.C4.3's recommended text. ADA posts via `bw comment stoa--myd "<text>"` (positional per `operating-disciplines.md` §12 / `MAJOR_PLINY.md` §6.1 — no `-m` flag). The comment carries the `[from: daedalus-the-stoa]` author tag at its head per the §7.1 fifth-beat canon.

Note: this is a bw operation, not a file edit. It does not produce a git commit on arc-41/build; the §4.7 probes verify the post-state via `bw show stoa--myd`. Per `MAJOR_POLYBIUS.md` §18.1, bw operations on the orphan beadwork branch are user-tier direct-commit lane; ADA executing a `bw comment` from inside the arc-41/build worktree commits to the bw beadwork branch (separate from arc-41/build) — that beadwork commit does NOT need a §28 trailer (per §28.2: bw operations are not CAPTAIN authorial commits). The arc-41/build branch carries the file-edit commits (§5.1-§5.4) only.

---

## 6. Self-assessed weak points

Per `CAPTAIN_DAEDALUS.md` §6.2: name the brittle assumptions ARGUS should look hardest at; defend each shape anyway.

### 6.1 — 3ml verification mechanics: what "current section count" actually means

**The brittle assumption:** the Thesis line claim `§1-§N` refers to numbered top-level sections only (`^## N. Title` shape) — not subsections, not unnumbered framing headings (Thesis itself, Agent-regime inverses, Empirical lineage).

**Why brittle:** the substrate file mixes numbered and unnumbered top-level headings; a future reader (or a future arc author) could reasonably count differently (e.g., "33 total ## headings" or "28 if you exclude appendix material"). The §4.4.3 probe pins to `^## [0-9]+\.` shape which encodes this interpretation, but the interpretation is an interpretation. If Arc 42 validate-spec (mechanical-check) decides the count rule should include unnumbered headings, this design's `§1-§31` ships drifted at validate-spec arc.

**Why this shape anyway:** the existing Thesis prose pre-edit already uses the `§1-§N` convention to mean numbered top-level; the `plus the autonomous-mode setup checklist` parenthetical originally accommodated a section that was OUTSIDE the §1-§N enumeration. Preserving the convention (numbered-only) is faithful to the pre-existing reading; expanding it to unnumbered headings would itself be a structural change requiring a separate canon decision. The §4.4.3 probe + ADA re-verification at build time give an out: if the count shifts before ship, the live count gets written.

### 6.2 — A5 Item 1 ε vs ζ pick defensibility under direct-to-main framing

**The brittle assumption:** the 5 VERA probe-regex tightening items belong in this arc's gauntlet (lane ε in-arc-build) rather than user-tier POLYBIUS direct-to-main housekeeping (lane ζ, the same lane mn3 takes per its ticket-body lean).

**Why brittle:** both pqn Item 1 and mn3 are design.md probe-spec fixes; mn3's ticket body explicitly PLINY-leans α direct-to-main per `MAJOR_POLYBIUS.md` §18.1 (design.md is past its review window; cleanest as separate housekeeping commit). Applying the same reasoning to pqn Item 1, ζ would have been the consistent pick — and pqn Item 1's "past the review window" property is identical to mn3's. The user-tier weak lean for ε ("craft scrutiny") is defensible but not load-bearing; ARGUS could surface that the consistency-with-mn3 reasoning outweighs the craft-scrutiny lean.

**Why this shape anyway:** the directive's A5 Item 1 framing explicitly offers DAEDALUS the choice and weakly leans ε. Honoring the lean keeps the gauntlet's redundant-checker property covering the 5 edits (ARGUS catches design-shape drift; CATO meta-verifies VERA on the changed probes). ζ direct-to-main bypasses both. The cost is one extra gauntlet round on small surface; the benefit is bundle-cohesion with the other Arc 36 follow-ups (Items 2 + 3 are intrinsically substrate-canon or bw-operations and have no ζ lane). If ARGUS surfaces consistency-with-mn3 as load-bearing, the pick can flip to ζ at rev1 — but the design's recommendation is ε.

### 6.3 — Cross-ref reciprocation incompleteness risk

**The brittle assumption:** the n2e + 58b cross-refs are sufficient at one direction (POLYBIUS → §20.3; PLINY → §20) without back-references from §20.3 + §20.

**Why brittle:** the cite-comment discipline (A10 LOCKED, Arc 38 A17, every cross-ref resolves at every read-site) is bidirectional in the formal canon. A reader landing in op-disc §20.3 has the §20 → MAJOR_POLYBIUS.md §13.1 path implicit (via §20's universal-seat enumeration at line 1238) but not explicit. Same for op-disc §20 lacking an explicit back-ref to MAJOR_PLINY.md §5.2.1. If ARGUS audits cite-resolution strictly per A10, both back-refs may be load-bearing additions.

**Why this shape anyway:** §3.C1 + §3.C2 both name the back-reference as optional contingent on ARGUS judgment; the design is buildable with one-directional cite-comments AND extensible to two-directional at rev1 if ARGUS surfaces the need. The cost of adding two back-ref cite-comments at op-disc §20.3 and §20 is one ADA edit; the cost of writing two-directional from the start is one extra paragraph each in C1 + C2 designs. DAEDALUS-discretion call: ship the design with one-directional; let ARGUS surface if cite-completeness escalates to load-bearing.

### 6.4 — rev2 probe-grounding meta-discipline (ARGUS-surfaced; folded)

**The brittle assumption:** rev1's §4.5 probe-block awk/grep patterns were authored without round-tripping each pattern against the live `agents/design/arc-36/design.md` file at design time. ARGUS-rev1 surfaced three probe-grounding defects (R1 em-dash false-PASS, R2 nonexistent §4.1.6b heading, R3 malformed inner regex) that all share root cause: probe patterns hand-typed against expected heading shapes rather than verified by execution against the live target.

**Why brittle:** the discipline parallels the Arc 40 CAPTAIN_VERA §5.11 probe-spec regex anchoring canon ("every regex anchored; every install.sh-flag citation grounded; every bw-output grep grounded") — but the canon applies to VERA's probes on substrate. The mirror discipline for DAEDALUS-authored verification probes on design.md (probes that probe OTHER design.md files) is not yet codified. The result was three false-PASS / false-FAIL surfaces that ARGUS caught on cold-read but which would have wasted VERA's mechanical re-execution cycle.

**Why this shape anyway (rev2 fold):** all three are now corrected with the awk patterns verified against the live arc-36/design.md at rev2 design time (R1 `'/^\*\*§4\.2\.2 /'` brackets 17 lines; R2 retargeted to §4.1.6 real heading with §4.1.7 terminator; R3 re-cast as two literal-anchored `grep -cF` structural property checks). The R4 coherence-check fold for §4.4 (eliminating hard-coded `Expected: 31` brittleness) + the R8 git-diff +-line scoping fold for §4.6.3 (mirroring §4.5.4 / §4.12.2) extend the meta-discipline preemptively. The remaining surface for ARGUS-rev2 to verify: did any §4.x probe I authored fresh in rev1 still carry an unverified pattern? Spot-checks against §4.2, §4.3, §4.6, §4.7, §4.9 all use shapes that I have either grounded at design time or that ADA grounds at build time per the §2.6 ADA brief preamble. No further probe-grounding defects expected; if ARGUS-rev2 surfaces a fourth, the meta-discipline should be promoted to an Arc 42 follow-up ticket (probe-grounding canon for DAEDALUS-authored verification probes, mirroring CAPTAIN_VERA §5.11).

---

## 7. Out of scope (per A14 hard-locks)

- No restructuring MAJOR_POLYBIUS.md §13.1 escalation-triggers section beyond the n2e bullet add + cite-comment.
- No restructuring MAJOR_PLINY.md §5 or §6 beyond the new §5.2.1 subsection insertion.
- No editing op-disc Thesis beyond the line-13 sentence-level edit.
- No widening pqn Item 3 organic-adoption observation into A2.5 scope expansion (explicit pqn-ticket + A14 hard-lock).
- No mn3 work (PLINY-lean is α direct-to-main per the mn3 ticket-body; user-tier handles post-Arc-41).
- No introducing new substrate skills or canon sections.
- No edits to other arcs' shipped design.md files beyond the 5 enumerated §3.C4.1 tightening sites in `agents/design/arc-36/design.md`.
- No recovery-discipline canon change at op-disc §11 step 1.5 beyond the observation-only surveillance line.

---

## 8. Provenance + N-framing

This is the third arc in the Pass-5/6/7 trio (Arcs 39+40+41) targeting `SPECIFICATION.md` §13.6-§13.8 — the make-the-team-meet-the-spec sequence. Arc 41 is the smallest of the three and the last canon-edit arc before Pass 8 reconciliation + Pass 9 validate-spec (Arc 42).

Per `MAJOR_POLYBIUS.md` §15 honest-scope: this design does NOT promote any new substrate discipline to canon. All four candidates are sentence-level / paragraph-level cite-and-cross-ref edits + one observation-comment routing. The arc's evidence value is in (a) self-application of the canon shipped in Arc 40 (squash-merge `--body` discipline at Phase 4), (b) accretion against `stoa--myd` (organic `[from:]` adoption N-evidence), (c) sequence-end pattern observation per directive self-application item #2 (does tight scope produce clean PASS-first?).

Per `operating-disciplines.md` §6.7.1 canon-promotion gate: nothing in Arc 41 reaches the multi-observation-across-defect-classes threshold. The arc executes existing canon under existing discipline; the substrate edits are localized refinements (one stale section-count fix + two cross-ref adds + three Arc 36 follow-ups) rather than novel structural additions.

---

## 9. ARGUS focus suggestions (residual questions for plan-critic)

These are explicit places ARGUS should look hardest, beyond the §6 self-assessed weak points:

1. **§3.C3 parenthetical drop:** the design recommends removing "plus the autonomous-mode setup checklist" along with the range update. Is this a load-bearing semantic change beyond a stale-reference fix, or is it correct cleanup-as-part-of-the-edit? If ARGUS reads this as a separate scope concern, the design can split into two edits (range update only; parenthetical drop as a separate ticket).

2. **§3.C2 §5.2.1 vs §5.x other:** DAEDALUS picked §5.2 as the dispatch-brief-authoring locus over §6 (Communication). ARGUS should sanity-check: is there a structurally better insertion point I missed (e.g., a new §5.13 alongside §5.12 seat-identity dispatch-brief naming)? §5.2 was picked because §5.2's prose IS the brief preamble — but §5.13-as-credential-discipline-cite would also be defensible.

3. **§3.C4.2 surveillance-line placement specificity:** the design recommends inserting at the close of the existing `durable: true` discipline paragraph. ARGUS to confirm this placement keeps the §11 step 1.5 structural flow readable — vs. e.g., inserting at the §11 step 1.5 tail as a separate "Surveillance" sub-paragraph.

4. **§4.5.5 §4.1.6b probe locator:** the design delegates the exact §4.1.6b probe-site location to ADA-discretion (the ticket cites the item without a line; ADA grep-locates). ARGUS should verify this is acceptable scope-delegation versus needing a design-time precise line. The 5-item-bounded property holds either way; the question is whether ADA-discretion on the site IS the contract or whether DAEDALUS owed a precise line at design time.

---

## 10. Cross-references

- Arc 41 directive: `substrate/arcs/arc-41-build-directive.md` (A1-A16 LOCKED).
- Source tickets: `stoa--n2e` (P3), `stoa--58b` (P3), `stoa--3ml` (P4), `stoa--pqn` (P4).
- Arc 36 design (pqn Item 1 target): `agents/design/arc-36/design.md`.
- Arc 36 ZENO + CATO verdicts (5-item probe-regex enumeration): `bw show stoa--jru` 2026-05-18T00:04:44Z + 00:02:52Z.
- myd accretion thread (pqn Item 3 target): `bw show stoa--myd` (multi-checker convergence accretion P4).
- Arc 40 ship commit (recent precedent): `dbb5b81`.
- §28 trailer canon: `operating-disciplines.md` §28 lines 1699-1786.
- §5.10 squash-merge canon (Arc 40 ship): `MAJOR_PLINY.md` §5.10 line 434.
- §5.11 paste archival (A16 wording-clarification reference): `MAJOR_PLINY.md` §5.11 lines 465-507.
- §20 credential discipline (n2e + 58b target): `operating-disciplines.md` §20 lines 1236-1305; §20.3 lines 1283-1291.
- §11 step 1.5 (pqn Item 2 target): `operating-disciplines.md` §11 step 1.5 lines 490-490+ surveillance insertion locus.
- §13.1 Universal escalation triggers (n2e target): `MAJOR_POLYBIUS.md` §13.1 lines 826-833.
- §5.2 ADA brief preamble (58b target): `MAJOR_PLINY.md` §5.2 lines 116-136.
- CAPTAIN_VERA.md §5.11 probe-spec regex anchoring discipline (Arc 40 shipped; pqn Item 1 N-evidence under this canon).
- CAPTAIN_DAEDALUS.md §6.1 restatement-gate + §6.2 self-assessed weak points + §6.5 cite-checking + §6.6 credential-discipline non-applicability gate.
