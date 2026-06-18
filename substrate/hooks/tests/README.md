# Author-gate regression corpus (Arc 65 / stoa--z2b)

This directory is the **regression guard** for the authorship-attribution gate's
`.md` matcher narrowing (`pretooluse-author-field-audit.sh` sub-check 2 +
`_hooklib.sh` `classify_author_file` / `extract_author_fields`). It is
**source-only** — it does NOT deploy. `install.sh` globs `substrate/hooks/*.sh`
non-recursively and copies `README.md` by basename only, so this `tests/` subdir
is invisible to the deploy.

Run it:

```bash
bash substrate/hooks/tests/run-author-gate-tests.sh
```

Exit 0 = all pass. Exit non-zero = at least one fixture failed (a regression).

## Why this exists — the BOTH-DIRECTIONS contract

The Arc 65 narrowing changed a SECURITY gate. Both directions are load-bearing,
and a one-direction pass is a FAIL:

1. **False-positive direction (must now PASS).** A PROSE `.md` whose **body**
   merely *discusses* authorship — a seat-attribution line, a verdict authorship-
   AUDIT line, a directive co-author trailer, a `§28` docs line — must no longer
   trip the gate. Before the fix, the gate scanned the whole `.md` blob and fired
   on these discussion-prose lines. After the fix, a prose `.md` is scanned in
   `md` mode (leading YAML frontmatter only), so the body emits nothing and the
   commit is ALLOWED. The `fp/` fixtures pin this.

2. **True-positive direction (must still BLOCK).** A real STRUCTURED author field
   naming a non-PRINCIPAL person must still block — across EVERY covered class:
   `package.json`, a `SKILL.md` YAML-frontmatter author field, `LICENSE`, `NOTICE`,
   `CITATION.cff`, AND the two `.md`-suffixed CONFIG-class collisions `LICENSE.md`
   and `*.claude-plugin/*.md` (which keep the OLD whole-file `cfg` coverage —
   they are config-class, NOT prose-md). The `tp/` fixtures pin this; `tp6`
   (`LICENSE.md`) and `tp7` (`.claude-plugin/*.md`) are the carve-out guards that
   go RED if a future edit ever routes those two classes to `md` mode and loses
   their body-line coverage.

3. **Control direction (must still PASS).** The happy structured path — the
   PRINCIPAL (Denson Smith) named in the right author position — must still be
   ALLOWED, including `ctl3` (`LICENSE.md` with a PRINCIPAL copyright → `cfg` →
   ALLOW), which proves the `LICENSE.md` cfg-routing does not OVER-block a
   legitimate copyright.

4. **Carve-out guards (classify-only manifest entries).** `notes.txt` is
   out-of-class (rc 1); `NOTICE.md` stays `md` mode (NOT over-corrected to `cfg`)
   — its body author line is the acceptable, explicitly-delegated residual (see
   the gate README §7). These prove the collision carve-out was applied exactly to
   the two classes that need it and no further.

## Known coverage boundary — LICENSE author/copyright forms (stoa--y12)

The true-positive `LICENSE` / `LICENSE.md` fixtures (`tp3`, `tp6`) pin the
**separator form** — an author/copyright field written as `field` + a separator
(a `:` or `=`) + value. The classic **separator-less** copyright sentence —
`Copyright (c) <year> <name>` with no separator — is NOT matched by the gate
extractor (it requires a `:` or `=` separator), and never was. This is a
**PRE-EXISTING non-coverage, unchanged by Arc 65** (the arc narrows the `.md`
path; it does not touch separator semantics, and the `cfg` path is byte-identical
to the pre-Arc-65 regex). It is tracked as a known gap in `stoa--y12`.

So a green corpus here means *"every separator-form wrong-person author/copyright
field BLOCKs"* — NOT *"every conceivable LICENSE prose form BLOCKs."* The
separator-less form is delegated to the prose discipline + manual audit + human
review until `stoa--y12` decides whether to extend coverage.

## How it exercises the REAL code (no reimplementation)

The runner **sources `substrate/hooks/_hooklib.sh`** and calls the ACTUAL
`classify_author_file` and `extract_author_fields`. It does not reimplement
either. The only thing it mirrors is the gate's tiny `is_principal` value-compare
(against a fixed test allow-list of the canonical PRINCIPAL tokens), because
`is_principal` is defined in the gate script, not the lib. The live re-probes
(`P4`-`P7`, run against a real armed throwaway gate) are the backstop for that
one mirrored compare.

For each manifest entry the runner: (1) calls `classify_author_file <intended_path>`
once and asserts its return code (membership) AND printed mode; (2) for fixtures
that carry a file, runs `extract_author_fields <mode>` over it and computes
ALLOW vs BLOCK via the `is_principal` mirror; (3) compares to the expectation.

## Fixture naming + the fictional name — IMPORTANT

**The fixtures are FICTIONAL TEST INPUT, not authorship claims on the-stoa.** The
only real PERSON the-stoa is authored by is **Denson Smith**. True-positive
fixtures use the INVENTED name `Fenwick Galsworthy` (not a real public figure) as
the "wrong person" a real author field would name. The corpus exists precisely to
prove the gate BLOCKS such a wrong-person field.

Every fixture carries a **`.fixture`** suffix. `.fixture` is NOT a triggering
basename under `classify_author_file` (it is not in the literal config list, does
not end `.md`, and is not under `*.claude-plugin/`), so a true-positive fixture's
non-PRINCIPAL content commits clean through the live gate. The runner reconstructs
the **intended path** the matcher must SEE from the manifest, NOT the on-disk
`.fixture` basename.

## Layout

```
tests/
  README.md                  # this file
  run-author-gate-tests.sh   # the runner (manifest embedded)
  fixtures/
    fp/      # false-positive — must now PASS (md mode emits nothing)
    tp/      # true-positive  — must still BLOCK (incl. tp6 LICENSE.md, tp7 plugin doc)
    control/ # control        — must PASS (happy structured path, incl. ctl3)
```
