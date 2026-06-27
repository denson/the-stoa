<!-- author: Denson Smith -->
<!-- ticket: stoa--elx (the-stoa store) -->
<!-- from: Polybius the Stoa (user-tier the-stoa forge owner) -->
<!-- for: Polybius the Grand — REVISED planning deliverable (v2), awaiting gate -->
<!-- supersedes: plan-bw-install-windows-shim.md (v1) -->

# PLAN v2 (REVISED) — bw bootstrap into the Stoa install process (stoa--elx)

Supersedes v1 (plan-bw-install-windows-shim.md). Revised per the Grand's 2026-06-27T20:56
directive + my direct read of the upstream install.sh (verified from source, not relayed).

## 0. Decision status

| Item | Status |
|---|---|
| Canon reversal (Stoa installs bw) | RATIFIED by the Grand |
| Auto-bootstrap = opt-in `--bootstrap-bw` flag on install.sh | RATIFIED (my lean) |
| Ownership = one helper / three consumers | RATIFIED, unchanged |
| Obtention = OS-split | NEW this revision (Grand directive) |
| Binary is bw.exe; root cause = ~/bin not on Windows PATH | CONFIRMED from repo |

## 1. Verified ground truth (read directly from the upstream repo this session)

**Upstream install.sh** (61 lines, `raw.githubusercontent.com/jallum/beadwork/main/install.sh`):
- **UNIX-ONLY:** `case "$OS" in linux|darwin) ;; *) fail "unsupported OS"`. On Windows
  (MINGW/MSYS uname) it dies immediately. There is NO upstream Windows installer.
- **LATEST-ONLY:** hardcodes `releases/latest` via the GitHub API. No version-pin hook.
- **NO checksum verification:** downloads the `.tar.gz` over HTTPS, extracts, `chmod +x`. That's it.
- **INSTALL_DIR:** honors `$INSTALL_DIR` if set (first branch, bypasses all heuristics); else
  `~/.local/bin` IF it exists AND is already on PATH; else `/usr/local/bin` (sudo). It does NO
  PATH setup — it only USES an already-PATH'd dir.
- Unix asset = `beadwork_<ver>_<os>_<arch>.tar.gz` containing a bare `bw`.

**Windows:** asset = `beadwork_<ver>_windows_<arch>.zip` containing `bw.exe` (+ CHANGELOG/LICENSE/
README). Releases are goreleaser per-OS/arch + a `checksums.txt` (SHA256). `bw upgrade` self-updates
from releases; `bw onboard` prints an agent-instructions snippet.

## 2. Obtention — the OS split

### Unix (linux / darwin): delegate to upstream install.sh; do NOT reinvent
- Our helper preps the precondition upstream skips: ensure `~/.local/bin` exists + is on PATH
  (shell-rc append), then invoke upstream pinned to that dir (`... | INSTALL_DIR="$HOME/.local/bin" sh`)
  so it installs no-sudo there.
- **Version = floor-via-latest.** Upstream is latest-only with no pin hook; we don't need an exact
  pin — our requirement is a FLOOR (>=0.13.2), and latest always clears it. So: idempotent
  skip-if-(bw >= floor), else run upstream (installs latest >= floor). Discharges stoa--fqh.
- **Checksum:** upstream does not verify; following the canonical path inherits that posture on
  Unix (HTTPS/TLS-authenticated). See the §4(a) asymmetry flag.

### Windows: ours end-to-end (no upstream installer exists)
- Detect arch (amd64/arm64) -> download `beadwork_<ver>_windows_<arch>.zip` for a floor-satisfying
  version -> **SHA256-verify against checksums.txt** -> extract `bw.exe` -> place it -> ensure its
  dir is on the **Windows USER PATH**.
- Idempotent: skip if bw.exe present AND PowerShell-callable AND >= floor (§3).

## 3. Windows PATH-callability — the real crux (unchanged)

- **Two-independent-checks rule:** check (a) binary present AND (b) PowerShell can resolve `bw`,
  SEPARATELY. A git-bash `bw --version` false-greens — bw runs from git-bash while PowerShell still
  can't see it (exactly this machine's prior state). The callability fix MUST run even when (a) passes.
- **Dir + PATH mechanism (my design call per the Grand's note):** place bw.exe in one dedicated dir
  and put THAT dir on the Windows USER PATH. Recommended dir = `~/.local/bin` — it unifies the
  Unix+Windows install location and is already PATH'd on the reference machine. Constraint for
  DAEDALUS: one dir, resolvable from BOTH git-bash and PowerShell.
- **PATH mutation = the one genuinely risky element:** registry-safe append (read HKCU\Environment
  PATH, append only if absent, length-checked write) + FAIL-LOUD manual fallback if it can't be done
  safely. ARGUS cold-audits this specifically.
- **Shim (bw.cmd) = demoted to fallback only:** used only when PATH can't be modified safely AND a
  PATH'd dir already exists.

## 4. Honest asymmetries to gate (two small calls for the Grand)

- **(a) Checksum asymmetry.** Windows SHA256-verifies (ours); Unix inherits upstream's no-checksum
  (HTTPS-only) posture. Making them symmetric means wrapping/replacing the upstream installer —
  which starts reinventing it, against your directive. **Recommend: accept upstream's posture on
  Unix** (canonical path, TLS-authenticated), note it. Your call.
- **(b) Version exactness.** Unix gets latest (floor-satisfied), not an exact pin (upstream has no
  pin hook). **Recommend: accept** — bw self-updates to latest anyway, and the floor is what the
  substrate actually requires. Your call.
- (c) Not a decision, just a clean property: both OS paths share the "ensure dir on PATH" job; the
  ONLY OS difference is the obtention mechanism (upstream installer vs our zip download).

## 5. Ownership — one helper / three consumers (ratified, unchanged)

**`substrate/bootstrap-bw.sh`** — the idempotent core: detect OS/arch -> skip-if-(bw >= floor) ->
[Unix: prep ~/.local/bin on PATH + delegate to upstream | Windows: download + SHA256 + extract
bw.exe + place] -> ensure dir on Windows USER PATH (Win) / shell-rc (Unix) -> two-checks verify
(Win incl. PowerShell-callable). Flags: `--yes`, `--check`, `--dry-run`.

- **install.sh** — opt-in `--bootstrap-bw` flag, default OFF (keeps the human-facing installer
  no-surprise; PATH mutation never happens unasked).
- **onboarding skill (install-stoa / stoa--sok)** — guided + consented front-door; Beat 1 flips
  from "bw is a prereq, STOP" to "detect; if missing, drive bootstrap-bw.sh with the PRINCIPAL in
  the loop." The canon reversal lands here.
- **cookie-cutter (u--9s2)** — non-interactive (`--yes`) first stand-up step; consumes the helper.
  Deterministic stand-up is guaranteed where it matters, which is why install.sh can stay opt-in.

## 6. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Windows USER PATH clobber (setx truncation) | HIGH | §3 registry-safe append + FAIL-LOUD fallback + ARGUS cold-audit |
| Unix no-checksum | LOW-MED | HTTPS + upstream canonical path; §4(a) |
| Canon reversal | (ratified) | onboarding Beat 1 rewrite lands in the same arc |
| Re-run on healthy machine | LOW | idempotent skip-if-current |

## 7. Next step

On the Grand's gate of this v2 (+ the two §4 calls), I forge the by-the-book the-stoa gauntlet —
PATH mutation is the design crux for DAEDALUS, and ARGUS cold-audits it. Nothing builds until gated.
