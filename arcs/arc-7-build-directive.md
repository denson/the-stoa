# Arc 7 build directive

**Audience:** the fresh Claude Code session opened in this repo to build Arc 7 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 4-6 (commits `67d4589`, `22780a0`, `0a9e5c1`) — substrate-redesign-from-v2 complete; canonical substrate is v2-aligned.

**You are MAJOR_PLINY for the agent-substrate Arc 7 engagement.** The user-tier Chief-of-Staff (POLYBIUS-equivalent) wrote this directive; you receive it and execute. Per v2 §4, MAJOR_PLINY is the orchestrator role. Read `MAJOR_PLINY.md` (this repo, Arc 4's v2-shape file) and assume the orchestrator role.

**Your one job for this engagement:** improve `install.sh` to fix four real gaps the substrate end-to-end test surfaced. Then return cleanly.

---

## Read first

1. **`install.sh`** in this repo — the script you're improving. Read it through to understand current behavior. (Voice debt at line 17 noted in `as--meq` is one of the things you fix.)

2. **`README.md`** "Testing the install" section — describes the manual test recipe. After your changes, this section needs updating to reflect new behavior.

3. **`plans/three-role-recursive-architecture.md` in user-beadwork — v2 spec.** Specifically:
   - §8 (onboarding flow + custom paste-instruction templating + communication-discipline-during-onboarding)
   - §12.1 (open question: install.sh Windows-bash portability)
   - §12.2 (open question: install.sh deploys `templates/`)
   - §12.3 (open question: install.sh next-step guidance)

4. **`u--7yg` design inputs** — primarily `u--7yg.20` (terminology fix) for the install.sh:17 cleanup; `u--7yg.13` for general architecture context.

5. **The existing `as--meq` ticket** in this repo's beadwork — concrete plan for the install.sh:17 sweep. Pick it up as part of Arc 7 work; resolve and close.

---

## What Arc 7 is

The end-to-end substrate test 2026-05-01 surfaced four real gaps in `install.sh`:

1. **install.sh:17 has a Colonel reference** (filed `as--meq` P2). Reflexive v1 vocabulary in a script header comment that v2's substrate sweep didn't catch because Arc 6's grep was scoped to ONBOARDING + templates only.

2. **`templates/` doesn't get deployed.** The Arc 6 templates (`paste-instruction-template.md`, `onboarding-questions.md`, `consent-prompts.md`) are POLYBIUS's runtime working tools, but install.sh only deploys the role files + CAPTAIN envelopes. POLYBIUS at runtime can't reach the templates from the deployed location.

3. **No next-step guidance on completion.** Real human installing this stares at `install.sh: done (applied)` and asks "ok, now what?" Install needs to print clear next steps.

4. **Windows-bash portability is undocumented.** PowerShell `bash` resolves to WSL relay which fails when no WSL distro is installed. Windows users have to know to call `& "C:\Program Files\Git\bin\bash.exe"` explicitly. Either documentation needs to call this out clearly, OR a sibling `install.ps1` with native PowerShell logic.

---

## Deliverables

### 1. Fix install.sh:17 Colonel reference (resolves `as--meq`)

Replace with PRINCIPAL or HUMAN per v2 voice. Read `as--meq`'s description for the concrete plan if needed.

### 2. Deploy `templates/` alongside role files

Extend install.sh to copy `templates/*.md` from `agent-substrate/templates/` to `<target>/.claude/templates/<filename>` at deploy time.

- Project-tier deploys to `<project>/.claude/templates/`
- User-tier deploys to `~/.claude/templates/`
- Idempotent — re-running install doesn't duplicate
- The three template filenames (paste-instruction-template, onboarding-questions, consent-prompts) deploy unsuffixed (templates aren't agent-shaped; they're shared tooling)
- New flag (suggested): `--no-templates` for opt-out (default: deploy templates)

### 3. Print next-step guidance on completion

After successful install, print a clear next-steps block. Pretty-print but not ASCII art. Something shaped like:

```
✓ Installed.

Next steps:
  1. cd <project-dir>
  2. Open Claude Code: claude
  3. Say "POLYBIUS" or "chief of staff" — the chief-of-staff
     will load and walk you through onboarding.

For re-paste recovery after compact/clear, MAJOR_POLYBIUS keeps
the latest activation paste at <project>/HUMAN_paste-orchestrator-
instruction.md once onboarding completes.
```

Customize the path text based on whether target is project or user. Suppress in `--dry-run` mode (since dry-run doesn't actually complete an install).

### 4. Windows-bash portability

Build session decides scope here based on time/complexity tradeoff:

- **(a) Document only** — README "Testing the install" section gets a Windows section: "Use Git Bash on Windows; PowerShell users invoke explicitly: `& \"C:\\Program Files\\Git\\bin\\bash.exe\" install.sh ...`". This is the minimum-viable fix. Cheap, no new file.

- **(b) Sibling `install.ps1`** — PowerShell-native installer with the same flag interface. Either calls into install.sh via Git Bash if available (auto-discover the path), OR re-implements the file-copy + CLAUDE.md append + next-step-print logic natively. Real value for Windows users; ~half-day's work.

PRINCIPAL recommends starting with (a) and stretching to (b) only if scope allows. Surface to PRINCIPAL if you want to escalate scope to (b).

### 5. README update

- "Testing the install" section reflects new behavior (templates deploy, next-step guidance)
- Windows portability documented per (4)
- Status line updated for Arc 7 ship

### 6. Tests

After the changes, re-run the manual test recipe:
- `./install.sh --help` — shows new flags + next-step framing
- Dry-run for project + user targets — no writes; shows what would happen
- Real install on `mktemp -d` — verify templates land + next-step block prints
- Idempotency — second install run doesn't duplicate templates, doesn't re-append CLAUDE.md, prints next-steps cleanly
- `--no-templates` flag (if implemented) — no templates land
- `--no-captains` (existing) — still works

---

## Definition of done

- install.sh:17 (and any other Colonel references in the script) cleaned to v2 voice
- `templates/` deploys alongside role files; tested in dry-run + real install + idempotent
- Next-step guidance prints on successful install (suppressed in dry-run)
- Windows portability handled per option (a) or (b)
- README updated
- All tests pass
- bw beadwork epic for Arc 7 closed; `as--meq` resolved + closed
- All committed to `main` and pushed to origin (autonomous-ship per `u--7yg.11`)

---

## Out of scope

- **Refactoring existing project deploys** — Arc 8 handles propagating Arcs 4-7's improvements to `agent-team-team` and `agent-character-builder`
- **The Stoa updates** — Arc 9
- **Sub-project spawning** — Arc 10
- **Re-authoring substrate role files** — Arcs 4-6 already shipped them; don't touch

---

## Beadwork

`bw` is initialized (`as-` prefix). File a new epic for Arc 7:

```
bw create "[EPIC] Arc 7 — install.sh improvements (templates deploy, next-step, Windows portability, voice cleanup)" -t epic -p 1
```

Wire `as--meq` as a child of the epic (or re-parent it):

```
bw update as--meq --parent <new-epic-id>
```

File children for each deliverable + tests pass + README update. Close as you go.

---

## Discipline

Same as Arcs 4-6:

- HITL default (v2 §7)
- Principal-as-router (`u--7yg.1`) — surface only project-direction calls
- Verify-then-execute (`u--7yg.10`, `u--7yg.18`)
- One job per agent (`u--7yg.17`) — your one job is Arc 7
- Wait-for-quiescence (`u--7yg.15`)
- Autonomous-ship on clean PASS (`u--7yg.11`) — push is part of ship
- Voice discipline (v2 §6) — `grep -i "colonel" install.sh` should be empty after your work (the script doesn't need any deliberate references to the reserved future agent rank)

---

## Operating mode

**Human-in-the-loop** (v2 §7). Surface for input at:
- (a) ambiguity that needs PRINCIPAL input — most likely place: deciding (a) vs (b) for Windows portability
- (b) work product ready for review (optional — autonomous push for clean self-validation)
- (c) done

For Arc 7 specifically: if you go with option (a) for Windows (docs only), no surface needed — that's the conservative default. If you want to escalate to (b) (sibling install.ps1), surface the scope question first.

---

## How to surface back

Either:
- Comment on a beadwork ticket in this repo (`as--*`)
- Write a short hand-back report; PRINCIPAL will relay

Standby, run.
