# the-stoa

The unified repo for the three-role agent substrate and **The Stoa** — the visualization-and-edit web app on top of it. Localhost-only deployment posture.

**Author:** Denson Smith.

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

## Deployment posture

Localhost-only for the foreseeable future. No staging, no production hosting, no auth surface beyond the user's own machine. The unified-repo decision is downstream of this posture: there's no deployment-side cost to colocating the editor with the canonical, and the same-repo relationship makes adapter wiring (Arc 10) trivially relative-path.

## Where work happens

- **Architecture spec + design inputs:** [user-beadwork/plans/three-role-recursive-architecture.md](https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md), and the `u--7yg` epic that captured the empirical signal that produced it
- **Build-arc directives** (the project's own change log): `substrate/arcs/`
- **Beadwork** for in-flight work in this repo: not yet initialized; will be filed against the first arc that operates here (Arc 9, post-consolidation)

## History

`agent-substrate` and `agent-character-builder` were two separate repos that consolidated into this one in Arc Z (2026-05-02). Git history from both was preserved via `git subtree`. The source repos are archived; new work happens here.

## License

Private repo; not licensed for distribution. Authored by Denson Smith.
