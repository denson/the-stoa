# Design — stoa--5ju (Arc 66): glob-derive the MAJOR set in check-substrate-updates + install.sh manifest

**Ticket:** stoa--5ju · **Arc:** 66 · **Author:** Denson Smith · **Seat:** CAPTAIN_DAEDALUS (architect)
**Branch:** arc-66/build · **Worktree root (cwd):** `.claude/worktrees/arc-66-build`

## §0 Problem restatement (pre-work gate)

The `check-substrate-updates` read-only update path hardcodes the expected MAJOR set to
POLYBIUS + PLINY at three loci in `check.sh`, and the deploy-time manifest writer in `install.sh`
emits manifest lines for POLYBIUS + PLINY only. CAPTAINs, templates, and skills are all
auto-discovered (glob / parse); MAJORs are the lone hardcoded anomaly. The Arc 61/62 MAJORs
CHIRON + HAMILTON are therefore invisible to the update path: `check.sh` reports them as neither
MISSING nor DRIFTED, so `apply.sh` silently skips the design layer when bringing an existing-Stoa
project current. (A *fresh* `install.sh` already deploys CHIRON/HAMILTON correctly — the deploy
path at `install.sh:954-998` is complete; the gap is the **update path only**.)

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
adjusted for the subproject-only MAJOR rule.

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
doc-comment substitution-policy block at `check.sh:101-102` (currently lists
`MAJOR_POLYBIUS*.md` / `MAJOR_PLINY*.md` as separate lines) to a single `MAJOR_*.md : NAME_SUFFIX`
line so the comment does not re-introduce the hardcoded enumeration as documentation drift.

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

**`nullglob` safety:** all four globs use `shopt -s nullglob` / `shopt -u nullglob`. If the source
dir somehow had zero `MAJOR_*.md`, the loop body never runs (no literal-glob line emitted). That is
a degenerate "broken substrate checkout" case; FAIL-LOUD is out of scope for this arc, but the
empty-loop behavior is at least not a corrupt manifest line. Flagged in §5.

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

---

## §4 Verification probes (concrete, runnable, falsifiable)

All probes run from the substrate source. Bash invocation (POSIX scripts; git-bash on Windows).
`<repo>` = the worktree root. Throwaway target = a fixed literal path (per §8.6 destructive-op
discipline — no `$VAR` in the `rm`).

### V1 — REAL DoD probe (project tier): MISSING detection for CHIRON/HAMILTON

```bash
# Fixed literal throwaway path (no var-expansion in destructive ops).
TW=/tmp/arc66-tw-project
rm -rf /tmp/arc66-tw-project
mkdir -p /tmp/arc66-tw-project
# 1. Deploy current substrate (project tier, with CAPTAINs).
bash substrate/install.sh --target project --dest /tmp/arc66-tw-project --with-captains   # confirm real flag names against install.sh --help first
# 2. FALSIFICATION BASELINE (pre-fix): on the PRE-FIX check.sh, CHIRON+HAMILTON are NOT reported.
#    Run BEFORE applying the fix; capture output. Expect: no CHIRON/HAMILTON MISSING line.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
# 3. Simulate a pre-design-layer deployment: remove deployed CHIRON + HAMILTON (literal paths).
rm -f /tmp/arc66-tw-project/.claude/MAJOR_CHIRON.md
rm -f /tmp/arc66-tw-project/.claude/MAJOR_HAMILTON.md
# 4. POST-FIX: re-run check.sh -> expect CHIRON + HAMILTON reported MISSING.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#    PASS: output names MAJOR_CHIRON.md AND MAJOR_HAMILTON.md as MISSING.
#    (Pre-fix step-2 baseline: they were absent from the report even when present on disk?
#     No — pre-fix they are simply never enumerated; with them removed pre-fix, still no MISSING line.
#     The falsifying contrast is: pre-fix removal -> silent; post-fix removal -> MISSING.)
# 5. apply delivers them.
bash substrate/skills/check-substrate-updates/apply.sh --workspace /tmp/arc66-tw-project   # confirm apply.sh flag/interface
# 6. Re-check -> clean (no MISSING, no DRIFTED for CHIRON/HAMILTON).
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
```
**Falsifier:** if step-4 does NOT name both CHIRON and HAMILTON as MISSING, the enumerate_deployed
glob (Locus 1) is wrong. If step-6 is not clean, source_path_for_deployed (Locus 2) or the
manifest (Locus 4) is wrong.

### V2 — DRIFTED detection (project tier): source_path_for_deployed round-trip

```bash
# After V1 step-1 (clean deploy), mutate a deployed MAJOR to force DRIFTED.
printf '\n# arc66-drift-probe\n' >> /tmp/arc66-tw-project/.claude/MAJOR_CHIRON.md
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#    PASS: MAJOR_CHIRON.md reported DRIFTED (proves source_path_for_deployed maps it back to source).
```
**Falsifier:** if CHIRON shows MISSING or OBSOLETE instead of DRIFTED, Locus 2's source mapping
returned empty (the `*)` unknown arm) → the generalized `MAJOR_*.md` arm is wrong.

### V3 — Subproject-tier slice (the suffix path) + FAIL-LOUD A–E via REAL recompose

```bash
TWS=/tmp/arc66-tw-subproj
rm -rf /tmp/arc66-tw-subproj
mkdir -p /tmp/arc66-tw-subproj
# Subproject deploy: SUFFIX_MAJORS=1 -> deployed names carry _<slug>; this is the REAL recompose
# that exercises FAIL-LOUD Checks A-E (NOT --dry-run, which early-returns at install.sh before the awk checks).
bash substrate/install.sh --target subproject --subproject arc66tw --dest /tmp/arc66-tw-subproj  # confirm subproject flag names
#    PASS condition 1 (FAIL-LOUD): install exits 0 — Checks A-E (install.sh:1092+) green; no err() abort.
#    Verify deployed MAJOR names ARE suffixed:
ls /tmp/arc66-tw-subproj/.claude/MAJOR_*.md
#    Expect: MAJOR_POLYBIUS_arc66tw.md, MAJOR_PLINY_arc66tw.md, MAJOR_CHIRON_arc66tw.md, MAJOR_HAMILTON_arc66tw.md
# Now the MISSING slice at subproject tier:
rm -f /tmp/arc66-tw-subproj/.claude/MAJOR_CHIRON_arc66tw.md
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-subproj
#    PASS: MAJOR_CHIRON_arc66tw.md (suffixed name) reported MISSING — proves enumerate_deployed
#    applied the subproject suffix to the glob-derived MAJOR.
```
**Falsifier (the footgun):** if check.sh reports `MAJOR_CHIRON.md` (unsuffixed) MISSING **and**
`MAJOR_CHIRON_arc66tw.md` OBSOLETE, the subproject suffix was not applied to the glob result —
Locus 1's `major_suffix` gate is wrong. If install.sh aborts with a Check A–E err(), the recompose
broke (out-of-scope regression — STOP).

### V4 — Project-tier no-false-suffix assertion (the inverse footgun)

```bash
# On the V1 clean project deploy: MAJOR names must be UNSUFFIXED at project tier.
bash substrate/skills/check-substrate-updates/check.sh --workspace /tmp/arc66-tw-project
#    PASS: zero MISSING and zero OBSOLETE for any MAJOR. A false suffix at project tier
#    (CAPTAIN-rule leakage) would produce exactly one MISSING + one OBSOLETE per MAJOR.
```
**Falsifier:** any MAJOR MISSING/OBSOLETE pair on the clean project deploy = the suffix rule leaked
the CAPTAIN (project+subproject) rule onto MAJORs at Locus 1.

### V5 — Manifest completeness (install.sh Locus 4)

```bash
# Project tier:
grep 'MAJOR_' /tmp/arc66-tw-project/.claude/.substrate-manifest
#   Expect 4 NAME_SUFFIX lines: MAJOR_POLYBIUS.md, MAJOR_PLINY.md, MAJOR_CHIRON.md, MAJOR_HAMILTON.md
#   (project tier -> empty replacement value is correct). NO USER_TIER_DIR line (project tier).
# Subproject tier:
grep 'MAJOR_' /tmp/arc66-tw-subproj/.claude/.substrate-manifest
#   Expect 4 lines with _arc66tw suffix in the dep-path AND _arc66tw replacement value.
```
**Falsifier:** fewer than 4 MAJOR lines = glob missed a MAJOR; a USER_TIER_DIR line for a
non-POLYBIUS MAJOR = the POLYBIUS-only guard is wrong; a suffix at project tier = invariant 1 broke.

### V6 — App green (full suite, re-derives the whole roster)

```bash
cd app && npm run gen-data && npm run build && npm test
```
Expected app-neutral (tooling change, no role-file edit), but assert from the FULL run — gen-data
re-derives the entire roster from current substrate and can surface pre-existing drift. PASS = all
green.

### V7 — No hardcoded POLYBIUS/PLINY-only MAJOR list remains at the four loci

```bash
grep -nE 'MAJOR_POLYBIUS|MAJOR_PLINY' substrate/skills/check-substrate-updates/check.sh
grep -nE 'MAJOR_POLYBIUS|MAJOR_PLINY' substrate/install.sh
```
PASS condition (manual classification, not a bare count): the ONLY surviving literal
`MAJOR_POLYBIUS` / `MAJOR_PLINY` references are LEGITIMATE singletons —
`detect_tier()` (`check.sh:354-369`, which keys tier detection on `MAJOR_POLYBIUS_*` /
`MAJOR_POLYBIUS.md` specifically — that is correct and out of scope), and the POLYBIUS-only
USER_TIER_DIR guard in install.sh Locus 4. **No surviving *paired POLYBIUS+PLINY enumeration list*
at the four fix loci.** A bare `grep -c` is NOT the gate — the gate is "no two-element MAJOR list";
classify each hit.

---

## §5 Self-assessed weak points (attack these hardest, ARGUS)

1. **`detect_tier()` is intentionally NOT in scope but is the one remaining hardcoded
   POLYBIUS reference (`check.sh:354-369`).** It keys tier detection on `MAJOR_POLYBIUS_<slug>.md`
   / `MAJOR_POLYBIUS.md` as the tier sentinel. This is *correct* (POLYBIUS is the canonical
   always-deployed MAJOR; using one sentinel is fine) and de-hardcoding it is out of the directive's
   scope. **Risk:** V7's grep will hit it; if the reviewer/builder reads V7 as "zero
   POLYBIUS/PLINY literals," they'll wrongly try to de-hardcode the tier sentinel. I've made V7 a
   *classified* check, not a count, but this is the most likely place the design is misread.
   *Why this shape anyway:* the tier sentinel is a different concern (detect-which-tier vs
   enumerate-all-MAJORs); folding it in would exceed the no-broader-refactor constraint.

2. **`source_path_for_deployed()` suffix-strip correctness at subproject tier (Locus 2).**
   The proposed `mbase="${mbase%${suffix}}"` strips the *slug* suffix. If a MAJOR mnemonic ever
   ended with a string equal to the slug, the strip could over-trim — extremely unlikely (mnemonics
   are uppercase Greek/historical names; slugs are lowercased project dirs) but it's a string-suffix
   strip, not a structural parse. *Why this shape anyway:* it exactly mirrors the existing CAPTAIN
   arm's `base="${base%${suffix}.md}"`, so it inherits the same (accepted) assumption already shipped
   for CAPTAINs; introducing a stricter parse only for MAJORs would diverge from the proven pattern.

3. **Probe interface names (`--dest`, `--with-captains`, `--workspace`, `--subproject`, apply.sh
   flags) are written from the directive's described behavior, not from a verified `--help` read.**
   §4 flags this inline ("confirm real flag names"). If install.sh/check.sh/apply.sh use different
   flag spellings, the probes need a one-line correction before VERA runs them. *Why this shape
   anyway:* probe *intent* (deploy → remove → check MISSING → apply → re-check clean) is exact and
   falsifiable; the flag spelling is a mechanical lookup ADA/VERA resolve at build/verify time.

4. **`nullglob` empty-loop on a MAJOR-less substrate emits zero manifest/enumeration lines
   silently.** Not FAIL-LOUD. A corrupt substrate checkout (no `MAJOR_*.md`) would produce an empty
   MAJOR set rather than an error. *Why this shape anyway:* FAIL-LOUD on empty-glob is a new behavior
   class outside the directive's "MAJOR-enumeration completeness fix only" scope; the parse-empty
   FAIL-LOUD pattern already exists for skills (`parse_skill_names_from_install`) and could be a
   follow-up, but adding it here mixes scope.

5. **Doc-comment drift surface.** Two doc-comment blocks (`check.sh:101-102` substitution policy;
   `check.sh:537` install.sh writer comment) currently spell out POLYBIUS/PLINY. Locus 3 updates the
   check.sh one; the install.sh comment is updated inline at Locus 4. If either is left naming the
   two MAJORs, the *code* is correct but the comment re-documents the old hardcoded set — a future
   reader could "restore consistency" by re-hardcoding. Low severity, named so ARGUS can confirm both
   comments were swept.

---

## §6 Out of scope (keeps ADA from scope-creep)

- `detect_tier()` tier-sentinel de-hardcoding — different concern, see §5.1.
- Role files `MAJOR_*.md` — untouched (deliverable constraint).
- Any broader `check-substrate-updates` refactor beyond the four enumeration loci.
- `deploy-stoa` / `install-stoa` skills — correct; the bug is downstream.
- `u--k5s` CRLF `agents.ts` item — separate.
- zeotek_newswire — probes use a throwaway; never touch A2A's project.
- Empty-glob FAIL-LOUD hardening (§5.4) — possible follow-up, not this arc.

## §7 Threat→mitigation map

No named threat. This is a process/tooling completeness fix with no runtime attack path
(`operating-disciplines.md` §35.5 carve-out): **not threat-ratified (process/tooling change, no
runtime attack path)** — ARGUS to confirm. No threat-anchored probe required (§6.13). The
suffix-correctness probes (V3/V4) defend against the silent-overwrite-adjacent false-MISSING/OBSOLETE
footgun, but that is a correctness hazard, not a security threat.
