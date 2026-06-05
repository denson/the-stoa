# Design — stoa--rdh (Arc 60): land 3 substrate skills + per-skill SKILL_NAMES wiring

**Ticket:** stoa--rdh (Phase 1 of the "finish the Stoa → Marianne walkthrough" re-scope)
**Seat:** CAPTAIN_DAEDALUS_the-stoa (ARCHITECT), Arc 60
**Branch:** `arc-60/build` — built IN-PLACE on the main working tree (untracked held inputs do not travel to a fresh `git worktree`)
**Drive mode:** HITL / co-driven; autonomous PAUSED. HARD STOP post-ARGUS → floor-manager → user-tier holds close-gate + merge.

---

## 1. Problem restatement

Three LIEUTENANT skills were authored during the 2026-06-04/05 debloat engagement and held UNCOMMITTED (substrate canon needs an arc, not direct-to-main). They exist now as untracked dirs under `substrate/skills/`: `decision-surface/`, `interactive-html-preview/`, `team-launcher/`. `substrate/install.sh` is already held-modified with `interactive-html-preview` appended to `SKILL_NAMES`. This arc version-controls all three and wires DEPLOYMENT per-skill by readiness — not all three deploy. The design decides, per skill, (i) land in-repo? and (ii) add to `SKILL_NAMES` (= deploy to consumer `.claude/skills/`)?, and specifies the build steps + the probe set that proves the per-skill split held.

**Imported assumptions (named per §6.1, not smoothed):**

1. **`SKILL_NAMES` membership == consumer deployment, but NOT == app visibility.** Two independent surfaces consume `substrate/skills/`: (a) `install.sh` deploys ONLY the dirs named in `SKILL_NAMES`; (b) `app/scripts/gen-data-lib.ts::discoverSkillFiles()` discovers EVERY subdir of `substrate/skills/` that contains a `SKILL.md`, regardless of `SKILL_NAMES`. Therefore "land but don't deploy" (decision-surface, and team-launcher under option (a)) means: committed to repo + appears in the app roster + reachable by a builder working in the-stoa tree, but NOT copied into a consumer install. This decoupling is load-bearing for the whole arc and the directive does not state it explicitly — I am importing it from reading both consumers. It is verified below (gen-data already emits all three into `agents.ts`).

2. **"DEPLOY" = present at `<dest>/.claude/skills/<name>/SKILL.md` after `install.sh --target project`.** That is the probe-able definition of deployed.

3. **The held `install.sh` +1 line is the ONLY install.sh edit this arc needs.** Verified: `git diff substrate/install.sh` shows exactly one added line (`+  interactive-html-preview`) inside the `SKILL_NAMES` array. No other install.sh change is in scope.

The restatement converges with the directive; no divergence to escalate. The one open design call (team-launcher hold-vs-generalize) is resolved in §2.3.

---

## 2. Approach

### 2.0 The deploy contract (how install.sh consumes SKILL_NAMES)

`install.sh` (lines 226–237, 806–813, 1210, 1606, 1695):
- **Validation gate (806–813):** for each `sname` in `SKILL_NAMES`, asserts `substrate/skills/$sname/` is a dir AND `substrate/skills/$sname/SKILL.md` exists — else hard `err` (install aborts). So every `SKILL_NAMES` entry MUST resolve to a real source dir; a typo or a name with no dir fails the install loudly. (This is also why a skill can be safely committed-but-not-listed: the validation loop never looks at unlisted dirs.)
- **Deploy (1210):** copies each listed skill's whole subtree to `<dest>/.claude/skills/<name>/`.
- **Obsolete-file sweep (1606, 1695):** subdirs of the DEST skills dir not in `SKILL_NAMES` are flagged as obsolete on re-install. A NET-NEW skill (no prior deploy) produces no obsolete warning. The new skills are net-new, so no obsolete warnings expected for them.

The deploy unit is the skill's subtree under `substrate/skills/<name>/` ONLY. Files outside that subtree (repo-root `launch-team.ps1`, repo-root `HUMAN_paste-*.md`, `MAJOR_*.md`) are NOT carried by a skill deploy. This fact decides §2.3.

### 2.1 interactive-html-preview → LAND + DEPLOY (in SKILL_NAMES)

Commit the dir; keep the held `SKILL_NAMES` +1 line. Justification: it is consumer-general (the render layer is Claude Preview MCP for builders + a self-contained HTML fallback that "opens in any browser" for consumers — stated in its own frontmatter). It has no the-stoa-internal dangling references: its cross-refs point at `docs/capability-registry.md`, `docs/case-study/architecture-kg.html`, and the sibling `decision-surface` skill. The case-study path is a documentation example, not a runtime dependency the skill executes; the skill is usable in a consumer tree without those files present. It is the dependency `decision-surface` Part-2 names, so it must ship first for decision-surface to ever become consumer-usable in Phase 2. This is exactly the existing held change — no new edit.

### 2.2 decision-surface → LAND in-repo, HOLD OUT of SKILL_NAMES

Commit the dir (`SKILL.md` + `worked-example-debloat.md`); do NOT add to `SKILL_NAMES`. Justification: its own frontmatter is `status: DRAFT (v0.1, 2026-06-04)` and open-question #6 reads "Gauntlet-ship — formalize, eval, and deploy this once the above settle (add to `install.sh` SKILL_NAMES)." The six open questions settle in Phase 2 (building the consumer surface). PRINCIPAL-confirmed: land the DRAFT for version control + app visibility, deploy in Phase 2. Landing-without-deploying is safe because the validation loop (§2.0) never inspects an unlisted dir, and gen-data discovers it for the app regardless.

### 2.3 team-launcher → DECISION: (a) HOLD out of SKILL_NAMES (land as the-stoa-internal / builder skill)

**Decision: option (a). Land in-repo, HOLD out of `SKILL_NAMES`. Do NOT deploy to consumers this arc.**

**Concrete justification — the dangling references a consumer install would inherit.** `team-launcher/SKILL.md` is structurally the-stoa-specific. Its runtime instructions and cross-references point at files that live OUTSIDE the skill's deploy subtree and therefore are NOT carried by `install.sh` (§2.0):

| Reference in team-launcher/SKILL.md | Where it actually lives | Deployed by a skill install? | Consumer result |
|---|---|---|---|
| `./launch-team.ps1` (the tool the whole skill documents — §"The tool", §"workflow" step 2, cross-refs) | the-stoa **repo root** (committed @2d34f55), NOT under `substrate/skills/` | **No** | The skill's central command `./launch-team.ps1` does not exist in the consumer tree — the skill is inert |
| `HUMAN_paste-polybius-the-stoa-init.md`, `HUMAN_paste-pliny-init.md` (workflow step 1 + cross-refs) | the-stoa **repo root** | **No** | Activation-paste files the skill tells the human to author/consume are absent |
| Default seats `POLYBIUS_the-stoa`, `PLINY_the-stoa` (hardcoded in the §"The tool" example) | the-stoa-specific seat names | n/a (prose) | Wrong seat names for any other project |
| `MAJOR_POLYBIUS.md` / `MAJOR_PLINY.md` (cross-refs) | deployed as `.claude/MAJOR_*.md` — these DO resolve | Yes | OK, but the surrounding skill is still inert |

Deploying team-launcher as-is would hand every consumer a skill whose load-bearing command (`./launch-team.ps1`) and activation files do not exist in their tree — a skill that cannot run and reads as broken. That is precisely the failure mode the directive §4 names. Option (b) — generalize now (deploy `launch-team.ps1` into the skill subtree + de-the-stoa the paste/seat refs + handle the cross-platform reality that the tool is Windows-`wt`-only) — is real work outside this arc's tight additive scope and would expand the diff into role/template-adjacent territory. Holding keeps the arc low-risk and additive while still version-controlling the verified `wt`/`claude` mechanics for the-stoa's own builder use (the app shows it; a builder in-tree can invoke it against the real `launch-team.ps1`).

**Follow-up ticket to file (deliverable of this arc):** `stoa--<new>` — "Generalize team-launcher for consumer deploy" — bundle `launch-team.ps1` into the skill subtree (`substrate/skills/team-launcher/launch-team.ps1`) so the deploy unit is self-contained; replace hardcoded `POLYBIUS_the-stoa`/`PLINY_the-stoa` + `HUMAN_paste-the-stoa-*` refs with parameterized/`<project-slug>` forms; address the Windows-`wt`-only constraint (graceful fallback or a documented platform precondition) for Mac consumers; THEN add to `SKILL_NAMES`. Blocked-by: nothing; schedule after Arc 60 merges. File this on the project bw before hand-back.

### 2.4 The exact final SKILL_NAMES after this arc

Net add this arc = `interactive-html-preview` ONLY (the existing held +1 line). decision-surface and team-launcher are committed but NOT listed. Final array (10 entries):

```
SKILL_NAMES=(
  agent-author
  check-substrate-updates
  credential-discipline
  check-bw-release
  inspect-script-output
  handoff-author
  save-verdict
  validate-spec
  workflow-composer
  interactive-html-preview
)
```

Confirm: 9 pre-existing entries + `interactive-html-preview` = the array as already held in `substrate/install.sh`. No further install.sh edit required — the held diff is final.

### 2.5 gen-data / app stays valid

`app/scripts/schemas.ts::skillFrontmatterSchema = z.object({ name, description })` — NOT `.strict()`, so the extra `status:` key in decision-surface frontmatter passes validation (unknown keys are stripped, not rejected). `discoverSkillFiles()` walks every `substrate/skills/*/SKILL.md`; all three are discovered. The directory NAME is the canonical skill name and gen-data-lib asserts frontmatter `name:` matches the dir name — verify all three match (they do: `team-launcher`, `interactive-html-preview`, `decision-surface`). Pre-verified: `agents.ts` already contains all three names (held gen-data output). Re-run `npm run gen-data` post-commit to re-confirm clean + no Zod throw.

### 2.6 Threat→mitigation map

This arc is a process/version-control + additive-skill change with no runtime attack path introduced. Per `operating-disciplines.md` §35.5 carve-out:

**not threat-ratified (additive skill landing + install-manifest wiring; no runtime attack path, no credentialed/network/PRINCIPAL-gate surface introduced).** ARGUS to CONFIRM. The one safety-adjacent property — "a consumer must not receive a skill with dangling references" — is a correctness/UX property handled by the §2.3 hold decision and probe P4, not a security mitigation; classifying it as not-threat-ratified does not waive that probe.

---

## 3. Build steps for ADA (in order)

All commands run from repo root `C:\Users\denso\claude_projects\the-stoa` (git-bash / WSL bash for install.sh; PowerShell acceptable for git + npm). Branch `arc-60/build` already created in-place by PLINY.

1. **Pre-flight authorship verify (BEFORE staging — §8 / P6).** Confirm `author: Denson Smith` present and unchanged in all three SKILL.md frontmatters; confirm the diff touches NO author-like field anywhere:
   ```bash
   grep -H '^author:' substrate/skills/decision-surface/SKILL.md substrate/skills/interactive-html-preview/SKILL.md substrate/skills/team-launcher/SKILL.md
   # expect all three: author: Denson Smith
   ```
2. **Confirm the held install.sh diff is exactly the +1 line (no accidental extra edit):**
   ```bash
   git diff substrate/install.sh    # expect: single +  interactive-html-preview inside SKILL_NAMES
   ```
3. **Stage the three skill dirs + the held install.sh change:**
   ```bash
   git add substrate/skills/decision-surface substrate/skills/interactive-html-preview substrate/skills/team-launcher substrate/install.sh
   ```
   Do NOT stage `launch-team.ps1` or `HUMAN_paste-*` from repo root in THIS arc's skill commit — they are separate already-committed (@2d34f55) artifacts; team-launcher is held, not generalized.
4. **Run gen-data and stage the regenerated output ONLY if it changed:**
   ```bash
   cd app && npm run gen-data && cd ..
   git diff --stat app/src/data/generated/agents.ts
   ```
   `agents.ts` is a gen-data OUTPUT — never hand-edit. If gen-data produced no change (already green), there is nothing to stage; if it changed, stage it. Either outcome is acceptable as long as gen-data exits 0 with no Zod error.
5. **install.sh smoke-test against a synthetic scratch parent** (see P1 for the exact assertions). Dry-run first, then real, into a throwaway dir; confirm validation passes and the per-skill split holds.
6. **Commit** on `arc-60/build` with the per-CAPTAIN seat-identity trailer (§28):
   ```
   directive(stoa--rdh): Arc 60 — land 3 substrate skills; wire interactive-html-preview into SKILL_NAMES

   <body: per-skill deploy split — interactive-html-preview DEPLOY, decision-surface DRAFT-held, team-launcher the-stoa-internal-held>

   Co-Authored-By: CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>
   ```
   `Author:` stays the PRINCIPAL's configured git identity (never overridden). Do NOT push or merge — HARD STOP; user-tier holds the merge gate.
7. **File the follow-up ticket** (§2.3) on the project bw: `bw add "[ROADMAP] Generalize team-launcher for consumer deploy (bundle launch-team.ps1 into skill subtree; de-the-stoa paste/seat refs; Windows-wt fallback; then add to SKILL_NAMES)"` — record the new id in the hand-back.

---

## 4. Verification probes (VERA — runnable)

Scratch parent: pick a throwaway dir, e.g. `/tmp/stoa-arc60-scratch` (git-bash) — a FIXED LITERAL path (no `$VAR` in any destructive op, per §8.6). Create empty, install into it, inspect, remove the literal path at the end.

**P1 — the Marianne fresh-clone install path (happy path).**
```bash
SCRATCH=/tmp/stoa-arc60-scratch        # name only; destructive ops below use the literal
rm -rf /tmp/stoa-arc60-scratch && mkdir -p /tmp/stoa-arc60-scratch
bash substrate/install.sh --target project --project-dir /tmp/stoa-arc60-scratch --dry-run   # plan prints; no error
bash substrate/install.sh --target project --project-dir /tmp/stoa-arc60-scratch             # real; validation passes
# assert every SKILL_NAMES entry resolved to a deployed SKILL.md:
for s in agent-author check-substrate-updates credential-discipline check-bw-release inspect-script-output handoff-author save-verdict validate-spec workflow-composer interactive-html-preview; do
  test -f /tmp/stoa-arc60-scratch/.claude/skills/$s/SKILL.md || echo "MISSING: $s"
done   # expect: no MISSING lines
```
Pass = dry-run + real both exit 0, validation passes, all 10 listed skills present in the deploy.

**P2 — decision-surface land-but-don't-deploy (all three checks).**
```bash
test -f substrate/skills/decision-surface/SKILL.md && echo "committed-source OK"   # (a) in-repo
git ls-files --error-unmatch substrate/skills/decision-surface/SKILL.md            # (a') tracked after commit
grep -q 'decision-surface' substrate/install.sh && echo "FAIL: in SKILL_NAMES" || echo "(b) absent from SKILL_NAMES OK"
test -e /tmp/stoa-arc60-scratch/.claude/skills/decision-surface && echo "FAIL: deployed" || echo "(c) absent from deploy OK"
```
Pass = source committed/tracked AND not in SKILL_NAMES AND not in the scratch deploy.

**P3 — interactive-html-preview deploys.**
```bash
grep -q '^  interactive-html-preview$' substrate/install.sh && echo "in SKILL_NAMES OK"
test -f /tmp/stoa-arc60-scratch/.claude/skills/interactive-html-preview/SKILL.md && echo "deployed OK"
```
Pass = listed in SKILL_NAMES AND present in the scratch deploy.

**P4 — team-launcher matches the §2.3 decision (HELD), with the dangling-ref guarantee.**
```bash
test -f substrate/skills/team-launcher/SKILL.md && echo "committed-source OK"        # landed in-repo
grep -q 'team-launcher' substrate/install.sh && echo "FAIL: in SKILL_NAMES" || echo "not in SKILL_NAMES OK"
test -e /tmp/stoa-arc60-scratch/.claude/skills/team-launcher && echo "FAIL: deployed" || echo "not deployed OK"
# dangling-ref guarantee: no consumer received the skill, so no dangling ./launch-team.ps1 reached a consumer tree:
test -e /tmp/stoa-arc60-scratch/launch-team.ps1 && echo "note: launcher present (unexpected)" || echo "launcher correctly absent from consumer OK"
```
Pass = landed in-repo AND not in SKILL_NAMES AND not deployed; the skill's dangling refs never reach a consumer because the skill itself is not deployed. (This is the threat-adjacent/UX guarantee from §2.3 — the held decision is what makes it true.)

**P5 — gen-data Zod-clean + app build clean.**
```bash
cd app && npm run gen-data    # exit 0, no Zod validation error printed
node -e "const d=require('./src/data/generated/agents.ts'.replace(/\.ts$/,''))" 2>/dev/null || true
npm run build                 # exit 0, no app regression
cd ..
# assert all three skills present in the generated output:
grep -q 'decision-surface' app/src/data/generated/agents.ts && \
grep -q 'interactive-html-preview' app/src/data/generated/agents.ts && \
grep -q 'team-launcher' app/src/data/generated/agents.ts && echo "all 3 in agents.ts OK"
```
Pass = gen-data exits 0 (no Zod throw), `npm run build` exits 0, all three skill names present in `agents.ts`. (Note the asymmetry vs deploy: all three appear in the app even though only one deploys — the §1 assumption-1 decoupling, verified here.)

**P6 — authorship unchanged; no author-field touched in the diff.**
```bash
grep -H '^author:' substrate/skills/*/SKILL.md | grep -v 'Denson Smith' && echo "FAIL: non-Denson author" || echo "all authors = Denson Smith OK"
git diff --cached -U0 | grep -iE '^\+.*(^|[^a-z])(author|authors|owner|creator|created_by|maintainer|maintainers|copyright|holder|vendor|publisher|by):' && echo "REVIEW: author-like field added/changed" || echo "no author-like field touched OK"
```
Pass = every SKILL.md author is `Denson Smith` AND the staged diff adds/changes no author-like field. (The three skills are net-new files, so their `author: Denson Smith` lines appear as additions — that is expected and correct; the check is that no author field names anyone OTHER than Denson Smith, and no PRE-EXISTING author field was altered.)

**Cleanup:** `rm -rf /tmp/stoa-arc60-scratch` (fixed literal path).

---

## 5. Self-assessed weak points

1. **The `git diff --cached` author-field grep in P6 will fire on the legitimate net-new `author: Denson Smith` additions** and could read as a false "REVIEW" if the grep isn't narrowed to non-Denson values. The first half of P6 (the non-Denson filter) is the load-bearing check; the second grep is a coarse "did the diff touch any author field at all" net that VERA must read as "expected to match on the three new Denson lines; the finding is ONLY a NON-Denson value or a change to a pre-existing field." I chose this shape anyway because an over-broad author-field tripwire that VERA reads correctly is safer than a narrow one that misses a regression — but VERA needs the interpretation note, which is why it's inline. *Why this shape anyway:* author-field regression is the CRITICAL repo invariant; a noisy-but-complete check beats a quiet-but-narrow one.

2. **`npm run build` / `node -e require('.ts')` portability in P5 is shaky.** `agents.ts` is TypeScript; the `node -e require` line is best-effort and may not execute under plain node — the authoritative checks are `npm run gen-data` exit 0 and `npm run build` exit 0 plus the grep-for-3-names. I left the `node -e` line in as a non-blocking convenience but flagged it `|| true`; VERA should treat gen-data exit-code + build exit-code + the name-grep as the real P5 gates and ignore the node-eval if it no-ops. *Why this shape anyway:* the exit-code + grep triad fully covers "Zod clean + all 3 present + no app regression"; the eval is redundant garnish, marked as such.

3. **install.sh runs under bash; the env is Windows/PowerShell.** The smoke-test (P1) assumes git-bash or WSL is available to execute `bash substrate/install.sh` and that `/tmp/...` resolves. The directive states install was "verified green from a clean clone on Windows/git-bash 2026-06-05," so the path exists, but if ADA/VERA run from PowerShell without invoking bash, the install.sh probes won't execute. *Why this shape anyway:* install.sh is a bash artifact by design (the deploy mechanism for Unix-and-git-bash consumers); testing it under its real interpreter is correct, and the directive confirms the interpreter is present.

4. **The team-launcher hold leaves a known consumer-incomplete skill version-controlled but un-generalized** — the follow-up ticket (§2.3) is the plan, but until it lands, a future agent skimming `substrate/skills/` could mistake team-launcher for a deployable skill and add it to SKILL_NAMES without first bundling `launch-team.ps1`. Mitigation lives in the skill's own the-stoa-specific prose + the filed ticket; I did NOT add a `status:`/`builder-only:` frontmatter marker because that would be a skill-content edit beyond "land as-is" and risks the gen-data schema-name assertion. *Why this shape anyway:* the directive scopes this arc to landing as-is; a frontmatter marker is itself a candidate for the generalization follow-up, not this arc.

---

## 6. Out of scope (keeps ADA from scope-creep; frames ARGUS's in-arc-vs-future)

- **Finishing decision-surface's 6 open questions** — Phase 2 (`stoa--uob`/`sok`/`gis`). This arc lands the DRAFT only.
- **Generalizing team-launcher for consumer deploy** — the §2.3 follow-up ticket; a later arc. Bundling `launch-team.ps1`, de-the-stoa-ing refs, Windows-`wt` fallback all live there.
- **The `sp1` 7–8 ported utility skills** — deferred, not this arc.
- **Any role-file / operating-disciplines / template edit** — explicitly OUT; this arc is skills + install.sh only. The surgical autonomous-pause is a SEPARATE change.
- **Adding a builder-only/status marker to team-launcher frontmatter** — candidate for the generalization follow-up, not this arc (would be a content edit + risks the gen-data name assertion).
- **Pushing / merging** — HARD STOP; user-tier holds the close-gate + merge.
