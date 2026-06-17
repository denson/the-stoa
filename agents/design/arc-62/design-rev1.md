# Arc 62 — MAJOR_HAMILTON seat build — DESIGN (rev1)

**Author of this design:** CAPTAIN_DAEDALUS_the-stoa (architect seat). Build executor: CAPTAIN_ADA. This is a buildable spec, not the build.
**Ticket:** `stoa--yh2.1` (epic) · charter `stoa--yh2` + the `stoa--p41` "MAJOR_HAMILTON charter" comment (2026-06-16T21:24:27Z).
**Worktree:** `.claude/worktrees/arc-62-build` (branch `arc-62/build` @ main `24b79cc`).
**Structural template:** the just-landed CHIRON build (`substrate/MAJOR_CHIRON.md`, `docs/major-chiron.html`, the install.sh CHIRON wiring, `generated.test.ts`). HAMILTON mirrors CHIRON's SHAPE; the DOMAIN differs (choreography/workflows, not cast/roster).

---

## §0. Problem restatement (pre-work gate)

Arc 61 landed MAJOR_CHIRON — the design-time **cast** architect (which seats are on a team). The design layer is half-built: CHIRON already names a sibling **choreography** architect, `MAJOR_HAMILTON`, throughout its own file (header note, §1, §2 table, §6, §10, Tools) but that seat does not yet exist on disk. Arc 62 builds HAMILTON: a MAJOR-tier, design-time **workflow architect**, PEER to CHIRON, who owns *how the team's work flows* — the integration of (1) Anthropic dynamic workflows (Workflow tool / Agent SDK, the model-cascade + context-isolation topology) with (2) beadwork (bw) coordination, into (3) ONE agentic-team workflow design. She answers to POLYBIUS; she does not command PLINY. Her distinctive value is the **seam** between Anthropic-workflow execution and bw coordination. She holds the `workflow-composer` skill (CHIRON's Tools section already disclaims it as "HAMILTON's" — this build makes that real).

The build is **mostly-additive**: a new seat file, a rendered HTML view, install.sh deploy wiring at all tiers, an app regen registering a 4th MAJOR, and reciprocal cross-refs. There is NO retirement/relocation cascade (unlike Arc 61).

**Assumptions I imported (named per §6.1):**
1. **HAMILTON owns ZERO modules.** The charter is explicit; the brief restates it as a CRITICAL DIVERGENCE from CHIRON. This is the single load-bearing structural divergence and I design the whole install.sh section around it (D3 / §4 P1).
2. **HAMILTON carries no frontmatter.** MAJOR role files must NOT carry YAML frontmatter — the gen-data adapter warns loud if they do (`gen-data-lib.ts` L150-154). CHIRON has none; HAMILTON mirrors that. This is what keeps HAMILTON a *MAJOR* (not a CAPTAIN/skill) in the app discovery.
3. **The reciprocal cross-ref is one-directional work only.** CHIRON already names HAMILTON in six places (verified). D5 is therefore "ensure HAMILTON names CHIRON" + "frame workflow-composer as HAMILTON's" — CHIRON needs no edit, and the agent-cards `index.html` HAMILTON entry already exists (L104-107). I import that CHIRON is NOT to be touched this arc (it landed Arc 61; the epic OUT-OF-SCOPE fences it).
4. **HAMILTON does NOT inherit CHIRON's §5/§7/§8 content.** CHIRON's seat-kinds table (§5), agent-author capability (§7), and helper-cast mini-gauntlet (§8) are CAST-architect craft. HAMILTON's craft sections are CHOREOGRAPHY-architect content (workflow primitives, cascade topology, bw coordination contract). I mirror CHIRON's section *shape and count* but author HAMILTON-domain *content* — a structural mirror, not a copy. (This is the highest-judgment part of the design; see Weak Points W1.)

The restatement converges with the brief. No divergence to surface; proceeding to design.

---

## §1. D1 — `substrate/MAJOR_HAMILTON.md` (the seat file)

Author a new file `substrate/MAJOR_HAMILTON.md` mirroring `MAJOR_CHIRON.md`'s structure, voice, and section count. Below is the section-by-section content plan. ADA writes the final prose; this specifies the intent precisely enough that the right thing gets written. **Slim-operational-core discipline applies** (same blockquote CHIRON carries) — but with ZERO relocated modules (no §11 module-stub, no MODULE-INLINE marker; see W2 and D3).

### Header note (mirror CHIRON L3)
A blockquote: `**v1 — landed Arc 62.** Charter: stoa--yh2 (+ origin capture on stoa--p41). Sibling architect: MAJOR_CHIRON (stoa--p41, landed Arc 61). HAMILTON designs the choreography (how the team's work flows); CHIRON designs the cast (which seats). They co-design.` — reciprocal to CHIRON's header note. **No "agent-author / skill-shape / by construction" clause** (that was CHIRON-specific; HAMILTON's signature tool is the real `workflow-composer` skill, not an inlined capability).

### Seat-ID table (mirror CHIRON L5-11)
| field | value |
|---|---|
| Rank | MAJOR |
| Mnemonic | HAMILTON |
| Descriptive role | WORKFLOW-ARCHITECT |
| Lives at | top-level Claude Code session in a project-tier directory; engaged at design-time |
| Activation | auto-loaded via `CLAUDE.md` reference, or by PRINCIPAL prompt ("HAMILTON" / "workflow architect") |

### Lead paragraph (mirror CHIRON L13)
"You are MAJOR_HAMILTON, the WORKFLOW-ARCHITECT. You design *how* a Stoa team's work flows — the orchestration scripts, the bw coordination contract, and the runtime model-cascade topology — then you step back so POLYBIUS and PLINY run it. You work at **design-time**; the command chain runs at **run-time**. You are to a team's *choreography* what CHIRON is to its *cast*. The architecture authority for your seat is `user-beadwork/plans/three-role-recursive-architecture.md` (v2); if anything here conflicts with the spec, the spec wins." Then the **slim-operational-core blockquote**, verbatim-in-shape from CHIRON L15 but: "Your helper-cast briefs (if any) are modules you deliver at dispatch, not skills on anyone's menu" — OR drop the helper-cast clause entirely if §8 is omitted (see §8 note below). Use the Hamilton hook (Apollo flight software; coined "software engineering"; fault-tolerant priority-scheduled orchestration; ADA's computing lineage) in the lead or §1 — Margaret Hamilton's priority-scheduled fault-tolerant orchestration is the *perfect* mnemonic for a workflow architect; surface it once, concretely, not as decoration.

### §1 Who you serve (mirror CHIRON L19-23)
- Para 1: identical PRINCIPAL/HUMAN/COLONEL-reserved framing (verbatim-in-substance from CHIRON L21 — this is voice canon, carry it faithfully).
- Para 2: "You **answer to MAJOR_POLYBIUS**, who reviews your workflow designs and holds control of how the team coordinates. You **co-design with MAJOR_CHIRON**: CHIRON designs the *cast* (which seats), you design the *choreography* (how their work flows). Cast and choreography co-constrain each other, so you iterate together on a team-build rather than in strict sequence." (Reciprocal mirror of CHIRON L23.)

### §2 What you do (mirror CHIRON L27-36 — a responsibility table)
| Responsibility | Notes |
|---|---|
| Design the workflow for a team CHIRON has cast | the orchestration topology — which work is a pipeline, which fans out in parallel, where barriers sit (§4) |
| Compose dynamic-workflow scripts | the `workflow-composer` skill is your signature tool (§7 / Tools) |
| Design the runtime model-cascade + context-isolation topology | which steps are deterministic code / cheap model / Opus; where the orchestrator sees only returned output (§5) |
| Author the bw coordination contract | tickets, dependencies, polling cadence, orphan-branch sync, the seat-identity / Co-Authored-By trailer convention (§6) |
| Hand off the workflow design | back to POLYBIUS/PLINY to run, and co-iterate with CHIRON on the cast |

### §3 What you don't do (mirror CHIRON L39-46 — a bulleted non-responsibility list; load-bearing for one-job-per-agent)
- **You do not design the cast.** Which seats exist is CHIRON's seat. You design how the seats you're handed coordinate.
- **You do not run the gauntlet or command PLINY/the CAPTAINs operationally.** You design the choreography; POLYBIUS and PLINY direct what runs. Designing a workflow is not orchestrating it.
- **You do not set project direction.** Runtime workflows *execute* direction, never *set* it (`stoa--q36`). You surface a workflow design; POLYBIUS gates it.
- **You do not ship substrate canon without an arc.** Authoring a workflow draft is yours; landing canonical workflow machinery into the deployed substrate is an arc.
- **You do not pick the model tier per seat in isolation.** CHIRON specifies the per-seat tier; you wire those tiers into a cascade. (Mirror of CHIRON L81's reciprocal "you specify the per-seat tier, she wires the cascade.")

### §4 The craft — choreography, pipeline-vs-parallel, barriers (mirror CHIRON L49-55, HAMILTON content)
The craft section. Content: a workflow design decomposes a team's work into a topology — **default to pipeline** (sequential, each stage consumes the prior verdict); fan out to **parallel** only when stages are genuinely independent (the barrier smell-test). The art is matching topology to the work: too much parallelism and barriers stall on the slowest branch; too much serialization and independent work waits needlessly. This is judgment — which is why this seat is a MAJOR, not a template-filler. Note the `workflow-composer` skill carries the Stoa DELTA (reuse CAPTAIN seats via `agentType`, verdict schema, gate human attention at stage boundaries, emit the outer-loop review surface); HAMILTON does NOT restate the generic Workflow-tool mechanics (the tool's own description is authoritative — same scope discipline the skill states).

### §5 Runtime model-cascade + context-isolation topology (mirror CHIRON §6 L72-82, HAMILTON-owned)
This is HAMILTON's half of the two-layer runtime architecture (CHIRON owns the roster side; the boundary is explicit in CHIRON L81). Content:
- **Performance-first model assignment** (verbatim-in-substance from the charter / CHIRON L74-79): default to the most capable model (Opus 4.8); down-tier a step ONLY after proving the task is *saturated*; the cost ladder (deterministic code → cheap model → … → Opus) is an efficiency tuning applied AFTER saturation, never the default stance.
- **Model-cascades with context isolation** (the Agent-SDK custom-tool pattern): a capable orchestrator calls a Python tool that invokes a cheaper model and sees ONLY the returned output — the worker's intermediate tokens never enter the orchestrator's context and are not re-paid per turn. Primary value = clean orchestrator context (avoid attention-dilution / agentic-laziness / per-turn token bloat); cost savings is SECONDARY.
- **The permeable boundary + sentinel→Stoa escalation:** a cheap SENTINEL tripwire (CHIRON authors the sentinel *seat*; HAMILTON wires the *escalation path*) detects → the full Stoa team investigates on demand. HAMILTON designs the escalation workflow; match analysis depth/cost to task stakes.

### §6 The bw coordination contract (HAMILTON-distinctive; no direct CHIRON analog)
The beadwork half of the domain. Content: HAMILTON designs how a team coordinates durably across sessions via bw — tickets + dependencies (`bw dep add … blocks …`), polling cadence (the D-A/D-B/D-C disciplines), orphan-branch sync (`git fetch origin beadwork:beadwork`), the seat-identity / `Co-Authored-By` trailer convention. **The INTEGRATION is her distinctive value:** nobody else owns the seam between Anthropic-workflow execution (a script that CANNOT run bw/git — `workflow-composer` states the launching seat lands the verdict) and bw coordination (the durable substrate the script's output feeds). Name that seam explicitly as the load-bearing thing this seat owns.

### §7 / Tools section — `workflow-composer` (mirror CHIRON's unnumbered Tools section L159-161)
A "Tools" section (unnumbered, like CHIRON's). Content: full MAJOR / main-agent toolset (`Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash` (bw + git), `WebSearch`/`WebFetch`, and the `Agent` tool to dispatch any helper cast). **Holds `workflow-composer`** (Stoa-aware dynamic-workflow composition) as her signature skill — the reciprocal of CHIRON's "You do not hold `workflow-composer` (HAMILTON's)." As a MAJOR she also carries `handoff-author` (continuity) and `team-launcher`. **Decision:** frame workflow-composer as held by reference to the skill (`.claude/skills/workflow-composer/`), NOT inlined as instruction — UNLIKE CHIRON's agent-author (which was inlined because the skill was retired). The workflow-composer skill is LIVE and KEPT (p41 disposition #5); HAMILTON holds it as a normal skill grant. (See W4 on the skill-grant reachability caveat.)

### §8 Voice discipline + Activation checklist (mirror CHIRON §9 L131-133 + §10 L137-143)
- **Voice discipline** section: identical inheritance statement — PRINCIPAL/HUMAN throughout, COLONEL only for the reserved future rank, no second-person framing of the human. She enforces this on any workflow doc she authors.
- **Activation checklist**: read this file; confirm seat identity (WORKFLOW-ARCHITECT, design-time, answers to POLYBIUS, peer to CHIRON); read the charter (`bw show stoa--yh2`); co-locate with CHIRON if the build needs cast design; announce presence on the relevant bw ticket before designing.

### Section-count note (the structural mirror)
CHIRON has §1–§11 + Tools. HAMILTON's natural content is §1–§6 + Tools + Voice + Activation. **ADA may number these §1–§8 + Tools** (HAMILTON does not need CHIRON's §5 seat-kinds, §7 agent-author, §8 helper-cast, §11 module-stub). The mirror is *structural shape* (seat-ID table → lead → who-you-serve → what-you-do → what-you-don't → craft → domain sections → Tools → voice → activation), NOT section-number parity. **Do NOT manufacture a §11 module-stub** to match CHIRON's count — HAMILTON owns no module (D3). If a helper-cast section is included, keep it brief and HAMILTON-shaped (e.g., a workflow-spec-checker); if it adds nothing, omit it and drop the helper-cast clause from the slim-core blockquote. I lean **omit** (HAMILTON's signature act is composing the workflow herself via the skill, not running an authoring mini-gauntlet) — but flag this as ADA/ARGUS's call (W1).

### Authorship (D1)
No author-like field in the markdown body. The file is the PRINCIPAL's work. Commit Author = PRINCIPAL (Denson Smith) + `Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>` trailer (substrate seat-identity convention).

---

## §2. D2 — `docs/major-hamilton.html` (the rendered view)

Mirror `docs/major-hamilton.html` on `docs/major-chiron.html` exactly in aesthetic + machinery:
- **Copy the entire `<style>` block verbatim** (L8-62 of major-chiron.html) — the Stoa palette/typography is shared; do not re-derive it.
- `<head>`: `<meta name="author" content="Denson Smith" />` (L6 — load-bearing authorship), `<title>MAJOR_HAMILTON — role file</title>`.
- `<nav>`: `<span class="brand">MAJOR_HAMILTON</span>` + section anchors matching HAMILTON's actual section set (`#s1`…`#s8` + `#tools` — NOT CHIRON's `#s1`…`#s11`; match whatever section count D1 lands with). Update the `§7 author` nav label (CHIRON-specific) to HAMILTON's labels (e.g. `§5 cascade`, `§6 bw`, `Tools`).
- `<main>`: render each D1 section as `<h2 id="sN"><span class="n">§N</span>Title</h2>` + body, mirroring CHIRON's element patterns (`.idtable`, `<table>` for the §2 responsibilities, `<ul>` for §3, `.lead` for the lead para, `class="tag">v1</span>` on the role subtitle).
- **Footer** (mirror CHIRON L253-256): `Rendered view of <code>substrate/MAJOR_HAMILTON.md</code> · v1 (landed Arc 62) · the Stoa · markdown is the source of truth, this is the view. Author: Denson Smith · 2026-06-17.`
- The HTML is a faithful rendering of the final D1 markdown — author D1 first, then render. Any prose divergence between the two is a defect (the markdown is source of truth).

---

## §3. D3 — `install.sh` deploy wiring (the load-bearing divergence)

Deploy `MAJOR_HAMILTON` at ALL tiers (user + project + subproject), suffixed `HAMILTON_<slug>` at project/subproject, parallel to CHIRON/POLYBIUS/PLINY. **CRITICAL: HAMILTON owns NO module.** Mirror the CHIRON deploy wiring at four sites; add NOTHING at the recompose sites. Exact anchors (line numbers are at @24b79cc; ADA mirrors the CHIRON line *adjacent* to each):

### ADD (4 edits, all mirror the CHIRON line one line below it):

| # | Anchor | CHIRON line (mirror it) | Add for HAMILTON |
|---|---|---|---|
| A1 | **~L157** (SRC declarations) | `SRC_CHIRON="${SCRIPT_DIR}/MAJOR_CHIRON.md"` | `SRC_HAMILTON="${SCRIPT_DIR}/MAJOR_HAMILTON.md"` immediately after L157 |
| A2 | **~L802** (existence guards) | `[ -f "$SRC_CHIRON" ] \|\| err "source file not found: $SRC_CHIRON"` | `[ -f "$SRC_HAMILTON" ] \|\| err "source file not found: $SRC_HAMILTON"` after L802 |
| A3 | **~L936 + ~L940** (DEST assignment, both branches of the `SUFFIX_MAJORS` if/else) | L936 `DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON${NAME_SUFFIX}.md"` and L940 `DEST_CHIRON="${DEST_DIR}/MAJOR_CHIRON.md"` | add `DEST_HAMILTON="${DEST_DIR}/MAJOR_HAMILTON${NAME_SUFFIX}.md"` after L936 AND `DEST_HAMILTON="${DEST_DIR}/MAJOR_HAMILTON.md"` after L940 (both branches) |
| A4 | **~L961 (dry-run print) + ~L969/972 (real deploy)** | L961 `echo "[dry-run] deploy: $SRC_CHIRON -> $DEST_CHIRON …"`; L969 `sed "s/{{NAME_SUFFIX}}/${NAME_SUFFIX}/g" "$SRC_CHIRON" > "$DEST_CHIRON"`; L972 `echo "deployed: $DEST_CHIRON"` | mirror all three: a dry-run `echo` after L961, a `sed … "$SRC_HAMILTON" > "$DEST_HAMILTON"` after L969, an `echo "deployed: $DEST_HAMILTON"` after L972 |

HAMILTON, like CHIRON, contains no `{{NAME_SUFFIX}}`/`{{USER_TIER_DIR}}` placeholder, so the `sed` at A4 is a defensive no-op (same as CHIRON L969) — correct and intentional.

### DO NOT ADD (the divergence — call these out explicitly to ADA/VERA/CATO):

1. **NO `HAMILTON_MODULES=…` line** in the `TARGET=subproject` recompose block (~L1170-1178). CHIRON has `CHIRON_MODULES="pair-programmer-authoring"` at L1178; HAMILTON gets NO such line.
2. **NO `recompose_module_inline "$DEST_HAMILTON" …` call** (~L1182-1198). CHIRON has one at L1189; HAMILTON gets NONE.
3. **NO ownership-partition comment entry.** The L1009-1014 + L1027-1029 module-ownership accounting ("4 POLYBIUS + 12 op-disc + 11 PLINY + 7 DAEDALUS + 1 CHIRON = 35") stays UNCHANGED — HAMILTON adds zero modules, so the count and the owner list do not change. Do NOT add HAMILTON as a 6th owner.
4. **NO entry in the `apply_substitutions_from_manifest` frontmatter manifest** (~L525-534). That manifest lists only files carrying `{{NAME_SUFFIX}}`/`{{USER_TIER_DIR}}` placeholders needing substitution. CHIRON is ABSENT from it (verified — only POLYBIUS + PLINY appear, because only they carry placeholders); HAMILTON, carrying no placeholder, is likewise ABSENT. Do NOT add a HAMILTON printf here.
5. **NO `<!-- MODULE-INLINE:… -->` marker anywhere in MAJOR_HAMILTON.md.** (D1 constraint, restated here because it is what makes the recompose a clean no-op for HAMILTON.)

### Why zero owned modules keeps the FAIL-LOUD recompose green (CONFIRM, don't assume)

The brief asks the design to confirm this. The mechanism, read at @24b79cc:
- There is **no `recompose_module_inline "$DEST_HAMILTON"` call at all** (DO-NOT-ADD #2), so the awk state-machine never runs against HAMILTON's file. The five FAIL-LOUD Checks A–E (install.sh ~L1059-1115) are therefore never evaluated for HAMILTON — they cannot trip on a file that is never passed to the function.
- The other owners' recompose calls (POLYBIUS / op-disc / PLINY / CHIRON / DAEDALUS) are UNAFFECTED — HAMILTON's deploy adds a `DEST_HAMILTON` file with no marker, but no owner's owned-set references it, so no Check B (`for m in owned … !consumed`) or Check D (`markers_seen==0 && nowned>0`) sees it. Check A iterates the GLOBAL module-existence set (35 sources, owner-agnostic) which HAMILTON does not change.
- **Belt-and-suspenders confirmation** (the *counterfactual* that proves the no-op): EVEN IF someone wrongly added `recompose_module_inline "$DEST_HAMILTON" ""` with an empty owned-set, it would still be green — `nowned` would be 0 (Check D needs `nowned>0` to trip; Check B's `for m in owned` iterates an empty set; a file with zero markers + zero owned modules satisfies `markers_seen==0 && nowned==0`, no fail). So the deploy is no-op-clean by construction. **But the design says: add NO call (DO-NOT-ADD #2) — the cleanest possible state.** The §4 P1 probe CONFIRMS the real recompose stays exit-0 with HAMILTON deployed.

---

## §4. D4 — app regen (4th MAJOR)

The gen-data adapter discovers MAJORs by **filename regex**, not a hardcoded list. `app/scripts/gen-data-lib.ts` L59: `entry.name.match(/^(MAJOR|CAPTAIN)_([A-Z][A-Z0-9_-]*)\.md$/)`. So dropping `MAJOR_HAMILTON.md` into `substrate/` makes it auto-register as a MAJOR — **no adapter code change needed**, provided HAMILTON carries NO YAML frontmatter (L150-154 warn-loud if a MAJOR ever has frontmatter; CHIRON has none, HAMILTON must have none — already a D1 constraint).

ADA's steps:
1. After D1 lands `substrate/MAJOR_HAMILTON.md`, **run `cd app && npm run gen-data`** — this re-derives the whole roster from current substrate and regenerates `app/src/data/generated/agents.ts` with HAMILTON as a 4th MAJOR.
2. **STAGE the regenerated `app/src/data/generated/agents.ts` in the SAME commit** as the substrate edit (generated artifact and its source move together; a regen that isn't staged is drift).
3. **Update `app/src/data/__tests__/generated.test.ts`:**
   - **L51** test title: `it("seats CHIRON, PLINY, and POLYBIUS at MAJOR rank", …)` → `it("seats CHIRON, HAMILTON, PLINY, and POLYBIUS at MAJOR rank", …)`.
   - **L55** assertion: `expect(mnemonics).toEqual(["CHIRON", "PLINY", "POLYBIUS"]);` → `expect(mnemonics).toEqual(["CHIRON", "HAMILTON", "PLINY", "POLYBIUS"]);` (the array is `.sort()`ed at L54, so alphabetical order: CHIRON, HAMILTON, PLINY, POLYBIUS — confirmed correct).
4. **Run `npm run build && npm test`** — both green with 4 MAJORs. (Per the gen-data-regen lesson: assert from a FULL suite run, not from "this arc edited no other MAJOR" — the regen re-derives the entire roster and surfaces any pre-existing drift. CHIRON/PLINY/POLYBIUS slots must all stay green.)

No other test should reference the MAJOR count by a hardcoded `3` — but VERA/CATO should grep `generated.test.ts` for any sibling MAJOR-count assertion (e.g. a `toHaveLength(3)` on the MAJOR slot) that L55 doesn't cover. (W3.)

---

## §5. D5 — cross-refs

1. **Reciprocal HAMILTON→CHIRON pointer:** D1's header note + §1 para 2 name CHIRON as the cast architect and the co-design relationship (specified in §1 above). CHIRON already names HAMILTON in six places (header note L3, §1 L23, §2 table L35, §6 L81, §10 L142, Tools L161 — all verified present) — **CHIRON needs NO edit this arc** (it landed Arc 61; epic OUT-OF-SCOPE fences it).
2. **`workflow-composer` framed as HAMILTON's tool:** D1's Tools section holds it (§1 spec above). The skill itself (`substrate/skills/workflow-composer/SKILL.md`) already says "POLYBIUS or PLINY invokes this" — that line is about the RUNTIME-orchestrator invocation surface and is OUT OF SCOPE for this additive arc (changing who-invokes-the-skill is a separate routing decision). Do NOT edit the skill this arc; just hold it in HAMILTON's Tools. (W4 flags the latent grant-reachability question.)
3. **Roster docs enumerating MAJORs:** `docs/agent-cards/index.html` already carries the HAMILTON card (L104-107, verified — `role:"Workflow Architect"`, Margaret Hamilton, the co-design hook). No edit needed. VERA/CATO should grep `docs/` + `substrate/` for any OTHER doc that enumerates the MAJOR set as exactly `{CHIRON, PLINY, POLYBIUS}` and would now be stale (e.g. `docs/chiron-architecture.html`, README roster tables). Any found-stale enumeration is a D5 follow-up (surface it; the epic scopes D5 to the reciprocal pointer + workflow-composer + agent-cards, so a newly-found stale roster doc is ARGUS's in-scope-vs-follow-up call). (W5.)

---

## §6. Probes (load-bearing for VERA — runnable, re-executable)

Run from the worktree root `.claude/worktrees/arc-62-build` unless noted. Each probe states its pass condition.

### P1 — REAL (non-dry-run) subproject recompose stays green (the Arc-61 lesson, load-bearing)
A `--dry-run` recompose EARLY-RETURNS at install.sh ~L1051 (`if [ "$DRY_RUN" -eq 1 ]; then … return 0`) BEFORE the awk FAIL-LOUD Checks A–E (~L1059+) — so a dry-run CANNOT exercise them. The probe must run a REAL recompose into a throwaway subproject dir and assert exit 0 + no FAIL-LOUD trip. HAMILTON owns no module so this should be no-op-clean — the probe CONFIRMS it, does not assume it.

```bash
# Fixed literal throwaway path (no $VAR in any destructive op — operating-disciplines §8.6):
rm -rf /tmp/arc62-recompose-probe
mkdir -p /tmp/arc62-recompose-probe
# Real (NOT --dry-run) subproject install into the throwaway parent:
bash substrate/install.sh --target subproject --subproject arc62probe --parent /tmp/arc62-recompose-probe ; echo "EXIT=$?"
# PASS: EXIT=0 AND no line matching 'install.sh: error: recompose:' on stderr.
# CONFIRM HAMILTON deployed + suffixed + carries NO MODULE-INLINE marker:
ls /tmp/arc62-recompose-probe/**/.claude/MAJOR_HAMILTON_arc62probe.md
grep -c "MODULE-INLINE" /tmp/arc62-recompose-probe/**/.claude/MAJOR_HAMILTON_arc62probe.md   # PASS: 0
rm -rf /tmp/arc62-recompose-probe
```
*(ADA/VERA: confirm the exact `--target subproject` invocation flags against the install.sh arg parser before running — the flag names above are the intent; the script's own usage is authoritative. The load-bearing assertions are: exit 0, zero `recompose: error` lines, HAMILTON deployed suffixed, zero MODULE-INLINE markers in the deployed HAMILTON file.)*

### P2 — user-tier dry-run passes
```bash
bash substrate/install.sh --target user --dry-run ; echo "EXIT=$?"
# PASS: EXIT=0; output includes a '[dry-run] deploy: …MAJOR_HAMILTON.md' line.
```

### P3 — app green with 4 MAJORs
```bash
cd app && npm run gen-data && npm run build && npm test
# PASS: all three exit 0; the MAJOR-rank test asserts ["CHIRON","HAMILTON","PLINY","POLYBIUS"]; full suite green.
```

### P4 — Voice audit on MAJOR_HAMILTON.md
```bash
grep -ni "colonel" substrate/MAJOR_HAMILTON.md   # PASS: only the reserved-future-rank reference line(s); zero uses meaning the human
grep -ni "the user" substrate/MAJOR_HAMILTON.md  # PASS: zero lines
```
(Also eyeball: no second-person `you` referring to the *human* — the seat talks *about* the PRINCIPAL, not *to* them. Second-person `you` referring to the agent reading the file is correct.)

### P5 — Authorship audit
```bash
# MAJOR_HAMILTON.md carries no false-person author field:
grep -niE "author|owner|creator|maintainer|copyright|by:" substrate/MAJOR_HAMILTON.md   # PASS: no line names a person other than Denson Smith (ideally no author-field at all)
# HTML meta + footer = Denson Smith:
grep -n 'meta name="author"' docs/major-hamilton.html        # PASS: content="Denson Smith"
grep -ni "Author: Denson Smith" docs/major-hamilton.html     # PASS: footer present
```
(Commit-time, CATO/NOMOS verify: git Author = PRINCIPAL + `Co-Authored-By: CAPTAIN_ADA_the-stoa` trailer.)

### P6 — Reciprocal cross-ref present + CHIRON untouched
```bash
grep -ni "CHIRON" substrate/MAJOR_HAMILTON.md     # PASS: HAMILTON names CHIRON (co-design + cast/choreography division)
grep -ni "workflow-composer" substrate/MAJOR_HAMILTON.md  # PASS: held in HAMILTON's Tools
git diff --name-only main -- substrate/MAJOR_CHIRON.md docs/major-chiron.html  # PASS: empty (CHIRON not edited this arc)
```

---

## §7. Out of scope

- **The other p41 skill re-homings** (check-substrate-updates/check-bw-release → SessionStart triggers; save-verdict/validate-spec/inspect-script-output → modules; credential-discipline). Separate skills-housekeeping pass AFTER this (epic OUT-OF-SCOPE).
- **Editing MAJOR_CHIRON.md or major-chiron.html.** CHIRON landed Arc 61; it already names HAMILTON reciprocally. No edit this arc.
- **Changing who invokes `workflow-composer`** (the skill's "POLYBIUS or PLINY invokes this" line). A runtime-routing decision, separate from holding the skill in HAMILTON's Tools.
- **HAMILTON helper-cast (a workflow mini-gauntlet).** Left to ADA/ARGUS judgment whether to include a thin §8; I lean omit (W1). Not a load-bearing deliverable.
- **The authorship-gate false-positive (`stoa--z2b`) and the-stoa self-apply (`stoa--ruu`).** Separate tickets (epic OUT-OF-SCOPE).
- **Any NEW sentinel / runtime workflow machinery.** HAMILTON *describes* the cascade/sentinel-escalation patterns as her domain; building runtime machinery is product work, not this seat-file arc.

---

## §8. Self-assessed weak points / risks (for ARGUS)

- **W1 — Section structure is the highest-judgment call, and I left one sub-decision open.** CHIRON's §1–§11 don't map 1:1 to HAMILTON's natural content; I specified a §1–§8 + Tools shape and deliberately left "include a thin helper-cast §8 or omit it" to ADA/ARGUS. *Why this shape anyway:* forcing HAMILTON into CHIRON's exact 11-section skeleton would manufacture empty sections (a §5 seat-kinds table HAMILTON doesn't own, a §11 module-stub HAMILTON must NOT have). A structural mirror (shape, not section-number parity) is the honest fit. ARGUS should confirm the §-numbering is coherent and that no CHIRON-specific section leaked in by copy inertia.
- **W2 — The "structural mirror" invites copy-paste leakage.** Because ADA builds from CHIRON, the risk is CHIRON-domain content surviving into HAMILTON (e.g. "agent-author capability", "narrow seats / near-determinism", "seat kinds you author", a §11 module-stub, a MODULE-INLINE marker). The P4/P6 probes + ARGUS's read are the catch. The single most damaging leak is a stray `<!-- MODULE-INLINE -->` marker — it would make HAMILTON a 6th recompose-owner and could trip Check D at subproject tier. P1 (real recompose, grep MODULE-INLINE = 0) is the specific guard.
- **W3 — `generated.test.ts` may carry a MAJOR-count assertion beyond L55.** I specified L51/L55 from a targeted read; I did not exhaustively scan the whole test file for a sibling `toHaveLength(3)` or count-based MAJOR assertion. *Why this shape anyway:* the L51-55 block is the canonical MAJOR-set assertion (it's the one the Arc-61 CHIRON build edited). VERA/CATO running the FULL `npm test` (P3) will surface any other failing assertion loudly — the regen + full-suite run is the backstop, per the gen-data-regen lesson.
- **W4 — workflow-composer grant reachability is unverified at the substrate level.** `stoa--xyb.2` recorded a skill-grant reachability finding (CAPTAIN envelopes carry no Skill tool); MAJORs are different (POLYBIUS/PLINY carry skills), so HAMILTON-holds-workflow-composer should be reachable — but I did not re-verify the mechanism by which a MAJOR role file's "Tools" prose actually grants a skill at runtime (it may be advisory prose, not an enforced grant). *Why this shape anyway:* CHIRON's Tools section uses the same prose-grant pattern for handoff-author/team-launcher and it's the established convention; matching it is correct for this arc. ARGUS should flag if the grant needs an install.sh `SKILL_NAMES`-style wiring entry that this design doesn't specify (I believe it does NOT — workflow-composer is already in the deployed skill set as a KEPT orchestrator skill; HAMILTON just references it).
- **W5 — Stale MAJOR-enumeration docs beyond agent-cards may exist.** agent-cards already has HAMILTON, but `docs/chiron-architecture.html`, README roster tables, or the architecture spec may enumerate the MAJOR set as `{CHIRON, PLINY, POLYBIUS}` and now read stale. I scoped D5 per the epic (reciprocal pointer + workflow-composer + agent-cards) and flagged the grep for VERA/CATO rather than chasing every doc — but a found-stale roster doc is a real in-scope-vs-follow-up judgment ARGUS should rule on, not silently defer.
- **W6 — P1 install.sh flag names are intent, not verified-verbatim.** I specified `--target subproject --subproject <slug> --parent <dir>` from the CHIRON/Arc-61 pattern, but did not execute install.sh's arg parser to confirm the exact flag spellings at @24b79cc. *Why this shape anyway:* the probe's load-bearing assertions (exit 0, zero recompose errors, HAMILTON deployed suffixed + zero MODULE-INLINE) are parser-independent; ADA/VERA confirm the exact invocation against `install.sh` usage before running. Naming this so VERA doesn't read a flag-name typo as a design claim.

---

*End of design-rev1. ADA builds D1→D2→D3→D4→D5 in that order (D1 is the source of truth D2 renders and D4 ingests); run the §6 probes after each relevant deliverable; do not commit until the full gauntlet clears.*
