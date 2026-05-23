# Arc 2 (Arc 45) — MAJOR_POLYBIUS.md debloat cut — design rev1

**Ticket:** stoa--xyb.6 (engagement epic stoa--xyb)
**Author:** Denson Smith (the PRINCIPAL — design synthesis, structural choices, relocation ledger)
**Seat:** CAPTAIN_DAEDALUS_the-stoa
**Builds on:** Arc 44 (c0b5610) — composition-layer mechanism (`substrate/modules/` glob deploy; `modules/README.md` 3 channels + 3 relocation classes; op-disc §33 thin rule).
**Acceptance bar:** LOSSLESS-ON-CANON at ALL tiers (user / project / subproject). ARGUS's primary audit target is LOST CANON.

---

## §1 — Problem restatement (pre-work gate)

`substrate/MAJOR_POLYBIUS.md` is 1299 lines and now a load-bearing problem: it cost ~52k tokens to read against a 25k harness cap (user-tier POLYBIUS had to paginate its own role file, per stoa--0hl 2026-05-23T01:26:38Z). The diagnosis is empirical-anchor + provenance accretion: every discipline carries a ticket cite + worked example + multi-paragraph provenance, so the *actionable* canon is roughly a third of the lines and the rest is the why/empirical record.

This arc applies the Arc-1 debloat method (the 3 relocation classes — CONDITIONAL → disk module, PROVENANCE → bw cite, DUPLICATE → pointer) to MAJOR_POLYBIUS.md section by section. The composition + enforcement layers shipped in Arc 44 are the safety net that makes the cut safe: relocated content has a lossless home and a slim-core cite-back so nothing is lost, only moved.

The cut must hold LOSSLESS-ON-CANON at **all tiers including subproject** — a slimmed subproject `MAJOR_POLYBIUS_<slug>.md` that points at modules absent from the subproject's `.claude/modules/` would break losslessness at that tier. The subproject module-access strategy is a design-phase requirement (probed live in §6 below).

This arc ALSO folds stoa--0hl (the §5.6 say-trigger team-deploy procedure + §4.5 two-mechanism reconciliation) into the cut — written LEAN from the start, not mirrored verbose. The 0hl fold is kept a SEPARABLE slice (own ledger rows, own build step) so ARGUS can audit LOSSLESS-ON-CANON on the cut independently of the 0hl addition.

### Imported assumptions (named per §6.1)

1. **op-disc §12 is the canonical bw-cookbook home** for the DUPLICATE class. Confirmed live: §12 self-declares "Role files reference this section; do not duplicate." (op-disc:729). The §7.3 dupe deletes to a pointer at §12.
2. **CONDITIONAL content relocates to the 5 NAMED Arc-2 modules** (modules/README.md §6). This arc CREATES + POPULATES those 5 files (Arc 1 only named them).
3. **The cut is to SOURCE** (`substrate/MAJOR_POLYBIUS.md`). The deployed user-tier copy (`~/.claude/MAJOR_POLYBIUS.md`, 1300 lines, AHEAD by the §5.6 fold) is the verbatim reference for the 0hl text but is NOT the cut target. Substrate-self-apply re-sync is user-tier POLYBIUS housekeeping, out of this arc's scope.
4. **Subagents inherit parent-session cwd; no per-subagent cwd override exists** (web-confirmed, §6). This is the load-bearing fact for the subproject strategy.
5. **The 0hl fold writes §5.6 LEAN.** The verbose user-tier reference text (~17 lines body + ~4 §4.5 lines) is the *source of truth for content*, not for length. The lean form keeps the rule + the 1-line empirical cite + the say-vs-paste contrast; the verbose worked-procedure prose is what gets compressed.

---

## §2 — Approach (the slim structure)

### 2.1 The slim core shape

Post-cut, MAJOR_POLYBIUS.md is the **slim operational core**: crisp rule per discipline + a one-line cite-back (routing-map row for CONDITIONAL, `Anchor:` for PROVENANCE, pointer for DUPLICATE) + the two always-loaded index tables (routing map + relocation index per Refinement 1). The 5 CONDITIONAL procedures move to disk modules; the provenance/empirical multi-paragraph blocks move to bw cites; the bw-cookbook dupe deletes to a pointer.

### 2.2 The two always-loaded index tables (Refinement 1 — index stays in core, NEVER a module)

Per modules/README.md §4, POLYBIUS's slim core carries both tables inline, always-loaded. They are added as a new **§3.5 "Composition layer — routing map + relocation index"** placed immediately after §3 (so the always-loaded indexes sit at the top of the operational core, before the disciplines that reference them). Tables are populated in §3 of THIS design.

### 2.3 The 5 CONDITIONAL module files (CREATED + POPULATED this arc)

| Module file | Source § (live line range) | What moves in |
|---|---|---|
| `substrate/modules/onboarding.md` | §5 Onboarding flow (159–376) **minus** §5.6 (the 0hl fold — see §2.4) | The 9-step onboarding procedure (§5 intro + code block), §5.1 string-substitution + slots, §5.1.1 / §5.1.1.1 positive-references discipline, §5.1.2 pre-branch-hygiene preamble, §5.1.3 cron-hygiene preamble, §5.2 install.sh-template, §5.3 consent moments, §5.4 external-directive-review, §5.5 activation-paste-filenames cheatsheet |
| `substrate/modules/sub-project-spawning.md` | §10 Sub-project spawning (538–635) | §10 intro + §10.1 trigger recognition + §10.2 walk-through (code block) + §10.3 asymmetric bw visibility + §10.4 the hand-off |
| `substrate/modules/pair-programmer-authoring.md` | §11 Pair-programmer Major authoring (638–726) | §11 intro + §11.1 trigger recognition + §11.2 walk-through + §11.3 empirical lineage + §11.4 asymmetric bw visibility |
| `substrate/modules/pair-programming-prototyping.md` | §12 Pair-programming-for-prototyping (Mode 2) (729–803) | §12 intro + §12.1 two-mode framing + §12.2 7-step cycle + §12.3 when-to-use + §12.4 empirical claim |
| `substrate/modules/substrate-update-check.md` | §14 Substrate-update check (885–895) | §14 full body (check mechanism, check.sh/apply.sh/revert.sh, .substrate-last-check semantics) |

Each module is a self-contained reference body; the module's first line restates which POLYBIUS § it relocated and cites this design + the epic (provenance header convention, mirroring modules/README.md:14-16).

### 2.4 The 0hl fold (SEPARABLE slice)

stoa--0hl folds in TWO edits, both written LEAN:

- **0hl Edit 1 — §4.5 two-mechanism reconciliation.** §4.5 stays inline in the slim core (it is a KEEP-TIGHTEN section). Append a LEAN 2-sentence paragraph: the on-disk-`.md` one-liner is the *paste-trigger* mechanism (fresh installs); for *already-deployed say-trigger* workspaces the durable artifact is a **bw ticket** and activation is the bare word `polybius`/`pliny` (full procedure → onboarding module §5.6). Invariant in both: durable instruction, short relay. 1-line empirical cite (2026-05-21 railway, Anchor: stoa--0hl).
- **0hl Edit 2 — §5.6 say-trigger team-deploy procedure.** §5.6 is CONDITIONAL content (an onboarding-class procedure), so it relocates INTO `onboarding.md` as a `## §5.6` section, written LEAN: the 4-step procedure (store instruction in bw ticket; optionally commit supporting `.md` to beadwork branch via worktree; human activates bare word; team self-discovers via §9 sweep) + the say-vs-paste contrast + 1-line empirical cite. The slim core keeps the §5 routing-map row only (no §5.6 inline prose in core).

**Why separable:** the 0hl fold is the ONLY net-ADD in an otherwise net-SUBTRACT arc. ARGUS audits LOSSLESS-ON-CANON on the cut (everything that existed at 1299 lines must have a home) independently of whether the 0hl ADD is well-formed. Ledger rows F1/F2 (§3.2) tag the fold distinctly; build Step 6 (§5) lands it as a distinct commit.

### 2.5 KEEP-TIGHTEN sections (stay inline; prose tightened; no relocation)

§1 (Who you serve), §2 (What you do), §3 (What you don't do — incl. the §3 "What you DO do" attention-map block), §6 (Compact-or-clear recovery), §8 (Voice discipline), §9 (Activation checklist). These are the always-needed operational core. Tighten verbose prose (e.g. the §3 attention-map block at 49–59 is 3 dense paragraphs reducible to a tight rule + cross-ref); no content relocates.

### 2.6 PROVENANCE relocations (C-1 / C-2 disposition per §3.3)

The "N=1 provenance + accretion path" + "Cross-references" subsections at the tail of §4 disciplines and §16/§17/§18/§19 relocate to bw cites. The slim core keeps the RULE + a one-line `Anchor: <bw-id>` cite-back. C-1 (already-in-bw) vs C-2 (not-in-bw) call is per-row in §3.3.

### 2.7 §-numbering coherence after the cut

The slim core RENUMBERS to close the gaps left by relocated whole-sections (§5, §10, §11, §12, §14 leave the core). Cross-refs within the file and from sibling substrate files (op-disc, MAJOR_PLINY, CAPTAIN envelopes) that point at MAJOR_POLYBIUS §N MUST be re-pointed. **This is a named weak point (§7).** The build step (§5 Step 5) includes a mandatory cross-ref re-point sweep with a grep-based proof. To keep the blast radius small and the proof tractable, the design specifies **section numbers are PRESERVED, not renumbered** — relocated whole-sections leave a 2-line stub at their original number (heading + routing-map pointer), so §6 stays §6, §16 stays §16, and every existing cross-ref (`§5`, `§10`, `§11`, `§12`, `§14`, and all the §16.x/§17.x/etc.) still resolves to a real anchor in the slim core. This trades ~10 stub lines for zero cross-ref churn across the substrate — a strongly net-positive trade given the substrate has dozens of `MAJOR_POLYBIUS.md §N` cross-refs in op-disc, MAJOR_PLINY, and the CAPTAIN envelopes.

**Stub shape (CONDITIONAL relocations):**
```
## 5. Onboarding flow
Relocated to `.claude/modules/onboarding.md` (CONDITIONAL — loaded at dispatch).
Routing-map + relocation-index rows in §3.5. Recover the full procedure via `Read .claude/modules/onboarding.md`.
```

---

## §3 — The relocation ledger (the losslessness proof artifact)

This ledger is the artifact ARGUS audits for LOST CANON. **One row per relocated chunk.** Every empirical anchor in the 1299-line source must appear as a ledger row with a lossless home, OR be a KEEP-TIGHTEN section that stays inline. Line ranges are grounded against the LIVE `substrate/MAJOR_POLYBIUS.md` (re-read this session), not the .6 section-map estimates.

### 3.1 CONDITIONAL relocations (→ disk module; slim-core residue = routing-map row + stub)

| Source (§ + live lines) | Class | New home | Slim-core residue (the 1-line rule/cite that stays) |
|---|---|---|---|
| §5 Onboarding flow + §5.1–§5.5 (159–379, excl §5.6) | CONDITIONAL | `modules/onboarding.md` | §5 stub heading + routing-map row `onboard new project → onboarding.md → disk` |
| §10 Sub-project spawning + §10.1–§10.4 (538–635) | CONDITIONAL | `modules/sub-project-spawning.md` | §10 stub + routing-map row `spawn sub-project → sub-project-spawning.md → disk` |
| §11 Pair-programmer Major authoring + §11.1–§11.4 (638–726) | CONDITIONAL | `modules/pair-programmer-authoring.md` | §11 stub + routing-map row `author pair-programmer → pair-programmer-authoring.md → disk` |
| §12 Pair-programming-for-prototyping + §12.1–§12.4 (729–803) | CONDITIONAL | `modules/pair-programming-prototyping.md` | §12 stub + routing-map row `prototype (Mode 2) → pair-programming-prototyping.md → disk` |
| §14 Substrate-update check (885–895) | CONDITIONAL | `modules/substrate-update-check.md` | §14 stub + routing-map row `substrate-drift check → substrate-update-check.md → disk` |

**Note on §13 (Operating engagement HITL/Autonomous, 806–881):** the .6 section map tagged 5/10/11/12/14 → reference. §13 was NOT in that list. §13 is a KEEP-TIGHTEN section (it carries the universal escalation triggers at 826–836, which are load-bearing operational core read every autonomous engagement — relocating them off-disk would degrade losslessness-of-availability). §13 stays inline, tightened. **This is a deliberate divergence from a naive reading of "all conditional → module"; flagged for ARGUS in §8.**

### 3.2 The 0hl fold rows (SEPARABLE slice — net-ADD, audit independently)

| Source | Class | New home | Slim-core residue |
|---|---|---|---|
| **F1** — 0hl Edit 1 (§4.5 two-mechanism reconciliation) | KEEP (lean ADD inline) | §4.5 (stays inline) | LEAN 2-sentence paragraph + `Anchor: stoa--0hl` (2026-05-21 railway empirical) |
| **F2** — 0hl Edit 2 (§5.6 say-trigger team-deploy) | CONDITIONAL (lean ADD) | `modules/onboarding.md` §5.6 | §5 stub already covers it (no separate core residue beyond the §5 routing-map row) |

### 3.3 PROVENANCE relocations (→ bw cite; slim-core residue = rule + `Anchor:`)

| Source (§ + live lines) | bw id(s) cited | C-1 / C-2 call | Slim-core residue |
|---|---|---|---|
| §4.3.1 PRINCIPAL-intent probe empirical (89–105: the 2026-05-13 four-option anchor at 103 + cross-refs at 105) | `stoa--ezj` | **C-1** (resolves live) | Keep the rule + 3-step probe; `Anchor: stoa--ezj`. Cross-ref line (105) kept as live pointer. |
| §5.1.1 empirical (244) | 2026-05-04 (in-prose, no ticket) | **C-2** → archive first | Moves WITH §5 into onboarding.md (it's onboarding CONDITIONAL); the empirical 1-liner stays in the module. NO bw cite needed because it relocates with its parent CONDITIONAL block, not as standalone provenance. |
| §5.1.1.1 cross-project-leak provenance block (264 — N=2 2026-05-17 ariadne) | in-prose N=2, no single ticket | **C-2** → see §3.4 | Moves WITH §5 into onboarding.md (CONDITIONAL). Verbose provenance paragraph (264) compresses to a 1-line empirical cite in the module. |
| §5.1.2 cross-refs + empirical (297–302) | `stoa--3cs` | **C-1** | Moves with §5 into onboarding.md; keep `Anchor: stoa--3cs`. |
| §5.1.3 provenance block (333 — multi-instance ad-hoc, N=0 canon) | no clean ticket (lists HUMAN_paste-* filenames) | **C-2** → see §3.4 | Moves with §5 into onboarding.md; verbose provenance (333) compresses to 1-line empirical cite in module. |
| §15 retrospective discipline empirical (914) | `stoa--nax`, `ariadne--8fd` | **C-1** | §15 is KEEP-TIGHTEN (stays inline core); compress the empirical paragraph to rule + `Anchor: stoa--nax`. |
| §16.1 source-of-truth declarations (922–930) | `stoa--32b.3` | **C-1** | Keep the rule; `Anchor: stoa--32b.3`. The two verbatim PRINCIPAL quotes (927, 929) move to the cite (already verbatim in stoa--32b.3 body — content-check gate). |
| §16.6 N=1 provenance + accretion (1022–1031) | `stoa--32b.3`, `stoa--32b`, `stoa--p5g`, `stoa--dxw` | **C-1** | Delete verbose block; `Anchor: stoa--32b.3 — N=1 provenance + accretion. Recover via bw show.` |
| §16.7 Cross-references (1034–1050) | mixed (bw ids + in-file §refs + sibling-file §refs) | **SPLIT** | bw-id provenance cross-refs → relocation-index/Anchor; in-file + sibling-file §refs are LIVE cross-refs — keep per modules/README.md §5.2 ("keep the existing in-file pointer convention"). Compress 17 lines → ~4 live cross-ref lines + 1 Anchor line. |
| §17.1 source-of-truth declaration (1096–1102) | `stoa--ads` | **C-1** | Keep rule; `Anchor: stoa--ads`. Verbatim quote (1100) → cite (content-check). |
| §17.5 N=1 provenance + accretion (1145–1155) | `stoa--ads` | **C-1** | Delete verbose block; `Anchor: stoa--ads`. |
| §17.6 Cross-references (1157–1164) | mixed | **SPLIT** (same as §16.7) | Live §refs kept; provenance → Anchor. |
| §18.5 N=1 provenance + accretion (1206–1215) | `stoa--k36` | **C-1** | Delete verbose block; `Anchor: stoa--k36`. |
| §18.6 Cross-references (1217–1225) | mixed | **SPLIT** | Live §refs kept; provenance → Anchor. |
| §19.6 N=1 provenance + accretion (1273–1282) | `stoa--86k` | **C-1** | Delete verbose block; `Anchor: stoa--86k`. |
| §19.7 Cross-references (1284–1295) | mixed | **SPLIT** | Live §refs kept; provenance → Anchor. |

**The C-1 content-check gate (REQUIRED per modules/README.md §5.2, carried into the build).** Before ADA deletes ANY C-1 inline provenance prose, ADA MUST run `bw show <cited-id>` and content-check that the cited ticket actually carries the full story the inline prose holds. This is a per-deletion gate — it turns each C-1 classification into a checkable losslessness proof. The design pre-verified all C-1 ticket ids RESOLVE (stoa--32b, stoa--32b.3, stoa--ads, stoa--k36, stoa--86k, stoa--ezj, stoa--3cs all EXIST live); the *content-match* check is ADA's per-deletion responsibility (resolution ≠ content-completeness). VERA re-executes a sample of these `bw show` checks as a verification probe (§4).

### 3.4 C-2 archive-first cases (the losslessness RISK points — flagged)

Two provenance blocks have NO clean single bw home. Per modules/README.md §5.2 C-2: **archive to bw FIRST, then delete inline + keep cite.**

- **§5.1.1.1 cross-project-leak provenance (264).** N=2 in-prose (2026-05-17 ariadne PLINY pastes). The DISCIPLINE moves with §5 into onboarding.md (CONDITIONAL); but the verbose 2-paragraph provenance (the N=2 worked anti-pattern/positive-pattern examples + the §6.7.1 future-accretion note) is what compresses. **C-2 disposition:** archive the verbose provenance prose to a bw comment on `stoa--xyb.6` (this arc's ticket) via `bw comment stoa--xyb.6 "<prose>"` BEFORE deleting, then the module keeps a 1-line empirical cite (`Anchor: stoa--xyb.6 — 2026-05-17 N=2 cross-project-leak provenance`). The DISCIPLINE itself (positive-references-only, the worked-example TABLE) is operational and stays in the module — only the multi-paragraph *why-N=2-and-future-accretion* prose archives.
- **§5.1.3 cron-hygiene provenance (333).** Multi-instance ad-hoc, N=0 canon. Same C-2 disposition: archive the verbose provenance paragraph (333 — the HUMAN_paste filename list + N=0 framing) to a `bw comment stoa--xyb.6` before deleting; module keeps the cron-hygiene preamble (operational, stays) + a 1-line cite.

**Why stoa--xyb.6 as the C-2 archive home:** it is THIS arc's ticket; the archive comment is discoverable via the same `bw show stoa--xyb.6` an auditor already reads. (modules/README.md §5.2 explicitly sanctions `bw comment <ticket-id> "<prose>"` for short prose rather than a file.)

### 3.5 DUPLICATE relocations (→ pointer; slim-core residue = 1-line pointer)

| Source (§ + live lines) | Class | Keep-home | Slim-core residue |
|---|---|---|---|
| §7.3 Working with beadwork — command syntax (423–453) | DUPLICATE | `operating-disciplines.md` §12 (confirmed canonical: §12 self-declares "do not duplicate", op-disc:729) | Delete the verbose cookbook (the `-m` table, the per-command table); keep a 1-line pointer: "bw command syntax → `operating-disciplines.md` §12 (canonical cookbook)." + the POLYBIUS-seat-specific framing (the `bw prime` at session start note + TIRO delegation note at 453) which is NOT duplicated content. Relocation-index row. |

**Scope note for §7.3:** §7.3 mixes DUPLICATE (the syntax cookbook, fully present at op-disc §12) with POLYBIUS-SPECIFIC framing (run `bw prime` at session start; TIRO specialist-delegation). The DUPLICATE *syntax* deletes to a pointer; the POLYBIUS-specific framing STAYS (it is not duplicated at §12 — §12 is universal-seat, §7.3's prime+TIRO notes are POLYBIUS-seat application). This is the modules/README.md §5.3 worked example exactly.

### 3.6 KEEP-TIGHTEN (stays inline; no ledger relocation — listed for completeness/audit)

§1 (15–23), §2 (27–39), §3 (41–59), §4 intro + §4.1–§4.8 disciplines [rules stay; provenance tail compresses per §3.3], §4.5 [+ 0hl F1], §6 (379–389), §7 [intro + §7.1/§7.2/§7.4/§7.5/§7.6 stay; §7.3 dupe relocates per §3.5], §8 (503–509), §9 (513–534), §13 (806–881, see §3.1 note), §15 (899–914), §16 intro + §16.2/§16.3/§16.4/§16.5/§16.8 [rules stay; §16.1/§16.6/§16.7 provenance compresses per §3.3], §17 intro + §17.2/§17.3/§17.4 [rules stay; §17.1/§17.5/§17.6 compress], §18 intro + §18.1/§18.2/§18.3/§18.4 [rules stay; §18.5/§18.6 compress], §19 intro + §19.1/§19.2/§19.3/§19.4/§19.5 [rules stay; §19.6/§19.7 compress].

### 3.7 Ledger summary (chunk counts per class)

- **CONDITIONAL:** 5 whole-section relocations (§5, §10, §11, §12, §14) → 5 new module files. + 1 fold-in (§5.6 → onboarding.md). = **6 CONDITIONAL chunks.**
- **PROVENANCE:** 9 C-1 (resolve live; ADA content-checks per-deletion) + 2 C-2 (archive-first to stoa--xyb.6) + 5 SPLIT cross-ref subsections (live §refs kept, provenance → Anchor) = **16 PROVENANCE chunks.**
- **DUPLICATE:** 1 (§7.3 cookbook → op-disc §12 pointer) = **1 DUPLICATE chunk.**
- **KEEP-TIGHTEN:** ~13 sections stay inline (prose tightened).
- **0hl fold:** 2 rows (F1 inline-lean, F2 → onboarding.md §5.6), audited as a separable slice.

---

## §4 — Verification probes (what would falsify the design's intended behavior)

Concrete probes VERA re-executes. The probe spec is load-bearing.

### P1 — Line-count target met (the cut actually cut)
```bash
wc -l substrate/MAJOR_POLYBIUS.md
```
**Pass:** core is in the **300–350 line** target band (down from 1299). **Falsifies if:** > 400 (cut too shallow) or < 250 (suspiciously aggressive — check for dropped rules). Also run op-disc §33's line-count discipline against each new module (no module is itself a re-bloat monolith).

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
grep -n '^## 12. bw cookbook' substrate/operating-disciplines.md       # the home exists
```
**Pass:** §7.3 carries a pointer to op-disc §12 AND op-disc §12 exists. **Falsifies if:** pointer present but §12 home gone, or the verbose cookbook still inline at §7.3 (dupe not actually deleted).

### P5 — C-1 content-check gate was honored (LOST-CANON proof — sampled)
For a sample of C-1 deletions (at minimum §16.6/stoa--32b.3, §17.5/stoa--ads, §18.5/stoa--k36, §19.6/stoa--86k):
```bash
for id in stoa--32b.3 stoa--ads stoa--k36 stoa--86k; do echo "=== $id ==="; bw show "$id" 2>&1 | head -40; done
```
**Pass:** each cited ticket's body materially carries the N=1 story the deleted inline prose held (the date, the PRINCIPAL declaration, the accretion framing). **Falsifies if:** any cited ticket is a thin stub that does NOT carry the deleted detail → that deletion dropped canon, classification was wrong (should have been C-2).

### P6 — C-2 archive-first executed BEFORE deletion (losslessness ordering)
```bash
bw show stoa--xyb.6 2>&1 | grep -iE 'cross-project-leak|cron-hygiene|5.1.1.1|5.1.3'
```
**Pass:** stoa--xyb.6 carries the archived verbose provenance for §5.1.1.1 + §5.1.3 as comments. **Falsifies if:** the verbose provenance is gone from the source AND not present in stoa--xyb.6 (LOST CANON — the C-2 archive step was skipped).

### P7 — Subproject-tier losslessness (THE BAR — see §6)
```bash
grep -nE 'modules/(onboarding|sub-project-spawning|pair-programmer-authoring|pair-programming-prototyping|substrate-update-check)\.md' substrate/MAJOR_POLYBIUS.md
```
Then confirm the subproject-tier strategy clause is present in the slim core (the rule that subproject orchestrators use CHANNEL 1/3, not CHANNEL 2 disk-module Read).
**Pass:** the slim core carries a §3.5 (or stub) clause stating that at subproject tier the CONDITIONAL content is delivered inline/bw (not via `Read .claude/modules/`), grounded in the §6 probe. **Falsifies if:** the slim core unconditionally instructs `Read .claude/modules/<X>.md` with no subproject-tier carve-out → breaks losslessness at subproject tier.

### P8 — 0hl fold landed lean + separable
```bash
git log --oneline arc-45/build | head    # F1/F2 land as a distinct commit
grep -n '5.6' substrate/modules/onboarding.md   # §5.6 say-trigger in the module
grep -n 'say-trigger\|paste-trigger' substrate/MAJOR_POLYBIUS.md   # §4.5 reconciliation lean
```
**Pass:** §5.6 present in onboarding.md (lean); §4.5 carries the 2-mechanism reconciliation; the fold is a separable commit. **Falsifies if:** §5.6 mirrored verbose (> ~25 lines) or the §4.5 reconciliation absent.

### P9 — No author-field regression (CLAUDE.md authorship discipline)
```bash
grep -niE '^(author|owner|creator|by|copyright|maintainer):' substrate/MAJOR_POLYBIUS.md substrate/modules/*.md
```
**Pass:** no author-like field names anyone other than Denson Smith (role files carry none; modules carry none). **Falsifies if:** any new module's provenance header introduces an author field with the wrong name.

---

## §5 — Build steps (for ADA — ordered; the cut sequence)

1. **Create the 5 module files** (`substrate/modules/*.md`), populating from the live source line-ranges in §3.1. Each module: provenance header (cites this design + stoa--xyb epic) → relocated content verbatim-tightened. Run op-disc §33 line-count discipline per module.
2. **Fold 0hl Edit 2 into onboarding.md** as a LEAN `## §5.6` (separable; per §2.4 / §3.2 F2).
3. **Execute C-2 archive-first** (§3.4): `bw comment stoa--xyb.6 "<verbose §5.1.1.1 provenance>"` and `bw comment stoa--xyb.6 "<verbose §5.1.3 provenance>"` BEFORE touching the source. (Losslessness ordering — bytes in bw before inline removal.)
4. **Cut the slim core** (`substrate/MAJOR_POLYBIUS.md`): for each CONDITIONAL section, replace body with the 2-line stub (§2.7 shape); for each PROVENANCE row run the C-1 `bw show` content-check (§3.3 gate) THEN delete-to-Anchor; delete §7.3 dupe to op-disc §12 pointer; tighten KEEP-TIGHTEN prose; add §3.5 (routing map + relocation index + subproject-tier clause). Fold 0hl Edit 1 lean into §4.5.
5. **Cross-ref re-point sweep** (named weak point §7): because section numbers are PRESERVED (§2.7), the sweep is a VERIFICATION not a churn — grep the substrate for `MAJOR_POLYBIUS.md §N` cross-refs and confirm each target still resolves to a real anchor (stub or live). Prove with: `grep -rn 'MAJOR_POLYBIUS' substrate/ | grep -oE '§[0-9.]+'` cross-checked against the slim core's headings.
6. **Commit the 0hl fold as a distinct commit** (F1+F2) so ARGUS audits it separably. Co-Authored-By trailer per §28.
7. **Run all probes P1–P9** as a self-check before returning to PLINY.

---

## §6 — Subproject-tier module-access strategy (PEER-MANDATED design-phase gate)

### 6.1 The probe (RUN live this design phase)

**Question:** does a subproject orchestrator's (`MAJOR_PLINY_<slug>` running for a subproject) dispatched CAPTAIN resolve `Read .claude/modules/<X>.md` to the PARENT workspace's `.claude/modules/`, or fail?

**Web-check (current behavior, May 2026):**
- Subagents inherit the **parent-session cwd**; there is **no per-subagent cwd override** (claude-code #31940 AgentDefinition lacks cwd/additionalDirectories; #12748 feature-request for Task-tool cwd still open).
- Subagent relative-path resolution is **fragile and contested**: #4754 (relative paths from CLAUDE.md resolve against cwd, not config dir), #31546 (subagents resolve to main repo root not worktree), #56686 (sub-agents DENIED Read on paths outside project root despite explicit allow rules), #15627 (path display relative to cwd not project root).

**Live filesystem probe (this design phase, against the REAL deployed subproject `ariadne-core-workspace/ariadne-core/`):**
1. The deployed subproject `.claude/` is a **fully self-contained substrate copy**: own `MAJOR_POLYBIUS_ariadne_core.md`, own `MAJOR_PLINY_ariadne_core.md`, own `operating-disciplines.md`, own `agents/`, own `skills/`. It does NOT read role files from the parent.
2. Neither the subproject's `.claude/` NOR the parent workspace's `.claude/` has a `modules/` directory (that deployment predates Arc 44; install.sh sets `DEST_MODULES_DIR=""` in subproject mode — deploy skipped, confirmed live at install.sh:624).
3. The §10.2 spawn convention launches the subproject orchestrator by **opening a new terminal in `<parent>/<slug>/`** — so the launch cwd IS the subproject root. A dispatched CAPTAIN inheriting that cwd resolves `Read .claude/modules/<X>.md` → `<parent>/<slug>/.claude/modules/<X>.md`, which **does not exist** (install.sh skips it). Simulated under both launch-cwd scenarios: subproject-root cwd → MISS; parent-root cwd → would hit parent modules but (a) parent may have no modules either in a real subproject-of-deployed-project and (b) relative-path resolution outside project root is web-confirmed-denied (#56686).

**Probe result:** CHANNEL 2 (disk-module via relative `Read .claude/modules/<X>.md`) is **NOT reliable at subproject tier.** The subproject either has no modules dir (the common case — install.sh skips it) or, even if cwd resolved upward, hits the #56686 outside-project-root denial. This matches the Arc-1 TRACKED gating question (modules/README.md §7) and resolves it: the answer is "Read does NOT reliably resolve parent modules from a subproject orchestrator."

### 6.2 The chosen strategy: **2b — KEEP CONDITIONAL content INLINE at subproject tier**

Given the probe, the brief offered: (a) extend modules glob deploy to subproject tier, OR (b) keep relocated CONDITIONAL content inline at subproject tier. **Strategy 2b is chosen.** Rationale:

- **2a (extend deploy) does not fix the resolution problem.** Even if install.sh deployed `<parent>/<slug>/.claude/modules/`, the dispatched CAPTAIN's `Read .claude/modules/<X>.md` STILL depends on the fragile/contested relative-path resolution (#56686 denial outside project root; #31546 worktree mis-resolution). Deploying the files does not guarantee the Read resolves. 2a adds deploy surface AND a still-unreliable Read — strictly worse than 2b.
- **2b is the only strategy that holds LOSSLESS-ON-CANON at subproject tier deterministically.** If the CONDITIONAL content is INLINE in the subproject's `MAJOR_POLYBIUS_<slug>.md`, no Read resolution is needed — the content is present in the role file the subproject already self-contains.

**Mechanism for 2b (the tier-aware cut):** the cut is **TIER-AWARE in install.sh**, not in the source file. The SOURCE `substrate/MAJOR_POLYBIUS.md` is the slim core (stubs + routing-map). At deploy time:
- **user / project tiers:** install.sh deploys the slim core AS-IS + deploys `.claude/modules/` (already does, Arc 44). The slim core's routing-map points at modules; CHANNEL 2 works (Read resolves at user/project tier — Arc 1 verified this end-to-end).
- **subproject tier:** install.sh deploys a **RECOMPOSED** `MAJOR_POLYBIUS_<slug>.md` = slim core with the 5 module bodies **re-inlined** at their stubs. The subproject role file is self-contained (matching the existing self-contained-subproject pattern probed live). No modules dir deployed (unchanged).

**This is a Step in install.sh (CONDITIONAL on subproject mode).** It is an `install.sh` change — which is substrate-tooling source (gauntlet-gated per §18.2), correctly inside this arc. The recompose is mechanical: `cat`-concatenate the 5 module bodies into the role file at their stub markers during subproject deploy. **This is a named weak point (§7) — install.sh recompose adds deploy-time complexity and is a new test surface; VERA verifies it on a throwaway subproject target (mirroring Arc 1's throwaway-target verification).**

### 6.3 The slim-core clause that makes the strategy auditable

The slim core's §3.5 carries a one-line tier-awareness rule (so the strategy is visible to a reader, not buried in install.sh):

> **Subproject-tier module access (per design-arc-45 §6):** at subproject tier the CONDITIONAL module content is re-inlined into this role file at deploy time (install.sh recompose) — subproject orchestrators do NOT `Read .claude/modules/<X>.md` (the path does not resolve reliably at subproject tier; claude-code #56686/#31546). At user/project tier the routing-map's `disk (Read)` channel applies. Anchor: stoa--xyb (Arc-1 tracked gating question §7) + design-arc-45 §6 probe.

**Why a clause and not silence:** ARGUS audits subproject-tier losslessness explicitly (brief). A reader at subproject tier seeing a routing-map row that says `Read onboarding.md → disk` would be misled if the content is actually inlined. The clause closes that gap.

### 6.4 Alternative considered + rejected: leave subproject unslimmed

Rejected: deploy the FULL (pre-cut, 1299-line) role file at subproject tier and the slim core only at user/project. This holds losslessness but (a) forks the source (two role-file bodies to maintain — exactly the duplication the debloat epic fights) and (b) the subproject tier is precisely where the 25k-cap pagination pain bites (the live ariadne-core subproject role file is 64KB). The recompose-at-deploy approach (2b) keeps ONE source (slim core + modules) and recomposes mechanically — single source of truth, no fork. The line-count pain at subproject tier is unavoidable IF losslessness is the bar (the content must be present somewhere readable); recompose puts it in the role file where it reads without a Read hop, same as today's self-contained subproject pattern.

---

## §7 — Self-assessed weak points

1. **The install.sh subproject recompose is a new deploy-time mechanism (highest-risk).** Strategy 2b requires install.sh to `cat`-concatenate 5 module bodies into the subproject role file at their stub markers — a new code path, a new test surface, and a place where a stub-marker mismatch silently drops a module body at subproject tier (the exact LOST-CANON failure at the exact tier ARGUS audits hardest). *Why this shape anyway:* it is the only strategy that holds losslessness deterministically at subproject tier without forking the source; the alternative (fork the full role file) re-introduces the duplication the epic exists to kill. Mitigation in the design: VERA verifies recompose on a throwaway subproject target (P7 + a dedicated recompose probe), and the §6.3 slim-core clause makes the mechanism auditable rather than implicit.
2. **The two C-2 cases (§5.1.1.1, §5.1.3) archive to a bw COMMENT, which is weaker provenance than a dedicated ticket.** A comment on stoa--xyb.6 is discoverable via `bw show stoa--xyb.6` but is co-mingled with the arc's other comments; a future auditor must scan the comment stream rather than hit a titled ticket. *Why this shape anyway:* modules/README.md §5.2 explicitly sanctions `bw comment <id> "<prose>"` for short C-2 prose; both blocks are 1–2 paragraphs (short), and minting a dedicated ticket per provenance fragment over-weights record-keeping. The build ordering (archive BEFORE delete, P6) guarantees the bytes survive; the weakness is discoverability, not loss.
3. **§13 and §16/§17/§18/§19 are KEEP-TIGHTEN, not relocate — the cut may under-deliver the line target if "tighten" is timid.** The biggest line-savings come from the 5 CONDITIONAL relocations (~600 lines move to modules) + the provenance compressions (~250 lines → ~30 Anchor lines). But §16–§19 are dense (each ~70–110 lines) and stay inline as rules; if ADA tightens them conservatively, the core could land at 380–420 rather than 300–350. *Why this shape anyway:* §16–§19 rules ARE operational core (lifecycle, base-vs-custom, two-team routing) read across sessions; relocating them off-disk would degrade availability-losslessness. The honest scoping: the 300–350 estimate assumes aggressive provenance compression + tight rule prose; P1 falsifies at >400, and a 360–400 landing is a partial-not-failure (the cut still ~3x's the file). Flagged so ARGUS can weigh whether §16–§19 rule-prose warrants its own future relocation arc rather than being forced under target here.

---

## §8 — Residual questions for ARGUS (explicit)

1. **§13 KEEP vs RELOCATE.** The .6 section map tagged 5/10/11/12/14 → reference; §13 (operating engagement HITL/Autonomous) was NOT tagged but is large (76 lines). I KEEP it inline (the universal escalation triggers at 826–836 are load-bearing operational core). Does ARGUS concur, or should §13.1's triggers stay inline while §13.2/§13.3/§13.4 (the mode-transition mechanics) relocate to a `mode-transitions.md` module? I judged the triggers' inline-availability outweighs the line savings; ARGUS owns the second opinion.
2. **C-2 archive home (stoa--xyb.6 comment vs dedicated ticket).** Weak point 2. Is a comment-stream archive acceptable for the two C-2 provenance blocks, or should they get a dedicated `stoa--xyb.6.N` child ticket each for cleaner recovery?
3. **Section-number PRESERVATION vs RENUMBER.** I chose to preserve section numbers (relocated sections leave a numbered stub) to avoid cross-ref churn across the substrate. The cost is ~10 stub lines in the core. Does ARGUS see a cross-ref the preservation MISSES, or prefer a clean renumber + a re-point sweep?
4. **install.sh recompose vs accept a 2-body fork at subproject tier.** Weak point 1 / §6.4. The recompose is mechanically clean but adds a deploy code path. ARGUS: is the recompose's LOST-CANON-at-subproject risk worth the single-source-of-truth benefit, or is a deliberately-forked full subproject body (maintained by install.sh copying pre-slim content) the safer call given subproject is the hardest-audited tier?

---

## §9 — Out of scope

- **Cutting the other 3 role files** (operating-disciplines.md 2138, MAJOR_PLINY.md 801, CAPTAIN_DAEDALUS.md 633). Per stoa--xyb.6: "After POLYBIUS proves the method, repeat for..." — those are subsequent arcs.
- **Substrate-self-apply re-sync** of the-stoa's deployed `.claude/` (lags source by Arc 44 + this arc). User-tier POLYBIUS housekeeping per §18.1; explicitly batched out by user-tier POLYBIUS (stoa--xyb 2026-05-23T06:50:01Z).
- **Re-syncing the user-tier deployed `~/.claude/MAJOR_POLYBIUS.md`** (which is AHEAD by the §5.6 fold). The fold's content is mirrored INTO source this arc; the deployed copy's re-sync is housekeeping.
- **Building the enforcement layer** (stoa--xyb.5 — sub-agent task-bounding hook). The routing-map/relocation-index formats are designed to be hook-parseable (Arc 1), but the hook is not built here.
- **A bw attachment-read primitive.** C-2 here uses `bw comment` (short prose), not `bw attach` (file) — so the bw-0.13.0 no-attachment-read limitation (modules/README.md §5.2 recovery note) does not bite this arc.

---

*Self-assessed weak points are in §7. Residual questions for ARGUS are in §8.*
