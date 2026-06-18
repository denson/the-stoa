# Design (rev2) — stoa--5ju (Arc 66): glob-derive the MAJOR set in check-substrate-updates + install.sh manifest

**Ticket:** stoa--5ju · **Arc:** 66 · **Author:** Denson Smith · **Seat:** CAPTAIN_DAEDALUS (architect)
**Branch:** arc-66/build · **Worktree root (cwd):** `.claude/worktrees/arc-66-build`
**Supersedes:** design-rev1.md (edac0bd). **rev2 scope:** §0–§3 edit logic CARRIED FORWARD UNCHANGED
(ARGUS + floor-manager + user-tier POLYBIUS independently cleared every cell of the §3 suffix table and
all four loci against actual source). rev2 **fully rewrites §4** (real flags, correct MISSING-vs-DRIFTED
delivery mechanisms, a coherent visibility-flip baseline, the shared-machinery non-MAJOR regression probe,
and the full-suite step) and adds **explicit ratifications** to §5/§7 for r5 (Locus 3 superset) and r7
(empty-glob silent-zero). This file is self-contained: ADA can build and VERA can verify from it alone.

> **rev1→rev2 changelog (verification-layer only; NO edit-logic change):**
> - r1: §4 probe flags corrected to the REAL interface, each verified by direct read of the arg-parse in
>   `install.sh` / `check.sh` / `apply.sh` (not from described behavior).
> - r2: §4 MISSING delivery = `install.sh` RE-RUN (not `apply.sh`); `apply.sh --all-differing` DRIFTED-only
>   harvest exercised separately on a stale (DRIFTED) MAJOR.
> - r3: §4 V1 falsification baseline rewritten to the clean visibility-flip contrast (pre-fix: neither
>   category; post-fix: MISSING).
> - r4: new probe V8 — full check-substrate-updates exercise across DRIFTED + MISSING + OBSOLETE on
>   NON-MAJOR categories, proving the three edited shared functions did not regress; plus the standing
>   full-suite step (app `npm test`, author-gate tests, FAIL-LOUD REAL recompose).
> - r6: §4 V7 PASS-condition pre-names every legitimate surviving POLYBIUS/PLINY locus.
> - r5/r7: ratified-with-eyes-open in §5/§7 (not "fixed").

## §0 Problem restatement (pre-work gate)

The `check-substrate-updates` read-only update path hardcodes the expected MAJOR set to
POLYBIUS + PLINY at three loci in `check.sh`, and the deploy-time manifest writer in `install.sh`
emits manifest lines for POLYBIUS + PLINY only. CAPTAINs, templates, and skills are all
auto-discovered (glob / parse); MAJORs are the lone hardcoded anomaly. The Arc 61/62 MAJORs
CHIRON + HAMILTON are therefore invisible to the update path: `check.sh` reports them as neither
MISSING nor DRIFTED, so the EXISTING-project update path silently skips the design layer when
bringing an existing-Stoa project current. (A *fresh* `install.sh` already deploys CHIRON/HAMILTON
correctly — the deploy path at `install.sh:954-998` is complete; the gap is the **update path only**.)

Fix: make the MAJOR set **glob-derived** (`MAJOR_*.md` from the substrate source dir) at all four
loci, applying the MAJOR-specific suffix rule (suffixed at **subproject tier only**; project + user
tiers carry no suffix — different from CAPTAINs, which suffix at project AND subproject). Then any
future MAJOR auto-discovers and this bug class cannot recur.

**Imported assumption (named):** "any future MAJOR follows the subproject-only suffix rule." This is
true for all four MAJORs today (install.sh `SUFFIX_MAJORS` governs all of them uniformly) and is the
de-facto MAJOR contract. The glob design *encodes* this rule rather than re-checking it per-MAJOR;
if a future MAJOR ever needed a different suffix rule, every locus would need a per-MAJOR branch.
Flagged in §5.

---

## §1 Confirmed diagnosis (own line numbers; cited against worktree, not directive)

Confirmed by direct read of the worktree files. Directive line numbers drifted by 1–6 lines
(NOMOS already noted this); the **code matches the diagnosis exactly**. No disagreement with the
verified diagnosis — I confirm it in full, including the CRITICAL suffix finding.

| # | Locus | File:lines (worktree) | Current behavior | Class |
|---|---|---|---|---|
| 1 | `enumerate_deployed()` MAJOR block | `check.sh:401-408` | two-branch hardcoded echo of `MAJOR_POLYBIUS`/`MAJOR_PLINY` (subproject-suffixed branch + unsuffixed branch) | **PRIMARY** (MISSING blind spot) |
| 2 | `source_path_for_deployed()` case | `check.sh:294-299` | case arms map only `MAJOR_POLYBIUS{.md,_*.md}` and `MAJOR_PLINY{.md,_*.md}` → source | SECONDARY (DRIFTED detection) |
| 3 | `apply_substitutions()` case | `check.sh:119` (fn head :107) | case pattern `.claude/MAJOR_POLYBIUS*.md\|.claude/MAJOR_PLINY*.md\|.claude/agents/CAPTAIN_*.md` | SECONDARY (subproject byte-compare; **legacy fallback path only** — manifest-driven `apply_substitutions_from_manifest` is primary per Arc 38) |
| 4 | `write_substrate_manifest()` MAJOR block | `install.sh:537-548` | emits manifest lines for POLYBIUS/PLINY only (subproject-suffixed branch + else branch with user-tier USER_TIER_DIR line) | SECONDARY (deploy-time manifest completeness) |

**Pattern to mirror (PRIMARY):** the CAPTAIN glob immediately below the MAJOR block —
`check.sh:414-421` — globs `${SUBSTRATE_DIR}/CAPTAIN_*.md`, strips to mnemonic, emits
`.claude/agents/CAPTAIN_<mnemonic>${suffix}.md`. The MAJOR fix mirrors this **but with the MAJOR
suffix rule, not the CAPTAIN suffix rule** (the `${suffix}` var the CAPTAIN loop uses is
project+subproject; the MAJOR loop must use subproject-only).

**Source dirs for the glob (confirmed):**
- `check.sh`: `SUBSTRATE_DIR` (`check.sh:35` = `${SCRIPT_DIR}/../..`) = the `substrate/` source root, where `MAJOR_*.md` and `CAPTAIN_*.md` live. The existing CAPTAIN glob already uses it.
- `install.sh`: `SCRIPT_DIR` (`install.sh:155` shows `SRC_POLYBIUS="${SCRIPT_DIR}/MAJOR_POLYBIUS.md"`) = the `substrate/` source root. Glob `${SCRIPT_DIR}/MAJOR_*.md`.

**Suffix rule CONFIRMED (the load-bearing footgun):**
- `install.sh:720` `SUFFIX_MAJORS=0` (default). `install.sh:813` sets `SUFFIX_MAJORS=1` **only** in the `subproject` target branch. Project + user branches leave it 0.
- `install.sh:954-963`: `SUFFIX_MAJORS=1` → `DEST_<MAJOR>="${DEST_DIR}/MAJOR_<MAJOR>${NAME_SUFFIX}.md"`; else unsuffixed. **All four MAJORs (POLYBIUS, PLINY, CHIRON, HAMILTON) are listed identically** — one shared suffix rule, no per-MAJOR special case. Deploy writes at `:993-998` already emit CHIRON/HAMILTON.
- `check.sh:397-399` + `:402` already encode this rule for MAJORs (`if [ "$tier" = "subproject" ]`); the bug is purely that the echoes inside that branch name only POLYBIUS/PLINY.
- Contrast CAPTAINs: `enumerate_deployed:398` sets `suffix="_${slug}"` for `project|subproject`, and the CAPTAIN loop at `:419` applies `${suffix}` unconditionally — project AND subproject suffixed.

**Conclusion:** glob `MAJOR_*.md` + reuse the *existing subproject-only* MAJOR-suffix conditional
is the correct shape at every locus. No per-MAJOR branching. No disagreement with the diagnosis.

---

## §2 Per-locus concrete edits (current → proposed)

### Locus 1 — `check.sh` `enumerate_deployed()` (PRIMARY)

**Current (`check.sh:401-408`):**
```bash
  # MAJOR files: subproject-tier suffixes both; project/user-tier do not.
  if [ "$tier" = "subproject" ]; then
    echo ".claude/MAJOR_POLYBIUS${suffix}.md"
    echo ".claude/MAJOR_PLINY${suffix}.md"
  else
    echo ".claude/MAJOR_POLYBIUS.md"
    echo ".claude/MAJOR_PLINY.md"
  fi
```

**Proposed:**
```bash
  # MAJOR files: glob substrate/MAJOR_*.md so any future MAJOR (CHIRON, HAMILTON, ...)
  # auto-discovers. MAJOR suffix rule (DIFFERENT from CAPTAINs): suffixed at
  # subproject tier ONLY; project + user tiers carry no suffix. Mirror of the
  # CAPTAIN glob below, but the MAJOR-suffix conditional replaces the CAPTAIN
  # ${suffix}. install.sh SUFFIX_MAJORS governs the same rule at deploy time.
  local majf maj_base major_suffix=""
  [ "$tier" = "subproject" ] && major_suffix="${suffix}"
  shopt -s nullglob
  for majf in "${SUBSTRATE_DIR}/MAJOR_"*.md; do
    maj_base="$(basename "$majf" .md)"   # "MAJOR_POLYBIUS"
    echo ".claude/${maj_base}${major_suffix}.md"
  done
  shopt -u nullglob
```
Note: `${suffix}` is already `_${slug}` for project|subproject (set at `:397-399`); gating on
`tier = subproject` for `major_suffix` reproduces the MAJOR rule exactly (empty at project/user).
`nullglob` is toggled the same way the CAPTAIN/template loops do (matched by `shopt -u` after).

### Locus 2 — `check.sh` `source_path_for_deployed()`

**Current (`check.sh:294-299`):**
```bash
    MAJOR_POLYBIUS.md|MAJOR_POLYBIUS_*.md)
      echo "MAJOR_POLYBIUS.md"
      ;;
    MAJOR_PLINY.md|MAJOR_PLINY_*.md)
      echo "MAJOR_PLINY.md"
      ;;
```

**Proposed (generalize both arms to one MAJOR arm, mirroring the CAPTAIN arm below it):**
```bash
    MAJOR_*.md)
      # Any deployed MAJOR maps back to its unsuffixed source name. Strip the
      # subproject suffix (present only at subproject tier) before reattaching .md.
      # MAJOR suffix rule: suffixed at subproject ONLY. ${suffix} is _${slug} for
      # project|subproject, but MAJORs are unsuffixed at project, so only strip
      # when tier=subproject. The deployed name's own suffix, if any, is what we strip.
      local mbase="${rel%.md}"            # "MAJOR_POLYBIUS_acme" or "MAJOR_POLYBIUS"
      if [ "$tier" = "subproject" ] && [ -n "$suffix" ]; then
        mbase="${mbase%${suffix}}"        # strip "_acme" -> "MAJOR_POLYBIUS"
      fi
      echo "${mbase}.md"
      ;;
```
Why suffix-stripping (not a fixed echo): the deployed name varies at subproject tier
(`MAJOR_CHIRON_acme.md`), so we must recover the source name `MAJOR_CHIRON.md` by removing the
known `${suffix}`. At project/user tier the deployed name is already unsuffixed, so `mbase` is the
answer directly. This mirrors the CAPTAIN arm's `base="${base%${suffix}.md}"` logic at `:303-312`,
adjusted for the subproject-only MAJOR rule. **Case-arm ordering is safe:** the
`operating-disciplines.md)` arm precedes this MAJOR arm (check.sh:300), so the generalized
`MAJOR_*.md)` arm cannot shadow it (ARGUS-confirmed; only four `substrate/MAJOR_*.md` exist, all role
files).

### Locus 3 — `check.sh` `apply_substitutions()` case (LEGACY fallback path)

**Current (`check.sh:119`):**
```bash
    .claude/MAJOR_POLYBIUS*.md|.claude/MAJOR_PLINY*.md|.claude/agents/CAPTAIN_*.md)
```

**Proposed:**
```bash
    .claude/MAJOR_*.md|.claude/agents/CAPTAIN_*.md)
```
`.claude/MAJOR_*.md` is a strict superset of `.claude/MAJOR_POLYBIUS*.md|.claude/MAJOR_PLINY*.md`
that also matches CHIRON/HAMILTON and any future MAJOR. The branch body (the `{{NAME_SUFFIX}}` sed)
is unchanged — all MAJORs take the same NAME_SUFFIX substitution. **Relationship preserved:** this
is the legacy fallback only; `apply_substitutions_from_manifest` (the Arc 38 primary path) is
untouched and remains primary — it reads the manifest, which Locus 4 fixes. Also update the
doc-comment substitution-policy block at `check.sh:101-103` (currently lists
`.claude/MAJOR_POLYBIUS*.md` / `.claude/MAJOR_PLINY*.md` as separate policy lines) to a single
`.claude/MAJOR_*.md : NAME_SUFFIX` line so the comment does not re-introduce the hardcoded
enumeration as documentation drift (a future reader could "restore consistency" by re-hardcoding).

> **r5 ratification (ratified-with-eyes-open; NOT a fix):** the `.claude/MAJOR_*.md` generalization is
> a genuine superset only because all four `substrate/MAJOR_*.md` sources are role files needing the
> NAME_SUFFIX substitution. A hypothetical pair-programmer-added **non-substrate** `.claude/MAJOR_FOO.md`
> at a workspace would, after this change, be force-substituted at check-time where before it fell to the
> verbatim default arm (`check.sh:125-128`). **Attack-path / behavior-change:** workspace adds a
> non-substrate `.claude/MAJOR_FOO.md` → check.sh byte-compare seds `{{NAME_SUFFIX}}` into it →
> spurious DRIFTED/clean delta on a file the substrate does not own. **Bounded:** check.sh is
> read-only/informational (exit 0 always; check.sh:27-28); it only affects the byte-compare *display*
> of a non-substrate MAJOR, never a write. apply.sh (the only writer) is untouched. **Decision: RATIFY.**
> Correct for all MAJORs today (all four are substrate role files); the custom-MAJOR convention is
> hard-locked out of scope (Arc 29 A7; check.sh:486-496 cite). If a future arc adds custom-MAJOR
> support, this arm needs the same base-vs-custom path-shape skip the CAPTAIN site documents. Noted, not
> defended-against, because no non-substrate MAJOR exists and the blast radius is an informational
> display only.

### Locus 4 — `install.sh` `write_substrate_manifest()` MAJOR block

**Current (`install.sh:537-548`):**
```bash
    # MAJOR_POLYBIUS.md: NAME_SUFFIX always; USER_TIER_DIR at user-tier only.
    # Subproject-tier suffixes the MAJOR filename; project + user tiers do not.
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
```

**Proposed (glob `${SCRIPT_DIR}/MAJOR_*.md`; preserve the subproject-only suffix + the
POLYBIUS-only USER_TIER_DIR special line):**
```bash
    # MAJOR files: glob substrate/MAJOR_*.md so any future MAJOR auto-discovers
    # in the manifest. NAME_SUFFIX substitution for all; subproject tier suffixes
    # the deployed filename, project + user do not (mirror install.sh SUFFIX_MAJORS
    # + check.sh enumerate_deployed). USER_TIER_DIR is a POLYBIUS-only placeholder
    # (only MAJOR_POLYBIUS.md carries {{USER_TIER_DIR}}), emitted at user-tier only.
    local srcmaj majname dep_name
    shopt -s nullglob
    for srcmaj in "${SCRIPT_DIR}/MAJOR_"*.md; do
      majname="$(basename "$srcmaj" .md)"        # "MAJOR_POLYBIUS"
      if [ "$tier" = "subproject" ]; then
        dep_name=".claude/${majname}${name_suffix}.md"
      else
        dep_name=".claude/${majname}.md"
      fi
      printf "%s\t{{NAME_SUFFIX}}\t%s\n" "$dep_name" "${name_suffix}"
      if [ "$tier" = "user" ] && [ -n "$USER_TIER_DIR" ] && [ "$majname" = "MAJOR_POLYBIUS" ]; then
        printf "%s\t{{USER_TIER_DIR}}\t%s\n" "$dep_name" "$USER_TIER_DIR"
      fi
    done
    shopt -u nullglob
```
**Two invariants preserved exactly:**
1. *Subproject suffixing* — `${name_suffix}` is `_${slug}` for project|subproject (set at `:504-506`) but the deployed filename only takes it at subproject (matches the current `if [ "$tier" = "subproject" ]`).
2. *USER_TIER_DIR is POLYBIUS-only* — the current code emits the `{{USER_TIER_DIR}}` line only for `MAJOR_POLYBIUS.md`. The proposed `[ "$majname" = "MAJOR_POLYBIUS" ]` guard preserves this; CHIRON/HAMILTON/PLINY get only the NAME_SUFFIX line. This is correct because only `MAJOR_POLYBIUS.md` source carries the `{{USER_TIER_DIR}}` placeholder (confirmed: `install.sh:988` substitutes USER_TIER_DIR into POLYBIUS only).

Also update the **install.sh writer doc-comment** at `install.sh:537` (currently names
`MAJOR_POLYBIUS.md` in the leading comment) so it does not re-document the old hardcoded set — the
proposed block's leading comment already does this.

**`nullglob` safety:** all four globs use `shopt -s nullglob` / `shopt -u nullglob`. If the source
dir somehow had zero `MAJOR_*.md`, the loop body never runs (no literal-glob line emitted). See §5.4
(r7) for the explicit ratify-or-defer decision on this.

---

## §3 Suffix-correctness table (per tier × locus — the footgun-killer)

For a MAJOR with mnemonic `<M>` (e.g. `POLYBIUS`, `CHIRON`) and project slug `<slug>`:

| Tier | Deployed filename | enumerate_deployed emits | source_path_for_deployed returns | manifest dep-path emitted | apply_substitutions match |
|---|---|---|---|---|---|
| **user** | `.claude/MAJOR_<M>.md` | `.claude/MAJOR_<M>.md` (no suffix) | `MAJOR_<M>.md` | `.claude/MAJOR_<M>.md` (+ USER_TIER_DIR line for POLYBIUS only) | `.claude/MAJOR_<M>.md` ✓ |
| **project** | `.claude/MAJOR_<M>.md` | `.claude/MAJOR_<M>.md` (no suffix) | `MAJOR_<M>.md` | `.claude/MAJOR_<M>.md` | `.claude/MAJOR_<M>.md` ✓ |
| **subproject** | `.claude/MAJOR_<M>_<slug>.md` | `.claude/MAJOR_<M>_<slug>.md` (suffixed) | `MAJOR_<M>.md` (strip `_<slug>`) | `.claude/MAJOR_<M>_<slug>.md` (suffixed) | `.claude/MAJOR_<M>_<slug>.md` ✓ |

Cross-check against CAPTAINs (must stay different): CAPTAIN is suffixed at **project AND
subproject** — `.claude/agents/CAPTAIN_<M>_<slug>.md` at both — unsuffixed only at user. The MAJOR
row at **project** is the one that must NOT carry a suffix; a copy-paste of the CAPTAIN rule there
is the exact failure that produces a false MISSING (`MAJOR_<M>_<slug>.md` expected, `MAJOR_<M>.md`
on disk) + a false OBSOLETE. Probe V4 (§4) targets this directly.

**Audit status:** ARGUS + floor-manager + user-tier POLYBIUS independently verified every cell of this
table against actual source, including the project-tier no-suffix cell (the attack target). rev2 does
NOT change any cell.

---

## §4 Verification probes (concrete, runnable, falsifiable) — FULLY REWRITTEN IN rev2

All probes run from the substrate source root (the worktree root `.claude/worktrees/arc-66-build`).
POSIX/bash scripts; git-bash on Windows. **All flag spellings below are verified by direct read of the
arg-parse in `install.sh` / `check.sh` / `apply.sh`** (not from described behavior — rev1 weak-point #3):

- **install.sh project deploy:** `--target project --project-dir <path>` (NOT `--dest`). CAPTAINs deploy
  by DEFAULT; flag to skip is `--no-captains` (there is no `--with-captains`). (`install.sh:618-666`,
  usage :26-28.)
- **install.sh subproject deploy:** `--target subproject --parent-dir <parent> --subproject <slug>`
  (deployed dir is `<parent>/<slug>`). (`install.sh:628-634`, :761-762.)
- **check.sh:** `--workspace <path>`. (`check.sh:45`.)
- **apply.sh:** requires `--workspace <path>` AND one of `--all-differing` | `--files <f>`. Bare
  `--workspace` (neither) HARD-ERRORS (`apply.sh:324`, exit 2). `--all-differing` harvests ONLY
  `"  - "` (DRIFTED) lines from check.sh output (`apply.sh:303-316`); it never delivers MISSING.
- **MISSING delivery = `install.sh` RE-RUN**, per check.sh's own routing footer
  (`check.sh:984-1000`): MISSING routes to `install.sh --target <tier> --project-dir <ws>`
  (project/user) or the `--parent-dir/--subproject` form (subproject); DRIFTED routes to `apply.sh`.
- **Output prefixes (check.sh:940-942 + emission :944-972):** DRIFTED `"  - "`, MISSING `"  + "`,
  OBSOLETE `"  ! "`.

Throwaway targets are FIXED LITERAL paths (per `operating-disciplines.md` §8.6 — no `$VAR` expansion
in any destructive `rm`).

### V1 — REAL DoD probe (project tier): the VISIBILITY FLIP for CHIRON/HAMILTON (r1 + r2 + r3)

**The point of this probe is VISIBILITY**, per the ratified DoD mechanism. The falsification baseline is
the clean contrast: PRE-FIX, removed CHIRON/HAMILTON appear in NEITHER category (the actual bug);
POST-FIX they report MISSING.

```bash
# --- BASELINE CAPTURE (run BEFORE the §2 edits land — on the PRE-FIX check.sh) ---
rm -rf /tmp/arc66-tw-project
mkdir -p /tmp/arc66-tw-project
# Deploy current substrate, project tier (CAPTAINs are default — no flag needed).
bash substrate/install.sh --target project --project-dir /tmp/arc66-tw-project
# Remove the deployed design layer to simulate a pre-design-layer (existing-Stoa) deployment.
rm -f /tmp/arc66-tw-project/.claude/MAJOR_CHIRON.md
rm -f /tmp/arc66-tw-project/.claude/MAJOR_HAMILTON.md
# PRE-FIX check: capture the report. EXPECT (the bug): CHIRON + HAMILTON appear in
# NEITHER the MISSING ("  + ") NOR the DRIFTED ("  - ") block — they are never enumerated.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project | tee /tmp/arc66-prefix-report.txt

# --- POST-FIX (after the §2 edits land) — same removed-file state ---
# (If the worktree state was rebuilt, re-deploy + re-remove CHIRON/HAMILTON identically first.)
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project | tee /tmp/arc66-postfix-report.txt
#   PASS: post-fix report names ".claude/MAJOR_CHIRON.md" AND ".claude/MAJOR_HAMILTON.md"
#         under the MISSING ("  + ") block. (Pre-fix they were in neither block.)

# --- DELIVERY of the MISSING seats = install.sh RE-RUN (NOT apply.sh) ---
bash substrate/install.sh --target project --project-dir /tmp/arc66-tw-project
# Re-check -> clean: no MISSING, no DRIFTED for CHIRON/HAMILTON.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
```
**Falsification baseline (the clean visibility-flip contrast):** PRE-FIX report = CHIRON/HAMILTON in
NEITHER category; POST-FIX report (identical removed-file state) = CHIRON/HAMILTON in MISSING. That
flip IS the falsifier. If POST-FIX does NOT name both under MISSING, the `enumerate_deployed` glob
(Locus 1) is wrong. If the post-delivery re-check is not clean, `source_path_for_deployed` (Locus 2) or
the manifest (Locus 4) is wrong.

> **Why install.sh-re-run, not apply.sh, for MISSING:** `apply.sh --all-differing` harvests only the
> DRIFTED (`"  - "`) prefix (apply.sh:303-316); MISSING (`"  + "`) is structurally never harvested.
> check.sh's own routing footer (check.sh:984-1000) routes MISSING to an install.sh re-run. apply.sh's
> DRIFTED-only path is exercised separately in V2.

### V2 — DRIFTED detection + apply.sh DRIFTED-only harvest (the SEPARATE apply.sh path)

This is the probe that exercises `apply.sh --all-differing` — on a deployed-but-stale (DRIFTED) MAJOR,
NOT on a MISSING one. It proves both `source_path_for_deployed` (Locus 2) maps a deployed MAJOR back to
source AND that apply.sh's DRIFTED harvest picks it up.

```bash
# On the V1 clean project deploy (CHIRON/HAMILTON present), mutate a deployed MAJOR to force DRIFTED.
printf '\n# arc66-drift-probe\n' >> /tmp/arc66-tw-project/.claude/MAJOR_CHIRON.md
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#   PASS-a: ".claude/MAJOR_CHIRON.md" reported under DRIFTED ("  - ") — proves Locus 2 maps it to source.
# Now exercise the apply.sh DRIFTED-only harvest (requires --all-differing; bare --workspace errors).
bash substrate/skills/check-substrate-updates/apply.sh --workspace /tmp/arc66-tw-project --all-differing --yes
#   PASS-b: apply.sh harvests MAJOR_CHIRON.md from the DRIFTED block and re-deploys it (exit 0).
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#   PASS-c: re-check clean for MAJOR_CHIRON.md (no DRIFTED).
```
**Falsifier:** if CHIRON shows MISSING/OBSOLETE instead of DRIFTED, Locus 2's source mapping returned
empty (the `*)` unknown arm) → the generalized `MAJOR_*.md` arm is wrong. If apply.sh reports "nothing
to apply" while check.sh shows CHIRON DRIFTED, the harvest/path-shape is wrong (not expected — apply.sh
is untouched by this arc; this is a round-trip sanity check on Locus 2's output feeding apply.sh).

### V3 — Subproject-tier slice (the suffix path) + FAIL-LOUD A–E via REAL recompose

```bash
rm -rf /tmp/arc66-parent
mkdir -p /tmp/arc66-parent
# Establish a parent project first (subproject deploys UNDER an existing parent).
bash substrate/install.sh --target project --project-dir /tmp/arc66-parent
# Subproject deploy: SUFFIX_MAJORS=1 -> deployed names carry _<slug>. This is the REAL recompose that
# exercises FAIL-LOUD Checks A-E (NOT --dry-run, which early-returns before the awk checks at :1078).
bash substrate/install.sh --target subproject --parent-dir /tmp/arc66-parent --subproject arc66tw
#   PASS condition 1 (FAIL-LOUD): install exits 0 — Checks A-E (install.sh recompose awk, :1085-1112)
#   green; no err() abort.
#   Verify deployed MAJOR names ARE suffixed at the subproject dir:
ls /tmp/arc66-parent/arc66tw/.claude/MAJOR_*.md
#   Expect: MAJOR_POLYBIUS_arc66tw.md, MAJOR_PLINY_arc66tw.md, MAJOR_CHIRON_arc66tw.md, MAJOR_HAMILTON_arc66tw.md
# Now the MISSING slice at subproject tier: remove a suffixed MAJOR.
rm -f /tmp/arc66-parent/arc66tw/.claude/MAJOR_CHIRON_arc66tw.md
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-parent/arc66tw
#   PASS: MAJOR_CHIRON_arc66tw.md (SUFFIXED name) reported MISSING — proves enumerate_deployed applied
#   the subproject suffix to the glob-derived MAJOR.
```
**Falsifier (the footgun):** if check.sh reports `MAJOR_CHIRON.md` (UNSUFFIXED) MISSING **and**
`MAJOR_CHIRON_arc66tw.md` OBSOLETE, the subproject suffix was not applied to the glob result — Locus
1's `major_suffix` gate is wrong. If install.sh aborts with a Check A–E `err()`, the recompose broke
(out-of-scope regression — STOP and surface).

### V4 — Project-tier no-false-suffix assertion (the inverse footgun)

```bash
# On the V1 clean project deploy: MAJOR names must be UNSUFFIXED at project tier.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#   PASS: zero MISSING and zero OBSOLETE for any MAJOR. A false suffix at project tier
#   (CAPTAIN-rule leakage) would produce exactly one MISSING + one OBSOLETE per MAJOR.
```
**Falsifier:** any MAJOR MISSING/OBSOLETE pair on the clean project deploy = the suffix rule leaked the
CAPTAIN (project+subproject) rule onto MAJORs at Locus 1.

### V5 — Manifest completeness (install.sh Locus 4)

```bash
# Project tier:
grep 'MAJOR_' /tmp/arc66-tw-project/.claude/.substrate-manifest
#   Expect 4 NAME_SUFFIX lines: MAJOR_POLYBIUS.md, MAJOR_PLINY.md, MAJOR_CHIRON.md, MAJOR_HAMILTON.md
#   (project tier -> empty replacement value). NO USER_TIER_DIR line (project tier).
# Subproject tier:
grep 'MAJOR_' /tmp/arc66-parent/arc66tw/.claude/.substrate-manifest
#   Expect 4 lines with _arc66tw suffix in the dep-path AND _arc66tw replacement value.
```
**Falsifier:** fewer than 4 MAJOR lines = glob missed a MAJOR; a USER_TIER_DIR line for a non-POLYBIUS
MAJOR = the POLYBIUS-only guard is wrong; a suffix at project tier = invariant 1 broke.

### V6 — App green (full suite, re-derives the whole roster)

```bash
cd app && npm run gen-data && npm run build && npm test
```
Expected app-neutral (tooling change, no role-file edit), but assert from the FULL run — `gen-data`
re-derives the entire roster from current substrate and can surface PRE-EXISTING drift (Arc 61 lesson:
assert from a full-suite run, not "this arc edited no X"). PASS = all green.

### V7 — No hardcoded POLYBIUS/PLINY-only MAJOR ENUMERATION remains at the four loci (r6)

```bash
grep -nE 'MAJOR_POLYBIUS|MAJOR_PLINY' substrate/skills/check-substrate-updates/check.sh
grep -nE 'MAJOR_POLYBIUS|MAJOR_PLINY' substrate/install.sh
```
PASS condition is **manual classification, not a bare `grep -c`**. The gate is: **no surviving
*paired POLYBIUS+PLINY enumeration list* at the four fix loci.** Every surviving literal
`MAJOR_POLYBIUS` / `MAJOR_PLINY` hit MUST be one of these PRE-NAMED legitimate loci (a hit anywhere
ELSE at the four fix loci is a FAIL):

1. **`detect_tier()` tier sentinel — `check.sh:354-369`.** Keys tier detection on
   `MAJOR_POLYBIUS_*.md` / `MAJOR_POLYBIUS.md` as the canonical always-deployed sentinel. POLYBIUS-only
   (no PLINY), different concern (which-tier vs enumerate-all), OUT OF SCOPE. LEGITIMATE survivor.
2. **POLYBIUS-only `USER_TIER_DIR` guard — `install.sh` Locus 4** (the
   `[ "$majname" = "MAJOR_POLYBIUS" ]` guard in the proposed block). LEGITIMATE — only POLYBIUS source
   carries `{{USER_TIER_DIR}}`.
3. **`detect_tier`'s `USER_TIER_DIR` / user-tier POLYBIUS guard** anywhere it keys on `MAJOR_POLYBIUS`
   as the user-tier sentinel. LEGITIMATE survivor (same sentinel concern as #1).

The following loci MUST have been swept of the paired enumeration / hardcoded names (a leftover here is
a FAIL, NOT a legitimate survivor):

4. **Doc-comment substitution-policy block — `check.sh:101-103`** — Locus 3 collapses the two
   `.claude/MAJOR_POLYBIUS*.md` / `.claude/MAJOR_PLINY*.md` policy lines into one `.claude/MAJOR_*.md`
   line. CONFIRM no `MAJOR_POLYBIUS`/`MAJOR_PLINY` survives in this comment.
5. **install.sh writer doc-comment — `install.sh:537`** — Locus 4's proposed block replaces the
   leading comment; CONFIRM no `MAJOR_POLYBIUS.md` survives there as a documented enumeration.

A hit at #4 or #5 means a doc-comment was left re-documenting the old hardcoded set (r6) — FAIL the
gate and sweep it.

### V8 — SHARED-MACHINERY non-MAJOR regression probe (r4 — REQUIRED new probe)

The three EDITED check.sh functions (`enumerate_deployed`, `source_path_for_deployed`,
`apply_substitutions`) drive DRIFTED / MISSING / OBSOLETE detection for ALL deployed file categories,
not just MAJORs. This probe proves the MAJOR-glob generalization did NOT regress non-MAJOR detection —
the "full suite catches what the bespoke probe doesn't" discipline (user-tier POLYBIUS on-ticket).

Run on a project-tier workspace carrying a KNOWN combination of NON-MAJOR DRIFTED + MISSING + OBSOLETE:

```bash
rm -rf /tmp/arc66-tw-regress
mkdir -p /tmp/arc66-tw-regress
bash substrate/install.sh --target project --project-dir /tmp/arc66-tw-regress

# (a) NON-MAJOR DRIFTED — operating-disciplines.md byte-compare must still flag DRIFTED.
printf '\n# arc66-regress-drift\n' >> /tmp/arc66-tw-regress/.claude/operating-disciplines.md
# (b) NON-MAJOR MISSING — remove a deployed CAPTAIN; must still report MISSING.
rm -f /tmp/arc66-tw-regress/.claude/agents/CAPTAIN_VERA.md
# (c) NON-MAJOR OBSOLETE — a non-substrate CAPTAIN must NOT false-flag OBSOLETE (custom-agent
#     convention); a bogus deployed CAPTAIN that has no source SHOULD flag OBSOLETE.
#     custom (base-vs-custom convention) — must NOT flag OBSOLETE:
mkdir -p /tmp/arc66-tw-regress/.claude/agents/custom
printf '# pair-programmer agent\n' > /tmp/arc66-tw-regress/.claude/agents/custom/CAPTAIN_PAIRBOT.md
#     base-path bogus CAPTAIN with no source — SHOULD flag OBSOLETE:
printf '# orphaned\n' > /tmp/arc66-tw-regress/.claude/agents/CAPTAIN_GHOST.md
# (d) pair-programmer NON-SUBSTRATE MAJOR — the MAJOR_*.md OBSOLETE glob is single-path-segment
#     (check.sh:498) and apply_substitutions now matches .claude/MAJOR_*.md (r5). Confirm a
#     base-path non-substrate MAJOR flags OBSOLETE (it has no source) but the MAJOR_*.md glob does
#     NOT over-match operating-disciplines.md (which is NOT a MAJOR_ file).
printf '# pair-programmer major\n' > /tmp/arc66-tw-regress/.claude/MAJOR_FOO.md

bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-regress
```
**PASS conditions (assert ALL):**
- (a) `.claude/operating-disciplines.md` reported **DRIFTED** (`"  - "`). Proves
  `source_path_for_deployed`'s `operating-disciplines.md)` arm still maps correctly and the generalized
  `MAJOR_*.md)` arm did NOT shadow it.
- (b) `.claude/agents/CAPTAIN_VERA.md` reported **MISSING** (`"  + "`). Proves enumerate_deployed's
  CAPTAIN glob still drives MISSING (untouched by the MAJOR edits).
- (c) `.claude/agents/custom/CAPTAIN_PAIRBOT.md` does **NOT** appear OBSOLETE (custom path-shape skip
  intact); `.claude/agents/CAPTAIN_GHOST.md` **DOES** appear OBSOLETE (`"  ! "`).
- (d) `.claude/MAJOR_FOO.md` appears OBSOLETE under the manual-rm MAJOR footer
  (`(dropped from source; manual-rm — see footer)`); `operating-disciplines.md` is NOT mis-listed as a
  MAJOR. Confirms the `MAJOR_*.md` glob over-match boundary.

**Falsifier:** any of (a)–(d) wrong = the MAJOR-glob change regressed shared non-MAJOR detection. In
particular, if `operating-disciplines.md` is mis-mapped or the generalized `MAJOR_*.md)` arm in
`source_path_for_deployed` swallows a non-MAJOR path, this probe catches it where V1–V7 (MAJOR-scoped)
would not.

### V9 — Other existing suites the change could touch (the standing full-suite step)

Per the ratified "full-suite + bespoke probes" VERA discipline:

```bash
# Author-gate hook tests (present at substrate/hooks/tests/run-author-gate-tests.sh).
bash substrate/hooks/tests/run-author-gate-tests.sh
#   PASS: all green (the change touches neither hooks nor author fields, but assert from a real run).
```
The FAIL-LOUD subproject recompose (REAL, not `--dry-run`) is covered by V3; the app full suite by V6.
**Falsifier:** any non-green here = an unexpected cross-surface regression — STOP and surface.

---

## §5 Self-assessed weak points (attack these hardest, ARGUS)

1. **`detect_tier()` is intentionally NOT in scope but is the one remaining hardcoded POLYBIUS
   reference (`check.sh:354-369`).** It keys tier detection on `MAJOR_POLYBIUS_<slug>.md` /
   `MAJOR_POLYBIUS.md` as the tier sentinel. This is *correct* (POLYBIUS is the canonical
   always-deployed MAJOR; one sentinel is fine) and de-hardcoding it is out of the directive's scope.
   **Risk:** V7's grep hits it; a reader who reads V7 as "zero POLYBIUS/PLINY literals" would wrongly
   try to de-hardcode the tier sentinel. rev2 V7 PASS-condition now PRE-NAMES it (locus #1) as a
   legitimate survivor. *Why this shape anyway:* the tier sentinel is a different concern
   (detect-which-tier vs enumerate-all-MAJORs); folding it in exceeds no-broader-refactor.

2. **`source_path_for_deployed()` suffix-strip correctness at subproject tier (Locus 2).** The proposed
   `mbase="${mbase%${suffix}}"` strips the *slug* suffix. If a MAJOR mnemonic ever ended with a string
   equal to the slug, the strip could over-trim — extremely unlikely (mnemonics are uppercase
   Greek/historical names; slugs are lowercased project dirs) but it is a string-suffix strip, not a
   structural parse. *Why this shape anyway:* it exactly mirrors the shipped CAPTAIN arm's
   `base="${base%${suffix}.md}"`, inheriting the same (accepted) assumption already in production for
   CAPTAINs; a stricter parse only for MAJORs would diverge from the proven pattern.
   (ARGUS-confirmed negligible + inherited, not newly introduced.)

3. **Probe interface names — RESOLVED in rev2.** rev1 wrote flags from described behavior. rev2 §4
   verified EVERY flag by direct read of the arg-parse (`install.sh:618-666`, `check.sh:45`,
   `apply.sh:37-70/324`) and the check.sh routing footer (`:984-1000`). Residual risk: line numbers can
   drift by a few lines on rebase (the diagnosis-vs-directive drift pattern NOMOS already noted); ADA/VERA
   should match by function name, not raw line, if a cited line does not land exactly.

4. **`nullglob` empty-loop on a MAJOR-less substrate emits zero manifest/enumeration lines silently —
   ratified, see §5(r7) below.** (No longer "flagged for ARGUS to decide"; rev2 makes the decision.)

5. **Doc-comment drift surface.** Two doc-comment blocks (`check.sh:101-103` substitution policy;
   `install.sh:537` writer comment) currently spell out POLYBIUS/PLINY. Locus 3 sweeps the check.sh one;
   Locus 4 sweeps the install.sh one. V7 PASS-condition loci #4/#5 now make a leftover comment an
   EXPLICIT gate FAIL (r6). *Why named:* a leftover comment leaves the code correct but re-documents the
   old hardcoded set; a future reader could "restore consistency" by re-hardcoding.

**r5 ratification (Locus 3 superset force-substitutes a non-substrate `.claude/MAJOR_FOO.md`):** stated
in full at §2 Locus 3. **Decision: RATIFY.** Correct for all four MAJORs today (all substrate role
files); the behavior change only affects the *informational byte-compare display* of a hypothetical
non-substrate MAJOR (check.sh is read-only; apply.sh untouched); custom-MAJOR support is hard-locked out
of scope (Arc 29 A7). Attack-path noted; not defended-against because no non-substrate MAJOR exists and
the blast radius is display-only. V8(d) exercises the related OBSOLETE-glob over-match boundary.

**r7 ratification (empty-glob `nullglob` silently enumerates zero MAJORs on a MAJOR-less substrate
checkout):** **Decision: DEFER as an out-of-scope follow-up — conscious ratification, not a silent
accept.** Rationale: (1) PRE-EXISTING — the CAPTAIN glob (`check.sh:416`) and the OBSOLETE workspace
glob (`check.sh:498`) already have the identical property; this arc neither introduces nor worsens it.
(2) The directive scopes the arc to "the MAJOR-enumeration completeness fix only; do NOT touch role
files or expand check.sh refactors" — adding FAIL-LOUD-on-empty-glob is a new behavior class that mixes
scope. (3) A substrate checkout with zero `MAJOR_*.md` is a corrupt-checkout degenerate case, not a
normal operating state. **Follow-up:** file a scoped ticket — "FAIL-LOUD on empty MAJOR_*.md / CAPTAIN_*.md
glob in check.sh enumerate_deployed + OBSOLETE detection + install.sh manifest writer" — to be picked up
when a check.sh-hardening arc is in scope. The parse-empty FAIL-LOUD pattern already exists for skills
(`parse_skill_names_from_install`) and is the model for that follow-up. (This is a TECHNICAL-tier
decision DAEDALUS/PLINY own per the Principal-as-router antipattern — NOT a PRINCIPAL gate.)

---

## §6 Out of scope (keeps ADA from scope-creep)

- `detect_tier()` tier-sentinel de-hardcoding — different concern, see §5.1.
- Role files `MAJOR_*.md` — untouched (deliverable constraint).
- Any broader `check-substrate-updates` refactor beyond the four enumeration loci.
- `deploy-stoa` / `install-stoa` skills — correct; the bug is downstream.
- `u--k5s` CRLF `agents.ts` item — separate.
- zeotek_newswire — probes use throwaways at fixed literal paths; never touch A2A's project.
- **Empty-glob FAIL-LOUD hardening (§5 r7) — DEFERRED to a scoped follow-up ticket, not this arc.**
- Custom-MAJOR support (the `.claude/custom/MAJOR_*.md` convention) — hard-locked out per Arc 29 A7;
  the r5 force-substitute behavior is correct precisely because no custom/non-substrate MAJOR exists.

## §7 Threat→mitigation map

No named threat. This is a process/tooling completeness fix with no runtime attack path
(`operating-disciplines.md` §35.5 carve-out): **not threat-ratified (process/tooling change, no
runtime attack path)** — ARGUS to confirm (ARGUS confirmed this carve-out in the rev1 verdict
non_findings; re-confirm against rev2). No threat-anchored probe required (§6.13). `check.sh` is
read-only/informational (exit 0 always; check.sh:27-28); `apply.sh` (the only writer) is UNTOUCHED by
this arc. The suffix-correctness probes (V3/V4) and the shared-machinery probe (V8) defend against the
silent false-MISSING/false-OBSOLETE correctness footgun — but that is a correctness hazard, not a
security threat. The r5 force-substitute behavior change is a display-only correctness consideration on
a non-existent non-substrate MAJOR, also not a security attack path.
