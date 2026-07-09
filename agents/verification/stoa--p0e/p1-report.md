# Attribution advisory report
scanned: diff-file substrate/skills/attribution-advisory/tests/fixtures/p1-edit-copyright.diff · at: 2026-07-09T20:14:47Z · findings: 1
(This is a REPORT, not a block. Nothing was prevented. Review each finding below.)

## PRIMARY — an existing attribution line was MODIFIED or DELETED
- file: LICENSE  (hunk @@ -1 +1 @@)
  removed: `Copyright (c) 2024 Jane Doe`
  WHY: modifying/deleting a line that already carried an author/copyright/license
       attribution is almost never legitimate — it is the plagiarism / license-breach
       direction (another author's credit erased or replaced).
  WHAT TO CHECK: confirm this change is legitimate (e.g. correcting YOUR OWN name, a
       routine copyright-year bump, or a license reformat); otherwise restore the
       original attribution before committing.

