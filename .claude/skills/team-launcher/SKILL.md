---
name: team-launcher
description: |
  Stand up a multi-seat Stoa agent team (POLYBIUS + PLINY by default) in terminal sessions on Windows, ready for activation — in ONE command instead of hand-opening terminals. Consumer-generic: the bundled `launch-team.ps1` derives the project + slug from where it is deployed and defaults to SAY-TRIGGER activation (pre-seeds the bare "polybius"/"pliny" so the workspace CLAUDE.md auto-loads the role). Three layouts: side-by-side PANES (default), TABS, or separate WINDOWS, via Windows Terminal (`wt`) with a windows fallback. Carries the VERIFIED `wt` + `claude` CLI mechanics (Microsoft WT docs + smoke test).

  Invoke when asked to "stand up / spin up / launch the team", "open POLYBIUS and PLINY", "start the agent sessions", "launch in panes/tabs/windows", or when a workspace needs its team brought online. Windows + Claude Code Desktop (builder tier).
author: Denson Smith
---

# team-launcher — stand up an agent team in terminals (Windows)

> **Verified mechanics, not theory.** The `wt` and `claude` flags below were confirmed against Microsoft's Windows Terminal command-line docs + a live smoke test (2026-06-04); the consumer-generic launcher was re-smoke-tested 2026-06-06 (parse + DryRun across panes / auto-derive / windows-fallback) under `stoa--h8w`. Sibling of `interactive-html-preview` (both hold verified builder-tier mechanics).

## The tool: `launch-team.ps1` (ships in this skill dir)
The script lives **beside this SKILL.md** and deploys with the skill into every workspace's `.claude/skills/team-launcher/`. One command brings up the whole team — each session named, in the project dir, and activated.

```powershell
# it derives the project + slug from its own deployed location:
.claude/skills/team-launcher/launch-team.ps1                 # PANES (default), say-trigger
.claude/skills/team-launcher/launch-team.ps1 -Layout Tabs    # one tab per seat
.claude/skills/team-launcher/launch-team.ps1 -Layout Windows # one OS window per seat (no wt needed)
.claude/skills/team-launcher/launch-team.ps1 -DryRun         # print the command, open nothing
# explicit project / slug, or a paste-trigger team:
.claude/skills/team-launcher/launch-team.ps1 -ProjectDir C:\path\to\proj -Slug proj
.claude/skills/team-launcher/launch-team.ps1 -Activation paste -Layout Windows -AutoPaste
```

**Project + slug auto-derive:** with no `-ProjectDir`, the script walks up from its own location to the workspace root (the dir containing `.claude/`); the slug defaults to that dir's leaf. So in `origindex` the seats are `POLYBIUS_origindex` / `PLINY_origindex`, floor-manager first.

**Activation modes:**
- **`say` (default)** — pre-seeds the bare word (`polybius` / `pliny`) as claude's positional prompt; the workspace `CLAUDE.md` say-trigger auto-loads the role. The common case for deployed workspaces. (If a pane doesn't fire, it is still named + ready — type the word.)
- **`paste`** — opens sessions ready for a manual activation paste; with `-Layout Windows -AutoPaste`, feeds each seat's `Paste` file as the first prompt (the-stoa-style paste-trigger).

## The verified `wt` mechanics (the part that trips you up)
- **Side-by-side panes = `split-pane -V` (`--vertical`).** `-H` stacks top/bottom. First seat is `new-tab`; each next seat is `split-pane -V` (panes) or `new-tab` (tabs).
- **`;` delimits `wt` commands** — passed as its own array token so PowerShell does not eat it as a statement separator.
- **`--title <name>` + `--startingDirectory <dir>` per pane/tab.**
- **Launch NON-blocking with `Start-Process wt …`** — a bare `wt` / `& wt` makes PowerShell wait for the window to close (WT is a Store app).
- Use the **full `claude.exe` path** (`(Get-Command claude).Source`) so PATH resolution inside the pane never bites.

## The verified `claude` CLI flags
- `--dangerously-skip-permissions` — the team runs unattended.
- `--model <name>` — `opus` alias works; full id `claude-opus-4-8` if an alias is rejected.
- `-n/--name <name>` — sets the session display name + terminal title (how each pane is labeled by seat).
- positional `[prompt]` — pre-seeds the interactive session (this is how say-trigger feeds `polybius`/`pliny`). Do **not** use `-p/--print` (non-interactive).
- In-session `/rename "<name>"` renames a live session.

## The workflow (say-trigger — the default)
1. **Launch:** `.claude/skills/team-launcher/launch-team.ps1`. Panes come up named, in the project dir, each pre-seeded its bare word; the workspace `CLAUDE.md` auto-loads each role (floor-manager = left pane / first tab).
2. **Confirm** the floor-manager's bw presence-announce before leaning on the worker.

For paste-trigger workspaces, use `-Activation paste` and paste each seat's file (floor-manager first), or `-Layout Windows -AutoPaste`.

## Gotchas (verified)
- **Don't reuse seat names of a team already running** — the same `--name` twice is a seat-identity collision. For throwaway runs use a distinct `-Slug` + a scratch `-ProjectDir`.
- **`bw comment` text is POSITIONAL, not `-m`** (`bw comment <id> "text"`). The `-m` habit silently records the body as `-m`. (Cross-ref: substrate §12.)
- **`-AutoPaste` is Windows-layout only** (a multi-line paste through a wt pane is brittle); a single bare word (say-trigger) is fine in panes.
- **Paths/names with spaces** are not quoted — keep them space-free.
- **Panes/Tabs need Windows Terminal (`wt`)** — absent → falls back to separate windows.

## Cross-references
- `launch-team.ps1` (this dir) — the tool. `-DryRun` previews without opening anything.
- `MAJOR_POLYBIUS.md` / `MAJOR_PLINY.md` — the seat roles; the activation order (floor-manager before worker) is theirs.
- The workspace `CLAUDE.md` — its say-trigger line ("when the user invokes POLYBIUS, read `.claude/MAJOR_POLYBIUS.md`") is what say-mode relies on.
- `interactive-html-preview` skill — sibling verified-mechanics skill.
- `stoa--h8w` — the generalization that made this skill consumer-deployable; `stoa--p7c` — the formal Role_Project_Instance id scheme to adopt for seat names later.
