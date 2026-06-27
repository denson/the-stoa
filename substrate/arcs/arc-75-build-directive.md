# Arc 75 build directive — bw bootstrap into the Stoa install process (OS-split obtention + registry-safe Windows PATH)

**Audience:** the fresh Claude Code sessions opened to build Arc 75 (PLINY_the-stoa + the floor-manager POLYBIUS_the-stoa).
**Authored by:** Polybius_the_Stoa (user-level Stoa agent, sid 990b0750-5572-4836-b9c7-18d626a12e96) on behalf of the PRINCIPAL (Denson Smith).
**Status:** DRAFT — pending NOMOS-on-the-directive, then committed + launched.
**Charter:** `stoa--elx` (carries the problem, the verified ground truth, both plan revisions, and the Grand's GATED GO).
**Gated artifact (READ IT FIRST):** `beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md` — the Grand GATED this v2 plan, both §4 calls ACCEPTED (checksum asymmetry; floor-via-latest). This directive locks it into a buildable spec; the plan is authoritative if any wording here conflicts.
**Builds on:** the-stoa `main` @ 7d20b5f. `install.sh` is the deploy mechanism that runs on every consumer install — treat regressions like a public-API break.

---

## Empirical anchor (hold it)

bw (beadwork) is the substrate's durable bus + need-board — fundamental to all substrate work — but the Stoa install process never installs it. `install.sh` ASSUMES bw is present and on PATH (it calls `bw init` but never obtains the binary); the onboarding skill explicitly says "do NOT install bw — out of scope." On a fresh Windows machine the bw-dependent flows fail SILENTLY: bw can be installed and working from git-bash (where `~/bin` is on PATH and MSYS resolves it) while PowerShell/cmd cannot see it at all — because the binary's dir is not on the WINDOWS USER PATH (the binary is `bw.exe`; PATHEXT already includes `.EXE`; it is a PATH problem, not an extension problem). The Grand hit this wall live on Denson's machine 2026-06-27. This arc makes a working, PowerShell-callable bw a DETERMINISTIC outcome of standing a machine up.

## Verified ground truth (from the upstream repo, read directly — do not re-derive from memory)

- Upstream `install.sh` (`raw.githubusercontent.com/jallum/beadwork/main/install.sh`, 61 lines) is **UNIX-ONLY** (`linux|darwin`; fails on Windows MINGW/MSYS uname), **LATEST-ONLY** (no version-pin hook), does **NO checksum verification** (HTTPS download + `tar -xzf` + `chmod +x`), and does **NO PATH setup** — it honors `$INSTALL_DIR` if set, else uses `~/.local/bin` only if already on PATH, else `/usr/local/bin` (sudo). Unix asset = `beadwork_<ver>_<os>_<arch>.tar.gz` containing a bare `bw`.
- Windows asset = `beadwork_<ver>_windows_<arch>.zip` containing `bw.exe`. **No upstream Windows installer exists** — the Windows hand-roll is necessary, not reinvention.
- Releases are goreleaser per-OS/arch + a `checksums.txt` (SHA256). `jallum/beadwork` is PUBLIC (no credentials). `bw upgrade` self-updates from releases; the installer only bootstraps the FIRST binary.

## Your one job

Build a single idempotent helper that makes a working, **PowerShell-callable** bw a deterministic install outcome, via an OS split — **Unix delegates to upstream's installer; Windows is ours end-to-end** — wired into `install.sh` behind an opt-in flag and into the onboarding skill as a guided front-door. The Windows USER PATH mutation is the design crux: it MUST be registry-safe + fail-loud, DAEDALUS owns it, ARGUS cold-audits it.

## Full gauntlet (DAEDALUS → ARGUS → ADA → VERA → CATO → NOMOS) — BY-THE-BOOK, NOT one-pass.
Design (DAEDALUS) is a SEPARATE phase with a go/no-go before build. Standard POLYBIUS+PLINY team — substrate tooling (a bash helper + install.sh + a skill edit), NOT a custom agent/workflow, so **no CHIRON/HAMILTON**.

---

## Comms — async with Polybius_the_Stoa via bw (`stoa--*`)

Coordinate on the charter `stoa--elx`. Polybius_the_Stoa (user-level owner) monitors + interjects; the floor-manager runs independent verification at each hand-back and relays up; the PRINCIPAL is NOT the relay — beadwork is. `bw comment <id> "text"` is positional, no `-m`; no backticks or `$()` in comment bodies. Run `bw prime` at activation. Every seat signs `[from: <NAME> | sid <session-id>]` (sid via the `whoami` skill).

---

## Read first

1. **The gated v2 plan** `beadwork:attachments/stoa--elx/plan-bw-bootstrap-v2.md` (the authoritative shape: OS-split, ratified decisions, the two accepted §4 calls).
2. **`stoa--elx` comment trail** — the problem, the bw.exe correction, the upstream-installer verification, the Grand's GATED GO + hard conditions.
3. **`substrate/install.sh`** — how it deploys today (2116 lines, bash, runs under git-bash on Windows; near-zero platform detection; calls `bw init` at the user-tier scaffold but never obtains bw). Where an opt-in pre-flight flag fits the existing flag set (`--help`).
4. **`skills/install-stoa/SKILL.md`** (repo root — NOT `substrate/skills/`; this is the-stoa's own onboarding skill per `stoa--sok`, not a deployed substrate skill). Beat 1 + the "What you must NOT do" list carry the canon being reversed.
5. **`substrate/modules/bw-upgrade.md`** — the existing bw-upgrade discipline (the helper bootstraps the FIRST binary; ongoing upgrades stay `bw upgrade`; do not duplicate that).

---

## Design items — DAEDALUS resolves in Phase A (surface at the design hand-back for go/no-go)

- **DC1 — the `substrate/bootstrap-bw.sh` helper (the one shared core; LOAD-BEARING).** Idempotent: detect OS (`uname -s`: `linux`/`darwin`/`MINGW*|MSYS*|CYGWIN*`=Windows) + arch (`uname -m`: x86_64/amd64, aarch64/arm64); **skip-if-(bw already >= floor)** before any download; OS-split obtention (DC4/DC5); ensure dir on PATH (DC2 on Windows, shell-rc on Unix); two-checks verify (DC3). Flags: `--yes` (non-interactive), `--check` (report only, no mutation), `--dry-run`. The floor is **>=0.13.2** (current latest; discharges `stoa--fqh`). The helper is the single home for all three consumers (DC6/DC7 + the u--9s2 cookie-cutter call-site which is OUT of this arc's scope but which the `--yes` mode must serve).

- **DC2 — Windows USER PATH mutation (DAEDALUS OWNS THIS; the Grand's hard condition; ARGUS cold-audits).** Place `bw.exe` in one dedicated dir and ensure THAT dir is on the **Windows USER PATH**. The mechanism MUST be **registry-safe append**: read `HKCU\Environment` PATH (e.g. `reg query`), append the dir only if absent, write back **length-checked** — NEVER a blind `setx` that truncates at 1024 chars or clobbers `%`-expanded values. If it cannot be done safely, **FAIL LOUD** with the exact one-line manual step for the PRINCIPAL — do not risk clobbering PATH. Recommended dir = `~/.local/bin` (unifies the Unix+Windows install location; already PATH'd on the reference machine) — DAEDALUS confirms, constraint: one dir resolvable from BOTH git-bash and PowerShell. The shim (`bw.cmd`) is a FALLBACK ONLY (can't-touch-PATH AND a PATH'd dir already exists).

- **DC3 — the two-independent-checks rule (MANDATORY, the Grand's hard condition).** On Windows, check (a) binary present AND (b) PowerShell can resolve `bw` — **SEPARATELY**. A git-bash `bw --version` FALSE-GREENS (bw runs from git-bash while PowerShell still cannot see it — exactly this machine's prior state). The PowerShell-callability fix MUST run even when the binary check passes. The verify probe must exercise PowerShell resolution (`Get-Command bw` / a PowerShell `bw --version`), not only a git-bash check.

- **DC4 — Unix obtention (delegate to upstream; do NOT reinvent).** Helper preps `~/.local/bin` (mkdir + ensure on PATH via shell-rc) then invokes upstream pinned to it (`... | INSTALL_DIR="$HOME/.local/bin" sh`, or download-then-run). **Version = floor-via-latest** (upstream is latest-only with no pin hook; latest always clears the floor; idempotent skip if already >= floor). **Checksum = accept upstream's no-checksum HTTPS posture** (Grand ACCEPTED §4a — making it symmetric means wrapping/replacing upstream, which the directive forbids). State this asymmetry plainly in the helper + design.

- **DC5 — Windows obtention (ours end-to-end).** Download `beadwork_<ver>_windows_<arch>.zip` for a floor-satisfying version (the `>=0.13.2` latest), **SHA256-verify against `checksums.txt`** (FAIL-CLOSED on mismatch), extract `bw.exe`, place it in the DC2 dir. No upstream installer exists for this path.

- **DC6 — `install.sh` opt-in flag.** Add `--bootstrap-bw` (default OFF) that invokes the helper as a pre-flight; document in `--help`. **When the flag is absent, install.sh behavior is byte-unchanged** (the regression bar — there is no install.sh test harness; the close-gate diffs a `--dry-run` with/without the flag). install.sh detects platform via `uname` and delegates the OS split to the helper (do not re-implement obtention in install.sh).

- **DC7 — onboarding skill canon reversal (`skills/install-stoa/SKILL.md`; RATIFIED).** Reverse Beat 1 + the "What you must NOT do" entries: from "bw is a prereq — STOP, do not install" to "detect bw; if missing, drive `bootstrap-bw.sh` with the PRINCIPAL in the loop — show the release source + (Windows) the SHA256 + the PATH change, get consent, then continue." Guided + consented (the human-facing front-door); the dry-run-first discipline already in the skill is preserved. Record the reversal justification (bw is fundamental; silent Windows failure; obtention is public + pinned + SHA256-verified + self-updating; the one-helper opt-in design preserves the separation-of-concerns spirit).

- **DC8 — honest stance + scope guard + threat posture.** This is a real trust surface: the helper DOWNLOADS and places an executable on PATH and MUTATES the Windows USER PATH. That makes it **threat-relevant** (supply-chain + PATH-mutation) — ARGUS weighs it; mitigations are SHA256-verify (Windows) + HTTPS/TLS + following the upstream canonical path (Unix) + registry-safe-append + fail-loud. Scope guard: this arc delivers the helper + the TWO in-repo consumers (DC6 install.sh flag, DC7 onboarding skill). The THIRD consumer — the cookie-cutter (u--9s2) non-interactive builder stand-up — has NO in-repo call-site (verified: `provision/` is the emit-then-apply choreography, not a machine stand-up); the helper is built `--yes`-ready for it, but its call-site lands in u--9s2, NOT here. The historical `arc-19` "do not install bw" directive is superseded-in-spirit by this arc; it is NOT edited (history stays).

---

## Deliverables (land together)

1. `substrate/bootstrap-bw.sh` (NEW) — the idempotent OS-split helper (DC1-DC5), `--yes`/`--check`/`--dry-run`.
2. `substrate/install.sh` — the opt-in `--bootstrap-bw` flag (DC6) + `--help` entry; absent-flag behavior byte-unchanged.
3. `skills/install-stoa/SKILL.md` — the Beat 1 + "must NOT" canon reversal (DC7).
4. Charter `stoa--elx` updated with the landing SHA + per-DC disposition.

## Verification / Definition of done

- **Mechanical (close-gate + VERA, assert on REAL execution, not a dry-run that early-returns):**
  - Helper is **idempotent**: on this machine (bw already present + >= floor) it correctly SKIPS obtention; `--check` reports state without mutating; `--dry-run` prints planned actions without writing.
  - **Windows PATH mutation is registry-safe + fail-loud** — VERA exercises the append logic against a THROWAWAY PATH value / probe dir, NEVER mutating this machine's real USER PATH (it already has a working bw — do not touch it). A blind `setx` that could truncate/clobber is an automatic route-back.
  - **Two-independent-checks present + correct (DC3):** the PowerShell-callability check runs even when the binary is present; a git-bash-only green cannot satisfy it. VERA demonstrates the false-green is caught.
  - **Windows SHA256 verify is fail-closed** (a corrupted/mismatched zip aborts; no extraction on mismatch).
  - **Unix path delegates to upstream** (does not re-implement download/extract), preps `~/.local/bin` on PATH, pins `INSTALL_DIR`; floor-via-latest; idempotent skip.
  - **install.sh with the flag ABSENT is byte-unchanged** — diff a `--dry-run` with/without `--bootstrap-bw` (regression bar; no install.sh test harness exists).
  - **`npm run gen-data` deterministic + the FULL app test suite green** (the standing regression bar even though this arc does not edit role files — run the full suite, not a narrow "we only touched install.sh/skill" claim).
  - **`Author=PRINCIPAL` (Denson Smith) zero-foreign + the §28.9 seat trailer** on the build commit(s); **NOMOS CONFORMANT** on the final commit.
- **ARGUS cold-audit (the Grand's hard condition):** the Windows PATH-mutation mechanism specifically — truncation/clobber safety, the fail-loud branch, the registry read/write correctness, and the supply-chain trust surface (download + place-on-PATH).
- **Judgment (honest stance):** a real-but-bounded trust surface (supply-chain + PATH mutation) with named mitigations; no over-claim of "fully sandboxed." The checksum asymmetry (Windows verifies / Unix inherits upstream HTTPS-only) is stated, not hidden.

## Out of scope (do NOT fold in)

- The cookie-cutter (u--9s2) builder-stand-up call-site — the helper is built `--yes`-ready, but wiring it lands in u--9s2.
- Mutating THIS machine's real Windows USER PATH during build/verify (it already has a working bw via the Grand's session shim — VERA uses throwaway probes only).
- Changes to the `bw upgrade` flow / `bw-upgrade.md` discipline (the helper bootstraps the FIRST binary; ongoing upgrades stay `bw upgrade`).
- Editing the historical `arc-19` directive (superseded-in-spirit, not rewritten).
- Deploying install-stoa into `substrate/skills/` (it is a the-stoa-root skill per `stoa--sok`; leave it there).
- Any real provisioning / money / credentials (N/A here — public download, no creds).

## Discipline

- BY-THE-BOOK gauntlet (NOT one-pass) — DAEDALUS designs, surfaces for go/no-go, THEN ADA builds. ARGUS cold-audits the PATH mutation specifically.
- `install.sh` is the deploy mechanism for every consumer — absent-flag behavior MUST be byte-unchanged; treat like a public-API change.
- Assert DoD on REAL execution, not a `--dry-run` that early-returns past the checks (per the directive-DoD-must-match-tool-reality discipline).
- Run the FULL app suite (gen-data deterministic + vitest) as the regression bar.
- One coherent slice — helper + install.sh flag + onboarding skill. No drive-by scope.
- bw syntax: positional `bw comment`, no backticks/`$()`; `bw prime` at activation; `--reason` on close.

## Suggested phasing

- **Phase A — design (DAEDALUS).** Resolve DC1-DC8; DC2 (registry-safe PATH mutation, DAEDALUS-owned) + DC3 (two-independent-checks) are load-bearing. ARGUS cold-audits the PATH mechanism. Surface to the floor-manager for go/no-go before build.
- **Phase B — build (ADA).** The helper + install.sh flag + onboarding-skill reversal, as one slice.
- **Phase C — verify (VERA/CATO + NOMOS).** Real-execution checks (idempotent skip, registry-safe PATH against a throwaway value, two-checks false-green caught, SHA256 fail-closed, Unix delegates to upstream, install.sh absent-flag byte-unchanged); gen-data deterministic + full suite green; ARGUS cold-audit satisfied.
- **Phase D — ship to the SECOND gate.** Commit; update `stoa--elx` with the SHA + dispositions; hand back to the floor-manager for relay-up to user-tier for the close-gate verify. **Nothing merges until the Grand gates the BUILT ARTIFACT** (the Grand's second gate). User-tier relays the built artifact UP; the Grand gates; THEN user-tier merges.

Standby, run.
