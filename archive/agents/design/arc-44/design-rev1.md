# Arc 44 (debloat Arc 1) — Composition-layer mechanism — design-rev1

Author: Denson Smith
Seat: CAPTAIN_DAEDALUS_the-stoa (ARCHITECT)
Ticket: stoa--xyb.4 (composition layer) | Epic: stoa--xyb | Arc: 44 (debloat Arc 1)
Inputs consumed: stoa--xyb (epic), stoa--xyb.1 (CLI-not-MCP), stoa--xyb.2 (skill-grant/caching/no-real-agent findings), stoa--xyb.3 (3-bucket method + 3-tier content), stoa--xyb.4 (composition-layer spec — primary)
Shipped files grounded against: substrate/install.sh (1199 lines), substrate/operating-disciplines.md (2110 lines, 32 numbered sections), substrate/MAJOR_POLYBIUS.md (§5/§10/§11/§12/§14 = Arc 2 relocation targets), .claude/ deployed layout.

---

## 1. Problem restatement

Build the **composition-layer mechanism only** — the framework that lets an orchestrator (POLYBIUS / PLINY) deliver instruction modules to a sub-agent **at dispatch time**, so that conditional/reference content can later be relocated OUT of the always-loaded role-file path without losing it. This is debloat **Arc 1**: it ADDS mechanism, it does not CUT any role-file content (that is Arc 2, the POLYBIUS cut, which USES this mechanism).

Concretely, Arc 1 ships:
- a new substrate source directory `substrate/modules/` whose contents `install.sh` deploys to `<DEST>/.claude/modules/`;
- one real deployable file in it — `substrate/modules/README.md` — which is both (a) the canon home for the detailed module-authoring procedure + the 3-channel delivery reference + the planned Arc-2 taxonomy, and (b) the live proof that the install.sh wiring works (deploy → `.claude/modules/README.md` exists);
- a thin, always-loaded rule + a **routing-map convention** added to `substrate/operating-disciplines.md` (new §33), kept minimal because op-disc is the worst bloat offender;
- the install.sh wiring (a `MODULE_NAMES` deploy class consistent with the existing `TEMPLATE_NAMES` / `SKILL_NAMES` idioms, including the source-existence check, the deploy step, and the staleness-scan entry).

**Imported assumptions named (per §6.1 — a restatement that hides imported scope has smoothed it):**

- **IA-1 (routing map = orchestrator-only operational core).** REFINEMENT 1 (peer-mandated) says the routing map / module index stays in always-loaded operational core and is NEVER relocated to a module. I read "operational core" as **the orchestrator role files' operational core** (MAJOR_POLYBIUS.md / MAJOR_PLINY.md), because the routing map is an orchestrator concern — leaf CAPTAINs receive modules, they do not route. The §33 op-disc rule therefore documents the *convention* (format + the must-stay-in-core rule) universally; the *populated* routing map lives inline in each orchestrator's core, authored per-orchestrator (POLYBIUS's actual entries are Arc 2). Arc 1 ships the convention + a worked template, not any orchestrator's populated map.
- **IA-2 (Arc-1 testability bar = wiring + consistency, NOT lossless-on-canon).** The brief states Arc 1 ADDS mechanism, so LOSSLESS-ON-CANON is not Arc 1's bar (that is Arc 2's bar). Arc 1's bar is: the deploy wiring fires, the README deploys, and the canon is internally consistent. I design VERA probes to that bar (§7).
- **IA-3 (taxonomy named, not populated).** Arc 1 NAMES the module filenames Arc 2 will populate (so Arc 2 is a clean fill-in) but creates NO content file for them. The only real content file Arc 1 creates under `substrate/modules/` is `README.md`. This keeps the Arc-1 diff clean and avoids shipping empty stubs that would deploy as zero-value files.
- **IA-4 (deploy-class = explicit manifest array, not glob).** Decision A below; flagged here because it is an imported judgment call the brief explicitly left to me.

This restatement converges with the brief. No divergence requiring a `refused`. The four imported assumptions are scope-clarifications, not re-scopings.

---

## 2. Approach (the design's shape)

The composition layer is **not new primitive** — it formalizes a primitive PLINY already uses (dispatch briefs already inject task context: MAJOR_PLINY §5.2 ADA preamble, §5.2.1 credential cite, "run bw start <id>"). Three delivery channels, all using tools every agent already has (Bash / Read / bw — no Skill grant, no MCP, per stoa--xyb.1):

```
                     ORCHESTRATOR (POLYBIUS / PLINY)
                     carries inline in slim core:
                     ┌─────────────────────────────┐
                     │  ROUTING MAP (always-loaded) │  <- §33 convention; never a module
                     │  task-type -> module(s)      │
                     └──────────────┬──────────────┘
                                    │ at dispatch time, selects + names
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                       ▼
   CHANNEL 1: inline       CHANNEL 2: disk module   CHANNEL 3: bw ticket
   in dispatch prompt      .claude/modules/X.md      bw show <id>
   (small, task-specific)  via Read                  (dynamic / bespoke /
                           (stable, reused)           must-persist)
                                    │
                                    │  recurrence in the bw custom-instruction
                                    │  stream (CHANNEL 3 record) is the SIGNAL
                                    └─ to author a reusable disk module (CHANNEL 2)
```

The mechanism has four parts. Three are built in Arc 1; the fourth (orchestrators' populated routing maps) is Arc 2+.

### 2.1 The deploy class (`substrate/modules/` → `.claude/modules/`)

A new install.sh-managed file class, wired exactly parallel to the existing `TEMPLATE_NAMES` class (templates are the closest sibling: shared tooling, agent-read, deployed unsuffixed at every tier). See Decision A (§3.A) for the explicit-array-vs-glob choice and §4 for the line-level wiring spec.

### 2.2 The canon split (dogfooding the 3-tier model on ourselves)

Per the method, operational core = the rule stated crisply (always loaded, small); reference = detailed procedure (on-demand). We apply this to the composition canon **itself**:

- **operational core (always loaded):** `substrate/operating-disciplines.md` **§33** — a thin rule (~25-35 lines): "instructions are a composable module library; orchestrators deliver via 3 channels; the routing map stays inline in orchestrator core; recurrence in the bw log → author a disk module" + a pointer to the on-demand README for the detail.
- **reference (on-demand):** `substrate/modules/README.md` — the detailed authoring procedure, the full 3-channel selection reference, the routing-map worked template, and the planned Arc-2 taxonomy. This file is itself a disk module (it lives in `.claude/modules/` after deploy), so the canon's detail is loaded the same way every other module's detail is loaded. That is the dogfood: the composition layer's own documentation rides the composition layer's own channel.

This split is the load-bearing structural choice. It is what keeps the op-disc addition minimal (the brief's hard constraint: op-disc is the 2110-line worst offender; what we ADD must be a thin rule + pointer).

### 2.3 The routing-map format

A small structured markdown table the orchestrator carries inline in its slim core (Decision D, §3.D). Format + worked template defined there; POLYBIUS's populated entries are Arc 2.

### 2.4 Module-authoring discipline

The recurrence rule: bw is the record of every custom instruction an orchestrator emits (CHANNEL 3); when an instruction recurs across dispatches, that recurrence is the signal to promote it to a disk module (CHANNEL 2). bw FEEDS the library; it is not the library. Canon home: README §3 + a one-line statement in op-disc §33 (Decision E, §3.E).

---

## 3. Concrete decisions (A–G) — enumerated + decided

### Decision A — Module source + deploy path, and the deploy-class mechanism

**Decided:** Source `substrate/modules/` → deployed `<DEST>/.claude/modules/`. Wire via an **explicit manifest array** `MODULE_NAMES=(README.md)`, NOT a glob over `substrate/modules/*.md`.

**Why explicit array over glob:**
1. **Consistency with shipped idioms is the brief's hard constraint.** install.sh manages every file class via an explicit array (`TEMPLATE_NAMES`, `CAPTAIN_NAMES`, `SKILL_NAMES`) plus a source-existence pre-check loop (L619-633). There is zero glob-driven deploy class in the shipped script. A glob would be the *only* glob-driven class and would break the §5.7 smoke-beat check pattern (the existence-check loop that every other class has).
2. **The smoke-beat check needs a manifest.** The brief calls out (Decision F + cross-cutting) that any new install.sh-managed file class needs deploy-plan wiring VERA/CATO can verify. An explicit array gives VERA a concrete invariant to probe ("`MODULE_NAMES` contains README.md AND the source file exists AND it deploys"); a glob gives only "whatever happened to be in the dir," which is unprobeable as a contract.
3. **The growing-library counter-argument is real but loses here.** A glob favors a growing module library (Arc 2+ adds modules without touching install.sh). But the manifest cost is one line per module per arc that adds modules — trivially cheap, and it is the SAME edit-the-array discipline that already governs every CAPTAIN/template/skill addition. The manifest also doubles as the canonical inventory (a reader can see every shipped module in one array), which a glob cannot give. The deferred cost (editing the array in Arc 2) is named in §8 as a weak point but is judged acceptable against the consistency + probeability wins.

**Wiring shape (parallel to TEMPLATE_NAMES — full line-level spec in §4):** add `SRC_MODULES_DIR`, `MODULE_NAMES`, a source-existence check loop, a deploy step (cp, unsuffixed — modules are shared tooling like templates), and a staleness-scan entry. Modules deploy at **all three tiers** (user/project/subproject) — like skills, because Claude Code Read-resolves `.claude/modules/X.md` relative to the active workspace, not a parent; a subproject must carry its own copy. (Contrast templates, which subproject mode skips because subproject reads the parent's templates — but modules are Read-by-path from dispatch, and the dispatch names a path relative to the active project, so each tier needs its own. This mirrors the SKILL_NAMES "always deploy at every tier including subproject" reasoning at install.sh L57-60 / L785-790.)

**No `--no-modules` opt-out flag.** Mirrors skills (always deployed, no opt-out): a deployed substrate that omits modules leaves orchestrators unable to Read the modules their routing map points at. One real file (README) makes the deploy near-free.

### Decision B — Where the composition canon lives (dogfood the method on itself)

**Decided:** Two homes, split by access tier (per §2.2):
- **`substrate/operating-disciplines.md` §33 (NEW, ~25-35 lines, operational core):** thin rule + routing-map-stays-in-core convention + a pointer to the README. Universal-team layer (op-disc is the universal doc all seats read).
- **`substrate/modules/README.md` (NEW, the only Arc-1 content file under modules/, on-demand reference):** the detailed authoring procedure, the full 3-channel selection reference, the routing-map worked template, the module-authoring discipline, and the planned Arc-2 taxonomy.

**Exact §33 content outline (kept minimal — this is what we ADD to the worst offender):**
```
## 33. Composition layer — instruction modules + orchestrator routing

[~2 sentences] Instructions are a composable library, not all-memorized. An
orchestrator selects what a task needs and delivers it AT DISPATCH TIME via
3 channels — all using tools every agent already has (no Skill grant, no MCP;
see stoa--xyb.1):
  - inline in the dispatch prompt — small, task-specific.
  - disk module `.claude/modules/<X>.md` via Read — stable, reused.
  - bw ticket via `bw show <id>` — dynamic / bespoke / must-persist.

ROUTING MAP (load-bearing — stays in orchestrator operational core, NEVER a
module): each orchestrator carries a small inline task-type -> module(s) table
in its always-loaded core. An index that must itself be loaded-on-demand never
fires. Format + worked template: `.claude/modules/README.md` §4.

AUTHORING SIGNAL: the bw custom-instruction stream is the RECORD, not the
library. Recurrence in that record -> author a reusable disk module.

Full authoring procedure, channel-selection guidance, and the module taxonomy:
`.claude/modules/README.md` (on-demand — read when authoring or relocating a
module).

[Cross-refs block: cite-at-read-site comments + bullet list per the op-disc
§32 cross-ref convention — point to modules/README.md, MAJOR_PLINY §5.2
(dispatch-brief precedent), stoa--xyb.4 (provenance), stoa--xyb.1 (CLI-not-MCP).]
```

**Why this split and these exact homes:**
- op-disc §33 is the right home for the *convention* because op-disc is the universal-team doc — both orchestrators and the convention's readers (anyone authoring a module) read it. Putting the thin rule here (not in a single orchestrator file) means it is stated once for the whole team.
- README is the right home for the *detail* because the detail is conditional (read only when authoring/relocating a module), which is exactly the access pattern the 3-tier model assigns to on-demand reference. Dogfooding: the composition layer documents itself via its own disk-module channel.
- The routing map's POPULATED form goes in each orchestrator's core (not op-disc, not README), per IA-1 — but Arc 1 ships only the convention + template, not any populated map.

### Decision C — The 3 delivery channels + selection guidance (canon in README)

**Decided:** Document all three as canon in README §2, with this selection guidance:

| Channel | Mechanism | Use when | Persists? |
|---|---|---|---|
| 1. inline | text in the dispatch prompt | small, task-specific, one-off instruction the orchestrator composes fresh | only in that dispatch payload |
| 2. disk module | `.claude/modules/<X>.md` via `Read <path>` | stable instruction reused across tasks/projects; orchestrator names the path in the dispatch | yes — versioned in substrate |
| 3. bw ticket | `bw show <id>` | dynamic / bespoke / single-use, OR anything that must persist or be shared across seats | yes — in bw, sharing-topology we control |

**The bw-feeds-the-library note (load-bearing, from stoa--xyb.4):** bw one-offs are NOT a curated library — they are the routine custom-instruction stream the orchestrator generates constantly, retained for record-keeping (audit trail of what each agent was told). Recurrence in that record is the SIGNAL to author a CHANNEL-2 disk module. README §2 states this explicitly so the channels are not misread as "bw = the module store."

**Compaction-proofness (the channel's reason for existing, from stoa--xyb.4):** selection rides the dispatch payload, delivered fresh at spawn — so a sub-agent always gets its modules even though its own context may later compact. README §2 names the known weak spot too (a sub-agent that compacts mid-task has no orchestrator re-telling it; mitigation = keep sub-agent tasks bounded — ties to the future enforcement layer, stoa--xyb.5).

### Decision D — The routing-map format (inline structured table + worked template)

**Decided:** A markdown table in the orchestrator's slim core. Columns: **task-type → module(s) to load → channel**. Worked template (goes in README §4; this is the FORMAT + example, NOT POLYBIUS's real entries):

```markdown
### Routing map (orchestrator core — always loaded)

| Task type | Module(s) to load | Channel |
|---|---|---|
| <onboard a new project>      | `onboarding.md`            | disk (Read) |
| <spawn a sub-project>        | `sub-project-spawning.md`  | disk (Read) |
| <author a pair-programmer>   | `pair-programmer-authoring.md` | disk (Read) |
| <one-off bespoke task>       | (compose inline)           | inline |
| <must-persist shared spec>   | `bw show <ticket-id>`      | bw |
```

**Properties the format is designed for:**
- **Inline + always-loaded** (per IA-1 / REFINEMENT 1): it is a small table, cheap to keep ambient.
- **Checkable** (per stoa--xyb.4: "should itself be checkable"): a future enforcement-layer hook (stoa--xyb.5) can parse the table and verify that, for a given dispatched task-type, the expected module path was actually referenced in the dispatch. The table's regular column shape (task-type / module / channel) is what makes that hook-parseable. Arc 1 does NOT build the hook — it designs the format so the hook is possible.
- **Module names are paths relative to `.claude/modules/`** so the orchestrator's dispatch can name `Read .claude/modules/<X>.md` directly.

POLYBIUS's actual routing-map rows are authored in Arc 2 (when its conditional sections become modules). Arc 1 ships the empty-shaped template + the example above.

### Decision E — Module-authoring discipline (recurrence → author a module)

**Decided:** Canon in README §3, one-line echo in op-disc §33. The rule: an orchestrator emits custom instructions constantly (CHANNEL 3, retained in bw for record-keeping). When the SAME instruction recurs across multiple dispatches, that recurrence is the trigger to promote it to a CHANNEL-2 disk module under `substrate/modules/` (and add it to `MODULE_NAMES` + the routing map). README §3 gives the concrete procedure:
1. Notice recurrence in the bw custom-instruction record.
2. Author `substrate/modules/<name>.md` (the reusable form).
3. Add `<name>.md` to install.sh `MODULE_NAMES`.
4. Add a routing-map row (task-type → `<name>.md` → disk) to the relevant orchestrator's core.
5. Redeploy via install.sh.

This is the accretion path that GROWS the module library over time — and the reason the explicit-manifest cost (Decision A) is acceptable: step 3 is one line, paid once per promoted module.

### Decision F — End-to-end testability (Arc 1 must be VERA-testable NOW)

**Decided:** `substrate/modules/README.md` is a real deployable file, so the full deploy path is exercisable today even though no conditional content has moved yet. VERA probe spec in §7. The §5.7 smoke-beat (any new install.sh-managed file class needs deploy-plan wiring) is satisfied by Decision A's manifest + existence-check + deploy-step + staleness-scan, all of which §7 probes.

### Decision G — Anticipate Arc 2 (name the taxonomy, build none of it)

**Decided:** Name the planned module filenames in README §5 + as commented routing-map rows, so Arc 2 is a clean fill-in. Mapping to MAJOR_POLYBIUS.md shipped section headers (grounded against the actual file, not the brief's labels):

| Planned module file | Relocates MAJOR_POLYBIUS § (shipped header) | Arc-1 status |
|---|---|---|
| `onboarding.md` | §5 Onboarding flow | NAMED only |
| `sub-project-spawning.md` | §10 Sub-project spawning | NAMED only |
| `pair-programmer-authoring.md` | §11 Pair-programmer Major authoring | NAMED only |
| `pair-programming-prototyping.md` | §12 Pair-programming-for-prototyping methodology (Mode 2) | NAMED only |
| `substrate-update-check.md` | §14 Substrate-update check (daily cadence) | NAMED only |

**Drift flag (per cross-cutting "shipped files are canon"):** the brief labeled §11+§12 jointly as "pair-programmer (~168)". The shipped file has them as TWO distinct sections (§11 authoring; §12 prototyping methodology). I taxonomize them as TWO modules (`pair-programmer-authoring.md` + `pair-programming-prototyping.md`) to give Arc 2 separable homes; if Arc 2 finds them tightly coupled it may merge to one — that is Arc 2's call. Either way the homes are adequate (the cross-cutting bar: "design the taxonomy so Arc 2's cut CAN be lossless" — two homes is a superset of one). NO content files for any of these are created in Arc 1.

---

## 4. install.sh wiring — line-level build spec (for ADA)

All additions parallel the existing `TEMPLATE_NAMES` class. Reference line numbers are from the shipped substrate/install.sh.

**(4.1) Source path + manifest array** — after `SRC_SKILLS_DIR` (L105) and after the `TEMPLATE_NAMES` array (L109-117), add:
```bash
SRC_MODULES_DIR="${SCRIPT_DIR}/modules"

# Instruction-module library (Arc 44 / stoa--xyb.4). Composable on-demand
# reference content an orchestrator names in a dispatch (Read .claude/modules/<X>.md)
# or that the team reads when authoring/relocating modules. Deployed unsuffixed
# at every tier (shared tooling, like skills); each tier needs its own copy
# because Read resolves the path relative to the active workspace, not a parent.
MODULE_NAMES=(
  README.md
)
```

**(4.2) Source-existence check** — after the skills existence loop (L629-633), add a modules loop in the same shape:
```bash
[ -d "$SRC_MODULES_DIR" ] || err "source modules directory not found: $SRC_MODULES_DIR"
for mname in "${MODULE_NAMES[@]}"; do
  [ -f "${SRC_MODULES_DIR}/${mname}" ] || err "source module not found: ${SRC_MODULES_DIR}/${mname}"
done
```

**(4.3) DEST var** — in each of the three `case "$TARGET"` arms (L531-607), add a `DEST_MODULES_DIR` alongside the existing `DEST_SKILLS_DIR`:
- user: `DEST_MODULES_DIR="${HOME}/.claude/modules"`
- project: `DEST_MODULES_DIR="${PROJECT_DIR}/.claude/modules"`
- subproject: `DEST_MODULES_DIR="${PARENT_DIR}/${SUBPROJECT}/.claude/modules"`

**(4.4) Plan line** — in the plan block (near L661 "deploy skills"), add:
```bash
echo "  deploy modules   : yes (${#MODULE_NAMES[@]} module(s) to ${DEST_MODULES_DIR})"
```

**(4.5) Deploy step** — add a new step **5b** after the skills deploy (after L826), modeled on the templates deploy (cp, not the skills cp -R, because modules are flat files not subtrees):
```bash
# 5b. Deploy instruction modules (Arc 44; always — no opt-out, mirrors skills).
# Flat .md files, deployed unsuffixed at every tier. cp overwrites in place
# (idempotent for unchanged source).
if [ ! -d "$DEST_MODULES_DIR" ]; then
  run_or_print "mkdir -p \"$DEST_MODULES_DIR\""
else
  log "modules directory already exists: $DEST_MODULES_DIR"
fi
for mname in "${MODULE_NAMES[@]}"; do
  src="${SRC_MODULES_DIR}/${mname}"
  dest="${DEST_MODULES_DIR}/${mname}"
  run_or_print "cp \"$src\" \"$dest\""
done
```
ADA decision point flagged for the build: place 5b BEFORE step 6 (CLAUDE.md append) so the numbered step order stays monotonic, OR keep it adjacent to skills as 5b. Either is fine; the design prefers 5b adjacent to skills (step 5) since modules are a sibling shared-tooling class.

**(4.6) Staleness scan** — add a modules block in the staleness section (after the skills scan, ~L1013), in the file-only single-segment-glob shape used by templates (NOT recursive — preserves any future base-vs-custom scoping):
```bash
if [ -d "$DEST_MODULES_DIR" ]; then
  shopt -s nullglob
  for f in "${DEST_MODULES_DIR}"/*; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    found=0
    for m in "${MODULE_NAMES[@]}"; do
      if [ "$m" = "$base" ]; then found=1; break; fi
    done
    if [ "$found" -eq 0 ]; then obsolete_files+=("$f"); fi
  done
  shopt -u nullglob
fi
```

**(4.7) Header doc-comment** — update the top-of-file usage comment (L13-20 region) to mention the modules deploy in the one-line inventory, parallel to how skills/templates are described. Small prose-only edit.

**Manifest writer (write_substrate_manifest, L396-456):** modules carry NO `{{NAME_SUFFIX}}` / `{{USER_TIER_DIR}}` substitution (they are unsuffixed flat content like templates, and templates are NOT in the manifest). So **no change to write_substrate_manifest is needed** — modules, like templates, are deployed verbatim and need no substitution record. Flagged for ADA/CATO: confirm templates are absent from the manifest writer (they are — only MAJORs + CAPTAINs are recorded), and keep modules consistent with templates (verbatim, no manifest entry).

---

## 5. Verification probes (for VERA — re-executable)

All probes run from the worktree root unless noted. Probes target the Arc-1 bar (wiring + deploy + consistency), not lossless-on-canon (IA-2).

**P1 — source file exists.** `test -f substrate/modules/README.md` → exits 0. (The one real content file.)

**P2 — install.sh dry-run shows the module deploy.** Run `bash substrate/install.sh --target project --project-dir <throwaway-clone> --dry-run` and confirm stdout contains both a `deploy modules` plan line AND a `[dry-run]` cp line for `modules/README.md`. (Use a throwaway clone per §6.5 below — do NOT dry-run against a real workspace even though --dry-run writes nothing; the user-tier path triggers interactive prompts. Use `--target project` with a throwaway dir to keep it non-interactive.)

**P3 — real deploy lands the README.** Against the same throwaway clone, run install.sh WITHOUT --dry-run (`--target project --project-dir <clone>`), then `test -f <clone>/.claude/modules/README.md` → exits 0.

**P4 — manifest array contains README.md.** `grep -q 'README.md' <(sed -n '/MODULE_NAMES=(/,/)/p' substrate/install.sh)` → exits 0. (Confirms the explicit-manifest invariant from Decision A.)

**P5 — source-existence check fires on a missing module.** Temporarily reference a nonexistent module in a COPY of install.sh (or assert by inspection) — the existence-check loop must `err` if a `MODULE_NAMES` entry has no source file. VERA may verify by code-reading §4.2 is present rather than mutating the script. (Probe is "the existence check exists and matches the TEMPLATE_NAMES shape," not a destructive run.)

**P6 — op-disc §33 exists and is thin.** `grep -q '^## 33\. Composition layer' substrate/operating-disciplines.md` → exits 0; AND the section is ≤ ~40 lines (sed the §33→§34/EOF range, `wc -l` ≤ 40). Enforces the "minimal addition to the worst offender" constraint.

**P7 — canon internal consistency (the three homes agree).** Confirm: (a) op-disc §33 points to `.claude/modules/README.md`; (b) README documents exactly the 3 channels named in §33; (c) the 5 taxonomy module names in README §5 match the Arc-2 mapping table (§3.G). VERA reads all three and confirms no contradiction (no channel named in one but missing in another; no taxonomy name drift).

**P8 — staleness scan covers modules.** Confirm a modules block exists in the staleness section (code-read of §4.6 presence) AND that a deployed `.claude/modules/` with an extra non-manifest file would be listed as obsolete (optional dynamic check against the throwaway clone: drop a `bogus.md` into `<clone>/.claude/modules/`, re-run install.sh, confirm `bogus.md` appears in the "Obsolete files detected" output).

**P9 — no role-file CONTENT was cut (Arc-1 clean-diff guard).** `git diff --stat arc-44/build` against the branch point must show ADDITIONS to install.sh + op-disc + the new modules/README.md + this design file ONLY — NO deletions from MAJOR_POLYBIUS.md / MAJOR_PLINY.md / any CAPTAIN file. This is the Refinement-2 "composition layer only, clean diff" guard, made probeable. (Permitted edits: install.sh wiring, op-disc §33 addition, the new modules/ dir, this design artifact. Any deletion from a role file = Arc-1 scope violation.)

**P10 — credential/CI structure (per §6.6):** N/A — this design touches NO credentialed third-party op (install.sh deploys local files; no API token, no cloud service). Stated explicitly so VERA can confirm the N/A rather than infer it.

---

## 6. Disciplines applied

- **§6.5 heartbeat / read-before-write:** followed throughout this dispatch (dispatch-entry beat + state-transition beats; read-before-write before each bw comment).
- **§6.6 credential discipline:** N/A — no credentialed op in scope (see P10). The design proposes no CLI call against any tokened service; install.sh writes local files only.
- **§6.7 PRINCIPAL-gate:** the brief contains NO PRINCIPAL-gating clause for Arc 1 (it is a mechanism-add, peer-approved by POLYBIUS in the epic thread). The settled decisions this design rests on (CLI-not-MCP stoa--xyb.1; routing-map-in-core REFINEMENT 1) are already PRINCIPAL-/peer-ratified upstream and CITED, not re-litigated. No new gate introduced. **One probe-design note (§6.7 / op-disc §25.5):** P2/P3/P8 mutate a workspace; the probe spec names the **throwaway-clone pattern** (`git clone --no-local` of the repo, or a scratch `--project-dir`) so VERA never mutates a real operator workspace — the catch-point for that sub-case is DAEDALUS at design time, and it is named here rather than left to a blanket "PRINCIPAL-discretion" clause.
- **§6.8 canonical-template alignment:** this design contains ONE inline copy of the op-disc §33 outline and ONE of the routing-map template and ONE of each install.sh wiring block — no two inline copies of the same canonical template within this design, so the within-design byte-alignment `diff` gate does not apply. (The op-disc §33 outline in §3.B is an OUTLINE/spec, not a second verbatim copy of a template that also appears elsewhere in this file.) Flagged so ARGUS can confirm the gate is correctly judged N/A rather than skipped.
- **§8 authorship:** the only author-bearing addition is this design's `Author: Denson Smith` header + the README's content (which carries no author frontmatter — it is substrate reference prose, consistent with the existing templates/*.md which carry no author field). No author-like field is set to anyone but the PRINCIPAL. install.sh's existing seat-identity Co-Authored-By trailer (per op-disc §28) is applied at commit by ADA, not by this design.

---

## 7. Out of scope (Arc 1 deliberately does NOT do)

- **Any role-file content cut / slimming.** Arc 2 (POLYBIUS cut) territory. Refinement 2: composition layer only, clean diff. (P9 guards this.)
- **Populating any orchestrator's routing map.** Arc 1 ships the convention + template; POLYBIUS's actual rows are Arc 2.
- **Creating content for any of the 5 taxonomy modules** (onboarding / sub-project / pair-programmer-authoring / pair-programming-prototyping / substrate-update-check). NAMED only (Decision G).
- **The enforcement layer** (hooks that verify the routing map fired; the checker agent). stoa--xyb.5 / Arc 3. The routing-map format is designed to be hook-checkable (Decision D) but Arc 1 builds no hook.
- **Migrating MAJOR_PLINY's existing dispatch-brief injections** (§5.2 ADA preamble etc.) into the module model. They are the PRECEDENT this formalizes; rewiring them is not Arc 1.
- **`--no-modules` opt-out flag.** Deliberately omitted (mirrors skills); revisit only if a module-free deploy mode is ever needed.
- **stoa--2i5** (install.sh gitignore for transient paths) — peer Refinement 2 explicitly keeps it OUT of Arc 1 (distinct concern, standalone arc).
- **The Anthropic Skill mechanism** — stoa--xyb.1 settled bw/disk/dispatch via Bash/Read; modules use Read, not the Skill tool. The skill-grant findings (stoa--xyb.2) govern any FUTURE Skill use, not this layer.

---

## 8. Self-assessed weak points (load-bearing for the ARGUS cold-audit)

1. **Explicit-manifest vs glob is a judgment call that could age poorly (Decision A).** I chose the explicit `MODULE_NAMES` array for consistency + probeability. The named cost: every Arc-2+ arc that adds a module must also add a line to `MODULE_NAMES` (and the routing map), and a builder who forgets the array line will ship a source file that never deploys (silent — no error, because the existence-check only fires for entries that ARE in the array). **Why this shape anyway:** it matches every other shipped deploy class exactly, and the smoke-beat probeability (P4) is worth more in a mechanism-defining arc than glob convenience; the forget-the-line risk is the same one that already governs CAPTAIN/template/skill additions, so it adds no NEW failure class. ARGUS should weigh whether a glob would better serve the *growing-library* thesis the whole epic is built on — this is the decision I am least certain about.

2. **The §33 thin-rule + README split could still under-serve "minimal addition to the worst offender."** I budgeted §33 at ~25-35 lines, but a cross-ref block in the op-disc §32 house style (cite-at-read-site comments + bullet list) can itself run 6-10 lines, pushing §33 toward 40. If ARGUS reads §33 as "still too much added to a 2110-line file," the cross-ref block is the first thing to trim (it could be a single pointer line instead of the full §32-style block). **Why this shape anyway:** op-disc's own §32 establishes the cross-ref-block convention; deviating from it for §33 would be its own inconsistency. The tension between "minimal" and "house-consistent" is real and I resolved it toward house-consistent — ARGUS should sanity-check that call against the debloat thesis.

3. **The routing-map "checkable" claim is asserted, not proven (Decision D).** I designed the table's regular column shape so a future enforcement hook CAN parse it, but Arc 1 builds no hook, so the checkability is a forward-looking design property I cannot demonstrate in Arc 1. If the table format I chose turns out to be awkward for the Arc-3 hook to parse (e.g., markdown table parsing in bash is fiddly), Arc 3 may need to revise the format — which would be a backward-incompatible change to a convention Arc 2 will have already populated. **Why this shape anyway:** a markdown table is the most human-readable inline format for the always-loaded core (the primary consumer is the orchestrator reading its own core), and deferring the exact machine-parse format to Arc 3 (when the hook is actually built) avoids over-designing a checker that does not exist yet. ARGUS should flag whether the format should be specified more rigidly NOW (e.g., a fixed delimiter) to protect Arc 2's population from an Arc-3 reformat.

4. **(lower confidence) Modules-deploy-at-every-tier-including-subproject may be wrong for subproject.** I reasoned modules deploy at all three tiers (like skills) because Read resolves relative to the active workspace. But templates DON'T deploy to subproject (subproject reads the parent's). If, in practice, an orchestrator's dispatch always names a module path relative to the PARENT (not the subproject), then subproject modules would be redundant duplicates. **Why this shape anyway:** the dispatch names `.claude/modules/<X>.md` and Claude Code Read resolves that against the active project root, so a subproject orchestrator dispatching a subproject CAPTAIN needs the module under the subproject's own `.claude/` — matching the skills reasoning (install.sh L57-60), not the templates reasoning. I am ~80% on this; ARGUS/VERA should confirm the Read-resolution-root assumption against actual Claude Code behavior (this is the kind of platform-behavior claim that warrants a web check or a live probe before Arc 2 relies on it).

---

## 9. Provenance + cross-refs

- Composition-layer spec: `bw show stoa--xyb.4` (primary input).
- 3-bucket method + 3-tier content: `bw show stoa--xyb.3`.
- CLI-not-MCP (delivery channels = Bash/Read/bw): `bw show stoa--xyb.1`.
- Skill-grant / agent-caching / no-real-agent findings: `bw show stoa--xyb.2`.
- Dispatch-brief precedent (the primitive this formalizes): MAJOR_PLINY.md §5.2 / §5.2.1.
- Substrate-component design principles (sibling framing): operating-disciplines.md §31.
- install.sh deploy-class idioms grounded against: substrate/install.sh `TEMPLATE_NAMES` (L109-117) / `SKILL_NAMES` (L142-151) / staleness scan (L904-1014) / next-step guidance (L1105+).
- Peer constraints (REFINEMENT 1 routing-map-in-core; REFINEMENT 2 composition-layer-only-clean-diff): MAJOR_POLYBIUS approval comment on stoa--xyb, 2026-05-23T05:52:53Z.
