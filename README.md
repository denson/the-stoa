# the-stoa

> **The Stoa** is a recursive three-role agent architecture for Claude Code, built on `bw` (beadwork) as durable cross-session substrate.
>
> Three seats, repeated at every tier (user / project / sub-project): a **chief-of-staff** (POLYBIUS) that converses with the human and holds memory across sessions, an **orchestrator** (PLINY) that dispatches the team and reconciles their verdicts, and a team of **specialized sub-agents** (CAPTAINs) each with one focused job — architect, plan-critic, executor, verifier, reviewer, etc. (ten in the current roster). The recursion is the architectural commitment — same shape at every scope, no special-casing.
>
> Two operational modes coexist: a formal multi-stage **gauntlet** for hardening work toward production, and **pair-programming** where the human actively co-drives and collaborates with the agents to get to a prototype worth iterating on. Without the pair-programming mode, the gauntlet would over-engineer drafts — running formal verification, review, and spec-checking on sketches that hadn't yet figured out what they were. Adding pair-programming for the discovery phase is what unlocked token-efficient exploration before the gauntlet's hardening machinery kicks in. Clean PASS ships autonomously — no routing every commit through the human.
>
> MIT-licensed; deployable onto your own work.

### → [Open the interactive knowledge graph](https://denson.github.io/the-stoa/case-study/architecture-kg.html)

The visualization is the fastest way in. Three modes (Pair Programming / Hardening Flow / Recursion); click around. Long-form companion: [`docs/case-study/case-study.md`](docs/case-study/case-study.md).

**Author:** Denson Smith.

## Getting started

Just cloned this and want a guided tour?

1. Open this repo in **Claude Code** (Desktop or CLI both work; Desktop with Chrome MCP unlocks the live-driven visual tour, CLI gets the same narration with a clickable link to the standalone).
2. Ask Claude something like *"what is this?"* — the agent reads `SKILL.md` at the repo root and routes you.
3. Recommended path: visual tour first (`/stoa-intro`), then guided install (`/install-stoa`) if you want to deploy the substrate to one of your projects.

The case study at `docs/case-study/case-study.md` is the deep dive (peer-technical working notebook); the interactive knowledge graph at `docs/case-study/architecture-kg.html` is the visual companion. Both are referenced by the skills above.

## What this is

The architecture that lives here is a recursive three-role agent substrate (HUMAN / MAJOR / CAPTAIN / LIEUTENANT, with the human always at the principal seat). Two pieces sit together in this repo because they are two halves of the same thing:

- **`substrate/`** — the deployable: role files, the install script, supporting templates, and historical artifacts. This is the source of truth for what gets deployed to user-tier and project-tier directories. (Was `agent-substrate`.)
- **`app/`** — **The Stoa**: a React/Vite web app for browsing, composing, and authoring AI agent teams against the canonical substrate. The Stoa is the editor; the substrate is what it edits. Same-repo because the editor-and-canonical relationship is intrinsic, not coordinational. (Was `agent-character-builder`.)

The architecture spec — what gets deployed and why — lives outside this repo at [user-beadwork/plans/three-role-recursive-architecture.md](https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md). This repo is the implementation of that spec.

## Layout

```
the-stoa/
├── README.md                # this file
├── substrate/               # the deployable
│   ├── MAJOR_POLYBIUS.md    # Chief-of-Staff role file
│   ├── MAJOR_PLINY.md       # Orchestrator role file
│   ├── CAPTAIN_*.md         # 10 CAPTAIN envelopes (DAEDALUS, ARGUS, ADA, VERA, CATO, STRABO, BARTLEBY, HERALD, CURATOR, PLINY)
│   ├── templates/           # POLYBIUS's runtime tooling (paste-instruction, onboarding-questions, consent-prompts)
│   ├── install.sh           # mechanical installer
│   ├── ONBOARDING.md        # narrative walkthrough + tabletop test harness
│   ├── arcs/                # build-arc directives (1–9 + Z, the consolidation arc)
│   ├── v1-historical/       # archived v1 role files (reference only)
│   └── README.md            # substrate-internal README
└── app/                     # The Stoa
    ├── src/                 # React/TypeScript source
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    ├── CLAUDE.md            # the deployed POLYBIUS reference for the app project itself
    ├── .claude/             # deployed substrate (gitignored; regenerable via substrate/install.sh)
    └── README.md            # app-internal README
```

## Using the substrate

The installer drops the role files + CAPTAIN envelopes + templates to either user-tier (`~/.claude/`) or project-tier (`<project>/.claude/`).

```bash
# project-tier deploy (also creates a CLAUDE.md reference at the project root):
substrate/install.sh --target project --project-dir <path-to-project> --modify-claude-md

# user-tier deploy (available across all projects):
substrate/install.sh --target user --modify-claude-md

# dry-run (no writes):
substrate/install.sh --target project --project-dir <path-to-project> --modify-claude-md --dry-run

# help:
substrate/install.sh --help
```

After install, the human opens Claude Code in the deployed-to directory and says "POLYBIUS" or "chief of staff" to load the role.

The script resolves its source paths via `BASH_SOURCE`-relative `dirname` — it can be invoked from any working directory.

## Running The Stoa app

```bash
cd app
npm install
npm run dev
```

Open the URL Vite prints (defaults to `http://localhost:5173/`; auto-bumps if the port is busy). v0.1 ships visual browse + officer detail + skill library + ⌘K command palette over an inline sample dataset; subsequent arcs wire it to the canonical substrate above.

A build-time **`gen-data` adapter** (`app/scripts/gen-data.ts`) reads the canonical role files in `substrate/`, validates their frontmatter against a Zod schema, and emits a typed module at `app/src/data/generated/agents.ts`. It runs automatically before `npm run dev` and `npm run build` (`predev` / `prebuild` hooks); regenerate manually with `npm run gen-data`. Override the source path with `AGENT_SUBSTRATE_PATH=<dir>`.

## Deployment posture

Localhost-only for the foreseeable future. No staging, no production hosting, no auth surface beyond the user's own machine. The unified-repo decision is downstream of this posture: there's no deployment-side cost to colocating the editor with the canonical, and the same-repo relationship makes adapter wiring (Arc 10) trivially relative-path.

## Where work happens

- **Architecture spec + design inputs:** [user-beadwork/plans/three-role-recursive-architecture.md](https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md), and the `u--7yg` epic that captured the empirical signal that produced it
- **Build-arc directives** (the project's own change log): `substrate/arcs/`
- **Beadwork** for in-flight work in this repo: not yet initialized; will be filed against the first arc that operates here (Arc 9, post-consolidation)

## History

`agent-substrate` and `agent-character-builder` were two separate repos that consolidated into this one in Arc Z (2026-05-02). Git history from both was preserved via `git subtree`. The source repos are archived; new work happens here.

## License

Licensed under the [MIT License](LICENSE) — see the `LICENSE` file for full text. Authored by Denson Smith, 2026.
