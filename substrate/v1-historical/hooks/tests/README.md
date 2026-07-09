# Author-gate regression corpus (ARCHIVED — Arc 65 / stoa--z2b; retired Arc stoa--p0e)

> **HISTORICAL.** This is the archived regression corpus for the
> `pretooluse-author-field-audit.sh` authorship deny-gate, which was RETIRED in
> Arc `stoa--p0e` (see `../RETIREMENT.md`). It is preserved as WHY-history — it
> documents what the retired gate covered and how it was tested — NOT as a
> fix-target or an active guard. The gate it tested no longer ships. The runner
> here sources `substrate/hooks/_hooklib.sh` (still present — the surviving gates
> use it), so it still executes, but nothing in the live substrate depends on it.

This directory was the **regression guard** for the authorship-attribution gate's
`.md` matcher narrowing (`pretooluse-author-field-audit.sh` sub-check 2 +
`_hooklib.sh` `classify_author_file` / `extract_author_fields`). It was
**source-only** — it did NOT deploy.

Run it (still works against the archived script + the surviving `_hooklib.sh`):

```bash
bash substrate/v1-historical/hooks/tests/run-author-gate-tests.sh
```

Exit 0 = all pass. Exit non-zero = at least one fixture failed.

## Why this existed — the BOTH-DIRECTIONS contract

The Arc 65 narrowing changed a SECURITY gate. Both directions were load-bearing,
and a one-direction pass was a FAIL:

1. **False-positive direction (must PASS).** A PROSE `.md` whose **body** merely
   *discusses* authorship — a seat-attribution line, a verdict authorship-AUDIT
   line, a directive co-author trailer, a `§28` docs line — must no longer trip
   the gate. After the fix, a prose `.md` is scanned in `md` mode (leading YAML
   frontmatter only), so the body emits nothing and the commit was ALLOWED. The
   `fp/` fixtures pin this.
2. **True-positive direction (must BLOCK).** A real STRUCTURED author field naming
   a non-PRINCIPAL person must still block — across every covered class:
   `package.json`, a `SKILL.md` YAML-frontmatter author field, `LICENSE`,
   `NOTICE`, `CITATION.cff`, and the two `.md`-suffixed CONFIG-class collisions
   `LICENSE.md` and `*.claude-plugin/*.md`. The `tp/` fixtures pin this.
3. **Control direction (must PASS).** The happy structured path — the PRINCIPAL
   (Denson Smith) named in the right author position — must still be ALLOWED. The
   `control/` fixtures pin this.

## Known coverage boundary — LICENSE author/copyright forms (stoa--y12)

The true-positive `LICENSE` / `LICENSE.md` fixtures (`tp3`, `tp6`) pinned the
**separator form** (`field` + `:`/`=` + value). The classic separator-less
`Copyright (c) <year> <name>` form was added later (Arc 69 / stoa--y12, the `cpat`
second pass in `_hooklib.sh`). This corpus predates and then tracks that gap.

## The fictional test name

**The fixtures are FICTIONAL TEST INPUT, not authorship claims on the-stoa.** The
only real PERSON the-stoa is authored by is **Denson Smith**. True-positive
fixtures use the INVENTED name `Fenwick Galsworthy` (not a real public figure) as
the "wrong person" a real author field would name. Every fixture carries a
`.fixture` suffix so its content never trips the (now-retired) live gate.

## Layout

```
tests/                       (archived under substrate/v1-historical/hooks/)
  README.md                  # this file
  run-author-gate-tests.sh   # the runner (manifest embedded)
  fixtures/
    fp/      # false-positive — must PASS (md mode emits nothing)
    tp/      # true-positive  — must BLOCK (incl. tp6 LICENSE.md, tp7 plugin doc)
    control/ # control        — must PASS (happy structured path, incl. ctl3)
```
