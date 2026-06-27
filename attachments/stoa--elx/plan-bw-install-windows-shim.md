<!-- author: Denson Smith -->
<!-- ticket: stoa--elx (the-stoa store) -->
<!-- from: Polybius the Stoa (user-tier the-stoa forge owner) -->
<!-- for: Polybius the Grand — planning deliverable, awaiting gate -->

# PLAN — bw bootstrap + Windows shim into the Stoa install process (stoa--elx)

## 0. TL;DR

Make a working `bw` a **deterministic outcome of standing a machine up**, not per-machine
archaeology. One mechanical helper, three consumers, each with the right consent posture.
The obtention story is unusually clean (public repo, goreleaser assets, SHA256 checksums,
built-in self-upgrade), so the risk is concentrated in exactly one place: the Windows
PATH mutation. Everything else is low-risk.

**The one decision I need from you (the Grand):** the consent posture / default —
specifically whether `install.sh` should bootstrap bw automatically when it detects bw is
missing, or only behind an explicit opt-in flag. My recommendation is opt-in flag in
`install.sh`, guided-and-consented in the onboarding skill, and non-interactive in the
cookie-cutter (§7). Everything else below I'm prepared to lock on your gate.

---

## 1. Verified ground truth (probed live 2026-06-27, not from memory)

- **bw on this machine:** PE32+ Windows console exe at `~/bin/bw`, extensionless, ~13.5 MB,
  Go-built, **0.13.1** live. Git-bash runs it natively (`~/bin` on git-bash PATH); PowerShell/cmd
  cannot name-resolve an extensionless PE — the exact wall you hit.
- **Upstream:** `github.com/jallum/beadwork` is **PUBLIC, not archived.** Latest tag **v0.13.2**
  (= the stoa--fqh upgrade target; this plan resolves stoa--fqh as a side effect on any machine
  that runs the bootstrap).
- **Release assets (goreleaser standard):** `beadwork_<ver>_<os>_<arch>.<ext>` for
  darwin/linux/windows x amd64/arm64. Windows ext = `.zip`; macOS/Linux = `.tar.gz`. A
  `beadwork_<ver>_checksums.txt` ships every release (SHA256, the integrity anchor).
- **Self-upgrade is built in:** `bw upgrade [--check] [--yes]` updates the binary from these
  same GitHub releases. **Consequence: the installer only needs to bootstrap the FIRST binary;
  bw carries itself forward.** No re-pin needed for future upgrades.
- **No credentials:** public download. This work does NOT touch credential-discipline.
- **install.sh today (2116 lines, bash):** assumes bw is present + on PATH. It CALLS `bw init`
  (L471, user-tier scaffold) but never installs the binary. Essentially zero platform detection
  (one stray comment at L1346). It runs under git-bash on Windows.
- **The proven shim (exists on disk, written by you 13:40 today):** `~/.local/bin/bw.cmd` —
  `@echo off` + `"%USERPROFILE%\bin\bw" %*`. Upgrade-proof (always invokes current ~/bin/bw),
  native Windows arg parsing (quoted multi-word args survive), cwd inherited. `~/.local/bin` is
  already on Denson's Windows PATH — a fresh builder's will not be (§4).

---

## 2. CANON-REVERSAL FLAG — gate this first

The current substrate canon says the **opposite** of what this ticket asks, in multiple places:

- `install-stoa` onboarding skill, Beat 1: *"Do not try to install bw from this skill. bw lives
  in a separate repo with its own install path."* Repeated 3x in "What you must NOT do."
- `arc-19-build-directive` L212/224-225: *"verify bw is installed... Do NOT try to install bw
  itself (out of scope; bw lives in a separate repo)."*

That was a deliberate decision (bw = heavy external dep, wrapping it is fragile). This plan
**reverses it.** The reversal is justified — the cost calculus inverted:
- bw is the substrate's durable bus + need-board; **fundamental** to all our work.
- On a fresh Windows machine the failure is **silent** (PowerShell can't resolve bw; flows
  fail until someone does PATH archaeology). You just hit it.
- Obtention turns out trivial + safe (public, checksummed, self-upgrading) — the original
  "fragile to wrap" premise no longer holds.

This is a standing must-NOT being overturned, so it must be **ratified, not slipped in.** That's
why it's decision #1 for your gate. If you ratify, the onboarding skill's Beat 1 + the "must NOT"
list get rewritten in the same arc that lands the bootstrap.

---

## 3. Q1 — How bw is obtained + where it lands

**DECISION:** Bootstrap by downloading the **pinned release archive** for the detected OS+arch
from the public jallum/beadwork releases, **SHA256-verified** against the shipped checksums.txt,
extracted, and placed at **`~/bin/bw`** (Windows: `~/bin/bw`, the extensionless PE; macOS/Linux:
`~/bin/bw` + chmod +x). Matches the existing machine convention and the ariadne Railway
`BW_SHA256` precedent (operating-disciplines bw-upgrade module §22.2).

- **Pin a FLOOR, not a ceiling:** bootstrap installs >= 0.13.2 (current latest). Thereafter
  `bw upgrade --yes` carries forward — the installer does not chase every release.
- **Idempotent:** if `bw --version` already reports >= floor, skip the download entirely.
- **Rejected alternatives:** build-from-source (needs a Go toolchain — heavy, fragile on
  Windows); `bw upgrade` as bootstrap (chicken-and-egg — needs a bw first).
- **Bonus:** running the bootstrap updates the stale `.bw-release-last-check` baseline
  (0.13.0 -> 0.13.2) and discharges stoa--fqh.

---

## 4. Q2 — The Windows shim + PATH (the ONE high-risk element)

**DECISION:** Adopt the proven `bw.cmd` forwarder verbatim. Two mechanical parts:

(a) **Write the shim** — `bw.cmd` containing `"%USERPROFILE%\bin\bw" %*`. Upgrade-proof,
    arg-safe, cwd-inherited. This part is trivial and proven.

(b) **Ensure the shim's directory is on the persistent Windows USER PATH.** This is the only
    genuinely risky bit. The shim is worthless if its dir isn't resolvable, and a fresh builder
    will NOT have `~/.local/bin` on PATH. The footgun: `setx PATH` truncates at 1024 chars and
    writes the *expanded* value, clobbering `%`-references. Mitigation (DAEDALUS owns the exact
    mechanism): read `HKCU\Environment` PATH via `reg query`, append the shim dir only if absent,
    write back safely (length-checked); if it can't be done safely, FAIL LOUD and surface the
    exact one-line manual step to the PRINCIPAL rather than risk clobbering PATH.

**This is the element most worth a gauntlet** — a PATH-clobber on a builder machine is a nasty,
hard-to-diagnose regression. ARGUS should cold-audit the PATH-mutation specifically.

---

## 5. Q3 — Platform detection / how a bash installer branches

install.sh runs under **git-bash on Windows**, so it can self-detect:
- `uname -s`: `MINGW*|MSYS*|CYGWIN*` => Windows; `Darwin` => macOS; `Linux` => Linux.
- `uname -m`: `x86_64` => amd64; `arm64|aarch64` => arm64.

The **bootstrap** (detect -> download -> verify -> extract -> place) is cross-platform bash.
The **shim + PATH** step (§4) is gated on the Windows branch only. On macOS/Linux the
equivalent is chmod +x + ensure `~/bin` on PATH via a shell-rc append (no shim needed —
extensionless binaries resolve natively there).

---

## 6. Q4 — Ownership: ONE helper, THREE consumers (RECOMMENDED architecture)

Don't fork the logic across install.sh / onboarding / cookie-cutter. Author it **once** and
let each surface consume it with its own consent posture:

**The helper — `substrate/bootstrap-bw.sh`** (new, shipped in substrate): idempotent, the whole
mechanical core — detect OS/arch -> check existing bw >= floor (skip if satisfied) ->
download + SHA256-verify + extract + place -> Windows shim + PATH (or macOS/Linux PATH) ->
verify `bw --version`. Flags: `--yes` (non-interactive), `--check` (report only), `--dry-run`.

**Consumer 1 — install.sh:** runs the helper as an **opt-in pre-flight** (a new `--bootstrap-bw`
flag, default OFF) OR detects missing bw and offers it. Default-off preserves install.sh's
"mechanical, no surprises" contract and respects that PATH mutation is a consent-bearing system
change. (This default is the §7 open question.)

**Consumer 2 — onboarding skill (install-stoa / stoa--sok):** becomes the **guided front-door.**
Beat 1 flips from "surface bw as a prereq and STOP" to "detect bw; if missing, drive
bootstrap-bw.sh with the PRINCIPAL in the loop — show the release URL + SHA256 + the PATH change,
get consent, then continue." This is the natural home for the human-in-the-loop install and
matches the credential-acquisition-default-UX + skill-accretion model (a friction point = a skill).

**Consumer 3 — cookie-cutter builder stand-up (u--9s2):** **consumes** the same helper as its
first stand-up step, non-interactive (`--yes`) — build machines are provisioned deterministically
and mandate computer-use, so no guided dialog. It does NOT re-implement; it calls the one helper.

Net: one auditable mechanical home; three call sites with correct consent posture. This is the
answer to your "where does it land" — it lands in ALL THREE, via a single shared helper.

---

## 7. OPEN QUESTION for the Grand (the one real fork)

**install.sh default behavior when bw is missing:** auto-bootstrap, or require the `--bootstrap-bw`
flag? Tradeoff:
- **Flag / opt-in (my recommendation):** install.sh stays mechanical + surprise-free; PATH
  mutation never happens without an explicit ask; the guided skill is where the human-in-loop
  bootstrap lives.
- **Auto-on-missing:** more "it just works" for someone running install.sh raw, but install.sh
  silently mutating a builder's Windows PATH on a bare run is exactly the kind of surprise the
  installer's contract avoids.

I lean opt-in. Your call — it's the only decision I'd take direction on before locking.

---

## 8. Risks + mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Windows PATH clobber via setx truncation | HIGH | §4(b) registry-safe append; FAIL LOUD + manual fallback; ARGUS cold-audit |
| Asset URL / naming shape drifts upstream | MED | goreleaser convention is stable; verify-then-execute probe at build (bw-upgrade §22 step 2); SHA256 gate fails closed |
| Reversing standing "never install bw" canon | MED | §2 explicit ratification gate; rewrite onboarding Beat 1 in the same arc |
| Re-running bootstrap on a healthy machine | LOW | idempotent: skip if bw >= floor already |
| arch mismatch (arm64 vs amd64) | LOW | uname -m branch + per-arch assets exist for all 3 OSes |

---

## 9. Recommended next step

This is substrate tooling (install.sh + a new shared helper + the onboarding skill + cookie-cutter
wiring) reversing a standing canon and carrying one genuinely risky mechanical element (PATH
mutation). That makes it **gauntlet-worthy** — a by-the-book arc, not a drive-by. On your gate of
this plan (and the §7 fork), I'll forge it as a fresh the-stoa gauntlet: directive -> NOMOS-on-
directive -> DAEDALUS (PATH-mutation is the design crux) -> ARGUS (cold-audit the PATH bit) ->
ADA -> VERA (verify on a clean PATH, both platforms if reachable) -> CATO -> NOMOS, then my
close-gate + merge, relayed back up to you.

Nothing to build until you gate. Plan is yours.
