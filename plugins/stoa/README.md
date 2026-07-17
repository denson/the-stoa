# stoa plugin — scope model, per-workspace control, deactivation

Plugin packaging of the Stoa substrate (see `plugins/sync-from-substrate.py` —
`substrate/` remains the canonical source pending the fleet-migration decision).
Author: Denson Smith (identity-by-hosting: all manifest fields resolve into
`github.com/denson`).

## Scope model (the universal end-state, verified 2026-07-17)

The plugin is installed at **user scope** — enabled by default in EVERY
workspace on the machine:

```
claude plugin install stoa@stoa-marketplace --scope user
```

Per-workspace state then follows Claude Code's strict override model
(narrower scope wins): `managed → user → project (.claude/settings.json,
committed) → local (.claude/settings.local.json, git-ignored)`. A `false` in a
narrower scope beats the user-scope `true`.

## Legacy workspaces (deployed `.claude/` substrate) — what ACTUALLY happens

Measured in `labstat_bls` (fresh legacy deploy) with the plugin enabled on top:

- **Coexistence, not collision.** The CAPTAIN roster appears in TRIPLICATE:
  deployed `CAPTAIN_ADA_labstat_bls` + plugin `CAPTAIN_ADA` (bare) +
  `stoa:CAPTAIN_ADA`. Nothing errors; nothing is shadowed; dispatch becomes
  ambiguous and context bloats.
- **Skills duplicate/triplicate** (deployed `gauntlet-setup` + plugin
  `stoa:gauntlet-setup`, with the bare name sometimes listed twice).
- **Deployed hooks keep firing regardless of the plugin** (the workspace's
  Stop/PreToolUse gates are settings-registered, independent of plugin state).
- Plugin commands (`/stoa:polybius`, …) become available alongside everything.

**Until a legacy workspace is properly migrated, DISABLE the plugin there**
(recipe below). Running both surfaces is safe but ambiguous — don't.

## Per-workspace disable (the verified recipe)

From the workspace root, personal/local (git-ignored — recommended interim):

```
claude plugin disable stoa@stoa-marketplace --scope local
```

or committed for the whole team: `--scope project`. Either writes
`"enabledPlugins": { "stoa@stoa-marketplace": false }` into the corresponding
settings file. VERIFY by changed behavior, not structure: `claude plugin list`
must show `stoa … disabled`, and `/stoa:polybius` must return
"Unknown command" in that workspace. Re-enable any time:
`claude plugin enable stoa@stoa-marketplace --scope local` (or delete the
override line).

Applied as of 2026-07-17: `labstat_bls` carries the local-scope disable (the
precedence test subject). All other legacy workspaces still list duplicates
until each is either disabled or migrated — deliberately NOT swept; the
fleet-migration decision belongs to the planning session.

## Per-workspace cleanup recipe (migration day — DOCUMENTATION ONLY, not yet run anywhere)

For a legacy workspace moving to plugin-only, in order:

1. Confirm the plugin is enabled and NOMINAL in that workspace first
   (say-trigger wakes a seat with runtime-derived identity — the changed-behavior
   smoke from the pilot).
2. Remove ONLY what `.claude/.substrate-manifest` records as substrate-deployed:
   the `MAJOR_*.md` role files, `agents/CAPTAIN_*_<slug>.md`, and the
   skills/modules/templates the manifest lists. **NEVER blind-prune**: the
   OBSOLETE-classification footgun (stoa--u6s) means anything the manifest
   has no record of deploying — hand-installed skills, workspace customs —
   must be left untouched.
3. Decide hooks separately: enforcement gates are settings-registered, not
   plugin-managed (pilot did not ship hooks). Keep the workspace's
   `settings.json` hooks block if the gates should stay armed; the plugin
   neither adds nor removes them.
4. Replace the workspace `CLAUDE.md` substrate reference block with plugin-era
   say-triggers (see `newswire_core/.claude/CLAUDE.md` — the pilot reference:
   two files is the entire consumer footprint).
5. Re-run the smoke (step 1's probe) after cleanup; the deployed duplicates
   must be gone and the plugin surface must be the only roster.

## Full deactivation (removing the plugin itself)

```
claude plugin disable stoa@stoa-marketplace --scope user     # soft: off everywhere, overrides still win
claude plugin uninstall stoa@stoa-marketplace                # removes the install + cache entry
claude plugin marketplace remove stoa-marketplace            # forgets the marketplace
```

Per-workspace overrides (`enabledPlugins` lines in project/local settings)
are inert after uninstall but should be deleted on next touch. Legacy deployed
workspaces are unaffected by deactivation — their `.claude/` trees are
self-contained.

## Versioning

Pin by tag (`stoa-v0.1.0`). Substrate change → rerun
`plugins/sync-from-substrate.py` → bump `plugin.json` + marketplace entry →
`plugins/release-check.sh` (advisory) → tag → consumers update deliberately.
