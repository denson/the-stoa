---
name: team-launcher
description: |
  Stand up a multi-seat agent team in terminal sessions on Windows, ready for activation. Each seat runs `claude --dangerously-skip-permissions --model <model> --name <seat>` in the project directory, named and ordered (floor-manager first). Three layouts: side-by-side PANES (default), TABS, or separate WINDOWS — all via the bundled `launch-team.ps1` and Windows Terminal (`wt`). Carries the VERIFIED `wt` + `claude` CLI mechanics (confirmed against Microsoft's Windows Terminal docs + smoke test, 2026-06-04) so a team comes up in one command instead of hand-opening terminals and pasting.

  Invoke when asked to "stand up / spin up / launch the team", "open POLYBIUS and PLINY", "start the agent sessions", "launch in panes/tabs/windows", or when a fresh project needs its team brought online for activation-paste. Windows + Claude Code Desktop (builder tier).
author: Denson Smith
---

# team-launcher — stand up an agent team in terminals (Windows)

> **Verified mechanics, not theory.** The `wt` and `claude` flags below were confirmed against Microsoft's Windows Terminal command-line docs (updated 2025-11) and a live smoke test on 2026-06-04. Sibling of `interactive-html-preview` (both hold verified builder-tier mechanics).

## The tool: `launch-team.ps1`
At the repo root. One command brings up the whole team, each session named and in the project dir, ready to paste the activation instructions into.

```powershell
./launch-team.ps1                      # PANES (default): side-by-side split panes, one window
./launch-team.ps1 -Layout Tabs         # one tab per seat, one window
./launch-team.ps1 -Layout Windows      # one separate OS window per seat
./launch-team.ps1 -Layout Windows -AutoPaste   # also feed each seat's paste file as the first prompt
# a different/specialized team:
./launch-team.ps1 -ProjectDir C:\path\to\proj -Seats @(@{Name='POLYBIUS_proj'},@{Name='PLINY_proj'})
```

Default seats are in **activation order** (floor-manager FIRST → left pane / first tab): `POLYBIUS_the-stoa` then `PLINY_the-stoa`.

## The verified `wt` mechanics (the part that trips you up)
- **Side-by-side panes = `split-pane -V` (`--vertical`).** `-H`/`--horizontal` stacks top/bottom. (The names feel backwards — verify, don't guess.) First seat is `new-tab`; each subsequent seat is `split-pane -V` (panes) or `new-tab` (tabs).
- **`;` delimits `wt` commands** — `wt new-tab … ; split-pane -V …`. In PowerShell `;` is also a statement separator, so either backtick-escape it (`` `; ``) or pass it as its own argument token in an array.
- **`--title <name>` per pane/tab; `--startingDirectory <dir>` per pane/tab.** The tab title reflects the focused pane.
- **Launch NON-blocking with `Start-Process wt …`.** A bare `wt …` or `& wt …` makes PowerShell **wait for the whole window to close** before returning (WT is a Store app) — it hangs your script. `Start-Process` spawns detached and returns immediately.
- Use the **full `claude.exe` path** as the pane's command (`(Get-Command claude).Source`) so PATH resolution inside the spawned pane never bites.

## The verified `claude` CLI flags
- `--dangerously-skip-permissions` — bypass permission prompts (the team runs unattended).
- `--model <name>` — `opus` alias works; full id `claude-opus-4-8` if an alias is ever rejected.
- `-n, --name <name>` — **sets the session display name + terminal title.** This is how each pane/window is labeled as its seat. (Note: this names the *session*, not the bw identity — bw identity comes from the activation paste the seat reads.)
- positional `[prompt]` — a prompt arg starts the interactive session pre-seeded with it (this is how `-AutoPaste` feeds the activation file). `-p/--print` would make it non-interactive — do **not** use it here.
- In-session, **`/rename "<name>"`** renames a live session — the manual equivalent of `--name`.

## The workflow
1. **Author the activation pastes** (one per seat) — see the `HUMAN_paste-*-init.md` files. Floor-manager first.
2. **Launch:** `./launch-team.ps1` (panes). Sessions come up named, in the project dir, at a ready `claude` prompt.
3. **Activate:** paste each seat's file into its session, **floor-manager first** (left pane). Confirm its bw presence-announce lands before bringing the worker online. `-AutoPaste` (Windows layout) skips the manual step.

## Gotchas (verified)
- **Don't reuse the seat names of a team that's already running** — two sessions both named `PLINY_the-stoa` is a seat-identity collision. For test/throwaway runs use distinct names (`POLYBIUS_test`) and a scratch `-ProjectDir`.
- **`bw comment` text is POSITIONAL, not `-m`** (`bw comment <id> "text"`). The `-m` habit silently records the body as `-m` and drops your text — it has bitten the activation pastes. (Cross-ref: substrate §12 bw cookbook.)
- **`-AutoPaste` is Windows-layout only** for now — feeding a multi-line paste file through `wt`'s pane command line is brittle; panes/tabs open for manual paste.
- **Paths/names with spaces** aren't quoted by the script — keep them space-free.
- **Panes/Tabs need Windows Terminal (`wt`).** If absent, the script falls back to separate windows.

## Cross-references
- `launch-team.ps1` (repo root) — the tool this skill documents.
- `HUMAN_paste-polybius-the-stoa-init.md` / `HUMAN_paste-pliny-init.md` — the activation pastes the launched sessions consume.
- `MAJOR_POLYBIUS.md` / `MAJOR_PLINY.md` — the seat roles; the activation order (floor-manager before worker) is theirs.
- `interactive-html-preview` skill — sibling verified-mechanics skill (the rendering layer for decision surfaces).
- Microsoft Windows Terminal command-line docs — the authority the `wt` mechanics were verified against.
