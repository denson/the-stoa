# Arc 2 (Arc 45) — MAJOR_POLYBIUS.md debloat cut — design rev2

**Ticket:** stoa--xyb.6 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (c0b5610) — composition-layer mechanism (`substrate/modules/` glob deploy; `modules/README.md` 3 channels + 3 relocation classes; op-disc §33 thin rule).
**Supersedes:** design-rev1.md (committed ea56fd7). ARGUS audited rev1 PASS-WITH-RISKS (`agents/verdicts/stoa--xyb.6/ARGUS-2026-05-23T07-09-08Z.md`) — the CUT is lossless and buildable; rev2 is TARGETED refinements, not a re-cut. The next ARGUS/ADA read THIS file alone.
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject). ARGUS's primary audit target is LOST CANON.

---

## Changes from rev1 (addressing ARGUS r1–r4 + residuals)

This rev2 is a standalone full design. The deltas against rev1, each tied to an ARGUS finding:

- **r1 [BLOCKING-grade, load-bearing] — install.sh subproject-recompose stub-marker format + algorithm SPECIFIED.** rev1 §6.2 said recompose "`cat`-concatenates the 5 module bodies into the role file at their stub markers" but never gave a marker FORMAT — leaving the LOST-CANON-at-subproject vector to ADA discretion. rev2 §2.7 + §6.5 specify a MACHINE-PARSEABLE paired-sentinel marker (`<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->`), the exact recompose ALGORITHM (awk state-machine, subproject-deploy-only, post-`sed`), FAIL-LOUD semantics (marker-without-module OR module-without-marker → `err` non-zero exit; silent skip is forbidden), and a numbered VERA recompose-completeness probe (P10).
- **r2 [BLOCKING-grade, load-bearing] — per-line SPLIT enumeration.** rev1 §3.3 classed the 4 SPLIT subsections (§16.7/§17.6/§18.6/§19.7) "live refs kept / provenance → Anchor" but did not say WHICH lines are which. rev2 §3.8 enumerates EACH cross-ref line per subsection, classified LIVE (operational pointer → stays inline in slim core) vs PROVENANCE (empirical-anchor/historical → relocates to Anchor), so ADA does not guess. A new probe (P11) grep-diffs the kept LIVE lines.
- **r3 [SHOULD-FIX] — relocation-ledger arithmetic fixed.** rev1 §3.7 claimed "5 SPLIT / 16 PROVENANCE"; actual is **4 SPLIT / 15 PROVENANCE** (9 C-1 + 2 C-2 + 4 SPLIT). rev2 §3.7 re-counts and is self-consistent; all per-class counts re-verified against the live source.
- **r4 [SHOULD-FIX] — lean-0hl deviation acknowledged explicitly.** rev1's §4.5 F1 fold is written LEAN (2 sentences), which deviates from stoa--0hl's "mirror the user-tier copy verbatim" instruction. rev2 §2.4 + §3.2 state this is INTENTIONAL per the debloat thesis + the peer's lean-from-start direction, so ADA lands it knowingly and a future reader sees the divergence is by-design, not an error.
- **residual-2 [ADJUDICATED by ARGUS] — C-2 archive home = DEDICATED CHILD TICKETS, not bw comments.** rev1 §3.4 archived the 2 C-2 provenance blocks to `bw comment stoa--xyb.6`. ARGUS adjudicated: these are the ONLY surviving copy once cut, so titled-id discoverability matters — use dedicated child tickets `stoa--xyb.6.1` / `stoa--xyb.6.2`. rev2 §3.4 specifies `bw create … --parent stoa--xyb.6 -d "<prose>"`, the per-deletion content-check gate against the child-ticket body, and updates P7's archive assertion.

CONCUR holds (ARGUS agreed with rev1, NO change): §13 KEEP-inline (escalation triggers are always-on core); section-number PRESERVE-via-stubs (zero cross-ref churn); recompose-not-fork (single source of truth). These are carried verbatim from rev1 with their rationale intact (§2.7, §3.1 note, §6.4).

**Process hazard carried for ADA (rev1 DAEDALUS hit it):** the Write tool can resolve relative paths against the MAIN repo root, not the worktree. ADA MUST use ABSOLUTE worktree paths (`C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-45-build/...`) for EVERY write, and verify each write landed in the worktree (e.g. `git -C <worktree> status` shows the file as modified/added in the worktree, not in main). See §5 Step 0.

---

## §1 — Problem restatement (pre-work gate)

`substrate/MAJOR_POLYBIUS.md` is 1299 lines and now a load-bearing problem: it cost ~52k tokens to read against a 25k harness cap (user-tier POLYBIUS had to paginate its own role file, per stoa--0hl 2026-05-23T01:26:38Z). The diagnosis is empirical-anchor + provenance accretion: every discipline carries a ticket cite + worked example + multi-paragraph provenance, so the *actionable* canon is roughly a third of the lines and the rest is the why/empirical record.

This arc applies the Arc-1 debloat method (the 3 relocation classes — CONDITIONAL → disk module, PROVENANCE → bw cite, DUPLICATE → pointer) to MAJOR_POLYBIUS.md section by section. The composition + enforcement layers shipped in Arc 44 are the safety net that makes the cut safe: relocated content has a lossless home and a slim-core cite-back so nothing is lost, only moved.

The cut must hold LOSSLESS-ON-CANON at **all tiers including subproject** — a slimmed subproject `MAJOR_POLYBIUS_<slug>.md` that points at modules absent from the subproject's `.claude/modules/` would break losslessness at that tier. The subproject module-access strategy is a design-phase requirement (probed live in §6; the recompose mechanism that resolves it is fully specified in §6.5 per ARGUS r1).

This arc ALSO folds stoa--0hl (the §5.6 say-trigger team-deploy procedure + §4.5 two-mechanism reconciliation) into the cut — written LEAN from the start, not mirrored verbose. **This is a deliberate, named deviation from stoa--0hl's "mirror the user-tier copy verbatim" instruction (§2.4, ARGUS r4):** the debloat thesis + the peer's lean-from-start direction override the verbatim-mirror instruction; the LEAN form is lossless-on-canon (rule + empirical cite + say-vs-paste contrast all preserved) and only compresses the verbose worked-procedure prose. The 0hl fold is kept a SEPARABLE slice (own ledger rows, own build commit) so ARGUS can audit LOSSLESS-ON-CANON on the cut independently of the 0hl addition.

### Imported assumptions (named per §6.1)

1. **op-disc §12 is the canonical bw-cookbook home** for the DUPLICATE class. Confirmed live: §12 self-declares "Role files reference this section; do not duplicate." (op-disc:729). The §7.3 dupe deletes to a pointer at §12. (ARGUS DISCHARGED.)
2. **CONDITIONAL content relocates to the 5 NAMED Arc-2 modules** (modules/README.md §6). This arc CREATES + POPULATES those 5 files (Arc 1 only named them).
3. **The cut is to SOURCE** (`substrate/MAJOR_POLYBIUS.md`). The deployed user-tier copy (`~/.claude/MAJOR_POLYBIUS.md`, 1300 lines, AHEAD by the §5.6 fold) is the verbatim reference for the 0hl text content but is NOT the cut target. Substrate-self-apply re-sync is user-tier POLYBIUS housekeeping, out of this arc's scope.
4. **Subagents inherit parent-session cwd; no per-subagent cwd override exists** (web-confirmed, §6; ARGUS DISCHARGED against the real ariadne deploy + current web #56686/#29423/#29610). This is the load-bearing fact for the subproject strategy.
5. **The 0hl fold writes §5.6 + §4.5 LEAN.** The verbose user-tier reference text is the *source of truth for content*, not for length. The lean form keeps the rule + the 1-line empirical cite + the say-vs-paste contrast; the verbose worked-procedure prose is what gets compressed. (See §2.4 r4 acknowledgement.)
6. **`bw create --parent <id> -d "<prose>"` is the C-2 archive primitive** (residual-2). Confirmed live this design phase: `bw create` supports `--parent ID` and `-d/--description TEXT`; the child auto-derives an ID under the parent (the `stoa--xyb.6.N` form). This replaces rev1's `bw comment` archive home per ARGUS's residual-2 adjudication.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, MAJOR_POLYBIUS.md is the **slim operational core**: crisp rule per discipline + a one-line cite-back (routing-map row for CONDITIONAL, `Anchor:` for PROVENANCE, pointer for DUPLICATE) + the two always-loaded index tables (routing map + relocation index per Refinement 1). The 5 CONDITIONAL procedures move to disk modules; the provenance/empirical multi-paragraph blocks move to bw cites; the bw-cookbook dupe deletes to a pointer.

### 2.2 The two always-loaded index tables (Refinement 1 — index stays in core, NEVER a module)

Per modules/README.md §4, POLYBIUS's slim core carries both tables inline, always-loaded. They are added as a new **§3.5 "Composition layer — routing map + relocation index"** placed immediately after §3 (so the always-loaded indexes sit at the top of the operational core, before the disciplines that reference them). Tables are populated in §3 of THIS design. The column shapes are the regular forms from modules/README.md §4.1/§4.2 (routing: task-type/module/channel; index: content/home/class) so a future enforcement-layer hook is parseable.

### 2.3 The 5 CONDITIONAL module files (CREATED + POPULATED this arc)

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/onboarding.md` | §5 Onboarding flow (159–376) **plus** the NEW §5.6 0hl fold (see §2.4) | The 9-step onboarding procedure (§5 intro + code block), §5.1 string-substitution + slots, §5.1.1 / §5.1.1.1 positive-references discipline, §5.1.2 pre-branch-hygiene preamble, §5.1.3 cron-hygiene preamble, §5.2 install.sh-template, §5.3 consent moments, §5.4 external-directive-review, §5.5 activation-paste-filenames cheatsheet, + NEW §5.6 say-trigger team-deploy (lean) |
| `substrate/modules/sub-project-spawning.md` | §10 Sub-project spawning (538–635) | §10 intro + §10.1 trigger recognition + §10.2 walk-through (code block) + §10.3 asymmetric bw visibility + §10.4 the hand-off |
| `substrate/modules/pair-programmer-authoring.md` | §11 Pair-programmer Major authoring (638–726) | §11 intro + §11.1 trigger recognition + §11.2 walk-through + §11.3 empirical lineage + §11.4 asymmetric bw visibility |
| `substrate/modules/pair-programming-prototyping.md` | §12 Pair-programming-for-prototyping (Mode 2) (729–803) | §12 intro + §12.1 two-mode framing + §12.2 7-step cycle + §12.3 when-to-use + §12.4 empirical claim |
| `substrate/modules/substrate-update-check.md` | §14 Substrate-update check (885–895) | §14 full body (check mechanism, check.sh/apply.sh/revert.sh, .substrate-last-check semantics) |

Each module is a self-contained reference body; the module's first line restates which POLYBIUS § it relocated and cites this design + the epic (provenance header convention, mirroring modules/README.md:14-16). **No module carries an author-like field** (P9 guards this).

> **r4 note (line-range correction from rev1):** rev1's onboarding row said "§5 (159–376) **minus** §5.6"; that phrasing was a harmless shorthand (ARGUS DISCHARGED it — §5.6 is a NEW fold, not present in source to exclude). rev2 states it correctly: the module relocates §5's existing body (159–376) AND ADDS a new lean §5.6 (the 0hl fold). There is nothing to "exclude" from the source.

### 2.4 The 0hl fold (SEPARABLE slice — INTENTIONAL lean deviation, ARGUS r4)

**Explicit deviation statement (ARGUS r4, load-bearing for ADA):** stoa--0hl's Edit 1 instruction reads "mirror the user-tier copy verbatim" (the ~7-sentence §4.5 paragraph already deployed at `~/.claude/MAJOR_POLYBIUS.md:106`). This design DELIBERATELY writes the fold LEAN instead, deviating from that instruction. The deviation is BY-DESIGN, not an error: the whole point of this arc is the debloat thesis (slim operational core), the peer's dispatch direction is "written LEAN from the start," and the lean form is lossless-on-canon (it preserves the rule + the say-vs-paste contrast + the 2026-05-21 railway empirical cite — only the verbose worked-procedure prose compresses). ADA lands the fold LEAN knowingly; the build commit message names the deviation so a future auditor reconciling 0hl against the built §4.5 is not confused by the length mismatch.

stoa--0hl folds in TWO edits, both written LEAN:

- **0hl Edit 1 — §4.5 two-mechanism reconciliation.** §4.5 stays inline in the slim core (it is a KEEP-TIGHTEN section). Append a LEAN 2-sentence paragraph: the on-disk-`.md` one-liner is the *paste-trigger* mechanism (fresh installs); for *already-deployed say-trigger* workspaces the durable artifact is a **bw ticket** and activation is the bare word `polybius`/`pliny` (full procedure → onboarding module §5.6). Invariant in both: durable instruction, short relay. 1-line empirical cite (2026-05-21 railway, `Anchor: stoa--0hl`).
- **0hl Edit 2 — §5.6 say-trigger team-deploy procedure.** §5.6 is CONDITIONAL content (an onboarding-class procedure), so it relocates INTO `onboarding.md` as a `## §5.6` section, written LEAN: the 4-step procedure (store instruction in bw ticket; optionally commit supporting `.md` to beadwork branch via worktree; human activates bare word; team self-discovers via §9 sweep) + the say-vs-paste contrast + 1-line empirical cite. The slim core keeps the §5 routing-map row only (no §5.6 inline prose in core).

**Why separable:** the 0hl fold is the ONLY net-ADD in an otherwise net-SUBTRACT arc. ARGUS audits LOSSLESS-ON-CANON on the cut (everything that existed at 1299 lines must have a home) independently of whether the 0hl ADD is well-formed. Ledger rows F1/F2 (§3.2) tag the fold distinctly; build Step 6 (§5) lands it as a distinct commit.

### 2.5 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

§1 (Who you serve), §2 (What you do), §3 (What you don't do — incl. the §3 "What you DO do" attention-map block), §6 (Compact-or-clear recovery), §8 (Voice discipline), §9 (Activation checklist), §13 (Operating engagement HITL/Autonomous — see §3.1 note + ARGUS CONCUR), §15 (retrospective discipline). These are the always-needed operational core. Tighten verbose prose (e.g. the §3 attention-map block at 49–59 is 3 dense paragraphs reducible to a tight rule + cross-ref); no content relocates.

### 2.6 PROVENANCE relocations (C-1 / C-2 / SPLIT disposition per §3.3 + §3.8)

The "N=1 provenance + accretion path" + "Cross-references" subsections at the tail of §4 disciplines and §16/§17/§18/§19 relocate to bw cites. The slim core keeps the RULE + a one-line `Anchor: <bw-id>` cite-back. C-1 (already-in-bw) vs C-2 (not-in-bw) call is per-row in §3.3; the 4 SPLIT cross-ref subsections get per-line LIVE-vs-PROVENANCE enumeration in §3.8 (ARGUS r2).

### 2.7 §-numbering coherence after the cut + the recompose stub marker (CONCUR + ARGUS r1)

The slim core PRESERVES section numbers, NOT renumbers (ARGUS CONCUR on residual 3). Relocated whole-sections leave a 2-line stub at their original number (heading + routing-map pointer), so §5 stays §5, §10 stays §10, §16 stays §16, and every existing cross-ref (`§5`, `§10`, `§11`, `§12`, `§14`, all the §16.x/§17.x/etc.) still resolves to a real anchor in the slim core. This trades ~10 stub lines for zero cross-ref churn across the substrate — strongly net-positive given dozens of `MAJOR_POLYBIUS.md §N` cross-refs in op-disc, MAJOR_PLINY, and the CAPTAIN envelopes. (ARGUS found NO cross-ref the preservation misses.)

**The stub carries a MACHINE-PARSEABLE recompose marker (ARGUS r1 — the load-bearing fix).** rev1's stub was pure human prose (`## 5. Onboarding flow` + 3 pointer lines). The recompose mechanism (§6.5) needs a marker that does NOT drift when a future tighten edit rewords the stub prose — a prose-heading match is exactly where a module body could silently fail to inline at subproject tier (the LOST-CANON-at-the-hardest-tier failure). The fix: each CONDITIONAL stub embeds a **paired HTML-comment sentinel** naming the module, with NOTHING between the open and close sentinel in the slim-core source:

**Exact stub shape (CONDITIONAL relocations) — the literal ADA writes:**
```
## 5. Onboarding flow
Relocated to `.claude/modules/onboarding.md` (CONDITIONAL — loaded at dispatch).
Routing-map + relocation-index rows in §3.5. Recover the full procedure via `Read .claude/modules/onboarding.md`.
<!-- MODULE-INLINE:onboarding -->
<!-- /MODULE-INLINE:onboarding -->
```

The paired sentinel `<!-- MODULE-INLINE:<module-name> -->` … `<!-- /MODULE-INLINE:<module-name> -->` is the recompose hook. `<module-name>` is the module's basename WITHOUT the `.md` extension (e.g. `onboarding`, `sub-project-spawning`, `pair-programmer-authoring`, `pair-programming-prototyping`, `substrate-update-check`) — install.sh appends `.md` and the `substrate/modules/` prefix to locate the body.

**Why paired HTML comments (justification, ARGUS r1):**
- **Machine-parseable, not prose.** An awk/grep state machine keys on the literal `<!-- MODULE-INLINE:` / `<!-- /MODULE-INLINE:` prefixes, which carry NO human-readable English a future tighten edit would touch. The 3 prose pointer lines above the marker can be reworded freely without affecting recompose — the marker is decoupled from the prose.
- **Invisible at user/project tier.** HTML comments render as nothing in a markdown reader. At user/project tier (where the slim core deploys AS-IS, no recompose) the marker is inert — a reader sees the stub prose + routing-map row, never the sentinel. This is why a paired sentinel beats a single self-closing sentinel that install.sh "expands": the empty paired form is a legal no-op at the tiers that do NOT recompose, AND gives the recompose algorithm an explicit close-anchor (so re-running recompose on an already-recomposed file is detectable — see §6.5 idempotency).
- **One module name per marker = 1:1 audit.** The `<module-name>` slot makes each marker self-identifying; the FAIL-LOUD check (§6.5) cross-references the marker set against the `substrate/modules/*.md` glob and errors on ANY mismatch in EITHER direction.

The DUPLICATE stub (§7.3 → op-disc §12) and the PROVENANCE `Anchor:` cites carry NO recompose marker — only the 5 CONDITIONAL relocations re-inline at subproject tier (DUPLICATE points at a deployed sibling file; PROVENANCE points at bw, neither of which is re-inlined into the role file).

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON. **One row per relocated chunk.** Every empirical anchor in the 1299-line source must appear as a ledger row with a lossless home, OR be a KEEP-TIGHTEN section that stays inline. Line ranges are grounded against the LIVE `substrate/MAJOR_POLYBIUS.md` (re-read this session), not the .6 section-map estimates. ARGUS independently walked all 87 source headers against rev1's ledger and found NO dropped canon; rev2 preserves that ledger and adds the r2 per-line SPLIT detail (§3.8) + the r3 arithmetic fix (§3.7).

### 3.1 CONDITIONAL relocations (→ disk module; slim-core residue = routing-map row + stub w/ recompose marker)

| Source (§ + live lines) | Class | New home | Slim-core residue (the 1-line rule/cite that stays) |
|---|---|---|---|
| §5 Onboarding flow + §5.1–§5.5 (159–376) | CONDITIONAL | `modules/onboarding.md` | §5 stub heading + routing-map row `onboard new project → onboarding.md → disk` + `<!-- MODULE-INLINE:onboarding -->` marker |
| §10 Sub-project spawning + §10.1–§10.4 (538–635) | CONDITIONAL | `modules/sub-project-spawning.md` | §10 stub + routing-map row `spawn sub-project → sub-project-spawning.md → disk` + `<!-- MODULE-INLINE:sub-project-spawning -->` |
| §11 Pair-programmer Major authoring + §11.1–§11.4 (638–726) | CONDITIONAL | `modules/pair-programmer-authoring.md` | §11 stub + routing-map row `author pair-programmer → pair-programmer-authoring.md → disk` + `<!-- MODULE-INLINE:pair-programmer-authoring -->` |
| §12 Pair-programming-for-prototyping + §12.1–§12.4 (729–803) | CONDITIONAL | `modules/pair-programming-prototyping.md` | §12 stub + routing-map row `prototype (Mode 2) → pair-programming-prototyping.md → disk` + `<!-- MODULE-INLINE:pair-programming-prototyping -->` |
| §14 Substrate-update check (885–895) | CONDITIONAL | `modules/substrate-update-check.md` | §14 stub + routing-map row `substrate-drift check → substrate-update-check.md → disk` + `<!-- MODULE-INLINE:substrate-update-check -->` |

**Note on §13 (Operating engagement HITL/Autonomous, 806–881) — KEEP-TIGHTEN (ARGUS CONCUR):** the .6 section map tagged 5/10/11/12/14 → reference; §13 was NOT in that list. §13 is a KEEP-TIGHTEN section (it carries the universal escalation triggers at 826–836, which are load-bearing operational core read every autonomous engagement — relocating them off-disk would degrade losslessness-of-availability). §13 stays inline, tightened, WHOLE. ARGUS checked §13.1's triggers (826–836) and CONCURred: read every autonomous engagement, MUST stay inline; do NOT split §13.2/§13.3/§13.4 to a `mode-transitions.md` module (the mechanics are read together with the triggers at mode-declaration time, and a 4-subsection section is below the line-savings threshold that justifies a new module + routing row + recompose-stub surface).

### 3.2 The 0hl fold rows (SEPARABLE slice — net-ADD, audit independently; ARGUS r4 lean deviation)

| Source | Class | New home | Slim-core residue |
|---|---|---|---|
| **F1** — 0hl Edit 1 (§4.5 two-mechanism reconciliation) | KEEP (LEAN ADD inline — DELIBERATE deviation from 0hl "mirror verbatim", §2.4 / ARGUS r4) | §4.5 (stays inline) | LEAN 2-sentence paragraph + `Anchor: stoa--0hl` (2026-05-21 railway empirical) |
| **F2** — 0hl Edit 2 (§5.6 say-trigger team-deploy) | CONDITIONAL (LEAN ADD) | `modules/onboarding.md` §5.6 | §5 stub already covers it (no separate core residue beyond the §5 routing-map row) |

### 3.3 PROVENANCE relocations (→ bw cite; slim-core residue = rule + `Anchor:`)

| Source (§ + live lines) | bw id(s) cited | C-1 / C-2 call | Slim-core residue |
|---|---|---|---|
| §4.3.1 PRINCIPAL-intent probe empirical (89–105) | `stoa--ezj` | **C-1** (resolves live; ARGUS spot-checked) | Keep the rule + 3-step probe; `Anchor: stoa--ezj`. The 4-option-to-5th-option anchor is in a stoa--ezj COMMENT (bw show surfaces it); the 3-step probe stays inline (KEEP) anyway. Cross-ref line (105) kept as live pointer. |
| §5.1.1 empirical (244) | 2026-05-04 (in-prose, no ticket) | (relocates WITH §5) | Moves WITH §5 into onboarding.md (it's onboarding CONDITIONAL); the empirical 1-liner stays in the module. NO standalone bw cite needed — it relocates with its parent CONDITIONAL block. |
| §5.1.1.1 cross-project-leak provenance block (264 — N=2 2026-05-17 ariadne) | in-prose N=2, no single ticket | **C-2** → §3.4 (dedicated child ticket) | Moves WITH §5 into onboarding.md (CONDITIONAL). Verbose provenance paragraph (264) compresses to a 1-line empirical cite in the module pointing at the child ticket. |
| §5.1.2 cross-refs + empirical (297–302) | `stoa--3cs` | **C-1** (ARGUS spot-checked) | Moves with §5 into onboarding.md; keep `Anchor: stoa--3cs`. |
| §5.1.3 provenance block (333 — multi-instance ad-hoc, N=0 canon) | no clean ticket (lists HUMAN_paste-* filenames) | **C-2** → §3.4 (dedicated child ticket) | Moves with §5 into onboarding.md; verbose provenance (333) compresses to 1-line cite pointing at the child ticket. |
| §15 retrospective discipline empirical (914) | `stoa--nax`, `ariadne--8fd` | **C-1** | §15 is KEEP-TIGHTEN (stays inline core); compress the empirical paragraph to rule + `Anchor: stoa--nax, ariadne--8fd`. |
| §16.1 source-of-truth declarations (922–930) | `stoa--32b.3` | **C-1** (ARGUS spot-checked) | Keep the rule; `Anchor: stoa--32b.3`. The two verbatim PRINCIPAL quotes (927, 929) move to the cite (already verbatim in stoa--32b.3 body — content-check gate). |
| §16.6 N=1 provenance + accretion (1022–1032) | `stoa--32b.3`, `stoa--32b`, `stoa--p5g`, `stoa--dxw` | **C-1** | Delete verbose block; `Anchor: stoa--32b.3 — N=1 provenance + accretion. Recover via bw show.` |
| §16.7 Cross-references (1034–1050) | mixed (bw ids + in-file §refs + sibling-file §refs) | **SPLIT** → per-line in §3.8 | Live §refs + sibling-file refs kept inline (per modules/README.md §5.2 "keep the existing in-file pointer convention"); bw-id provenance → relocation-index/Anchor. Per-line enumeration: §3.8. |
| §17.1 source-of-truth declaration (1096–1102) | `stoa--ads` | **C-1** (ARGUS spot-checked) | Keep rule; `Anchor: stoa--ads`. Verbatim quote (1100) → cite (content-check). |
| §17.5 N=1 provenance + accretion (1145–1155) | `stoa--ads` | **C-1** (ARGUS spot-checked) | Delete verbose block; `Anchor: stoa--ads`. |
| §17.6 Cross-references (1157–1164) | mixed | **SPLIT** → per-line in §3.8 | Live §refs kept; provenance → Anchor. |
| §18.5 N=1 provenance + accretion (1206–1215) | `stoa--k36` | **C-1** (ARGUS spot-checked) | Delete verbose block; `Anchor: stoa--k36`. |
| §18.6 Cross-references (1217–1225) | mixed | **SPLIT** → per-line in §3.8 | Live §refs kept; provenance → Anchor. |
| §19.6 N=1 provenance + accretion (1273–1282) | `stoa--86k` | **C-1** (ARGUS spot-checked) | Delete verbose block; `Anchor: stoa--86k`. |
| §19.7 Cross-references (1284–1295) | mixed | **SPLIT** → per-line in §3.8 | Live §refs kept; provenance → Anchor. |

**The C-1 content-check gate (REQUIRED per modules/README.md §5.2, carried into the build).** Before ADA deletes ANY C-1 inline provenance prose, ADA MUST run `bw show <cited-id>` and content-check that the cited ticket actually carries the full story the inline prose holds. This is a per-deletion gate — it turns each C-1 classification into a checkable losslessness proof. The design pre-verified all C-1 ticket ids RESOLVE (stoa--32b, stoa--32b.3, stoa--ads, stoa--k36, stoa--86k, stoa--ezj, stoa--3cs all EXIST live; ARGUS spot-checked 6/9 recover the inline story via bw show); the *content-match* check for the 3 unsampled cites (nax, ariadne--8fd, the 32b/p5g/dxw cluster) is ADA's per-deletion responsibility (resolution ≠ content-completeness). VERA re-executes a sample of these `bw show` checks (P5).

### 3.4 C-2 archive-first cases — DEDICATED CHILD TICKETS (ARGUS residual-2 adjudication)

Two provenance blocks have NO clean single bw home AND are the ONLY surviving copy once cut. ARGUS adjudicated residual-2: archive each to a **DEDICATED CHILD TICKET** (`stoa--xyb.6.1`, `stoa--xyb.6.2`), NOT a bare `bw comment` on stoa--xyb.6. A titled child ticket is retrievable by a future auditor via `bw show` of a NAMED id (discoverable from the relocation-index Anchor); a comment buried in xyb.6's stream (which already carries this whole audit's heartbeats) is materially less discoverable. modules/README.md §5.2 sanctions `bw comment` for SHORT prose, but "sanctioned" is the floor, not the right call when the prose is the only copy. Cost (2 `bw create` calls) is trivial against sole-surviving-copy stakes.

**Mechanism (confirmed live: `bw create` supports `--parent` + `-d`):**

- **§5.1.1.1 cross-project-leak provenance (264).** N=2 in-prose (2026-05-17 ariadne PLINY pastes). The DISCIPLINE (positive-references-only, the worked-example TABLE) moves with §5 into onboarding.md (CONDITIONAL) and STAYS — it is operational. Only the multi-paragraph *why-N=2-and-future-accretion* prose archives. **C-2 disposition:** ADA creates the child ticket at build time:
  ```
  bw create "Arc 45 C-2 archive: §5.1.1.1 cross-project-leak provenance (N=2 2026-05-17 ariadne)" --parent stoa--xyb.6 -d "<the verbose §5.1.1.1 provenance prose, verbatim>"
  ```
  Then the onboarding module keeps a 1-line cite (`Anchor: stoa--xyb.6.1 — 2026-05-17 N=2 cross-project-leak provenance. Recover via bw show.`). ADA records the assigned child id (it should be `stoa--xyb.6.1`; if bw assigns a different id, ADA uses the ACTUAL assigned id in the cite — the cite must match the created ticket).
- **§5.1.3 cron-hygiene provenance (333).** Multi-instance ad-hoc, N=0 canon. Same disposition:
  ```
  bw create "Arc 45 C-2 archive: §5.1.3 cron-hygiene provenance (N=0 canon, HUMAN_paste filename list)" --parent stoa--xyb.6 -d "<the verbose §5.1.3 provenance prose, verbatim>"
  ```
  The cron-hygiene preamble (operational) STAYS in the module; the module keeps a 1-line cite (`Anchor: stoa--xyb.6.2 — N=0 cron-hygiene provenance. Recover via bw show.`).

**Per-deletion content-check gate STILL APPLIES (carried from rev1, against the child-ticket body).** Before deleting EITHER inline C-2 block, ADA runs `bw show <child-id>` and verifies the child ticket's DESCRIPTION carries the full verbose prose. This is the C-2 analogue of the C-1 content-check: archive-FIRST (the `bw create`), content-CHECK (`bw show` confirms the bytes landed in the description), THEN delete inline. The ordering guarantees losslessness — the bytes live in a titled child ticket before the inline copy is removed. (P7 asserts this.)

**Why child tickets, not comments (ARGUS residual-2, recorded for the auditor):** these 2 blocks are the genuinely not-yet-in-bw provenance — their bw record IS the sole surviving copy. A NAMED child id is the discoverable home; a comment stream is not. DAEDALUS's own rev1 weak point 2 conceded the discoverability gap; ARGUS's adjudication closes it.

### 3.5 DUPLICATE relocations (→ pointer; slim-core residue = 1-line pointer)

| Source (§ + live lines) | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| §7.3 Working with beadwork — command syntax (423–453) | DUPLICATE | `operating-disciplines.md` §12 (confirmed canonical: §12 self-declares "do not duplicate", op-disc:729; ARGUS DISCHARGED) | Delete the verbose cookbook (the `-m` table, the per-command table); keep a 1-line pointer: "bw command syntax → `operating-disciplines.md` §12 (canonical cookbook)." + the POLYBIUS-seat-specific framing (the `bw prime` at session start note + TIRO delegation note at 453) which is NOT duplicated content. Relocation-index row. NO recompose marker (DUPLICATE points at a deployed sibling file, not re-inlined). |

**Scope note for §7.3:** §7.3 mixes DUPLICATE (the syntax cookbook, fully present at op-disc §12) with POLYBIUS-SPECIFIC framing (run `bw prime` at session start; TIRO specialist-delegation). The DUPLICATE *syntax* deletes to a pointer; the POLYBIUS-specific framing STAYS (it is not duplicated at §12 — §12 is universal-seat, §7.3's prime+TIRO notes are POLYBIUS-seat application). This is the modules/README.md §5.3 worked example exactly. (ARGUS DISCHARGED.)

### 3.6 KEEP-TIGHTEN (stays inline; no ledger relocation — listed for completeness/audit)

§1 (15–23), §2 (27–39), §3 (41–59), §4 intro + §4.1–§4.8 disciplines [rules stay; provenance tail compresses per §3.3], §4.5 [+ 0hl F1 lean], §6 (379–389), §7 [intro + §7.1/§7.2/§7.4/§7.5/§7.6 stay; §7.3 dupe relocates per §3.5], §8 (503–509), §9 (513–534), §13 (806–881, KEEP-TIGHTEN WHOLE — see §3.1 note + ARGUS CONCUR), §15 (899–914), §16 intro + §16.2/§16.3/§16.4/§16.5/§16.8 [rules stay; §16.1/§16.6/§16.7 provenance compresses per §3.3+§3.8], §17 intro + §17.2/§17.3/§17.4 [rules stay; §17.1/§17.5/§17.6 compress], §18 intro + §18.1/§18.2/§18.3/§18.4 [rules stay; §18.5/§18.6 compress], §19 intro + §19.1/§19.2/§19.3/§19.4/§19.5 [rules stay; §19.6/§19.7 compress].

### 3.7 Ledger summary (chunk counts per class — RE-COUNTED, self-consistent; ARGUS r3 fix)

rev1's §3.7 claimed "5 SPLIT / 16 PROVENANCE" — an off-by-one in the losslessness-proof's own count. The live source has exactly **4 SPLIT** cross-ref subsections (§16.7 at 1034, §17.6 at 1157, §18.6 at 1217, §19.7 at 1284 — confirmed by grep this design phase). Corrected counts:

- **CONDITIONAL:** 5 whole-section relocations (§5, §10, §11, §12, §14) → 5 new module files. + 1 fold-in (§5.6 → onboarding.md). = **6 CONDITIONAL chunks.**
- **PROVENANCE:** **9 C-1** (resolve live; ADA content-checks per-deletion) + **2 C-2** (archive-first to dedicated child tickets stoa--xyb.6.1 / .6.2) + **4 SPLIT** cross-ref subsections (live §refs kept, provenance → Anchor; per-line in §3.8) = **15 PROVENANCE chunks.** (9 + 2 + 4 = 15. Self-consistent.)
  - The 9 C-1: §4.3.1/ezj, §15/nax+ariadne--8fd, §16.1/32b.3, §16.6/32b.3-cluster, §17.1/ads, §17.5/ads, §18.5/k36, §19.6/86k, §5.1.2/3cs. (Count: 9.)
  - The 2 C-2: §5.1.1.1, §5.1.3. (Count: 2.)
  - The 4 SPLIT: §16.7, §17.6, §18.6, §19.7. (Count: 4.)
- **DUPLICATE:** 1 (§7.3 cookbook → op-disc §12 pointer) = **1 DUPLICATE chunk.**
- **KEEP-TIGHTEN:** ~13 sections stay inline (prose tightened): §1, §2, §3, §4 (rules), §6, §7 (rules minus §7.3), §8, §9, §13, §15, §16 (rules), §17 (rules), §18 (rules), §19 (rules).
- **0hl fold:** 2 rows (F1 inline-lean, F2 → onboarding.md §5.6), audited as a separable slice.

**Note (§5.1.1 sub-empirical):** §5.1.1's in-prose 2026-05-04 empirical (244) is NOT counted as a standalone PROVENANCE chunk — it relocates WITH its parent §5 CONDITIONAL block into onboarding.md (the 1-liner stays in the module). It is listed in §3.3 for completeness but is part of the §5 CONDITIONAL relocation, not a separate provenance row.

### 3.8 SPLIT per-line enumeration (ARGUS r2 — the load-bearing fix; deterministic, no ADA guessing)

Each of the 4 SPLIT cross-ref subsections mixes THREE ref types: (a) LIVE in-file `§N` pointers, (b) LIVE sibling-file `<file> §N` pointers, (c) PROVENANCE bw-id / dated-empirical / source-doc lines. The rule: **type (a) + (b) = LIVE → stay inline VERBATIM in the slim core's cross-ref subsection; type (c) = PROVENANCE → collapse into the section's `Anchor:` line** (the empirical anchor already exists in the §N.6 N=1 provenance row's Anchor, so the bw-id provenance lines fold into it, not a NEW anchor). A mis-split that relocates a LIVE operational pointer = dropped canon. The enumeration below is per-line against the live source so ADA does NOT judge.

**Convention for "LIVE":** any line whose payload is a pointer to a section/file a reader follows to find OPERATIONAL content (a discipline, a mechanism, a paired framing) is LIVE. Any line whose payload is "this rule exists because <ticket/date>" or "the source-of-truth for this section's content is <ticket/doc>" is PROVENANCE.

#### §16.7 Cross-references (live lines 1034–1050)

| Source line(s) | Payload | Class | Disposition |
|---|---|---|---|
| 1036 | `stoa--32b` parent epic + `stoa--32b.1` / `stoa--32b.2` sibling future arcs (epic-structure provenance) | **PROVENANCE** | Fold into §16's Anchor (the epic + sibling-arc ids are provenance, recoverable via bw show). |
| 1037–1040 | "Load-bearing **sources** for this arc's content" — `stoa--32b.3` ticket body (primary source), `HANDOFF_POLYBIUS_2026-05-16.md` (worked example source), `docs/sessions/...-retro.md` (adjacent context source) | **PROVENANCE** | These are source-of-truth-for-content cites = provenance. Fold the bw-id (`stoa--32b.3`) into §16's Anchor; the on-disk source-doc paths (HANDOFF, retro) fold into the Anchor's recovery note (`Anchor: stoa--32b.3 — sources: HANDOFF_POLYBIUS_2026-05-16.md, docs/sessions/2026-05-16-...retro.md`). |
| 1041–1046 | "Within this file" — §4.5, §6, §7, §14, §15 (5 in-file pointers, each with operational gloss: "the authoring pattern this extends", "the analogous PLINY-side discipline", "bw is the durable-substrate channel", "daily-cadence mechanism", "the gate this passes through") | **LIVE** | Keep ALL 5 in-file `§N` pointers inline VERBATIM (these are operational cross-refs a reader follows). Tighten the gloss prose if verbose, but the pointers stay. |
| 1047 | `operating-disciplines.md` §21 (Ariadne-search-ready authoring — universal-team framing) | **LIVE** | Keep (sibling-file operational pointer). |
| 1048 | §16.8 (bw 0.13.0 primitives — the two forward-only primitives) | **LIVE** | Keep (in-file operational pointer). |
| 1049 | `operating-disciplines.md` §30 (Four-layer identity model — structural framing) | **LIVE** | Keep (sibling-file operational pointer). |
| 1050 | `substrate/skills/handoff-author/SKILL.md` (operational shape of §16.3's handoff authoring; invoke before /compact) | **LIVE** | Keep (operational skill pointer). |

**§16.7 net:** 8 LIVE pointers kept inline (§4.5, §6, §7, §14, §15, op-disc §21, §16.8, op-disc §30, handoff-author skill — that is 9 by enumerated lines; §4.5/§6/§7/§14/§15 = 5, + op-disc§21 + §16.8 + op-disc§30 + skill = 4, total 9 LIVE). 2 PROVENANCE clusters (1036 epic-structure; 1037–1040 sources) fold into the §16 Anchor. 17 source lines → ~9 LIVE cross-ref lines + the existing §16 Anchor (no NEW anchor line).

#### §17.6 Cross-references (live lines 1157–1164)

| Source line(s) | Payload | Class | Disposition |
|---|---|---|---|
| 1159 | `operating-disciplines.md` §23 (Base vs custom — universal-team cut; "every seat reads that section, this one is POLYBIUS-specific") | **LIVE** | Keep (sibling-file operational pointer). |
| 1160 | `MAJOR_POLYBIUS.md` §14 (substrate-update check — the daily-cadence mechanism that catches drift on BASE files) | **LIVE** | Keep (in-file operational pointer). |
| 1161 | `MAJOR_POLYBIUS.md` §15 (N=1 honest-scope — the gate this passes through) | **LIVE** | Keep (in-file operational pointer). |
| 1162 | `substrate/install.sh`, `check.sh`, `apply.sh` (the three tools that scope-to-base via cite-comments referencing this section) | **LIVE** | Keep (operational tooling pointers — a reader follows these to the tools that honor §17.3). |
| 1163 | `stoa--ads` (this arc's ticket) + forthcoming railway_stoa custom team arc (empirical anchor) | **PROVENANCE** | Fold `stoa--ads` into §17's Anchor (it's the §17.5 N=1 ticket); the railway_stoa empirical-anchor note folds into the Anchor's recovery note. |
| 1164 | `MAJOR_POLYBIUS.md` §19 (Two-team architecture — paired behavioral framing to §17's path convention) | **LIVE** | Keep (in-file operational pointer). |

**§17.6 net:** 5 LIVE pointers kept (op-disc §23, §14, §15, the 3 tools, §19). 1 PROVENANCE line (1163) folds into the §17 Anchor. 8 source lines → ~5 LIVE lines + existing §17 Anchor.

#### §18.6 Cross-references (live lines 1217–1225)

| Source line(s) | Payload | Class | Disposition |
|---|---|---|---|
| 1219 | Project-root `CLAUDE.md` (the universal-rule prose that cross-refs THIS section as the explicit-exception canon) | **LIVE** | Keep (operational pointer — the reciprocal of CLAUDE.md's pointer here; load-bearing for the exception-canon coherence). |
| 1220 | `MAJOR_PLINY.md` §5.9 (pre-branch hygiene check 2; §18.3 names the push-immediately discipline that keeps it passing) | **LIVE** | Keep (sibling-file operational pointer). |
| 1221 | `MAJOR_POLYBIUS.md` §15 (N=1 honest-scope — the gate this passes through) | **LIVE** | Keep (in-file operational pointer). |
| 1222 | `operating-disciplines.md` §6.7.1 (the canon-promotion gate this discipline enters off-gate on) | **LIVE** | Keep (sibling-file operational pointer — a reader follows it to the gate mechanism). |
| 1223 | `operating-disciplines.md` §12 (bw cookbook; the bw operations §18.1 names operate on the orphan beadwork branch) | **LIVE** | Keep (sibling-file operational pointer). |
| 1224 | Empirical anchor: `stoa--k36` (2026-05-17 user-tier POLYBIUS end-of-session hygiene audit; folded as C1 in Arc 34) | **PROVENANCE** | Fold `stoa--k36` into §18's Anchor (it's the §18.5 N=1 ticket). |
| 1225 | `MAJOR_POLYBIUS.md` §19 (Two-team architecture — §18's carve-out sits inside §19's picture) | **LIVE** | Keep (in-file operational pointer). |

**§18.6 net:** 6 LIVE pointers kept (CLAUDE.md, MAJOR_PLINY §5.9, §15, op-disc §6.7.1, op-disc §12, §19). 1 PROVENANCE line (1224) folds into the §18 Anchor. 9 source lines → ~6 LIVE lines + existing §18 Anchor.

#### §19.7 Cross-references (live lines 1284–1295)

| Source line(s) | Payload | Class | Disposition |
|---|---|---|---|
| 1286 | `MAJOR_POLYBIUS.md` §17 (Base vs custom agents — the path-convention layer; §19 is the behavioral-framing layer; "the two are paired") | **LIVE** | Keep (in-file operational pointer). |
| 1287 | `MAJOR_POLYBIUS.md` §14 (Substrate-update check — keeps the base team in sync) | **LIVE** | Keep (in-file operational pointer). |
| 1288 | `MAJOR_POLYBIUS.md` §18 (user-tier direct-commit carve-out within the two-team picture) | **LIVE** | Keep (in-file operational pointer). |
| 1289 | `MAJOR_POLYBIUS.md` §17.4 (Custom CAPTAIN name discipline — the silent-collision footgun; incl. the disambiguation note that op-disc §17 is NOT the intended target) | **LIVE** | Keep VERBATIM incl. the disambiguation parenthetical (it prevents a same-number cross-file mis-resolution — load-bearing operational note, NOT provenance). |
| 1290 | `operating-disciplines.md` §23 (Base vs custom — universal-team layer; §19 extends into the behavioral layer) | **LIVE** | Keep (sibling-file operational pointer). |
| 1291 | `operating-disciplines.md` §29 (Multi-team interoperation — the next level up; §19 intra-workspace, §29 inter-workspace) | **LIVE** | Keep (sibling-file operational pointer). |
| 1292 | `substrate/skills/check-substrate-updates/` (the base-team sync skill) | **LIVE** | Keep (operational skill pointer). |
| 1293 | `substrate/skills/agent-author/` (skill the base team uses authoring project-team specialists) | **LIVE** | Keep (operational skill pointer). |
| 1294 | `substrate/skills/tier2-project-onboarding/` (existing onboarding skill; may extend in a future arc) | **LIVE** | Keep (operational skill pointer). |
| 1295 | Empirical anchor: `stoa--86k` (2026-05-13 PRINCIPAL substrate-architecture discussion) + §17.5 / §18.5 (the conventions this section's framing extends from) | **SPLIT WITHIN LINE** | `stoa--86k` → fold into §19's Anchor (PROVENANCE). The "§17.5 / §18.5 (the conventions this extends from)" clause is a LIVE in-file pointer → keep inline as a short cross-ref. |

**§19.7 net:** 9 full LIVE pointers + 1 LIVE half of line 1295 (§17.5/§18.5) kept; 1 PROVENANCE half of line 1295 (stoa--86k) folds into the §19 Anchor. 12 source lines → ~10 LIVE lines + existing §19 Anchor. **Line 1295 is the only intra-line split — flagged for ADA: split the line, keep the §17.5/§18.5 half, fold the stoa--86k half into the Anchor.**

**SPLIT enumeration summary:** across the 4 subsections, 29 LIVE cross-ref lines stay inline (9 + 5 + 6 + 9, plus the 1295 LIVE half); 5 PROVENANCE clusters fold into the 4 existing §N Anchors (§16.7 has 2 clusters: 1036 + 1037–1040; §17.6/§18.6/§19.7 have 1 each). NO new Anchor lines are minted — the bw-id provenance folds into the Anchor already created by the paired §N.6 N=1 provenance row. The deterministic rule for ADA: **keep every line that points at a §/file/skill/tool a reader follows to operational content; fold every line that says "exists because <ticket/date>" or "source-of-truth is <ticket/doc>" into the section's existing Anchor.**

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing. P1–P9 carry from rev1 (P7 updated for residual-2 child tickets); P10 + P11 are NEW (ARGUS r1 recompose-completeness + r2 SPLIT-live-preservation).

### P1 — Line-count target met (the cut actually cut)
```bash
wc -l substrate/MAJOR_POLYBIUS.md
```
**Pass:** core is in the **300–350 line** target band (down from 1299). **Falsifies if:** > 400 (cut too shallow) or < 250 (suspiciously aggressive — check for dropped rules). A 360–400 landing is a partial-not-failure (ARGUS r6 CONCUR — §16–§19 rules are dense always-on core; P1 >400 is the falsifier guard). Also run op-disc §33's line-count discipline against each new module (no module is itself a re-bloat monolith).

### P2 — Every relocated CONDITIONAL section has a real module home + a routing-map row
```bash
for m in onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check; do
  test -s "substrate/modules/$m.md" && echo "OK $m" || echo "MISSING $m"
done
```
**Pass:** all 5 module files exist and are non-empty. Then grep the slim core for a routing-map row naming each module path. **Falsifies if:** any module missing/empty, or any routing-map row points at a module file that doesn't exist (dangling reference = LOST CANON).

### P3 — Every relocated section leaves a stub at its original number (cross-ref preservation)
```bash
grep -nE '^## (5|10|11|12|14)\.' substrate/MAJOR_POLYBIUS.md
```
**Pass:** §5, §10, §11, §12, §14 headings still present (as stubs). **Falsifies if:** any relocated section number is GONE (would break every cross-ref pointing at it).

### P4 — DUPLICATE pointer resolves to the canonical home
```bash
grep -n 'operating-disciplines.md.*§12' substrate/MAJOR_POLYBIUS.md   # the §7.3 pointer exists
grep -n '^## 12\. ' substrate/operating-disciplines.md                # the home heading exists
```
**Pass:** §7.3 carries a pointer to op-disc §12 AND op-disc §12 exists. **Falsifies if:** pointer present but §12 home gone, or the verbose cookbook still inline at §7.3 (dupe not actually deleted).

### P5 — C-1 content-check gate was honored (LOST-CANON proof — sampled)
For a sample of C-1 deletions (at minimum §16.6/stoa--32b.3, §17.5/stoa--ads, §18.5/stoa--k36, §19.6/stoa--86k):
```bash
for id in stoa--32b.3 stoa--ads stoa--k36 stoa--86k; do echo "=== $id ==="; bw show "$id" 2>&1 | head -40; done
```
**Pass:** each cited ticket's body materially carries the N=1 story the deleted inline prose held (the date, the PRINCIPAL declaration, the accretion framing). **Falsifies if:** any cited ticket is a thin stub that does NOT carry the deleted detail → that deletion dropped canon, classification was wrong (should have been C-2).

### P6 — (RETIRED — folded into P7.) rev1's P6 grepped stoa--xyb.6 comments for the C-2 archive. Residual-2 moves the C-2 archive to dedicated child tickets, so the assertion changes home — see P7.

### P7 — C-2 archive-first executed BEFORE deletion, in DEDICATED CHILD TICKETS (residual-2)
```bash
# The two C-2 child tickets exist under the arc ticket and carry the verbose prose in their description:
bw list --all 2>&1 | grep -E 'xyb\.6\.(1|2)'
bw show stoa--xyb.6.1 2>&1 | grep -iE 'cross-project-leak|ariadne|N=2'
bw show stoa--xyb.6.2 2>&1 | grep -iE 'cron-hygiene|HUMAN_paste|N=0'
# And the slim-core/module cite-back points at the child id:
grep -nE 'stoa--xyb\.6\.(1|2)' substrate/modules/onboarding.md
```
**Pass:** both child tickets exist (parent = stoa--xyb.6), each description carries its verbose provenance, and onboarding.md's cite-back names the correct child id. **Falsifies if:** a C-2 verbose block is gone from source AND not present in a child-ticket description (LOST CANON — the C-2 archive step was skipped or archived to a comment instead of a description), OR the cite-back id does not match the created ticket.

### P8 — 0hl fold landed lean + separable (ARGUS r4 — lean-by-design)
```bash
git log --oneline arc-45/build | head    # F1/F2 land as a distinct commit, message names the lean deviation
grep -n '5.6\|5\\.6' substrate/modules/onboarding.md   # §5.6 say-trigger in the module
grep -n 'say-trigger\|paste-trigger' substrate/MAJOR_POLYBIUS.md   # §4.5 reconciliation lean
```
**Pass:** §5.6 present in onboarding.md (lean, ≤ ~25 lines); §4.5 carries the 2-mechanism reconciliation (lean, ~2 sentences); the fold is a separable commit whose message states the lean-vs-0hl-verbatim deviation is by-design. **Falsifies if:** §5.6 mirrored verbose (> ~25 lines) — that would mean ADA reverted to 0hl's verbatim instruction instead of the design's intentional lean form — or the §4.5 reconciliation absent.

### P9 — No author-field regression (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/MAJOR_POLYBIUS.md substrate/modules/*.md
```
**Pass:** no author-like field names anyone other than Denson Smith (role files carry none; modules carry none). **Falsifies if:** any new module's provenance header introduces an author field with the wrong name.

### P10 — Subproject recompose completeness (ARGUS r1 — THE LOST-CANON-at-subproject probe; NEW)

Run on a THROWAWAY subproject deploy (mirroring Arc-1's throwaway-target verification — do NOT mutate any operator-owned workspace; per op-disc §25.5 use a `git clone --no-local` or a synthetic parent dir under a tmp path):
```bash
# 0. Synthetic throwaway parent + run install.sh in subproject mode against it:
TMP=$(mktemp -d); mkdir -p "$TMP/myproj"
bash substrate/install.sh --target=subproject --parent="$TMP" --subproject=myproj --yes
RECOMPOSED="$TMP/myproj/.claude/MAJOR_POLYBIUS_myproj.md"

# (a) ZERO unexpanded markers remain in the recomposed subproject role file:
grep -cE '<!-- /?MODULE-INLINE:' "$RECOMPOSED"    # expect 0

# (b) EVERY module body is present (assert each module's first-heading line appears in the recomposed file):
for m in onboarding sub-project-spawning pair-programmer-authoring pair-programming-prototyping substrate-update-check; do
  head1=$(head -1 "substrate/modules/$m.md")
  grep -Fq "$head1" "$RECOMPOSED" && echo "OK body present: $m" || echo "MISSING body: $m"
done

# (c) recomposed subproject file is canon-equivalent to project-tier full content:
#     line count is in the FULL band (the 5 module bodies are re-inlined), NOT the slim band:
wc -l "$RECOMPOSED"     # expect ~1200+ (full content re-inlined), NOT 300-350 (that would mean recompose silently no-op'd)
```
**Pass:** (a) zero `MODULE-INLINE` markers survive in the recomposed file (every paired sentinel was expanded); (b) all 5 module first-heading lines appear in the recomposed file; (c) the recomposed file is in the FULL line band (~1200+), proving the bodies re-inlined rather than the markers being silently stripped to nothing. **Falsifies if:** any unexpanded marker remains (recompose skipped a marker → LOST CANON at subproject tier), OR any module's body is absent (a marker referenced a body that did not inline), OR the recomposed file is still in the slim band (recompose silently no-op'd — the catastrophic failure r1 names). **Also assert FAIL-LOUD:** a deliberately-broken run (rename one module source, or delete one stub marker from the slim core, then re-run install.sh subproject mode) MUST exit non-zero with a clear error — NOT deploy a partial file (P10-negative; see §6.5).

### P11 — SPLIT LIVE cross-refs preserved inline (ARGUS r2 — the per-line-split proof; NEW)

After the cut, assert every LIVE cross-ref enumerated in §3.8 still appears in the slim core's §16.7/§17.6/§18.6/§19.7, and the PROVENANCE bw-ids folded into the §N Anchors:
```bash
# LIVE pointers that MUST survive in the slim core (sample the load-bearing ones from §3.8):
#   §16.7 LIVE: §4.5, §6, §7, §14, §15, op-disc §21, §16.8, op-disc §30, handoff-author skill
#   §17.6 LIVE: op-disc §23, §14, §15, install.sh/check.sh/apply.sh, §19
#   §18.6 LIVE: CLAUDE.md, MAJOR_PLINY §5.9, §15, op-disc §6.7.1, op-disc §12, §19
#   §19.7 LIVE: §17, §14, §18, §17.4, op-disc §23, op-disc §29, check-substrate-updates, agent-author, tier2-project-onboarding, §17.5/§18.5
grep -nE '§21|§30|handoff-author|§23|§29|§6\.7\.1|§17\.4|agent-author|tier2-project-onboarding' substrate/MAJOR_POLYBIUS.md
# PROVENANCE bw-ids that MUST be GONE from the cross-ref subsections (folded into Anchors instead):
#   §16.7: stoa--32b.1/.2 epic-structure + HANDOFF/retro source cites folded;
#   §17.6: stoa--ads (in §17 Anchor); §18.6: stoa--k36 (in §18 Anchor); §19.7: stoa--86k (in §19 Anchor)
# Spot-check the §19.7 intra-line split: §17.5/§18.5 LIVE half present, stoa--86k folded to Anchor:
grep -nE '§17\.5|§18\.5' substrate/MAJOR_POLYBIUS.md
grep -nE 'Anchor.*stoa--86k' substrate/MAJOR_POLYBIUS.md
```
**Pass:** every LIVE pointer from §3.8 resolves in the slim core (none dropped); the PROVENANCE bw-ids appear in the §N Anchor lines (folded) not orphaned in a cross-ref bullet; the §19.7 intra-line split kept the §17.5/§18.5 LIVE half. **Falsifies if:** any §3.8 LIVE pointer is missing from the slim core (a LIVE operational pointer was wrongly relocated = dropped canon — the exact r2 failure), OR a PROVENANCE bw-id is still sitting as a standalone cross-ref bullet (not folded).

---

## §5 — Build steps (for ADA — ordered; the cut sequence)

**Step 0 (process hazard — DO THIS FIRST).** Confirm cwd is the worktree (`git -C C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-45-build rev-parse --show-toplevel` resolves to the worktree, branch `arc-45/build`). Use ABSOLUTE worktree paths for EVERY Write (`C:/Users/denso/claude_projects/the-stoa/.claude/worktrees/arc-45-build/...`). After each write, verify it landed in the worktree (`git -C <worktree> status` shows the file as modified/added there) and NOT in main (`git -C C:/Users/denso/claude_projects/the-stoa status` should NOT show your edit). The rev1 DAEDALUS hit the Write-resolves-against-main-root hazard; this gate catches it before it compounds.

1. **Create the 5 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §3.1. Each module: provenance header (cites this design + stoa--xyb epic) → relocated content verbatim-tightened. Module first line is a stable heading (P10 keys on it). Run op-disc §33 line-count discipline per module. NO author field (P9).
2. **Fold 0hl Edit 2 into onboarding.md** as a LEAN `## §5.6` (separable; per §2.4 / §3.2 F2 — lean by design, ≤ ~25 lines).
3. **Execute C-2 archive-first as DEDICATED CHILD TICKETS** (§3.4 / residual-2): `bw create "Arc 45 C-2 archive: §5.1.1.1 ..." --parent stoa--xyb.6 -d "<verbose prose>"` and the §5.1.3 equivalent, BEFORE touching the source. Record the assigned child ids. Run `bw show <child-id>` to content-check each description carries the verbose prose (archive-FIRST, content-CHECK, THEN delete). Write the cite-backs in onboarding.md using the ACTUAL assigned child ids.
4. **Cut the slim core** (`substrate/MAJOR_POLYBIUS.md`):
   - For each CONDITIONAL section, replace body with the 2-line stub + the paired `<!-- MODULE-INLINE:<name> -->` … `<!-- /MODULE-INLINE:<name> -->` marker (§2.7 exact literal).
   - For each PROVENANCE row run the C-1 `bw show` content-check (§3.3 gate) THEN delete-to-Anchor.
   - For each SPLIT subsection, apply the §3.8 per-line enumeration: keep LIVE pointers inline verbatim, fold PROVENANCE bw-ids into the §N Anchor (incl. the §19.7 line-1295 intra-line split).
   - Delete §7.3 dupe to op-disc §12 pointer (keep the POLYBIUS-specific prime+TIRO framing).
   - Tighten KEEP-TIGHTEN prose (incl. §13 WHOLE — do NOT split, ARGUS CONCUR).
   - Add §3.5 (routing map + relocation index + subproject-tier clause §6.3). Fold 0hl Edit 1 lean into §4.5.
5. **Add the install.sh subproject-recompose step** (§6.5 — substrate-tooling source, gauntlet-gated per §18.2, correctly inside this arc): the awk state-machine + FAIL-LOUD checks, gated on subproject mode, post-`sed` (after L757-765 writes `$DEST_POLYBIUS`). Smoke-test against a throwaway synthetic parent (P10) before considering the step done.
6. **Cross-ref re-point sweep** (named weak point §7): because section numbers are PRESERVED (§2.7), the sweep is a VERIFICATION not a churn — grep the substrate for `MAJOR_POLYBIUS.md §N` cross-refs and confirm each target still resolves to a real anchor (stub or live). Prove with: `grep -rn 'MAJOR_POLYBIUS' substrate/ | grep -oE '§[0-9.]+'` cross-checked against the slim core's headings.
7. **Commit the 0hl fold as a distinct commit** (F1+F2) — commit message NAMES the lean-vs-0hl-verbatim deviation as by-design (ARGUS r4). Co-Authored-By: `CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` per op-disc §28.
8. **Run all probes P1–P11** as a self-check before returning to PLINY.

---

## §6 — Subproject-tier module-access strategy (PEER-MANDATED design-phase gate)

### 6.1 The probe (RAN live; ARGUS DISCHARGED against the real ariadne deploy + current web)

**Question:** does a subproject orchestrator's (`MAJOR_PLINY_<slug>` running for a subproject) dispatched CAPTAIN resolve `Read .claude/modules/<X>.md` to the PARENT workspace's `.claude/modules/`, or fail?

**Web-check (current behavior, May 2026):**
- Subagents inherit the **parent-session cwd**; there is **no per-subagent cwd override** (claude-code #31940 AgentDefinition lacks cwd/additionalDirectories; #12748 feature-request for Task-tool cwd still open).
- Subagent relative-path resolution is **fragile and contested**: #4754 (relative paths from CLAUDE.md resolve against cwd, not config dir), #31546 (subagents resolve to main repo root not worktree), #56686 (sub-agents DENIED Read on paths outside project root despite explicit allow rules), #15627 (path display relative to cwd not project root). ARGUS corroborated #56686 current (~2 wks) + NEW #29423 (subagents skip project config) + #29610 (bypassPermissions no help for bg subagents).

**Live filesystem probe (against the REAL deployed subproject `ariadne-core-workspace/ariadne-core/`; ARGUS independently re-confirmed):**
1. The deployed subproject `.claude/` is a **fully self-contained substrate copy**: own `MAJOR_POLYBIUS_ariadne_core.md`, own `MAJOR_PLINY_ariadne_core.md`, own `operating-disciplines.md`, own `agents/`, own `skills/`. It does NOT read role files from the parent. (ARGUS: self-contained 64KB role file.)
2. Neither the subproject's `.claude/` NOR the parent workspace's `.claude/` has a `modules/` directory (install.sh sets `DEST_MODULES_DIR=""` in subproject mode — deploy skipped, confirmed live at install.sh:624).
3. The §10.2 spawn convention launches the subproject orchestrator by **opening a new terminal in `<parent>/<slug>/`** — so the launch cwd IS the subproject root. A dispatched CAPTAIN inheriting that cwd resolves `Read .claude/modules/<X>.md` → `<parent>/<slug>/.claude/modules/<X>.md`, which **does not exist** (install.sh skips it). Under the parent-root-cwd scenario it would hit the #56686 outside-project-root denial.

**Probe result:** CHANNEL 2 (disk-module via relative `Read .claude/modules/<X>.md`) is **NOT reliable at subproject tier.** This resolves the Arc-1 TRACKED gating question (modules/README.md §7): "Read does NOT reliably resolve parent modules from a subproject orchestrator."

### 6.2 The chosen strategy: **2b — RECOMPOSE-INLINE at subproject tier** (ARGUS CONCUR over 2-body fork)

Given the probe, the brief offered: (a) extend modules glob deploy to subproject tier, OR (b) keep relocated CONDITIONAL content inline at subproject tier. **Strategy 2b is chosen** (ARGUS CONCUR on residual 4 — recompose over fork). Rationale:

- **2a (extend deploy) does not fix the resolution problem.** Even if install.sh deployed `<parent>/<slug>/.claude/modules/`, the dispatched CAPTAIN's `Read .claude/modules/<X>.md` STILL depends on the fragile/contested relative-path resolution (#56686 denial outside project root; #31546 worktree mis-resolution). Deploying the files does not guarantee the Read resolves. 2a adds deploy surface AND a still-unreliable Read — strictly worse than 2b.
- **2b is the only strategy that holds LOSSLESS-ON-CANON at subproject tier deterministically.** If the CONDITIONAL content is INLINE in the subproject's `MAJOR_POLYBIUS_<slug>.md`, no Read resolution is needed — the content is present in the role file the subproject already self-contains.

**Mechanism for 2b (the tier-aware recompose):** the cut is **TIER-AWARE in install.sh**, not in the source file. The SOURCE `substrate/MAJOR_POLYBIUS.md` is the slim core (stubs w/ markers + routing-map). At deploy time:
- **user / project tiers:** install.sh deploys the slim core AS-IS (the `sed` at L757-765) + deploys `.claude/modules/` (Arc 44). The slim core's routing-map points at modules; CHANNEL 2 works (Read resolves at user/project tier — Arc 1 verified end-to-end). The `MODULE-INLINE` markers are inert HTML comments (invisible to a reader).
- **subproject tier:** install.sh deploys a **RECOMPOSED** `MAJOR_POLYBIUS_<slug>.md` = slim core with the 5 module bodies **re-inlined at their paired markers** (§6.5 algorithm). The subproject role file is self-contained (matching the existing self-contained-subproject pattern probed live). No modules dir deployed (unchanged — `DEST_MODULES_DIR=""`).

This is an `install.sh` change — substrate-tooling source (gauntlet-gated per §18.2), correctly inside this arc.

### 6.3 The slim-core clause that makes the strategy auditable

The slim core's §3.5 carries a one-line tier-awareness rule (so the strategy is visible to a reader, not buried in install.sh):

> **Subproject-tier module access (per design-arc-45 §6):** at subproject tier the CONDITIONAL module content is re-inlined into this role file at deploy time (install.sh recompose at the `<!-- MODULE-INLINE:<name> -->` markers) — subproject orchestrators do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably at subproject tier; claude-code #56686/#31546/#29423). At user/project tier the routing-map's `disk (Read)` channel applies and the markers are inert. Anchor: stoa--xyb (Arc-1 tracked gating question §7) + design-arc-45 §6 probe.

### 6.4 Alternative considered + rejected: leave subproject as a 2-body fork (ARGUS CONCUR rejected)

Rejected: deploy the FULL (pre-cut, 1299-line) role file at subproject tier and the slim core only at user/project. This holds losslessness but (a) FORKS the source (two role-file bodies to maintain — exactly the duplication the debloat epic fights) and (b) the subproject tier is precisely where the 25k-cap pagination pain bites (the live ariadne-core subproject role file is 64KB). The recompose-at-deploy approach (2b) keeps ONE source (slim core + modules) and recomposes mechanically — single source of truth, no fork. ARGUS CONCURred: the fork re-introduces the exact duplication the epic exists to kill; recompose keeps single-source-of-truth, with the r1 marker-hardening as the build requirement that contains the LOST-CANON-at-subproject risk.

### 6.5 The recompose ALGORITHM + FAIL-LOUD semantics (ARGUS r1 — the load-bearing spec)

**Where it runs.** A NEW step in `install.sh`, gated `if [ "$TARGET" = "subproject" ]`, placed IMMEDIATELY AFTER the MAJOR_POLYBIUS `sed`-substitution writes `$DEST_POLYBIUS` (current install.sh L757-765). At that point `$DEST_POLYBIUS` holds the slim core (markers inert). The recompose step rewrites `$DEST_POLYBIUS` in place, expanding each paired marker into the module body. (It does NOT touch `$SRC_POLYBIUS` — the source stays slim; recompose is deploy-time-only, subproject-only.) Honors `$DRY_RUN` (print the plan, do not rewrite).

**The marker (from §2.7).** Paired HTML-comment sentinel in the slim-core source:
```
<!-- MODULE-INLINE:<module-name> -->
<!-- /MODULE-INLINE:<module-name> -->
```
`<module-name>` = module basename without `.md`. The body to inline is `${SRC_MODULES_DIR}/<module-name>.md` (the SOURCE module — recompose reads from substrate source, where install.sh runs, NOT from a deployed modules dir which subproject mode never creates).

**The algorithm (awk state-machine — deterministic, single pass):**
1. Read `$DEST_POLYBIUS` line by line.
2. On a line matching `^<!-- MODULE-INLINE:(.+) -->$`: capture `<module-name>`; assert `${SRC_MODULES_DIR}/<module-name>.md` EXISTS (FAIL-LOUD check A — see below); emit the OPEN marker line (kept, so the recomposed file remains idempotently re-recomposable AND a reader sees the provenance of the inlined block), then emit the ENTIRE body of `${SRC_MODULES_DIR}/<module-name>.md`; set state = "inside-marker:<module-name>".
3. While state = "inside-marker:<X>": SKIP every source line until the matching close `^<!-- /MODULE-INLINE:X -->$` (this skips the empty gap in a fresh slim core, OR the previously-inlined body if re-recomposing — idempotency). On the matching close line: emit it (kept), clear state.
4. A mismatched/missing close marker before EOF or before the next open marker = FAIL-LOUD check C.
5. All other lines: emit verbatim.
6. After the pass: FAIL-LOUD check B (every `substrate/modules/*.md` must have been referenced by some marker).

**FAIL-LOUD semantics (REQUIRED — silent skip is the LOST-CANON failure; install.sh `err()` exits non-zero):**
- **Check A — marker references a non-existent module.** A `<!-- MODULE-INLINE:X -->` whose `${SRC_MODULES_DIR}/X.md` does NOT exist → `err "recompose: marker MODULE-INLINE:X has no module source at ${SRC_MODULES_DIR}/X.md"`. (Catches a stub-marker typo or a deleted module.)
- **Check B — module exists with no marker.** After the pass, every `${SRC_MODULES_DIR}/*.md` must have been consumed by exactly one marker. Any module file NOT referenced by a marker → `err "recompose: module X.md exists but no MODULE-INLINE:X marker in the slim core — body would be DROPPED at subproject tier"`. (This is the precise LOST-CANON-at-subproject guard: a module that exists but is never inlined is canon present at user/project tier but ABSENT at subproject tier.)
- **Check C — unbalanced markers.** An open marker with no matching close (or a close with no open) → `err "recompose: unbalanced MODULE-INLINE markers for X"`. (Catches a hand-edit that broke the pairing.)
- **Check D — zero markers found AND modules exist.** If the slim core has NO `MODULE-INLINE` markers but `substrate/modules/*.md` is non-empty → `err`. (Defends against a future tighten edit that accidentally strips ALL markers — without this, recompose would silently produce the slim file at subproject tier, the catastrophic no-op P10(c) guards.)

A non-zero exit aborts the deploy — install.sh NEVER writes a partial/slim role file to a subproject. This is the structural property: a recompose that cannot prove completeness FAILS rather than ships LOST CANON.

**The README.md module is excluded from the marker-set check.** `substrate/modules/README.md` is the composition-layer reference doc, not a relocated POLYBIUS section — it has no `MODULE-INLINE` marker and is not inlined into any role file. Check B's "every module must have a marker" applies to the 5 relocated CONDITIONAL modules only; install.sh's recompose glob excludes `README.md` explicitly (e.g. `for src in ${SRC_MODULES_DIR}/*.md; do [ "$(basename "$src")" = README.md ] && continue; ...`). This exclusion is itself FAIL-LOUD-safe: README is never a marker target, so excluding it cannot drop a relocated body.

**Idempotency.** Because the algorithm keeps the OPEN and CLOSE marker lines and skips whatever sits between them on re-read, running recompose on an already-recomposed file produces the same output (re-inlines the body fresh from source, replacing the prior inlined copy). This makes a re-deploy safe (the existing install.sh idempotency property holds).

**Why this is a NEW code path (named weak point §7).** install.sh today is a pure `sed`-substitution + `cp` deploy (no body-injection). Recompose is wholly new — the highest-risk surface in the arc. The mitigations are structural: machine markers (not prose), the 4 FAIL-LOUD checks, P10's throwaway-target completeness probe, and P10-negative's deliberate-break test that asserts the err() fires.

**Generality note (ARGUS r5 CONSIDER — flagged, scoped to follow-up).** The recompose step is data-driven from the markers + the `substrate/modules/*.md` glob, NOT a hardcoded 5-module list. This is deliberate so the NEXT arc (cut MAJOR_PLINY.md, per the epic) reuses the SAME recompose code path without an install.sh re-edit — the markers in MAJOR_PLINY's slim core + its modules drive recompose identically. (Caveat: install.sh deploys BOTH MAJORs from one path; the recompose must run for BOTH `$DEST_POLYBIUS` and `$DEST_PLINY` in subproject mode. THIS arc only authors POLYBIUS markers, so `$DEST_PLINY` has zero markers and recompose is a clean no-op for it — Check D's "zero markers AND modules exist" must be evaluated PER-ROLE-FILE against the markers IN THAT FILE, not against the global module glob, OR scoped so PLINY's marker-less file does not trip Check D before PLINY is cut. ADA: scope Check D to "this role file has zero markers but references modules that exist for it" — for THIS arc, the simplest correct form is to run recompose+checks against `$DEST_POLYBIUS` only, and add `$DEST_PLINY` to the same data-driven loop when MAJOR_PLINY is cut. Flagged as weak point §7.4.)

---

## §7 — Self-assessed weak points (refreshed for rev2)

1. **The install.sh subproject recompose is a new deploy-time mechanism (highest-risk — now SPECIFIED, ARGUS r1).** rev2 specifies the marker + algorithm + 4 FAIL-LOUD checks, which converts rev1's open-ended risk into a bounded, testable one — but it is still a wholly new code path (install.sh today is pure sed+cp, no body-injection) and still the single place a marker/module mismatch could drop a body at the hardest-audited tier. *Why this shape anyway:* it is the only strategy that holds losslessness deterministically at subproject tier without forking the source (ARGUS CONCUR); the FAIL-LOUD checks make a mismatch ABORT the deploy rather than ship LOST CANON, and P10 + P10-negative verify both the happy path and that the err() fires. The residual risk is implementation-correctness of the awk state-machine, which VERA's throwaway-target probe exercises end-to-end.
2. **§16/§17/§18/§19 are KEEP-TIGHTEN, not relocate — the cut may under-deliver the line target if "tighten" is timid (ARGUS r6 CONCUR).** The biggest savings come from the 5 CONDITIONAL relocations (~600 lines move) + the provenance compressions (~250 lines → ~30 Anchor lines). §16–§19 are dense (~70–110 lines each) and stay inline as rules; conservative tightening could land the core at 380–420 rather than 300–350. *Why this shape anyway:* §16–§19 rules ARE operational core (lifecycle, base-vs-custom, two-team routing) read across sessions; relocating off-disk degrades availability-losslessness. A 360–400 landing is partial-not-failure (the cut still ~3x's the file); P1 falsifies at >400. ARGUS CONCURred the KEEP/relocate boundary is correctly drawn and flagged §16–§19 rule-prose as a candidate for its OWN future relocation arc rather than being forced under target here.
3. **The SPLIT per-line enumeration (§3.8) is grounded against TODAY's live source line numbers — a future re-read drift would mis-target it.** §3.8 cites specific source lines (e.g. §16.7 at 1036/1037–1040 as the PROVENANCE clusters). If the source shifts before ADA executes (it should not — same worktree, same commit-base), the line cites drift. *Why this shape anyway:* the enumeration ALSO carries the payload text per line (not just the line number), so ADA matches on CONTENT not just position; the line numbers are the locator, the payload description is the disambiguator. P11 verifies by GREPPING the LIVE pointer text (not line numbers), so the probe is drift-resistant even if the cites drift.
4. **Check D (zero-markers guard) interacts with the both-MAJORs-from-one-path deploy (ARGUS r5 surface).** install.sh deploys both POLYBIUS and PLINY at subproject tier from one code path; THIS arc authors POLYBIUS markers only, so PLINY's slim file has zero markers and a naive global Check D ("zero markers AND modules exist") would FALSE-POSITIVE on PLINY. *Why this shape anyway:* the spec scopes recompose+checks to `$DEST_POLYBIUS` ONLY for this arc (PLINY is untouched until its own cut), and the data-driven design means adding `$DEST_PLINY` to the loop when PLINY is cut needs no new code path — the markers in each file drive it. The weak point is that an ADA who wires the loop over BOTH files prematurely would trip Check D on PLINY; §6.5's generality note + this weak point name the trap explicitly so ADA scopes to POLYBIUS this arc.

---

## §8 — Residual questions for ARGUS (rev2 — re-confirm scope)

ARGUS adjudicated all 4 of rev1's residuals (CONCUR on §13 KEEP, PRESERVE numbers, RECOMPOSE over fork; ADJUDICATED C-2 → child tickets). rev2 carries those resolutions. The remaining items for the focused re-confirm:

1. **Recompose algorithm correctness (r1 closure).** Does the §6.5 awk state-machine + 4 FAIL-LOUD checks + idempotency spec close r1 to ARGUS's satisfaction, or is there a marker-format / algorithm edge case the spec misses (e.g. a module body that itself contains a literal `<!-- MODULE-INLINE: -->` string in a code fence — escaping concern)? I judge the 5 relocated modules carry no such literal; ARGUS owns the second look.
2. **SPLIT per-line enumeration completeness (r2 closure).** §3.8 enumerates every cross-ref line in the 4 subsections with a LIVE/PROVENANCE call. Does ARGUS see a line I mis-classed — particularly the §19.7 line-1295 intra-line split (stoa--86k PROVENANCE / §17.5+§18.5 LIVE) and the §16.7 "sources" cluster (1037–1040) which I classed PROVENANCE because they are source-of-truth-for-content cites, not operational pointers?
3. **Check D per-role-file scoping (weak point §7.4).** Is scoping recompose to `$DEST_POLYBIUS`-only for this arc (PLINY untouched) the right call, or should the spec mandate the data-driven both-files loop NOW with Check D evaluated per-file-markers so the PLINY cut is zero-install.sh-edit (r5 generality)? I scoped to POLYBIUS-only to keep this arc's install.sh blast radius minimal; ARGUS may prefer the forward-compatible loop landed now.

---

## §9 — Out of scope

- **Cutting the other 3 role files** (operating-disciplines.md ~2138, MAJOR_PLINY.md 801, CAPTAIN_DAEDALUS.md 633). Per stoa--xyb.6: "After POLYBIUS proves the method, repeat for..." — those are subsequent arcs. (The §6.5 recompose is designed data-driven so the MAJOR_PLINY cut reuses it — but that cut is a separate arc.)
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/` (lags source by Arc 44 + this arc). User-tier POLYBIUS housekeeping per §18.1; explicitly batched out by user-tier POLYBIUS (stoa--xyb 2026-05-23T06:50:01Z).
- **Re-syncing the user-tier deployed `~/.claude/MAJOR_POLYBIUS.md`** (AHEAD by the §5.6 fold). The fold's content is mirrored INTO source this arc (LEAN, per r4); the deployed copy's re-sync is housekeeping.
- **Building the enforcement layer** (stoa--xyb.5 — sub-agent task-bounding hook). The routing-map/relocation-index + the `MODULE-INLINE` marker formats are designed to be hook-parseable (Arc 1 + this arc), but the hook is not built here.
- **A bw attachment-read primitive.** C-2 here uses `bw create --parent -d` (a titled child ticket description), not `bw attach` (file) — so the bw-0.13.0 no-attachment-read limitation (modules/README.md §5.2 recovery note) does not bite this arc; recovery is a plain `bw show <child-id>`.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8. This rev2 supersedes design-rev1.md; the next ARGUS/ADA read THIS file alone.*
