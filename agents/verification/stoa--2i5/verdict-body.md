status: completed
ticket: stoa--2i5
verdict: pass
design_artifact_verified_against: agents/design/stoa--2i5/design.md (§4 P1-P4)
build_verified: arc-55/build @ acf944c (worktree .claude/worktrees/arc-55-build)

probes_executed:
- probe_id: p1
  description: AC3 — fresh install into clean synthetic workspace; simulate runtime transients; assert substrate-transient paths are IGNORED (not untracked in git status). This is the W1 path-relativity catch.
  quadrant_classification: easy-easy
  command_or_method: |
    rm -rf /tmp/stoa-2i5-probe && mkdir -p /tmp/stoa-2i5-probe && git -C /tmp/stoa-2i5-probe init -q
    bash substrate/install.sh --target project --project-dir /tmp/stoa-2i5-probe   # exit 0, "wrote gitignore"
    mkdir -p .../worktrees .../skills/foo/__pycache__
    touch .../scheduled_tasks.lock .../.substrate-last-check .../skills/foo/__pycache__/x.pyc
    git -C /tmp/stoa-2i5-probe status --porcelain -uall | grep -E 'scheduled_tasks\.lock|worktrees|substrate-last-check|pycache|\.pyc'
    git -C /tmp/stoa-2i5-probe check-ignore -q <each transient path>
  expected: grep over untracked (-uall expanded) prints NOTHING (exit 1); check-ignore confirms all 4 transient paths IGNORED.
  observed: |
    install exit=0; .claude/.gitignore written (786 bytes) with BARE-RELATIVE entries (worktrees/ not .claude/worktrees/).
    grep over `git status --porcelain -uall` exit=1 (no transient path untracked).
    check-ignore: IGNORED .claude/scheduled_tasks.lock | IGNORED .claude/worktrees/ | IGNORED .claude/.substrate-last-check | IGNORED .claude/skills/foo/__pycache__/x.pyc (all 4).
    git status --ignored confirms `!! .claude/.substrate-last-check`, `!! .claude/scheduled_tasks.lock`, `!! .claude/skills/foo/__pycache__/x.pyc`.
  result: pass
- probe_id: p2
  description: Idempotency — run install three times total into same workspace; assert no duplicated content lines in .claude/.gitignore.
  quadrant_classification: easy-easy
  command_or_method: |
    bash substrate/install.sh --target project --project-dir /tmp/stoa-2i5-probe   (x2 more; 3 total)
    sort .claude/.gitignore | uniq -d | grep -vE '^\s*(#.*)?$'
  expected: prints NOTHING (no duplicated non-blank/non-comment line); line count stable.
  observed: run2 exit=0, run3 exit=0; uniq-d grep exit=1 (no dup content lines); wc -l = 20 (stable). Full-overwrite heredoc — duplication structurally impossible.
  result: pass
- probe_id: p3
  description: --dry-run prints the gitignore intent line and writes NO file.
  quadrant_classification: easy-easy
  command_or_method: |
    bash substrate/install.sh --target project --project-dir /tmp/stoa-2i5-probe2 --dry-run 2>&1 | grep -F '[dry-run] write:' | grep -F '.gitignore'
    test ! -e /tmp/stoa-2i5-probe2/.claude/.gitignore
  expected: dry-run intent line printed; file absent on disk.
  observed: |
    printed: "[dry-run] write: /tmp/stoa-2i5-probe2/.claude/.gitignore (substrate-transient paths: scheduled_tasks.lock, worktrees/, .substrate-last-check, __pycache__/, *.pyc)" (grep exit 0)
    DRYRUN-OK: no .gitignore written (file absent).
  result: pass
- probe_id: p4
  description: AC2 — install.sh --help and substrate/README.md document the transient paths. Also verifies ARGUS r1 condition (doc lands inside the usage()-scraped header block).
  quadrant_classification: easy-easy
  command_or_method: |
    bash substrate/install.sh --help 2>&1 | grep -iE 'gitignore|transient'
    grep -niE 'gitignore|transient' substrate/README.md
    # r1 check: confirm transient doc is captured by the FIRST sed range (lines 3..119, terminator '# Dry-run:' at :119)
    sed -n '3,119 p' substrate/install.sh | grep -F 'Transient-path .gitignore (Arc 55'
  expected: both grep print matches; transient doc present inside the header block before the '# Dry-run:' terminator.
  observed: |
    --help grep exit=0 (transient-path doc present); README grep exit=0 (line 30 documents .claude/.gitignore + all transient paths + .substrate-manifest carve-out).
    r1 SATISFIED: "Transient-path .gitignore (Arc 55 / stoa--2i5)" is at install.sh:106-117, inside the intended usage() sed range 3->119 (terminator '# Dry-run:' at :119). AC2 doc is captured by the correct first range independent of the overrun noted below.
  result: pass

methodology_concerns: |
  MC1 (pre-existing, ORTHOGONAL to Arc 55 — surfaced not blocking): install.sh --help over-emits.
  usage() scrapes via `sed -n '/^# install\.sh/,/^# Dry-run:.*$/p'`. The START anchor `^# install\.sh`
  matches TWO lines: the header (install.sh:3, intended) AND a body comment "# install.sh edit — the
  file class the epic is designed to grow continuously" (install.sh:169). With GNU sed, the range
  re-opens at the second start-match; since there is no second `# Dry-run:` terminator after :169, the
  range runs :169 -> EOF. Net: `--help` emits 1753 lines instead of the intended ~117 (1636 lines of
  spurious overrun, incl. the function body). VERIFIED PRE-EXISTING: on main (pre-Arc-55) the same anchor
  exists at :158 and --help already overruns to 1687 lines; Arc 55 only shifted the line number (added
  lines above it). It does NOT falsify any AC for this arc — the AC2 transient doc lands inside the
  correct first range (3->119), so P4 passes legitimately. Per CLAUDE.md "fix known bugs immediately,"
  this latent --help defect warrants a follow-up ticket: anchor the sed range tighter (e.g. start
  `/^# install\.sh — /` with the em-dash, which the body comment at :169 does NOT have — body comment is
  "# install.sh edit"), or add a unique header-start sentinel. Recommend PLINY file a fast-follow.
  No other methodology concerns. Probe-spec regex anchoring (§5.11) checked: P1/P2 assertions key on
  exit-1-on-grep (correct absence semantics) + check-ignore (location, not count) — not under-anchored.

falsifying_evidence_summary: ""

verification_artifacts_path: agents/verification/stoa--2i5/ (this verdict body; probe transcripts captured inline above — synthetic workspaces /tmp/stoa-2i5-probe{,2} created and cleaned up)

summary: |
  All four design probes PASS; ACs 1-3 satisfied. The build (acf944c) writes a canonical, idempotent
  .claude/.gitignore via write_substrate_gitignore() (install.sh:541, called unconditionally at :1657).
  The load-bearing probe was P1 (W1 path-relativity catch): bare-relative entries (worktrees/, not
  .claude/worktrees/) are correct — verified directly with `git check-ignore` that all four transient
  paths (including the empty worktrees/ dir) are matched by the nested .gitignore inside .claude/, and
  via `git status --porcelain -uall` that none appear as untracked. The earlier `?? .claude/` porcelain
  summary line is git collapsing the whole untracked subtree (nothing tracked yet), NOT a transient leak
  — rigorously disambiguated with -uall + check-ignore. P2 idempotency holds by full-overwrite heredoc
  (no dup lines after 3 runs). P3 dry-run prints intent + writes nothing. P4: --help (ARGUS r1 condition
  satisfied — doc inside the scraped header block) + README both document the transient paths and the
  .substrate-manifest carve-out. One pre-existing, Arc-55-orthogonal --help over-emit defect surfaced as
  MC1 (recommend fast-follow ticket); it does not falsify this arc. git-bash environment note: ran
  cleanly under MINGW64 bash 5.2.15; /tmp resolved consistently; no heredoc-EOF or bash-vs-Python
  path-mismatch failures observed (the quoted <<'EOF' heredoc wrote literally as designed). No probe was
  UNVERIFIABLE. Verdict: PASS.
