# Arc 44 (debloat Arc 1) — Composition-layer mechanism — design-rev2

Author: Denson Smith
Seat: CAPTAIN_DAEDALUS_the-stoa (ARCHITECT)
Ticket: stoa--xyb.4 (composition layer) | Epic: stoa--xyb | Arc: 44 (debloat Arc 1)
Inputs consumed: stoa--xyb (epic), stoa--xyb.1 (CLI-not-MCP), stoa--xyb.2 (skill-grant/caching/no-real-agent findings), stoa--xyb.3 (3-bucket method + 3-tier content), stoa--xyb.4 (composition-layer spec — primary), design-rev1.md (prior), ARGUS verdict 2026-05-23T06-11-21Z (r1-r6).
Shipped files grounded against: substrate/install.sh (1199 lines), substrate/operating-disciplines.md (2110 lines, §32 ends L2087 then UN-numbered trailing matter L2089/L2100, EOF L2110), substrate/MAJOR_POLYBIUS.md (§7.3 bw-cookbook dupe; §5/§10/§11/§12/§14 = Arc-2 CONDITIONAL targets; §16.6/16.7/17.5/17.6/18.5/18.6/19.6/19.7 = PROVENANCE subsections; §16.8 bw attach primitive), substrate/MAJOR_PLINY.md (§6.1 bw-cookbook dupe).

---

## 0. Changes from rev1 (addressing ARGUS r1–r6)

This is a **full standalone design**; the next ARGUS/ADA reads rev2 alone. This map exists only to make the audit trail explicit.

| ARGUS | rev1 state | rev2 resolution | Where |
|---|---|---|---|
| **r1 [BLOCKING]** — define lossless homes for ALL THREE .3 buckets, not just CONDITIONAL | rev1 §3.G homed only CONDITIONAL (5 modules); PROVENANCE/DUPLICATE were generic channels | rev2 defines **three relocation classes** with a concrete lossless home for each: CONDITIONAL→disk module; **PROVENANCE→bw-cite** (archive via `bw attach` / already-in-bw, slim-core `Anchor:` cite-back); **DUPLICATE→pointer** (existing single consolidation target, no module). | §2.5, §3.B (new), §3.C (new), §3.H |
| **r2 [BLOCKING]** — routing map / relocation index must express all three classes | rev1's table (task-type→module→channel) expressed CONDITIONAL only | rev2 adds a sibling **Relocation Index** table in always-loaded core that records what-was-relocated-where for ALL three classes (CONDITIONAL / PROVENANCE / DUPLICATE), with a worked template per class. Routing map (dispatch-time) and relocation index (audit-time) are two distinct always-loaded tables. | §2.6, §3.E (new) |
| **r3 [BLOCKING]** — fix the op-disc §33 insertion point | rev1 said EOF-append; op-disc does NOT end with numbered content | rev2 build spec specifies §33 inserted **after §32's content (L2087) and BEFORE the un-numbered "Agent-regime inverses" section (L2089)** — NOT EOF-append. P6 gains a placement assertion (§33 appears after the §32 region AND before "Agent-regime inverses"). | §4.0, §5 P6 |
| **r4 [PLINY: adopt glob]** — module deploy = GLOB, not explicit array | rev1 chose explicit `MODULE_NAMES` array | rev2 deploys `substrate/modules/*.md` via **glob discovery** (nullglob single-segment, consistent with the install.sh staleness-scan idiom). Authoring a module needs no install.sh edit. install.sh enumerates/logs what it deployed (observable). Adds a **deploy-COMPLETENESS probe** (every `substrate/modules/*.md` present in `.claude/modules/` after deploy). | §3.A, §4.1–§4.7, §5 P4 |
| **r5 [TRACK]** — subproject-tier module deploy | rev1 asserted deploy-at-all-3-tiers at ~80% confidence | rev2 records this as an explicit **Arc-2-gating OPEN QUESTION** (§6): Read-tool relative-path resolution at subproject tier is web-confirmed contested (claude-code #24987 / never-fixed #2571 lineage / #4754/#15627/#18200). LIVE probe required before any Arc-2+ subproject orchestrator relies on a module path. Arc 1 only needs project-tier deploy to verify. Not an Arc-1 gate. | §6 |
| **r6 [CAP]** — keep op-disc §33 ≤ ~30 lines | rev1 budgeted ~25-35, risked 40 with full §32-style cross-ref block | rev2 hard-caps §33 at **≤30 lines** and collapses the cross-ref block to a **single pointer line** (not the full §32-style HTML-comment + bullet block) to stay under cap. P6 asserts ≤30. | §3.B, §4.0, §5 P6 |

Held from rev1 (non-findings ARGUS confirmed clean — do not regress): clean-diff scope (mechanism only, REFINEMENT 2, P9); routing map in always-loaded core (REFINEMENT 1); 3 delivery channels (Bash/Read/bw — no Skill/no-MCP per .1/.2); dogfood split (thin §33 + on-demand `substrate/modules/README.md`); README as the real deployable file that makes the deploy VERA-testable now; the Arc-2 CONDITIONAL taxonomy (5 names for POLYBIUS §5/§10/§11/§12/§14 — §11 and §12 kept as two distinct homes per the shipped-section drift). write_substrate_manifest needs no modules entry. Credential N/A. Authorship clean. IA-1 (routing-map-in-orchestrator-core) consistent with REFINEMENT 1.

---

## 1. Problem restatement

Build the **composition-layer mechanism only** — the framework that lets an orchestrator (POLYBIUS / PLINY) deliver instruction modules to a sub-agent **at dispatch time**, AND that records where relocated content went, so the Arc-2 POLYBIUS cut can move content OUT of the always-loaded role-file path **losslessly across all three of the .3 method's relocation buckets**. This is debloat **Arc 1**: it ADDS mechanism, it does not CUT any role-file content (that is Arc 2, which USES this mechanism).

The .3 method (stoa--xyb.3) names three kinds of bloat, each with a different lossless home. Arc 1's contract with Arc 2 is to provide a defined, indexable home for **all three**:

1. **CONDITIONAL** (needed only sometimes) → on-demand **disk module** (`.claude/modules/<X>.md`, Read at dispatch). ~500 lines in POLYBIUS.
2. **PROVENANCE** (why a rule exists / the empirical N=1 story / cross-references) → **archived in bw, CITED not inlined**. ~330 lines in POLYBIUS (the `### X.6 N=1 provenance + accretion path` and `### X.7 Cross-references` subsections in §16/§17/§18/§19, plus §4's per-subsection provenance). Much of this content **already names a bw ticket** — the disciplines already cite `u--7yg.X` / `stoa--X`.
3. **DUPLICATE** (same content in 2-3 homes) → **consolidate to one existing home + leave a one-line pointer**. ~30+ lines; the canonical example is the triplicated bw cookbook (op-disc §12 = the keep-home; MAJOR_POLYBIUS §7.3 + MAJOR_PLINY §6.1 = the delete-and-point copies).

Concretely, Arc 1 ships:
- a new substrate source directory `substrate/modules/` whose `*.md` contents `install.sh` deploys (via glob discovery) to `<DEST>/.claude/modules/`;
- one real deployable file in it — `substrate/modules/README.md` — which is both (a) the canon home for the detailed module-authoring procedure + the 3-channel delivery reference + the **three relocation classes** + the planned Arc-2 CONDITIONAL taxonomy, and (b) the live proof that the install.sh wiring works (deploy → `.claude/modules/README.md` exists);
- a thin, always-loaded rule + the **routing-map convention** + the **relocation-index convention** added to `substrate/operating-disciplines.md` (new §33), hard-capped at ≤30 lines because op-disc is the worst bloat offender;
- the install.sh **glob-based** deploy wiring (source-existence check, glob deploy step, enumerated/logged deploy, staleness-scan entry) consistent with install.sh idioms.

**Imported assumptions named (per §6.1 — a restatement that hides imported scope has smoothed it):**

- **IA-1 (routing map + relocation index = orchestrator-only operational core).** REFINEMENT 1 (peer-mandated) says the routing map / module index stays in always-loaded operational core and is NEVER relocated to a module. I read "operational core" as **the orchestrator role files' operational core** (MAJOR_POLYBIUS.md / MAJOR_PLINY.md), because routing + the relocation index are orchestrator concerns — leaf CAPTAINs receive modules, they do not route or track relocations. The §33 op-disc rule documents the *conventions* (formats + the must-stay-in-core rule) universally; the *populated* maps/indexes live inline in each orchestrator's core, authored per-orchestrator (POLYBIUS's actual entries are Arc 2). Arc 1 ships the conventions + worked templates, not any orchestrator's populated maps. ARGUS confirmed this consistent with REFINEMENT 1 in rev1; held.
- **IA-2 (Arc-1 testability bar = wiring + consistency + the 3-class contract being DEFINED, NOT lossless-on-canon being EXECUTED).** Arc 1 ADDS mechanism, so LOSSLESS-ON-CANON execution is Arc 2's bar. Arc 1's bar is: the deploy wiring fires, the README deploys, the canon is internally consistent, AND **the mechanism defines a concrete lossless home + index slot for each of the three buckets** (the r1/r2 fix — this is the part of "mechanism" rev1 under-delivered). I design VERA probes to that bar (§5).
- **IA-3 (CONDITIONAL taxonomy named, not populated; PROVENANCE/DUPLICATE conventions defined, not executed).** Arc 1 NAMES the CONDITIONAL module filenames Arc 2 will populate (so Arc 2 is a clean fill-in) but creates NO content file for them. Arc 1 DEFINES the PROVENANCE archive+cite-back convention and the DUPLICATE consolidate+pointer convention but executes NEITHER (no provenance is archived, no dupe is deleted in Arc 1 — that is the Arc-2 cut, guarded by the clean-diff probe P9). The only real content file Arc 1 creates under `substrate/modules/` is `README.md`.
- **IA-4 (deploy class = glob discovery).** PLINY decision per r4. Glob over `substrate/modules/*.md`; no explicit manifest array; install.sh enumerates/logs the discovered set; a completeness probe asserts every source `*.md` deployed. Replaces rev1's explicit-array choice. Decided in §3.A; the install.sh-reason-it-can't-work check (per the brief's escape hatch) is discharged in §3.A (it can work cleanly).

This restatement converges with the brief and the ARGUS-corrected scope. No divergence requiring a `refused`. The four imported assumptions are scope-clarifications, not re-scopings.

---

## 2. Approach (the design's shape)

The composition layer is **not a new primitive** — it formalizes a primitive PLINY already uses (dispatch briefs already inject task context: MAJOR_PLINY §5.2 ADA preamble, §5.2.1 credential cite, "run bw start <id>"). Three delivery channels, all using tools every agent already has (Bash / Read / bw — no Skill grant, no MCP, per stoa--xyb.1):

```
                     ORCHESTRATOR (POLYBIUS / PLINY)
                     carries inline in slim core, always-loaded:
                     ┌──────────────────────────────┐    ┌──────────────────────────────┐
                     │  ROUTING MAP (dispatch-time)  │    │  RELOCATION INDEX (audit-time)│
                     │  task-type -> module + channel│    │  what moved -> where + class  │
                     └───────────────┬──────────────┘    │  CONDITIONAL / PROVENANCE /   │
                                     │                    │  DUPLICATE                    │
                                     │ at dispatch         └──────────────────────────────┘
                                     │ selects + names               (§33 conventions; NEVER a module)
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                        ▼
   CHANNEL 1: inline        CHANNEL 2: disk module    CHANNEL 3: bw ticket
   in dispatch prompt       .claude/modules/X.md       bw show <id> / bw attach
   (small, task-specific)   via Read                   (dynamic / bespoke / must-persist;
                            (stable, reused)            ALSO the PROVENANCE archive home)
                                     │
   THREE RELOCATION CLASSES (the .3 method's three buckets, each with a lossless home):
     CONDITIONAL -> CHANNEL 2 (disk module)      [home: substrate/modules/<X>.md]
     PROVENANCE  -> CHANNEL 3 (bw archive+cite)  [home: bw ticket via bw attach / already-in-bw; slim-core Anchor: cite-back]
     DUPLICATE   -> consolidate to ONE existing home + one-line pointer  [home: the existing keep-target, e.g. op-disc §12; NO module]
```

The mechanism has five parts. Four are built in Arc 1; the fifth (orchestrators' POPULATED routing maps + relocation indexes) is Arc 2+.

### 2.1 The deploy class (`substrate/modules/` → `.claude/modules/`)

A new install.sh-managed file class, deployed via **glob discovery** over `substrate/modules/*.md` (per r4 / PLINY decision). See §3.A for the glob-vs-array decision and §4 for the line-level wiring spec. install.sh enumerates and logs the discovered set so the deploy is observable; a completeness probe (P4) asserts every source `*.md` lands in dest.

### 2.2 The canon split (dogfooding the 3-tier model on ourselves)

Per the method, operational core = the rule stated crisply (always loaded, small); reference = detailed procedure (on-demand); provenance = bw-cited. We apply this to the composition canon **itself**:

- **operational core (always loaded):** `substrate/operating-disciplines.md` **§33** — a thin rule (≤30 lines, hard cap per r6): "instructions are a composable module library; orchestrators deliver via 3 channels; the routing map AND the relocation index stay inline in orchestrator core; the three relocation classes; recurrence in the bw log → author a disk module" + a single pointer line to the on-demand README for the detail.
- **reference (on-demand):** `substrate/modules/README.md` — the detailed authoring procedure, the full 3-channel selection reference, the **three relocation classes with worked templates**, the routing-map + relocation-index worked templates, and the planned Arc-2 CONDITIONAL taxonomy. This file is itself a disk module (it lives in `.claude/modules/` after deploy), so the canon's detail is loaded the same way every other module's detail is loaded. That is the dogfood.

This split is the load-bearing structural choice. It keeps the op-disc addition minimal (the brief's hard constraint: op-disc is the 2110-line worst offender; what we ADD must be a thin rule + pointer, ≤30 lines).

### 2.3 The routing-map format (dispatch-time)

A small structured markdown table the orchestrator carries inline in its slim core: **task-type → module(s) to load → channel**. This answers *at dispatch time, what does this task need?* Format + worked template in README; POLYBIUS's populated entries are Arc 2.

### 2.4 Module-authoring discipline

The recurrence rule: bw is the record of every custom instruction an orchestrator emits (CHANNEL 3); when an instruction recurs across dispatches, that recurrence is the signal to promote it to a disk module (CHANNEL 2). bw FEEDS the library; it is not the library. Canon home: README + a one-line statement in op-disc §33. Under glob deploy (§3.A), authoring a module is: write `substrate/modules/<name>.md` → redeploy (no install.sh edit) → add routing-map + relocation-index rows.

### 2.5 The three relocation classes (the r1 fix — lossless home per bucket)

Arc 1 DEFINES three relocation classes, one per .3 bucket, each with a concrete lossless home and an authoring discipline. This is the Arc-1→Arc-2 contract ARGUS r1 found incomplete in rev1. Defined in detail in §3.B/§3.C/§3.H; summarized:

| Class | .3 bucket | Lossless home | Cite-back in slim core | Arc-1 status |
|---|---|---|---|---|
| **CONDITIONAL** | needed-only-sometimes | disk module `.claude/modules/<X>.md` (CHANNEL 2) | routing-map row (task-type → module → disk) | convention + 5 NAMED module homes + worked template |
| **PROVENANCE** | why-it-exists / N=1 story / cross-refs | bw ticket (CHANNEL 3): `bw attach` for not-yet-in-bw prose, or already-in-bw (just delete + keep cite) | one-line `Anchor: <bw-id>` (§3.C format) + relocation-index row | convention + cite-back format + worked template |
| **DUPLICATE** | same content in 2-3 homes | the EXISTING single keep-target (e.g. op-disc §12) — NO module | one-line pointer at each deleted site + relocation-index row | convention + worked template + named keep-targets |

### 2.6 The relocation-index format (audit-time — the r2 fix)

A second small structured markdown table the orchestrator carries inline in its slim core, sibling to the routing map: **relocated-content → new-home → relocation-class**. This answers *where did the content that used to be here go?* — the REFINEMENT-1 "index of what-was-relocated-where," now first-class for ALL THREE classes (rev1's single table expressed only CONDITIONAL). Distinct from the routing map: the routing map is consulted at dispatch time to compose a payload; the relocation index is consulted at audit/recovery time to find moved content. Both stay inline in always-loaded core; both NEVER become a module (an index that must itself be loaded-on-demand never fires). Format + per-class worked template in §3.E; POLYBIUS's populated rows are Arc 2.

---

## 3. Concrete decisions (A–H) — enumerated + decided

### Decision A — Module source + deploy path, and the deploy-class mechanism (GLOB per r4)

**Decided:** Source `substrate/modules/` → deployed `<DEST>/.claude/modules/`. Wire via **glob discovery** over `substrate/modules/*.md` — NOT an explicit manifest array. PLINY decision (r4).

**Why glob (the r4 rationale, now adopted):**
1. **Serves the epic's growing-library thesis.** Modules are the ONE file class the epic is designed to grow continuously (Decision F accretion: recurrence → author module → redeploy). A glob means authoring a new module needs NO install.sh edit — the highest-churn file class is the one where the manual-array tax and its silent failure mode (author a module, forget the array line, it never deploys, no error) would bite hardest. Glob eliminates that failure class entirely.
2. **It is consistent with shipped install.sh idioms.** install.sh already uses `shopt -s nullglob` single-segment globs (`for f in "${DEST_TEMPLATES_DIR}"/*` at the staleness scan L970; `for f in "${DEST_SKILLS_DIR}"/*/` L989). Glob deploy reuses the SAME idiom on the source side. It is not the "only glob in the script" (rev1's mistaken claim) — the staleness scanner is already glob-driven.
3. **Completeness becomes the probeable contract.** The brief notes any new install.sh-managed file class needs deploy-plan wiring VERA can verify. Under glob, the verifiable contract is *deploy COMPLETENESS*: every `substrate/modules/*.md` is present in `.claude/modules/` after deploy. P4 (§5) re-runs the source glob and asserts each basename landed in dest — a stronger contract than rev1's "the array contains README.md" grep, because it catches a deploy-step bug that drops a file, not just an array-membership fact.
4. **install.sh logs what it deployed (observability, per r4's note).** The plan line + deploy step echo the discovered count and each filename, so the deploy is observable in stdout (a reader/CATO can see exactly which modules deployed without reading an array).

**Escape-hatch check (per brief: surface back if glob can't work cleanly).** It works cleanly. The one concern a glob raises is "what if the source dir is empty / the glob matches nothing" — handled by `nullglob` + a source-dir-existence `err` check (§4.2): the dir must exist; if it is empty the deploy is a no-op (zero modules) which is a valid state pre-Arc-2 except that Arc 1 ships README.md, so a completeness probe that finds zero source modules would itself fail loudly. No install.sh reason to revert to the array. Glob adopted.

**Wiring shape (parallel to the templates class, glob-driven — full line-level spec in §4):** add `SRC_MODULES_DIR`, a source-dir-existence check, a glob-discovery deploy step (cp, unsuffixed — modules are shared tooling like templates), an enumerate/log of the discovered set, and a staleness-scan entry. Modules deploy at user + project tiers; subproject tier is a TRACKED OPEN QUESTION (§6) — Arc 1 wires project + user (the README deploys + verifies at project tier), and explicitly defers the subproject DEST wiring decision to the Arc-2-gating live probe rather than asserting it now.

**No `--no-modules` opt-out flag.** Mirrors skills (always deployed, no opt-out): a deployed substrate that omits modules leaves orchestrators unable to Read the modules their routing map points at. One real file (README) makes the deploy near-free.

### Decision B — Where the composition canon lives (dogfood the method on itself)

**Decided:** Two homes, split by access tier (per §2.2):
- **`substrate/operating-disciplines.md` §33 (NEW, ≤30 lines HARD CAP per r6, operational core):** thin rule + the three-channel naming + the routing-map-and-relocation-index-stay-in-core convention + the three relocation classes named in one line each + a SINGLE pointer line to the README. Universal-team layer (op-disc is the universal doc all seats read). The single pointer line replaces rev1's full §32-style HTML-comment + bullet cross-ref block, to stay under the ≤30 cap (r6).
- **`substrate/modules/README.md` (NEW, the only Arc-1 content file under modules/, on-demand reference):** the detailed authoring procedure, the full 3-channel selection reference, the **three relocation classes with worked templates** (§3.C/§3.E/§3.H), the routing-map + relocation-index worked templates, the module-authoring discipline, and the planned Arc-2 CONDITIONAL taxonomy.

**Exact §33 content outline (≤30 lines — this is what we ADD to the worst offender):**
```
## 33. Composition layer — instruction modules + orchestrator routing

[~2 sentences] Instructions are a composable library, not all-memorized. An
orchestrator selects what a task needs and delivers it AT DISPATCH TIME via 3
channels, all using tools every agent already has (no Skill grant, no MCP; see
stoa--xyb.1):
  - inline in the dispatch prompt — small, task-specific.
  - disk module `.claude/modules/<X>.md` via Read — stable, reused.
  - bw ticket via `bw show <id>` (or `bw attach` to archive) — dynamic /
    bespoke / must-persist; ALSO the provenance archive home.

THREE RELOCATION CLASSES (how the .3 debloat method's buckets find lossless
homes; populated indexes are per-orchestrator core, Arc 2):
  - CONDITIONAL -> disk module (CHANNEL 2).
  - PROVENANCE  -> bw archive + a one-line `Anchor: <bw-id>` cite in slim core.
  - DUPLICATE   -> consolidate to the ONE existing home + a one-line pointer.

ROUTING MAP + RELOCATION INDEX (load-bearing — both stay inline in orchestrator
operational core, NEVER a module): the routing map (task-type -> module +
channel, dispatch-time) and the relocation index (relocated-content -> new-home
+ class, audit-time). An index that must itself be loaded-on-demand never fires.

AUTHORING SIGNAL: the bw custom-instruction stream is the RECORD, not the
library. Recurrence in that record -> author a reusable disk module.

Full procedure, channel-selection + relocation-class templates, taxonomy:
`.claude/modules/README.md` (on-demand).
```
(That outline is ~28 lines including the header and the blank lines between blocks — at the ≤30 cap. If ADA's line-count comes out over 30, the trim order is: collapse the three-channel sub-bullets to a single line, then the three-relocation-class sub-bullets to a single line. The single README pointer line is already minimal — do NOT expand it into a §32-style block.)

### Decision C — The PROVENANCE → bw-cite mechanism (the r1 fix, part 1)

**Decided:** PROVENANCE content (the `### X.6 N=1 provenance + accretion path` and `### X.7 Cross-references` subsections in MAJOR_POLYBIUS §16/§17/§18/§19, plus §4's per-subsection provenance; ~330 lines per .3 LINE MATH) relocates to bw, **cited not inlined**. Two sub-cases by where the prose currently lives:

**(C-1) Already-in-bw provenance (the common case).** Most provenance prose ALREADY names its bw ticket — §16.6 cites `stoa--dxw` / `stoa--p5g` / `stoa--32b.3`; §16.7 cites the parent epic + handoff doc; §4 subsections cite `u--7yg.X`. For these, the bw ticket already IS the durable home. The Arc-2 cut is: **delete the verbose inline prose, keep a one-line cite-back** pointing at the ticket(s) already named. Nothing is archived (it is already in bw); the relocation is delete + cite.

**(C-2) Not-yet-in-bw provenance.** Where verbose provenance prose has NO bw home (a long empirical-story paragraph that exists only inline), the Arc-2 cut **archives it to bw first** via `bw attach <ticket-id> <file-path>` (the §16.8 primitive — reads a file from disk, stores its bytes at `attachments/<ticket-id>/<stored-path>` on the beadwork ref, commits a one-line intent comment) OR as a `bw comment` on the relevant ticket if it is short prose rather than a file. THEN delete the inline prose and keep the cite-back. This guarantees lossless: the bytes live in bw before the inline copy is removed.

**The cite-back format (slim-core, what survives the cut):** a one-line `Anchor:` cite at the point the provenance used to be inline:
```
Anchor: <bw-id>[, <bw-id>...]  — N=1 provenance + accretion path. Recover via `bw show <id>` (or `bw show --attachments <id>` if archived via bw attach).
```
For cross-references that point at OTHER substrate sections (not provenance story), the existing in-file `§X` / `operating-disciplines.md §Y` pointer convention is kept (those are not provenance to archive — they are live cross-refs; only the verbose *story* moves to bw). README documents the C-1 vs C-2 split + the `Anchor:` format + a worked example (the .3 worked example: §4.3.1's 2026-05-13 four-options empirical story → `bw show stoa--ezj` cite, ~17 lines → ~5).

**Why bw is the right provenance home (not a disk module):** provenance is read rarely (only when someone asks *why does this rule exist*), it is inherently historical (tied to a ticket + a date), and bw is already the substrate's durable cross-session record. A disk module would be the wrong home — modules are for CONDITIONAL operational content an orchestrator delivers at dispatch; provenance is not dispatched, it is recovered. This matches the .3 method exactly ("provenance: archived in bw, CITED not inlined").

### Decision D — The 3 delivery channels + selection guidance (canon in README)

**Decided:** Document all three as canon in README, with this selection guidance:

| Channel | Mechanism | Use when | Persists? |
|---|---|---|---|
| 1. inline | text in the dispatch prompt | small, task-specific, one-off instruction the orchestrator composes fresh | only in that dispatch payload |
| 2. disk module | `.claude/modules/<X>.md` via `Read <path>` | stable instruction reused across tasks/projects; orchestrator names the path in the dispatch | yes — versioned in substrate |
| 3. bw ticket | `bw show <id>` / `bw attach <id> <file>` | dynamic / bespoke / single-use, OR anything that must persist or be shared across seats; ALSO the PROVENANCE archive home (Decision C) | yes — in bw, sharing-topology we control |

**The bw-feeds-the-library note (load-bearing, from stoa--xyb.4):** bw one-offs are NOT a curated library — they are the routine custom-instruction stream the orchestrator generates constantly, retained for record-keeping. Recurrence in that record is the SIGNAL to author a CHANNEL-2 disk module. README states this explicitly so the channels are not misread as "bw = the module store." Note the dual role: CHANNEL 3 is BOTH the live custom-instruction stream AND the PROVENANCE archive destination (Decision C) — these are two uses of the same bw substrate, not a contradiction.

**Compaction-proofness (the channel's reason for existing, from stoa--xyb.4):** selection rides the dispatch payload, delivered fresh at spawn — so a sub-agent always gets its modules even though its own context may later compact. README names the known weak spot too (a sub-agent that compacts mid-task has no orchestrator re-telling it; mitigation = keep sub-agent tasks bounded — ties to the future enforcement layer, stoa--xyb.5).

### Decision E — The routing-map + relocation-index formats (the r2 fix)

**Decided:** TWO inline structured markdown tables in the orchestrator's slim core, both always-loaded, both NEVER a module.

**(E-1) Routing map (dispatch-time).** Columns: **task-type → module(s) to load → channel**. Worked template (goes in README; FORMAT + example, NOT POLYBIUS's real entries):
```markdown
### Routing map (orchestrator core — always loaded — dispatch-time)

| Task type | Module(s) to load | Channel |
|---|---|---|
| <onboard a new project>      | `onboarding.md`            | disk (Read) |
| <spawn a sub-project>        | `sub-project-spawning.md`  | disk (Read) |
| <author a pair-programmer>   | `pair-programmer-authoring.md` | disk (Read) |
| <one-off bespoke task>       | (compose inline)           | inline |
| <must-persist shared spec>   | `bw show <ticket-id>`      | bw |
```

**(E-2) Relocation index (audit-time — the r2 fix).** Columns: **relocated content → new home → class**. This is the REFINEMENT-1 "index of what-was-relocated-where," now expressing ALL THREE relocation classes (rev1's single table expressed CONDITIONAL only). Worked template (goes in README; FORMAT + one worked row per class, NOT POLYBIUS's real entries):
```markdown
### Relocation index (orchestrator core — always loaded — audit-time)

| Relocated content (was here) | New home | Class |
|---|---|---|
| §5 Onboarding flow            | `onboarding.md` (disk module)            | CONDITIONAL |
| §16.6 N=1 provenance          | `bw show stoa--dxw` (Anchor cite)        | PROVENANCE  |
| §7.3 bw cookbook (dupe)       | op-disc §12 (consolidated; pointer kept) | DUPLICATE   |
```

**Properties both formats are designed for:**
- **Inline + always-loaded** (per IA-1 / REFINEMENT 1): small tables, cheap to keep ambient.
- **All three classes expressible** (the r2 fix): the relocation index's `Class` column makes CONDITIONAL / PROVENANCE / DUPLICATE first-class index entries a reader/orchestrator can follow to recover any moved content. A reader of the slim-core index can now see *deleted-bw-cookbook-lives-at-op-disc-§12* and *provenance-archived-at-bw-stoa--dxw*, which rev1 could not express.
- **Checkable** (per stoa--xyb.4): the regular column shape (routing map: task-type/module/channel; relocation index: content/home/class) is what makes a future enforcement-layer hook (stoa--xyb.5) parseable. Arc 1 does NOT build the hook — it designs the formats so the hook is possible.
- **Two tables, two purposes (do not merge):** the routing map answers "at dispatch, what does this task need?"; the relocation index answers "where did moved content go?". A task-type does not map 1:1 to a relocated section (one task may load several modules; one relocated section may serve several task-types; PROVENANCE/DUPLICATE relocations have no dispatch-time task-type at all). Keeping them as two tables is why all three classes get a home — forcing PROVENANCE/DUPLICATE into the dispatch-time routing map (rev1's single-table approach) is exactly what made them inexpressible.

POLYBIUS's actual rows for both tables are authored in Arc 2. Arc 1 ships the empty-shaped templates + the examples above.

### Decision F — Module-authoring discipline (recurrence → author a module)

**Decided:** Canon in README, one-line echo in op-disc §33. The rule: an orchestrator emits custom instructions constantly (CHANNEL 3, retained in bw for record-keeping). When the SAME instruction recurs across multiple dispatches, that recurrence is the trigger to promote it to a CHANNEL-2 disk module under `substrate/modules/`. Under glob deploy (Decision A) the procedure is shorter than rev1's (no array edit):
1. Notice recurrence in the bw custom-instruction record.
2. Author `substrate/modules/<name>.md` (the reusable form).
3. Redeploy via install.sh (glob auto-discovers the new file — NO install.sh edit).
4. Add a routing-map row (task-type → `<name>.md` → disk) + (if it relocates inline content) a relocation-index row to the relevant orchestrator's core.

This is the accretion path that GROWS the module library over time — and the reason glob (not the array) is the right deploy class (Decision A): step 3 is zero install.sh edits, paid every time, on the most-frequently-grown class.

### Decision G — End-to-end testability (Arc 1 must be VERA-testable NOW)

**Decided:** `substrate/modules/README.md` is a real deployable file, so the full deploy path is exercisable today even though no conditional content has moved yet. VERA probe spec in §5. The "any new install.sh-managed file class needs deploy-plan wiring" smoke-beat is satisfied by Decision A's source-existence check + glob deploy step + enumerate/log + completeness probe + staleness-scan, all of which §5 probes.

### Decision H — Anticipate Arc 2 (define all three classes' homes; build none of the cut)

**Decided:** Arc 1 gives Arc 2 a clean fill-in for ALL THREE relocation classes (the r1 contract). For CONDITIONAL, name the planned module filenames in README + as commented routing-map rows. For PROVENANCE and DUPLICATE, define the convention + worked template + name the concrete keep-targets (Arc 2 executes the archive/delete; Arc 1 names where).

**(H-1) CONDITIONAL — 5 named module homes** (grounded against the actual MAJOR_POLYBIUS.md shipped headers, not the brief's labels):

| Planned module file | Relocates MAJOR_POLYBIUS § (shipped header) | Arc-1 status |
|---|---|---|
| `onboarding.md` | §5 Onboarding flow | NAMED only |
| `sub-project-spawning.md` | §10 Sub-project spawning | NAMED only |
| `pair-programmer-authoring.md` | §11 Pair-programmer Major authoring | NAMED only |
| `pair-programming-prototyping.md` | §12 Pair-programming-for-prototyping methodology (Mode 2) | NAMED only |
| `substrate-update-check.md` | §14 Substrate-update check (daily cadence) | NAMED only |

**Drift flag (held from rev1, ARGUS-confirmed):** the brief labeled §11+§12 jointly as "pair-programmer (~168)". The shipped file has them as TWO distinct sections (§11 authoring; §12 prototyping methodology). I taxonomize them as TWO modules to give Arc 2 separable homes; if Arc 2 finds them tightly coupled it may merge to one — that is Arc 2's call. Two homes is a superset of one. NO content files for any of these are created in Arc 1.

**(H-2) PROVENANCE — named keep/archive targets** (Arc 2 archives via Decision C; Arc 1 names where the provenance lives):

| Provenance subsection (was here) | Already-in-bw? | Arc-2 action (Decision C) |
|---|---|---|
| §16.6 N=1 provenance + accretion path | YES (`stoa--dxw`, `stoa--p5g`, `stoa--32b.3`) | C-1: delete prose, keep `Anchor:` cite |
| §16.7 Cross-references | partial (parent epic + handoff doc named) | C-1 for the bw-named refs; keep live `§X` cross-refs inline |
| §17.5 / §17.6 (base-vs-custom provenance + cross-refs) | named in body | C-1 |
| §18.5 / §18.6 (direct-commit provenance + cross-refs) | named in body | C-1 |
| §19.6 / §19.7 (provenance + cross-refs) | named in body | C-1 |
| §4 per-subsection N=1 provenance (`u--7yg.X` cites) | YES (`u--7yg.X`) | C-1 |
| any verbose inline empirical story with NO bw home | NO | C-2: `bw attach`/`bw comment` first, THEN delete + cite |

**(H-3) DUPLICATE — named consolidation target** (Arc 2 deletes the dupes + leaves pointers; Arc 1 names the keep-home):

| Duplicated content | Keep-home (consolidation target) | Delete + point (Arc 2) |
|---|---|---|
| bw cookbook (triplicated) | **op-disc §12** (the fullest copy, ~77 lines) | MAJOR_POLYBIUS §7.3 (~32 lines) + MAJOR_PLINY §6.1 (~34 lines) → delete, leave one-line pointer to op-disc §12 |

**The DUPLICATE relocation class is explicitly NOT a module** (the r1 explicit statement): the home is the EXISTING single consolidation target. No new file is authored, no `substrate/modules/` entry is created. The relocation is purely delete-dupe + leave a one-line pointer at each deleted site + a relocation-index row. README names this as a defined relocation class with its worked template (the bw-cookbook example above).

NO content cut for any of H-1/H-2/H-3 happens in Arc 1 (clean-diff, P9). Arc 1 ships only the conventions + templates + named targets.

---

## 4. install.sh wiring — line-level build spec (for ADA)

All additions parallel the existing templates class but use **glob discovery** (per Decision A / r4). Reference line numbers are from the shipped substrate/install.sh; locate by idiom if line refs have drifted (ARGUS noted minor line-ref drift is locate-by-idiom-able).

**(4.0) op-disc §33 insertion point (the r3 fix — load-bearing build-correctness).** op-disc does NOT end with numbered content. The structure at the tail is:
- L2042: `## 32. Test-environment timing discipline` (start)
- L2087: end of §32's content (the `---` separator closing §32's cross-refs block)
- L2089: `## Agent-regime inverses` (UN-numbered trailing section)
- L2100: `## Empirical lineage` (UN-numbered trailing section)
- L2110: EOF

**§33 MUST be inserted AFTER §32's content (after the L2087 `---` separator) and BEFORE the `## Agent-regime inverses` un-numbered section (L2089).** It is NOT an EOF-append (rev1's error — that would place numbered canon §33 AFTER the un-numbered closing matter, breaking the doc's structure). The insertion is: locate the `## Agent-regime inverses` header, insert the §33 block (a `---` separator + the §33 content + a `---` separator, matching the existing inter-section separator style) immediately BEFORE it. **Re-verify these exact line numbers against the live file at build time before editing** (they may shift if any earlier edit lands first). The anchor to locate by is the literal string `## Agent-regime inverses` — insert above it, after §32's closing `---`.

**(4.1) Source path** — after `SRC_SKILLS_DIR` (L105), add:
```bash
SRC_MODULES_DIR="${SCRIPT_DIR}/modules"

# Instruction-module library (Arc 44 / stoa--xyb.4). Composable on-demand
# reference content an orchestrator names in a dispatch (Read .claude/modules/<X>.md)
# or that the team reads when authoring/relocating modules. Deployed unsuffixed
# (shared tooling, like templates). GLOB-DISCOVERED from substrate/modules/*.md
# (per stoa--xyb.4 r4 / PLINY decision) so authoring a new module needs NO
# install.sh edit — the file class the epic is designed to grow continuously.
```
No `MODULE_NAMES` array (glob, not manifest — r4).

**(4.2) Source-existence check** — after the skills existence loop (L629-633), add a modules source-dir check + a non-empty assertion (the glob must match at least the README, else the source is broken):
```bash
[ -d "$SRC_MODULES_DIR" ] || err "source modules directory not found: $SRC_MODULES_DIR"
# Glob-discover module sources; assert at least one (.md) exists so an empty
# or mis-pathed source dir fails loudly rather than silently deploying nothing.
shopt -s nullglob
_src_modules=( "${SRC_MODULES_DIR}"/*.md )
shopt -u nullglob
[ "${#_src_modules[@]}" -gt 0 ] || err "no module sources found: ${SRC_MODULES_DIR}/*.md"
```

**(4.3) DEST var** — in the user + project `case "$TARGET"` arms (L536-537 user; L552-553 project), add a `DEST_MODULES_DIR` alongside the existing `DEST_SKILLS_DIR`:
- user: `DEST_MODULES_DIR="${HOME}/.claude/modules"`
- project: `DEST_MODULES_DIR="${PROJECT_DIR}/.claude/modules"`
- **subproject:** set `DEST_MODULES_DIR=""` for now (NOT used in subproject mode in Arc 1) — subproject-tier module deploy is a TRACKED OPEN QUESTION (§6); the README deploys + verifies at project tier, so Arc 1 wires only user + project. Mirror the templates pattern (`DEST_TEMPLATES_DIR=""` at L594) so the deploy step's `[ -n "$DEST_MODULES_DIR" ]` guard skips subproject cleanly. **Do NOT assert subproject deploy works** (rev1's ~80% claim — now §6).

**(4.4) Plan line** — in the plan block (near L661 "deploy skills"), add (count comes from the source glob; observable per r4):
```bash
echo "  deploy modules   : yes (${#_src_modules[@]} module(s) to ${DEST_MODULES_DIR})"
```
(Guard with `[ -n "$DEST_MODULES_DIR" ]` for the subproject-skip case, matching the templates plan-line guard at L656-660.)

**(4.5) Deploy step** — add a new step after the skills deploy (after L826 region), glob-driven, modeled on the templates deploy (cp flat files), with an enumerate/log so the deploy is observable (r4):
```bash
# Deploy instruction modules (Arc 44; always — no opt-out, mirrors skills).
# GLOB-discovered flat .md files, deployed unsuffixed. cp overwrites in place
# (idempotent for unchanged source). Enumerated/logged so the deploy is
# observable in stdout. Skipped in subproject mode (DEST_MODULES_DIR empty —
# see §6 tracked open question).
if [ -n "$DEST_MODULES_DIR" ]; then
  if [ ! -d "$DEST_MODULES_DIR" ]; then
    run_or_print "mkdir -p \"$DEST_MODULES_DIR\""
  else
    log "modules directory already exists: $DEST_MODULES_DIR"
  fi
  shopt -s nullglob
  for src in "${SRC_MODULES_DIR}"/*.md; do
    mname="$(basename "$src")"
    dest="${DEST_MODULES_DIR}/${mname}"
    log "deploy module: ${mname}"   # enumerate/log each deployed module (r4 observability)
    run_or_print "cp \"$src\" \"$dest\""
  done
  shopt -u nullglob
fi
```

**(4.6) Staleness scan** — add a modules block in the staleness section (after the skills scan, ~L987-1014), glob-driven, comparing deployed files against the SOURCE glob (not an array), in the file-only single-segment shape used by templates:
```bash
if [ -n "${DEST_MODULES_DIR:-}" ] && [ -d "$DEST_MODULES_DIR" ]; then
  shopt -s nullglob
  # Build the source basename set from the glob (no array to compare against).
  declare -A _src_module_set=()
  for s in "${SRC_MODULES_DIR}"/*.md; do _src_module_set["$(basename "$s")"]=1; done
  for f in "${DEST_MODULES_DIR}"/*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    if [ -z "${_src_module_set[$base]:-}" ]; then obsolete_files+=("$f"); fi
  done
  shopt -u nullglob
fi
```

**(4.7) Header doc-comment** — update the top-of-file usage comment (L13-20 region) to mention the modules deploy in the one-line inventory, parallel to skills/templates. Small prose-only edit.

**Manifest writer (write_substrate_manifest, L396-456):** modules carry NO `{{NAME_SUFFIX}}` / `{{USER_TIER_DIR}}` substitution (unsuffixed flat content like templates, which are NOT in the manifest). **No change to write_substrate_manifest needed** — modules, like templates, are deployed verbatim and need no substitution record. (ARGUS confirmed this non-finding in rev1; held.)

---

## 5. Verification probes (for VERA — re-executable)

All probes run from the worktree root unless noted. Probes target the Arc-1 bar (wiring + deploy + consistency + the 3-class contract being DEFINED), not lossless-on-canon execution (IA-2). Probes that mutate a workspace use a **throwaway clone** (`git clone --no-local` of the repo, or a scratch `--project-dir`) per op-disc §25.5 — VERA never mutates a real operator workspace.

**P1 — source file exists.** `test -f substrate/modules/README.md` → exits 0. (The one real content file.)

**P2 — install.sh dry-run shows the module deploy.** Run `bash substrate/install.sh --target project --project-dir <throwaway-clone> --dry-run` and confirm stdout contains both a `deploy modules` plan line AND a `[dry-run] ... cp` line (via `run_or_print`) for `modules/README.md`. Use `--target project` with a throwaway dir to keep it non-interactive (the user-tier path triggers prompts).

**P3 — real deploy lands the README.** Against the same throwaway clone, run install.sh WITHOUT `--dry-run` (`--target project --project-dir <clone>`), then `test -f <clone>/.claude/modules/README.md` → exits 0.

**P4 — deploy COMPLETENESS (the r4 glob contract — replaces rev1's array grep).** After the P3 real deploy, assert EVERY `substrate/modules/*.md` source landed in `<clone>/.claude/modules/`. Re-run the source glob and check each basename in dest:
```bash
fail=0
for s in substrate/modules/*.md; do
  b="$(basename "$s")"
  test -f "<clone>/.claude/modules/$b" || { echo "MISSING in dest: $b"; fail=1; }
done
exit $fail
```
→ exits 0. This is a STRONGER contract than rev1's "the array contains README.md" grep: it catches a deploy-step bug that drops a file, and it auto-covers any future module Arc 2+ adds (no probe edit needed — the growing-library thesis the glob serves). Also confirm install.sh logs the discovered set (the `deploy module: <name>` log line from §4.5 appears in stdout — observability per r4).

**P5 — source-existence check fires on an empty source dir.** Assert (by code-read of §4.2, or against a throwaway clone with `substrate/modules/*.md` removed) that install.sh `err`s with "no module sources found" when the glob matches nothing. (Confirms the glob's loud-fail-on-empty escape-hatch from Decision A.) Non-destructive variant: VERA confirms the §4.2 nullglob-count-check + `err` is present and matches the shape.

**P6 — op-disc §33 exists, is correctly PLACED, and is ≤30 lines (the r3 + r6 fixes).**
- (a) Existence: `grep -q '^## 33\. Composition layer' substrate/operating-disciplines.md` → exits 0.
- (b) **Placement (r3):** §33 appears AFTER the §32 region AND BEFORE the un-numbered `## Agent-regime inverses` section. Concretely: the line number of `^## 33\. Composition layer` is greater than the line number of `^## 32\.` AND less than the line number of `^## Agent-regime inverses`. (e.g. via `awk`/`grep -n` line-number comparison: `L(§33) > L(§32)` and `L(§33) < L(Agent-regime inverses)`.) This catches the rev1 EOF-append error.
- (c) **Cap (r6):** the §33 section (sed the §33→`## Agent-regime inverses` range, `wc -l`) is ≤30 lines. Enforces the hard cap on the worst offender.

**P7 — canon internal consistency (the three homes + three classes agree).** Confirm: (a) op-disc §33 points to `.claude/modules/README.md`; (b) README documents exactly the 3 channels named in §33; (c) README documents all THREE relocation classes (CONDITIONAL/PROVENANCE/DUPLICATE) named in §33, each with a worked template; (d) the 5 CONDITIONAL taxonomy module names in README (§3.H-1) match the Arc-2 mapping; (e) README's routing-map AND relocation-index templates both appear and the relocation-index template has a worked row for each of the 3 classes. VERA reads §33 + README and confirms no contradiction (no channel/class named in one but missing the other; no taxonomy drift).

**P8 — staleness scan covers modules (glob-based).** Confirm a modules block exists in the staleness section (code-read of §4.6 presence) AND that a deployed `.claude/modules/` with an extra non-source file is listed as obsolete (dynamic check: drop a `bogus.md` into `<clone>/.claude/modules/`, re-run install.sh, confirm `bogus.md` appears in the "Obsolete files detected" output — the glob-based scan compares dest against the SOURCE glob, so a file not in `substrate/modules/*.md` is flagged).

**P9 — no role-file CONTENT was cut (Arc-1 clean-diff guard, REFINEMENT 2).** `git diff --stat` against the branch point must show ADDITIONS to install.sh + op-disc (the §33 insert) + the new `modules/README.md` + this design file ONLY — NO deletions from MAJOR_POLYBIUS.md / MAJOR_PLINY.md / any CAPTAIN file. Permitted edits: install.sh wiring, op-disc §33 insertion (additive — note: an insertion mid-file shows as additions only, no deletions, since §33 goes BEFORE existing content not over it), the new `modules/` dir, this design artifact. Any deletion from a role file = Arc-1 scope violation (the Arc-2 cut is where deletions happen).

**P10 — credential/CI structure (per §6.6 of the DAEDALUS envelope):** N/A — this design touches NO credentialed third-party op (install.sh deploys local files; no API token, no cloud service). Stated explicitly so VERA confirms the N/A rather than infers it.

---

## 6. TRACKED Arc-2-gating OPEN QUESTION — subproject-tier module path-resolution (the r5 fix)

**This is NOT an Arc-1 gate.** Arc 1 deploys + verifies modules at PROJECT tier (the one real README, P1-P4); subproject correctness only matters when an Arc-2+ subproject orchestrator dispatches a module path. Recorded here as an explicit open question Arc 2+ MUST resolve with a LIVE probe before relying on a subproject module path.

**The contested assumption.** rev1 asserted modules deploy at all 3 tiers (like skills) because Read resolves relative to the active workspace, at ~80% confidence. ARGUS r5 + a web check (2026-05-23) found this rests on a contested platform behavior:
- The skills-subproject precedent (install.sh L52-60 / L789-790) is about **Skill-TOOL discovery resolution**, NOT **Read-TOOL explicit-path resolution**. Modules are Read-by-explicit-path, so the precedent is NOT directly transferable.
- Claude Code's relative/subdirectory path-resolution for files read in subprojects/sub-agents is web-confirmed contested/buggy as of early 2026: claude-code issue #24987 (subdirectory CLAUDE.md not loaded on Read, VS Code v2.1.39), the never-fixed #2571 lineage (subdirectory CLAUDE.md auto-load), plus the issues ARGUS cited (#4754 / #15627 / #18200 / #11374). The exact Read-tool path-resolution ROOT for a sub-agent in a subproject is platform behavior that cannot be settled from repo + docs alone.

**Arc-1 decision (consequent):** Arc 1 wires `DEST_MODULES_DIR` for user + project tiers only; subproject `DEST_MODULES_DIR=""` (deploy skipped in subproject mode, §4.3). Arc 1 does NOT assert subproject module deploy works.

**The required Arc-2-gating probe (for VERA/whoever runs it before Arc 2+ subproject reliance):** in a real subproject layout, have a subproject-tier orchestrator dispatch a sub-agent with `Read .claude/modules/<X>.md` and confirm the path resolves to the SUBPROJECT's `.claude/modules/` (not the parent's, not a failure). Only after that probe passes does the subproject DEST wiring get added (and the choice of whether modules deploy per-subproject or are read from the parent gets made on the probe's evidence). Until then, Arc-2 subproject orchestrators MUST use CHANNEL 1 (inline) or CHANNEL 3 (bw) for module-equivalent content, NOT CHANNEL 2 (disk module by subproject path).

**Where this is tracked:** this section + a `follow_ups` entry in the verdict + (recommend) a bw ticket under the epic so Arc 2 cannot start subproject module work without seeing it.

---

## 7. Disciplines applied

- **§6.5 heartbeat / read-before-write:** followed throughout this dispatch (dispatch-entry beat + state-transition beats; read-before-write `bw show` before each `bw comment`).
- **§6.6 credential discipline:** N/A — no credentialed op in scope (see P10). The design proposes no CLI call against any tokened service; install.sh writes local files only.
- **§6.7 PRINCIPAL-gate:** the brief contains NO PRINCIPAL-gating clause for Arc 1 (mechanism-add, peer-approved by POLYBIUS in the epic thread; the r4/r5/r1-r6 dispositions are PLINY decisions relayed in the dispatch brief, already ratified upstream and CITED, not re-litigated). No new PRINCIPAL gate introduced. **Probe-design sub-case (§6.7 / op-disc §25.5):** P2/P3/P4/P5/P8 mutate a workspace; the probe spec names the **throwaway-clone pattern** (`git clone --no-local` / scratch `--project-dir`) so VERA never mutates a real operator workspace — the catch-point for that sub-case is DAEDALUS at design time, named here (§5 preamble) rather than left to a blanket clause.
- **§6.8 canonical-template alignment:** this design contains the op-disc §33 outline ONCE (§3.B), the routing-map template ONCE (§3.E-1), the relocation-index template ONCE (§3.E-2), and each install.sh wiring block ONCE (§4) — no two BYTE-IDENTICAL inline copies of the same canonical template within this design, so the within-design byte-alignment `diff` gate (§6.8) does not apply. The §33 outline in §3.B is an OUTLINE/spec, not a second verbatim copy of a template that also appears elsewhere in this file. Flagged so ARGUS can confirm the gate is correctly judged N/A rather than skipped. (Note: the two install.sh staleness/deploy globs in §4.5/§4.6 are different blocks for different purposes, not two copies of one template.)
- **§8 authorship:** the only author-bearing addition is this design's `Author: Denson Smith` header + the README's content (which carries no author frontmatter — substrate reference prose, consistent with existing templates/*.md which carry no author field). No author-like field is set to anyone but the PRINCIPAL. install.sh's existing seat-identity Co-Authored-By trailer (op-disc §28) is applied at commit by the building seat, not by this design.

---

## 8. Out of scope (Arc 1 deliberately does NOT do)

- **Any role-file content cut / slimming.** Arc 2 (POLYBIUS cut) territory across all three classes. Refinement 2: composition layer only, clean diff. (P9 guards this.) Arc 1 DEFINES the three lossless homes; Arc 2 EXECUTES the moves.
- **Executing any PROVENANCE archive or DUPLICATE delete.** Arc 1 defines the conventions + templates + names the targets (§3.C, §3.H); Arc 2 runs the `bw attach`/`bw comment` archives and the dupe-deletes.
- **Populating any orchestrator's routing map OR relocation index.** Arc 1 ships both conventions + both templates; POLYBIUS's actual rows are Arc 2.
- **Creating content for any of the 5 CONDITIONAL taxonomy modules.** NAMED only (Decision H-1).
- **The enforcement layer** (hooks that verify the routing map / relocation index fired; the checker agent). stoa--xyb.5 / Arc 3. The formats are designed to be hook-checkable (Decision E) but Arc 1 builds no hook.
- **Subproject-tier module deploy + path resolution.** TRACKED Arc-2-gating open question (§6); Arc 1 wires user + project tiers only.
- **Migrating MAJOR_PLINY's existing dispatch-brief injections** (§5.2 ADA preamble etc.) into the module model. They are the PRECEDENT this formalizes; rewiring them is not Arc 1.
- **`--no-modules` opt-out flag.** Deliberately omitted (mirrors skills).
- **stoa--2i5** (install.sh gitignore for transient paths) — peer Refinement 2 keeps it OUT of Arc 1 (distinct concern, standalone arc).
- **The Anthropic Skill mechanism** — stoa--xyb.1 settled bw/disk/dispatch via Bash/Read; modules use Read, not the Skill tool. The skill-grant findings (stoa--xyb.2) govern any FUTURE Skill use, not this layer.

---

## 9. Self-assessed weak points (load-bearing for the ARGUS re-audit)

1. **The glob deploy + completeness probe trades the array's silent-deploy-gap for a different (smaller) failure surface (Decision A / r4).** Glob eliminates the authored-but-not-arrayed silent gap (the r4 win) — but it introduces its own edge: a non-module `*.md` accidentally dropped into `substrate/modules/` (e.g. a stray note) would deploy as a real module with no gate stopping it, because the glob deploys whatever matches `*.md`. The mitigation is the staleness scan (which flags dest files not in source) but NOT a source-side "is this a real module" gate. **Why this shape anyway:** PLINY decided glob (r4), and the failure mode is symmetric-and-smaller than the array's (a stray source file deploying is more visible — it shows in the enumerated deploy log P4 checks — than a real module silently NOT deploying, which produced no signal at all). The convention "only real modules live in `substrate/modules/*.md`" is the same single-dir discipline that governs `templates/` and `skills/`. ARGUS should weigh whether a source-side module-shape gate (e.g. a required frontmatter marker) is worth adding now or is over-engineering for a one-file Arc-1.

2. **The PROVENANCE C-1/C-2 split assumes the Arc-2 cutter can reliably tell "already-in-bw" from "not-yet-in-bw" (Decision C).** I designed two sub-cases: delete-and-cite (C-1, when a bw ticket is already named) vs archive-then-cite (C-2, when no bw home exists). The split is only lossless if Arc 2 correctly classifies each provenance block — and "is this story already captured in the cited ticket, or does the inline prose carry detail the ticket lacks?" is a judgment call, not a mechanical test. A C-1 classification that is wrong (the ticket does NOT actually carry the full inline story) would drop content. **Why this shape anyway:** the alternative (archive EVERYTHING via C-2, even already-in-bw content) would duplicate content into bw attachments redundantly and bloat the beadwork ref. The C-1/C-2 split matches the .3 method's "CITED not inlined" intent and the empirical reality that most provenance ALREADY names its ticket (§16.6/§16.7/§4 all do). The safeguard I can name: Arc 2's lossless-on-canon probe should, for each C-1 deletion, confirm the cited ticket actually contains the deleted detail (a `bw show <id>` content-check) before the inline prose is removed — that turns the judgment call into a checkable gate. ARGUS should flag whether that per-deletion bw-content-check belongs in THIS design (as an Arc-2 probe-requirement) or is Arc 2's to specify.

3. **The relocation index (audit-time) and routing map (dispatch-time) being two separate always-loaded tables adds a second always-loaded structure to the very core the epic wants to shrink (Decision E / r2).** I split them deliberately (the merge is what made PROVENANCE/DUPLICATE inexpressible in rev1) — but two inline tables in orchestrator core is more always-loaded content than one. For an orchestrator whose core the epic is trying to slim, "now carry TWO index tables forever" is a real cost. **Why this shape anyway:** the relocation index is the lossless-recovery mechanism for ~360 lines (PROVENANCE + DUPLICATE) being removed from core — a few dozen always-loaded index rows to enable removing hundreds of always-loaded content lines is a strongly net-negative line count, which is the whole debloat thesis. And REFINEMENT 1 mandates the index stays in core. ARGUS should sanity-check that the index rows themselves stay terse (one line each) so the index does not re-bloat what the cut removed — and whether the two tables could share one physical table with a `class` column distinguishing dispatch-time vs audit-time rows (I judged separate-tables clearer for the orchestrator reading its own core, but it is a defensible merge that would halve the table-count cost; this is the Decision-E call I am least certain about).

---

## 10. Provenance + cross-refs

- Composition-layer spec: `bw show stoa--xyb.4` (primary input).
- 3-bucket method + 3-tier content: `bw show stoa--xyb.3`.
- CLI-not-MCP (delivery channels = Bash/Read/bw): `bw show stoa--xyb.1`.
- Skill-grant / agent-caching / no-real-agent findings: `bw show stoa--xyb.2`.
- Prior design + ARGUS verdict (this rev2's direct inputs): `agents/design/arc-44/design-rev1.md`; `agents/verdicts/stoa--xyb.4/ARGUS-2026-05-23T06-11-21Z.md`.
- bw archive primitive for PROVENANCE (Decision C): MAJOR_POLYBIUS.md §16.8 (`bw attach`).
- DUPLICATE consolidation target (Decision H-3): operating-disciplines.md §12 (bw cookbook keep-home); dupes at MAJOR_POLYBIUS.md §7.3 + MAJOR_PLINY.md §6.1.
- op-disc §33 insertion anchor (Decision §4.0 / r3): operating-disciplines.md §32 ends L2087; insert before `## Agent-regime inverses` (L2089).
- Dispatch-brief precedent (the primitive this formalizes): MAJOR_PLINY.md §5.2 / §5.2.1.
- install.sh deploy-class idioms grounded against: substrate/install.sh templates class (SRC_TEMPLATES_DIR L104, deploy L770-783, staleness L961-985) / skills class (L789-810) / nullglob single-segment-glob idiom (staleness L970, L989).
- r5 subproject path-resolution web check (2026-05-23): claude-code issues #24987 / #2571 lineage / #4754 / #15627 / #18200 / #11374.
- Peer constraints (REFINEMENT 1 routing-map/index-in-core; REFINEMENT 2 composition-layer-only-clean-diff): MAJOR_POLYBIUS approval comment on stoa--xyb, 2026-05-23T05:52:53Z.
