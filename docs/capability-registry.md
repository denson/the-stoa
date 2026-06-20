# Capability Registry — skills, workflows & tools available to the Stoa builder seats

A **living inventory** of the skills, workflows, and MCP tools available in the builder environment (Claude Code Desktop, Mac/Windows), with **empirically verified** capabilities — not assumed ones. We test as we go and record what we actually confirm.

> **Why this exists:** "I think tool X can do Y" has burned us repeatedly. The rule is **verify, then record here.** A description tells you what a tool is *for*; only a test tells you what it *does*.

## How to verify an entry (methodology)
Don't trust the description. To confirm what a skill/workflow actually does:
1. **Invoke + inspect** — run it on a task and watch what it touches.
2. **Read its generated script** — a workflow writes its script to `~/.claude/projects/<session>/workflows/scripts/`. Read *that* (this is how we nailed deep-research).
3. **Probe to falsify** — give it a task designed to *fail* if the capability is absent (e.g. "read this local file" against a web-only tool).

Record the finding **and the evidence** (script line, observed behavior, date).

**Status legend:** ✅ VERIFIED (tested + evidence) · 🔲 UNTESTED (description only) · ⚠️ CAVEAT (partial / known limit)

---

## Built-in (ship with Claude Code Desktop)

| Skill / Workflow | What it's for (per description) | Status + verified findings |
|---|---|---|
| `deep-research` | Fan-out web search → fetch → **adversarial 3-vote verify** → cited report | ✅ **WEB-ONLY** (2026-06-04). Read the 349-line generated script: `WebSearch`/`WebFetch` only, **zero** local access (no Bash/Read/grep/bw). Line-9 comment: *"Ported from bughunter architecture. WebSearch/WebFetch instead of git/grep."* Cannot read the repo or beadwork. → For local grounding, reverse-port to a custom workflow. |
| `code-review` | Review the diff for correctness bugs + reuse/simplification | 🔲 UNTESTED. Likely the productized Frontier-Red-Team **adversarial-verification bug-hunting** ("bughunter" lineage). Relevant to substrate debloat. |
| `security-review` | Security / vulnerability review of code | 🔲 UNTESTED. bughunter-lineage; productized vuln-finding. |
| `review` | Review a pull request | 🔲 UNTESTED |
| `simplify` | Review changed code for reuse/simplification/efficiency, then apply | 🔲 UNTESTED. **Directly relevant to the debloat.** |
| `verify` | Run the app + observe behavior to confirm a change works | 🔲 UNTESTED |
| `run` | Launch + drive the project's app | 🔲 UNTESTED |
| `schedule` / `loop` | Scheduled / recurring agents (cron, polling) | ⚠️ in use (Monitor crons) |
| `claude-api` | Build/debug Claude API + SDK apps | 🔲 UNTESTED |
| `fewer-permission-prompts` / `update-config` / `keybindings-help` / `init` | Harness config | 🔲 |

## `anthropic-skills` plugin

| Skill | For | Status |
|---|---|---|
| `skill-creator` | Create / modify / eval skills | 🔲 — for *building* the decision-surface skill |
| `intent-engineering` | Design agents + agentic workflows | 🔲 — relevant to the workflow-encoding |
| `consolidate-memory` | Merge duplicate memories, fix stale facts, prune index | 🔲 — a working **model for the debloat/consolidation half** |
| `docx` / `pdf` / `pptx` / `xlsx` | Office doc create/read/edit | 🔲 |
| `conceptviz-prompt-generator` | Generate illustration prompts (ConceptViz) | 🔲 |
| `setup-cowork` | Cowork setup | 🔲 |

## the-stoa substrate skills (our own — behavior known from source)
`workflow-composer` · `gauntlet-setup` · `save-verdict` · `handoff-author` · `check-substrate-updates` · `check-bw-release` · `validate-spec` · `cite-check` · `credential-discipline` · `inspect-script-output` · `copy-artifact` · `edit-json` · `format-validate` · `runner` · `transcribe-bw-to-disk` · `youtube-transcript-extract`

## Marketplace plugins
`ariadne-core-*` (install / deploy / build / router / walkthrough / document-intelligence) — the ariadne-core project's skills.

## MCP tool-servers (capabilities, not skills)

| Server | Capability | Status |
|---|---|---|
| **Claude Preview** (`mcp__Claude_Preview__*`) | preview a dev server + DOM-aware interact | ✅ **VERIFIED (2026-06-04)** — rendered the 37-card debloat decision-surface successfully. **Model:** `preview_start` runs a **dev server from `.claude/launch.json`** (e.g. `python -m http.server --directory docs`), *not* a direct static-file open. Full DOM-aware toolkit: `screenshot` / `snapshot` (a11y tree) / `inspect` (computed styles) / `click` / `fill` / `eval` / `console_logs` / `network` / `resize`. Interactive vanilla-JS works; TS/build apps would serve via Vite etc. "Live-update as you talk" = edit source + reload. Precedent: the case-study `architecture-kg.html` uses the same pattern (`stoa-kg` config). |
| **Claude in Chrome** (`mcp__Claude_in_Chrome__*`) | DOM-aware browser control | 🔲 |
| **ghost** | managed Postgres (provision/fork/SQL) | 🔲 |
| **computer-use** | desktop control (screenshot/click/type) | ⚠️ DISCONNECTED this session |
| Google connectors (gmail / calendar / drive) | per-session productivity | 🔲 |

---

## Workflows note
- **Only `/deep-research` is a bundled workflow.** No user-accessible bundled-workflows directory exists.
- **"bughunter"** is the internal Anthropic **Frontier Red Team** architecture deep-research was ported from (CTF + national-lab + production vuln-hunting; the *adversarial self-verification* spine). **Not reachable by that name.** Reconstruct it by reverse-porting the deep-research script (git/grep/bw instead of WebSearch/WebFetch).
- **Custom workflows** are authored via the `workflow-composer` skill → saved to `.claude/workflows/` (`s` in `/workflows`), auto-discovered as `/<name>`, no registry needed (verified vs the workflow docs 2026-06-04).

---
*Maintained by user-tier POLYBIUS. Last updated 2026-06-04. Promotable to a deployable builder-onboarding skill once stable.*
