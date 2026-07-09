# Attribution advisory report
scanned: diff-file substrate/skills/attribution-advisory/tests/fixtures/p2-newfile-principal.diff · at: 2026-07-09T20:15:30Z · findings: 1
(This is a REPORT, not a block. Nothing was prevented. Review each finding below.)

## SECONDARY — a NEW non-PRINCIPAL author-like field (outside vendored paths)
- file: pyproject.toml  (added)
  field: authors = "Denson Smith"
  WHY: a new author/owner/creator/... field naming someone who is not the PRINCIPAL,
       in a non-vendored path, may be a mis-attribution of the PRINCIPAL's own work.
  WHAT TO CHECK: if this is a CITED source author, move it to prose/citation; if it is
       a legitimate PRINCIPAL identity, add it to .claude/hooks/principal-identity.

