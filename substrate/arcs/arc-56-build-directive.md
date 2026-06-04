# Arc 56 build directive — save-verdict/Windows cluster (stoa--wq0 + xxy + 7b1.2 + 7ap)

**Tickets:** `stoa--wq0` (P2, the Windows-tester blocker), `stoa--xxy` (P3), `stoa--7b1.2` (P3), `stoa--7ap` (P3) — bucket B (tester-facing bugs)
**Driver:** PLINY_the-stoa
**Drive mode:** autonomous (bucket B — autonomous-ship on clean PASS per `stoa--ikr`; surface the design ONLY if a real judgment call appears)
**Worktree:** `.claude/worktrees/arc-56-build` (branch `arc-56/build`)
**Gauntlet:** DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS → ZENO (no HARD STOP — bucket B not PRINCIPAL-gated)
**Environment advantage:** these are Windows git-bash bugs and we ARE on Windows git-bash — VERA can reproduce + verify the real failures directly, not by proxy.

## Why these four bundle as one arc

Two DISJOINT surfaces (§6.3 bundle-shape rule — disjoint ⇒ one CATO review, each sub-section independent):
- **Surface 1 — the save-verdict skill** (`substrate/skills/save-verdict/`): wq0 + xxy + 7b1.2 are three complementary fixes to the SAME skill → one coherent skill-hardening change.
- **Surface 2 — worktree-remove cleanup discipline** (`.claude/modules/arc-close-hygiene.md` §5.10 + substrate source): 7ap is a different surface (the cleanup discipline, not the skill).

They review cleanly side-by-side. Keep the diff sectioned by surface.

---

## Ticket 1 — stoa--wq0 (THE BLOCKER): save-verdict fails on Windows git-bash

### Ground truth (PLINY pre-read — confirm, don't re-derive from scratch)
The Python writer `substrate/skills/save-verdict/_save_verdict.py` is ITSELF robust (argparse, `--body`/`--body-path` XOR, sha256 round-trip, exit-code contract). **The failure is in the INVOCATION pattern**, two coupled root causes:

1. **bash heredoc-quoted-EOF for the body.** CAPTAINs construct the verdict body in a bash `cat <<'EOF' … EOF` heredoc (to a temp file, then `--body-path`). On Windows git-bash this breaks — **apostrophes in the body break the heredoc EVEN under the quoted `<<'EOF'` delimiter** (confirmed 2026-06-01 Arc 52: CAPTAIN_ARGUS had to author the entire verdict apostrophe-free after multiple retries).
2. **`/tmp` git-bash-vs-Python path divergence.** A CAPTAIN writes the body to git-bash `/tmp/…` (MSYS `/tmp`), then Python on Windows resolves `/tmp/…` to a DIFFERENT location (`C:\tmp\…`). Result: `--body-path /tmp/x` → either exit-4 "body-path does not exist" OR — the latent correctness risk — reads a STALE/WRONG file and writes a **silent-green** verdict with wrong content.

### Fix direction (from the ticket; DAEDALUS designs the concrete mechanism)
"Drop the bash-heredoc-with-quoted-EOF pattern; resolve a portable temp location consistently (don't assume bash /tmp == Python /tmp on Windows); ideally write + read through the same runtime."

**PLINY's steer (DAEDALUS may override with justification):** the cleanest "same-runtime" path is to have the CAPTAIN author the verdict body using the **Write tool** (harness runtime — no shell quoting, no heredoc, no apostrophe bug) to an **explicit repo/worktree-relative path** (NOT `/tmp`), then invoke `_save_verdict.py --body-path <that-relative-path>`. An explicit repo-relative path is resolved IDENTICALLY by the Write tool and by Python's `pathlib` — sidestepping BOTH root causes. This makes the fix primarily a **SKILL.md procedure change** (+ possibly a CAPTAIN role-file invocation-guidance touch, + possibly a small `_save_verdict.py` hardening such as a `--body-stdin` option or a louder error when a `/tmp`-style path is passed). DAEDALUS: investigate where the heredoc/`/tmp` pattern is actually DOCUMENTED or TAUGHT (SKILL.md step 9 bash example? CAPTAIN role files? the save-verdict skill's own examples?) and fix it at the source.

### Hard constraint (correctness)
The silent-green failure mode (wrong-content verdict reads as success) is the most dangerous facet. Any fix MUST make a path-mismatch FAIL LOUD, never silently write the wrong file. If `_save_verdict.py` can detect a suspicious temp-path input, it should error, not guess.

---

## Ticket 2 — stoa--xxy: receipt filename collision + sub-agent-writes-to-main-root facet

Two coupled facets, same root cause (write-location hygiene):
1. **Receipt filename collision:** generic receipt names overwrite prior arcs' receipts. Fix: namespace receipts per-arc/ticket (e.g. `agents/save-verdict/<ticket-id>/<officer>-<phase>.txt` or include the ticket-id in the name). Investigate the current `--artifact-path` / `<request-id>.txt` scheme in SKILL.md "Output contract" + `_save_verdict.py` `_write_record_artifact`.
2. **Sub-agent write resolves to MAIN ROOT not the worktree:** sub-agents inherit the parent session cwd, so `--cwd` defaults to the wrong tree. **This bug manifested LIVE in Arc 55** — NOMOS flagged that VERA/CATO wrote verdicts to the MAIN tree's `agents/verdicts/` while ARGUS wrote to the worktree tree. Fix: the verdict + receipt must land at an EXPLICIT per-arc worktree path. Consider whether the skill should require an explicit `--cwd`/dest rather than defaulting, OR whether the dispatch brief must always pass the worktree path. DAEDALUS: decide where the fix lives (skill default behavior vs. PLINY's dispatch-brief discipline vs. both).

---

## Ticket 3 — stoa--7b1.2: save-verdict ships a .gitignore for __pycache__

Running save-verdict (a Python skill) regenerates `__pycache__/*.pyc` in the skill tree (recurred across 3 seats × 2 sub-builds — ksge D4). **Note: the source tree ALREADY HAS `substrate/skills/save-verdict/_lib/__pycache__/` committed** — confirm and clean that up too if appropriate. Fix: ship a `substrate/skills/save-verdict/.gitignore` covering `__pycache__/` + `*.pyc`. Coordinate semantics with the Arc 55 `install.sh` post-copy pycache strip + the new `.claude/.gitignore` (don't duplicate/conflict — the skill-shipped .gitignore protects the SOURCE skill tree + any consumer who runs the skill).

---

## Ticket 4 — stoa--7ap (Surface 2): Windows worktree-remove orphan dir

On Windows, `git worktree remove` can de-register a worktree (so `git worktree list` shows it gone) yet FAIL to delete the directory — observed errors "Permission denied" (Arc 2) AND "Device or resource busy" (Arc 3), N=2 recurring. The orphan dir is then invisible to the registration view. The §5.10 verify-before-claim discipline has reliably CAUGHT it (no silent failure), but the cleanup itself should **retry + verify the DIR is gone**, not just the registration.

Fix surface: `.claude/modules/arc-close-hygiene.md` (§5.10) — the canonical home of the cleanup sequence. Update the cleanup procedure to: after `git worktree remove`, assert the directory is actually gone (`[ ! -d <path> ]`); on failure, retry (and/or `rm -rf` the orphan dir) and re-assert. Document both observed Windows error strings. **This is a DOC/DISCIPLINE change to a substrate module** — confirm whether the module is the only home or whether a future enforcement hook is referenced (out of scope to BUILD a hook; in scope to update the discipline).

---

## Scope lock
- IN: `substrate/skills/save-verdict/` (SKILL.md, _save_verdict.py, _lib/, a new .gitignore), `.claude/modules/arc-close-hygiene.md` source (i.e. `substrate/` source-of-truth for that module — confirm the source path; modules deploy from `substrate/modules/`), and any CAPTAIN role-file invocation-guidance touch strictly needed for the wq0 fix.
- OUT: building a new enforcement hook (7ap references a possible future hook — do NOT build it). The broader PowerShell-native-tool fix (u--h8q canary) — NOT this arc. Any save-verdict facet not in the four tickets. Do NOT touch the Arc 55 install.sh work (shipped).

## Probes (VERA — refine into concrete Windows git-bash repros)
- **P-wq0a (heredoc/apostrophe):** reproduce the OLD failure (a verdict body containing apostrophes via the old heredoc pattern fails on Windows git-bash), then prove the NEW pattern writes the SAME body — apostrophes intact, sha256 round-trip pass — with no retries.
- **P-wq0b (/tmp mismatch + silent-green):** prove the new pattern does NOT silently write wrong content when a temp-path-style input is involved; a genuine path mismatch FAILS LOUD (non-zero exit), never green-with-wrong-bytes.
- **P-xxy1 (receipt namespacing):** two save-verdict calls from different arcs/tickets do NOT overwrite each other's receipts.
- **P-xxy2 (worktree-path):** a save-verdict invoked in the arc worktree context writes the verdict to the WORKTREE tree, not main root (the Arc 55 regression).
- **P-7b1.2 (gitignore):** running save-verdict leaves no untracked `__pycache__`/`*.pyc` in `git status` of the skill tree.
- **P-7ap (cleanup discipline):** the updated §5.10 cleanup procedure asserts dir-gone + handles the retry/orphan case (verify the documented procedure is correct + internally consistent; a doc-probe since it's a discipline change).

## Per-CAPTAIN seat-identity (worktree commits)
`seat-identity: CAPTAIN_<MNEMONIC>_the-stoa <captain-<mnemonic>@the-stoa.local>` per §28 — ADA commits carry `CAPTAIN_ADA_the-stoa <captain-ada@the-stoa.local>`.
