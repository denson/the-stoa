# Arc 19 build directive — distribution-readiness entry-point skills

**Audience:** the fresh Claude Code session opened to build Arc 19 deliverables.
**Authored by:** user-tier Chief-of-Staff (POLYBIUS-equivalent) + the PRINCIPAL (Denson Smith).
**Status:** active directive.
**Builds on:** Arcs 1-18 (the-stoa main `e71e794`).

**Your one job:** make `the-stoa` cold-cloneable. When a fresh user clones `github.com/denson/the-stoa.git` and opens it in Claude Code (preferably Desktop), the agent should auto-discover an entry-point `SKILL.md` at the repo root that gives a 30-second pitch and routes the user to either a visual Chrome-MCP tour or a guided install. The case study + standalone KG visualization (already shipped) become reference material; the skill is the user-facing entry.

This is **template + skill authoring work** — small, prose-heavy, no code beyond skill frontmatter YAML and bash snippets. Comparable in scope to Arc 17 (which authored the agent-author skill).

---

## Comms — direct async via bw

POLYBIUS will be polling `stoa--<this-arc-id>` while you work. PLINY follows the surface-and-wait discipline (Arc 18): poll only when you've surfaced a question and are waiting for the response. Otherwise execute autonomously.

bw command syntax discipline: `bw comment <id> "text"` — positional, no `-m` flag (Arc 16.1 §6.1).

---

## Read first

1. **`docs/case-study/case-study.md`** — the long-form narrative; the about skill quotes from this. §1 (what this is), §3 (why three roles), §3.5 (trust patterns), §6 (information flow), §6.5 (two operational modes), §8 (disciplines).
2. **`docs/case-study/kg-spec.md`** — KG vocabulary; the tour skill references this when narrating modes.
3. **`design/Stoa_architecture/Stoa Architecture KG _standalone_.html`** — the standalone Chrome-MCP-rendered KG; the tour skill drives this. **You don't need to read its source — just reference its path.**
4. **`substrate/install.sh --help`** — the actual install CLI; the install-stoa skill wraps this.
5. **`substrate/ONBOARDING.md`** — the existing onboarding narrative (5 scenarios); the install-stoa skill uses Scenario 1-4 patterns (depending on tier).
6. **`substrate/templates/consent-prompts.md`** — consent prompt patterns; the install-stoa skill follows these for the dry-run-first / --modify-claude-md consent beats.
7. **README.md** — current developer-facing README; you'll prepend a new section, not rewrite.
8. **LICENSE** — already exists at root (POLYBIUS wrote this pre-dispatch — standard MIT, copyright Denson Smith 2026). Verify it's there; do not modify.

---

## Phase A — Architectural decisions (LOCKED pre-dispatch by PRINCIPAL)

You do NOT need to surface these as Phase A calls — they were settled during the directive review:

### A1. File structure — LOCKED

```
the-stoa/
├── LICENSE                              # already exists; standard MIT
├── README.md                            # MODIFY — prepend new "Getting started" section + update License section
├── SKILL.md                             # NEW — root entry-point "about" skill; agent discovers automatically
├── CLAUDE.md                            # NEW — auto-read by Claude Code; tells agent about SKILL.md
└── skills/
    ├── stoa-intro/SKILL.md              # NEW — visual Chrome-MCP tour
    └── install-stoa/SKILL.md            # NEW — guided install walkthrough
```

### A2. Skill naming — LOCKED

- Root entry-point skill frontmatter `name`: `the-stoa-about` (no slash command — agent discovers via CLAUDE.md hook)
- Tour skill: `stoa-intro` (slash command `/stoa-intro` — directory `skills/stoa-intro/`)
- Install skill: `install-stoa` (slash command `/install-stoa` — directory `skills/install-stoa/`)

### A3. Audience and tone — LOCKED

- **Audience:** the beadworks team (peer engineers comfortable with multi-actor systems) and adjacent technical readers who clone the repo to evaluate or fork.
- **Tone:** working-notebook, peer-to-peer. Same voice as the case study. **Not a sales pitch, not a 101 explainer.**
- **Pitch Claude Code Desktop hard for the visual tour** — the standalone KG rendering needs Chrome MCP. **Gracefully degrade** to text + path-pointer if Chrome MCP isn't reachable.
- **Do not suggest forking.** People will fork or not on their own.

### A4. License + distribution policy — LOCKED

- Repo is MIT-licensed (LICENSE file already at root).
- README's existing license section ("Private repo; not licensed for distribution") needs update to point to the new LICENSE file with MIT framing. PRINCIPAL is making this distributable via `github.com/denson/the-stoa.git`.

### A5. Deprioritized: in-Stoa-app port of case study + KG

The earlier plan to port the Claude Design case-study mini-site + KG visualization into the Stoa app at `/#/about` and `/#/architecture` is **deprioritized**. The skill-driven walkthrough supersedes that need: the case study lives where it's best used (in the agent's context window), and the KG lives where it's best used (in Chrome via the tour skill). The Stoa app stays focused on agent roster + skill rendering. Do NOT touch the Stoa app in Arc 19.

---

## Deliverables

### 1. README.md — prepend "Getting started" section + update License

**Location:** `the-stoa/README.md` (modify in place).

**Before:** the existing README opens with `# the-stoa` then "The unified repo for the three-role agent substrate..." then `**Author:** Denson Smith.`

**After:** insert a new `## Getting started` section between `**Author:** Denson Smith.` and the existing `## What this is` section. The new section is short (under 200 words) and tells a fresh user what to do. Approximate shape:

> "Just cloned this and want a guided tour?
>
> 1. Open this repo in **Claude Code Desktop** (Chrome MCP unlocks the interactive visual tour; the CLI works too with text-only narration).
> 2. Ask Claude something like *"what is this?"* — the agent will read `SKILL.md` at the repo root and route you.
> 3. Recommended path: visual tour first (`/stoa-intro`), then guided install (`/install-stoa`) if you want to deploy the substrate to one of your projects.
>
> The case study at `docs/case-study/case-study.md` is the deep dive (peer-technical working notebook); the interactive knowledge graph at `design/Stoa_architecture/Stoa Architecture KG _standalone_.html` is the visual companion. Both are referenced by the skills above."

Also update the existing **License** section. Replace:

> Private repo; not licensed for distribution. Authored by Denson Smith.

with:

> Licensed under the [MIT License](LICENSE) — see the `LICENSE` file for full text. Authored by Denson Smith, 2026.

Everything else in the README stays as-is (developer-facing layout, install commands, app dev setup, deployment posture, history).

---

### 2. SKILL.md (root) — the "about" skill

**Location:** `the-stoa/SKILL.md` (new file at literal repo root, NOT under `skills/`).

**Purpose:** the entry-point skill any agent in this repo finds first. Gives a 30-second pitch + routes the user to tour, install, or deeper reading.

**Frontmatter:**

```yaml
---
name: the-stoa-about
description: Entry-point skill for The Stoa repo. Reads when a fresh user lands cold; gives a 30-second pitch and routes to the visual tour (skills/stoa-intro/) or guided install (skills/install-stoa/).
---
```

**Body sections (suggested, adjust as needed for clarity):**

1. **What this skill is for** — one paragraph: the agent reads this when the user asks "what is this?" or seems exploratory.
2. **30-second pitch of The Stoa** — drawn from case study §1 + §3 + §6.5; covers the three-role architecture, the recursion claim, the two operational modes.
3. **Three places to go from here** — explicit branch to:
   - **Visual tour** → read `skills/stoa-intro/SKILL.md` and follow its procedure
   - **Install** → read `skills/install-stoa/SKILL.md` and follow its procedure
   - **Read the case study** → read `docs/case-study/case-study.md`; pick sections matched to user's stated interest
4. **Pitch Desktop for the visual tour** — explicit beat: "the visual tour works best in Claude Code Desktop with Chrome MCP. CLI users get a text-only fallback."
5. **What you must NOT do** — short list: don't auto-run tour or install without consent, don't pitch hard, don't recite case study end-to-end.

Length target: ~150-300 lines. Procedural skill in the agent-author / consent-prompts pattern — instructions for the agent in the second person ("you do X").

**Voice grounding:** the about skill speaks with the same tone as the case study + the substrate's MAJOR_POLYBIUS.md role file. PRINCIPAL/HUMAN throughout (per voice discipline u--7yg.20). Don't say "user" when "PRINCIPAL" or "the human" works better.

---

### 3. CLAUDE.md (root) — auto-discovery hook

**Location:** `the-stoa/CLAUDE.md` (new file at root).

**Purpose:** Claude Code auto-reads project-level CLAUDE.md when the user opens the cloned repo. This file tells the agent: "if user is exploratory, read SKILL.md and surface its procedure."

**Required sections (approximate):**

1. **Web-search rule** at the top, verbatim from `~/.claude/CLAUDE.md` ("Your training data is out of date — search the web (CRITICAL)" — full block). Per the global rule, this section MUST be added verbatim to every new CLAUDE.md.
2. **What this repo is** — one paragraph: The Stoa, recursive three-role agent architecture on top of bw, authored by Denson Smith. Substrate at `substrate/` is the deployable; app at `app/` is the visualizer.
3. **If the user has just cloned this and is exploring** — explicit instruction: read `SKILL.md` at the repo root and follow its procedure. The skills under `skills/stoa-intro/` and `skills/install-stoa/` are downstream branches.
4. **If the user is editing this repo** — short paragraph: forward template / substrate / app / docs work happens on a feature branch (not main); the contributor model lives in `substrate/README.md` and the substrate's bw epic.
5. **Authorship attribution** — the standard rule (verify Denson Smith in author/copyright/maintainer fields before committing; references to other people's work in prose are not authorship claims).

Length target: ~80-150 lines. **Do NOT re-articulate disciplines that live in user-tier `~/.claude/CLAUDE.md` (fix-now, etc.).** This file is repo-specific instructions only.

---

### 4. skills/stoa-intro/SKILL.md — visual Chrome-MCP tour

**Location:** `the-stoa/skills/stoa-intro/SKILL.md` (new directory, new file).

**Purpose:** drives Chrome MCP to render the standalone KG and narrates the three modes. Falls back to text narration with paths if Chrome MCP isn't available.

**Frontmatter:**

```yaml
---
name: stoa-intro
description: Visual walkthrough of The Stoa architecture using the interactive knowledge graph. Drives Chrome MCP to render the standalone HTML and narrates the three modes (Pair Programming, Hardening Flow, Recursion). Pitches Claude Code Desktop hard; falls back to text narration with paths if Chrome MCP isn't available.
---
```

**Required procedure beats (in order):**

1. **Pre-flight check** — verify Chrome MCP availability (try `mcp__Claude_in_Chrome__tabs_context_mcp`). If unavailable, branch to text fallback or offer the user to switch sessions.
2. **Spin up static server** — Chrome MCP can't load `file://` URLs, so the standalone needs to be served via HTTP. Run `python -m http.server 8765` (or similar) from `design/Stoa_architecture/`. Wait 2 seconds for it to come up.
3. **Open the standalone in a new tab** — navigate to `http://localhost:8765/Stoa%20Architecture%20KG%20_standalone_.html`. Wait 3-5s for React + Babel to compile.
4. **Read source materials before narrating** — `docs/case-study/case-study.md` and `docs/case-study/kg-spec.md`. Don't recite; use as context.
5. **Walk Mode 1 — Pair Programming** (default landing). Narrate the three-role layout, point at PLINY's decision basin, optionally play the 9-step animation.
6. **Walk Mode 2 — Agent Team Hardening Flow.** Narrate the 14-step gauntlet. Highlight ARGUS surfacing risk + the loop firing back to DAEDALUS. Point at the dashed-red back-edges as the load-bearing visual.
7. **Walk Mode 3 — Recursion.** Narrate the three-tier stack. Point at the visibility cones (the asymmetric load-bearing constraint). Point at the "OVER-SCOPE DETECTED" callout for sub-project spawning.
8. **Disciplines pitch** — pick 2-3 high-leverage `u--7yg` disciplines from case study §8 based on what the user said they care about. Suggested defaults: u--7yg.17 (one job per agent), u--7yg.20 (voice discipline), u--7yg.11 (autonomous-ship on clean PASS).
9. **Land the close** — branch to install / read deeper / pause. Stop the static server when the user is done (`pkill -f "http.server 8765"` or equivalent).

**Text fallback section** (when Chrome MCP isn't reachable): tell the user "open `design/Stoa_architecture/Stoa Architecture KG _standalone_.html` in any browser; I'll narrate alongside." Same three modes, same disciplines pitch, same close.

**What the skill must NOT do:**
- Open the tour in a browser tab without first checking Chrome MCP availability
- Leave the static server running after the tour ends
- Auto-launch the install skill (let the user choose)
- Recite the case study end-to-end

Length target: ~250-400 lines. Detailed procedure is appropriate — the agent reads this once and acts on it.

---

### 5. skills/install-stoa/SKILL.md — guided substrate install

**Location:** `the-stoa/skills/install-stoa/SKILL.md` (new directory, new file).

**Purpose:** wraps `substrate/install.sh` with a question-driven dialog so the user picks the right tier, project path, and flags before the actual install runs.

**Frontmatter:**

```yaml
---
name: install-stoa
description: Guided walkthrough of installing The Stoa substrate onto a target project (or user-tier, or sub-project tier). Wraps substrate/install.sh with a question-driven dialog and dry-run-first discipline.
---
```

**Required procedure beats (in order):**

1. **Pre-flight check** — verify `bw` (beadwork) is installed and on PATH (`bw --version`). If not, surface clear next steps for the user to install bw first.
2. **Verify git working tree clean** (if installing into an existing project). Warn if dirty; allow user to proceed if they choose.
3. **Ask: what tier?** — read `substrate/install.sh --help` so descriptions match the actual installer. Three tiers: user (`~/.claude/`), project (`<project>/.claude/`), sub-project (recursive case under existing Stoa-installed project; per Arc 14).
4. **Ask: target path** (project / sub-project tiers only). Verify path exists and is a git repo.
5. **Ask: `--modify-claude-md`?** — explain what it does ("writes a CLAUDE.md at the project root pointing at the installed substrate"). Recommend yes; require explicit consent per `templates/consent-prompts.md`.
6. **Dry-run first** — always run with `--dry-run` before committing. Show the user what would be created. Get explicit consent to drop `--dry-run` and re-run.
7. **After install — verify** — files exist at expected paths, sha256 of new CLAUDE.md (provenance), suggest opening Claude Code in deployed-to dir and invoking POLYBIUS.
8. **Optional smoke test** — walk through opening Claude Code in the deployed-to dir, invoking POLYBIUS, verifying the role file loads cleanly.

**What the skill must NOT do:**
- Run install without `--dry-run` first
- Run with `--modify-claude-md` without explicit consent
- Proceed if `bw` isn't installed (direct user to install bw first)
- Try to install bw itself (out of scope; bw lives in a separate repo)
- Modify the user's git config or any system files
- Skip the dry-run beat even if the user asks ("just do it" doesn't override the discipline)

Length target: ~200-350 lines.

---

## Phase B — Smoke test

After all 5 deliverables are in place, run a smoke test before committing:

1. **Frontmatter validity:** parse the YAML frontmatter on `SKILL.md`, `skills/stoa-intro/SKILL.md`, `skills/install-stoa/SKILL.md`. Each must have a valid `name` and `description`. (Use `python -c` with PyYAML or similar; or just visually verify the `---` blocks are well-formed.)
2. **Cross-references resolve:** every path mentioned in skill bodies must exist in the repo. Quick check: extract markdown links + bare-quoted paths and verify each. Specifically:
   - `docs/case-study/case-study.md` ✓
   - `docs/case-study/kg-spec.md` ✓
   - `design/Stoa_architecture/Stoa Architecture KG _standalone_.html` ✓
   - `substrate/install.sh` ✓
   - `substrate/ONBOARDING.md` ✓
   - `substrate/templates/consent-prompts.md` ✓
   - `LICENSE` ✓
3. **README still renders:** opening `README.md` on GitHub or in a markdown preview should show the new "Getting started" section above the existing "What this is" section. No broken markdown.
4. **CLAUDE.md syntax check:** valid markdown, web-search rule verbatim at top, links resolve.
5. **Author attribution:** any author/copyright/maintainer field touched in this arc must say Denson Smith. The LICENSE already does (verify).

If smoke fails on any beat, surface to POLYBIUS via `bw comment <ticket-id> "smoke fail: <which beat> — <details>"` and wait for guidance.

---

## Phase C — Ship

Clean PASS → autonomous ship per u--7yg.11. Otherwise surface back to POLYBIUS via the bw ticket.

**Commit message shape:**

```
Arc 19: distribution-readiness entry-point skills

Adds the cold-clone entry point: a root SKILL.md (the "about" skill)
that any agent finds when the user opens the freshly-cloned repo, plus
two downstream skills (`/stoa-intro` for the visual Chrome-MCP tour,
`/install-stoa` for the guided substrate install). README updated with
a "Getting started" section pointing at the SKILL.md flow. License
moved from "private; not for distribution" to MIT (LICENSE file at root).

Closes stoa--<ticket-id>.
```

Push to origin/main on clean PASS. The arc directive itself (`substrate/arcs/arc-19-build-directive.md`) was committed by POLYBIUS before dispatch — don't include it in your commit.

---

## Out of scope

- Touching the Stoa app at `app/`. Per A5, the in-app port of case study + KG is deprioritized.
- Touching the substrate role files (MAJOR_POLYBIUS.md, MAJOR_PLINY.md, CAPTAIN_*.md). Arc 19 is repo-distribution surface only.
- Modifying the case study or KG spec. Both are reference material — final.
- Modifying `bw`, the standalone HTML, or the Claude Design bundles. Frozen inputs.
- Cross-repo work (user-beadwork, agent-gauntlet). All work in the-stoa.

---

## Surface back when done

`bw comment <ticket-id> "Arc 19 shipped at commit <sha>, pushed to origin/main. Smoke test passed: <brief summary of beats>. Files added: <list>. Files modified: <list>."`

Then close the ticket: `bw close <ticket-id>`.
