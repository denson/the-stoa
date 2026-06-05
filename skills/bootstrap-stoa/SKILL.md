---
name: bootstrap-stoa
description: "Zero-to-running setup of a USER-LEVEL Stoa team for a newcomer who has only Claude Code Desktop — possibly no git, no beadworks (bw). Detects what is already present and installs only what is missing, then deploys the team. The chain: install git (if missing) -> install bw (jallum's beadwork, if missing) -> clone the-stoa -> run install.sh --target user (which git-inits + bw-inits user-beadwork and deploys the substrate to ~/.claude/). Windows-first (winget for git; bw release .zip), with macOS/Linux paths. Surfaces platform security prompts (UAC / SmartScreen / Gatekeeper / sudo) before they fire. Triggers: set up the stoa, install the stoa from scratch, get the stoa running, I don't have git, bootstrap the stoa, onboard me to the stoa, start a stoa team."
author: Denson Smith
---

# bootstrap-stoa — zero to a running user-level Stoa team

**Agent-execution shape.** The human points their Claude Code Desktop session at this file; you (their AI) read it and drive the setup on their behalf. The human makes a few yes/no choices and approves the OS security prompts; you do the rest. **End state:** git + `bw` installed, the-stoa cloned, a user-level Stoa team deployed at `~/.claude/`, ready for the human to say "POLYBIUS."

This is the layer **below** `install-stoa`: that skill assumes git + bw already exist (it pre-flight-checks `bw` and stops if it is missing). This skill installs those prerequisites first, then hands off to the user-level install.

> **Dependency citation (required, load-bearing).** `bw` (beadwork) is **jallum's** tool — https://github.com/jallum/beadwork. The Stoa is built *on* it; we did not write it. **Credit `bw` to jallum** wherever provenance comes up. (The Stoa substrate and this skill are Denson Smith's, MIT — that is a metadata fact, not something to recite in user-facing prose. Do **not** credit Denson Smith in the install narration.)

---

## Detect audience + environment FIRST (install only what is missing)

**Audience.** If another AI / automated system is executing, use the **AI path** blocks (terse, no explanation unless something fails). If a **human is at the keyboard**, use the **Human path** blocks: explain each step, and **prep every platform security prompt before it fires** — non-technical users abandon installs when a UAC / SmartScreen / Gatekeeper box surprises them. Removing that surprise is your job.

**Environment.** The user may already have git and/or bw (e.g. a developer machine). Detect, then **skip any step whose tool is already present and new enough.**

**AI path — probe:**
```bash
# OS (Windows has no uname unless in Git Bash)
uname -s 2>/dev/null || echo "windows"
# git present?
git --version 2>/dev/null && echo "GIT: present" || echo "GIT: MISSING"
# bw present + new enough (need >= 0.13.0)?
bw --version 2>/dev/null && echo "BW: present" || echo "BW: MISSING"
```

Map the result: **GIT present → skip Step 1. BW present and ≥ 0.13.0 → skip Step 2.** Always run Steps 3–5.

**On Windows specifically:** the Stoa installer (`install.sh`) is a bash script, so it runs in **Git Bash** — which is bundled with Git for Windows. So Step 1 (install git) is also what gives a Windows user the shell the rest of the bootstrap needs. Run Steps 2–5 from a **Git Bash** prompt.

---

## Step 1 — install git (only if MISSING)

### Windows

**Human path — prep the prompt first:**
> *"Installing Git for Windows will pop a Windows permission box (UAC) asking to allow the installer to make changes — that's expected; click Yes. It also installs 'Git Bash,' a terminal the rest of the setup runs in."*

**AI path — winget (ships on Windows 10/11):**
```powershell
winget install --id Git.Git -e --source winget
```
This launches the official Git for Windows installer (Inno Setup) and will raise a UAC prompt. Git Bash is included by default. After it finishes, **open a fresh Git Bash window** so `git` is on PATH, and continue the remaining steps there.

**Fallback if `winget` is absent** (older Windows): direct the human to download + run the installer from **https://git-scm.com/download/win** (accept the defaults — they include Git Bash), then reopen Git Bash. Do not invent a different URL.

### macOS
```bash
git --version   # on macOS this alone triggers the Xcode Command Line Tools install prompt if git is absent
# or, if Homebrew is present: brew install git
```
Gatekeeper / a CLT install dialog may appear — tell the human to approve it.

### Linux
```bash
sudo apt-get install -y git    # Debian/Ubuntu;  dnf/pacman/zypper on other distros
```
Surface that the package manager will ask for the sudo password (it won't echo as they type — that's normal).

Verify before moving on: `git --version` returns a version.

---

## Step 2 — install bw / beadwork (only if MISSING) — jallum's tool

`bw` is **jallum's** beadwork (https://github.com/jallum/beadwork) — a single Go binary, no runtime needed. The canonical, maintained install playbook is the **`beadwork-install`** skill in the `beadwork-skills` marketplace (https://github.com/denson/beadwork-skills); reuse it if you can fetch it. The essential binary-install steps are inlined below so this bootstrap is self-contained.

> **You only need the bw *binary* here.** The Stoa's `install.sh --target user` (Step 4) does its own `bw init` for the user-beadwork store, so do **not** run `bw init` / pick a storage mode in this step — that is `install.sh`'s job. (If the user later wants bw in their own *project* repos with the full storage-mode walkthrough, point them at `beadwork-install`.)

### Windows — release `.zip` (jallum's `install.sh` is POSIX-only and refuses Windows)

**Human path — prep the prompt first:**
> *"`bw` is an unsigned open-source binary, so Windows SmartScreen/Defender may warn the first time it runs. That's expected for unsigned tools — choose 'More info → Run anyway'. I'm downloading it from jallum's official GitHub release."*

**AI path (Git Bash):**
```bash
VERSION=$(curl -fsSL https://api.github.com/repos/jallum/beadwork/releases/latest \
          | grep '"tag_name"' | sed 's/.*"v\(.*\)".*/\1/')
echo "latest bw release: ${VERSION:-unknown}"
ARCH=amd64                          # use arm64 only on Windows-on-ARM
mkdir -p ~/bin
curl -fsSL -o /tmp/bw.zip \
  "https://github.com/jallum/beadwork/releases/download/v${VERSION}/beadwork_${VERSION}_windows_${ARCH}.zip"
unzip -o /tmp/bw.zip -d /tmp/bw-extract
[ -f ~/bin/bw.exe ] && cp ~/bin/bw.exe ~/bin/bw-prior.exe   # back up any prior binary
cp /tmp/bw-extract/bw.exe ~/bin/bw.exe
which bw >/dev/null 2>&1 || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
bw --version
```
Re-open Git Bash if `bw` isn't found immediately. Verify the version reads **0.13.0 or higher**.

### macOS / Linux — jallum's `install.sh` one-liner
```bash
INSTALL_DIR="$HOME/.local/bin" curl -fsSL https://raw.githubusercontent.com/jallum/beadwork/main/install.sh | sh
bw --version
```
(`INSTALL_DIR=~/.local/bin` keeps it a user-local, no-sudo install.) Verify **≥ 0.13.0**.

---

## Step 3 — clone the-stoa (now that git exists)

**AI path:**
```bash
cd ~
git clone https://github.com/denson/the-stoa.git
cd the-stoa
```
**Human path:** *"Now I'll download the Stoa itself into your home folder with git."* Run it; confirm `the-stoa/` exists.

---

## Step 4 — install the user-level Stoa team

`substrate/install.sh --target user` does three things: scaffolds the user-tier directory (where your projects live), **git-inits + bw-inits** a `user-beadwork` store there, and deploys the substrate (the MAJOR role files + CAPTAIN envelopes + templates + skills + modules) into `~/.claude/`. On Windows, run it from **Git Bash**.

**Human path — one question to ask first** (the installer also asks this itself):
> *"Where do you keep your projects? The Stoa installs there so the chief-of-staff can see them. If you don't have a projects folder yet, the default `~/stoa_projects/` will be created."*

**AI path:**
```bash
# from inside the-stoa/ ; --modify-claude-md appends the auto-load reference to ~/.claude/CLAUDE.md
# Dry-run FIRST (discipline: never a real install without showing the plan):
bash substrate/install.sh --target user --modify-claude-md --dry-run
# then, on confirmation, the real run (drop --dry-run). Pass --user-tier-dir to skip the interactive prompt:
bash substrate/install.sh --target user --user-tier-dir "$HOME/stoa_projects" --modify-claude-md
```
The dry-run beat is non-negotiable even if the user says "just do it" — show the plan, then run for real on their nod.

---

## Step 5 — verify + first session

**AI path:**
```bash
ls ~/.claude/MAJOR_POLYBIUS.md ~/.claude/MAJOR_PLINY.md ~/.claude/agents/CAPTAIN_*.md
bw --version
git -C "$HOME/stoa_projects/user-beadwork" rev-parse --verify beadwork >/dev/null 2>&1 && echo "user-beadwork OK"
```
Should list 2 MAJORs + the CAPTAIN envelopes, a working `bw`, and the `beadwork` orphan branch in `user-beadwork/`.

**Then hand off to the first real session:**
> *"You're set up. Open a new Claude Code session and say **POLYBIUS** (or 'chief of staff') — the chief-of-staff will introduce itself, ask your name, and walk you through onboarding."*

---

## Hard rules

1. **Credit `bw` to jallum** wherever provenance comes up; never imply the Stoa team wrote beadwork. Do **not** credit Denson Smith in the user-facing install narration (metadata only).
2. **Install only what is missing.** Detect git + bw first; skip satisfied steps. The user may already have a developer machine.
3. **Prep every platform security prompt before it fires** — UAC (winget / git installer), SmartScreen/Defender (unsigned `bw.exe`), Gatekeeper (macOS), sudo (Linux). The prep copy above is the model.
4. **Install the prebuilt bw *release binary*; never build from source** (no Go toolchain). jallum's `install.sh` is POSIX-only — on Windows use the release `.zip`. Only need the binary here; `install.sh --target user` does the `bw init`.
5. **Don't invent install URLs.** Canonical: `winget install --id Git.Git -e` or git-scm.com/download/win (git); jallum's `install.sh` (macOS/Linux bw) or the `beadwork_<ver>_windows_<arch>.zip` release asset (Windows bw); `github.com/denson/the-stoa` (the Stoa). If unsure, point at the upstream README rather than guess.
6. **Default to user-local, no-admin paths** (`~/bin`, `~/.local/bin`, `~/.claude/`, `~/stoa_projects/`). Nothing here needs Administrator beyond the one UAC box the git installer raises.
7. **Dry-run `install.sh` before the real run, always** — show the plan even if the user says "just do it."

## Cross-references

- `skills/install-stoa/SKILL.md` — the next layer up (guided substrate install; assumes git + bw, which this skill provides). Hand off to it / to its logic once prerequisites are in place.
- `skills/stoa-intro/SKILL.md` — the visual tour, for a user who wants to understand the Stoa before/after installing.
- `substrate/install.sh` — the mechanical installer this skill drives in Step 4 (`--help` for the full flag set).
- **`beadwork-install`** (in jallum-dependency marketplace `github.com/denson/beadwork-skills`) — the canonical, steward-maintained bw install playbook; Step 2 inlines its essential binary-install path and defers the fuller storage-mode walkthrough to it.
- `bw` itself: **https://github.com/jallum/beadwork** (jallum). Git for Windows: https://git-scm.com/download/win. winget: https://learn.microsoft.com/windows/package-manager/winget/.
