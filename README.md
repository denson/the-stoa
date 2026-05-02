# agent-substrate

The deployable substrate for the three-role recursive agent architecture. Contains the role files (`POLYBIUS.md`, `MAJOR_PLINY.md`), the install script, and supporting deliverables that get deployed to user-tier and project-tier directories.

**Author:** Denson Smith.

## What this repo is

This is the *source of truth for the deployable*. The architecture spec — what gets deployed and why — lives in:

- **Architecture spec:** [user-beadwork/plans/three-role-recursive-architecture.md](https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md)
- **Design inputs:** [user-beadwork epic u--7yg](https://github.com/denson/user-beadwork/blob/beadwork/issues/u--7yg.json) and its children (the empirical observations + disciplines that produced the architecture)

This repo is not the spec. It is the implementation of the spec.

## What gets deployed

When a user runs the install script, this repo's contents get distributed to the appropriate tier:

- **`POLYBIUS.md`** — Chief-of-Staff role file. The seat that converses with humans, holds durable memory via beadwork, writes instructions for the orchestrator.
- **`MAJOR_PLINY.md`** — Orchestrator role file. The seat that runs the team via Agent-tool dispatch.
- **`install.sh`** — Template install script. POLYBIUS customizes the actual run-time install per user feedback.
- **Supporting files** — anything else POLYBIUS or MAJOR_PLINY needs at runtime (skills, templates, default configs).

## Status

**Arc 1 in progress.** Per the planning doc §12, work is broken into five small incremental arcs:

- **Arc 1 (current):** Core deployable — `POLYBIUS.md` + `MAJOR_PLINY.md` + minimal `install.sh`
- Arc 2: POLYBIUS's interactive onboarding flow
- Arc 3: Refactor existing wrong-shape deploys in `agent-team-team` and `agent-character-builder`
- Arc 4: Sub-project spawning mechanism
- Arc 5: Officer rename sweep (CAPTAIN_* prefix consistency)

Each arc is small enough to ship cleanly. See planning doc §12 for sequencing rationale.

## Repo conventions

- `main` branch: stable deliverables ready to deploy
- `beadwork` branch: per-arc journey tickets (will be initialized when Arc 1 build session opens)
- Each Arc files its own ticket chain in this repo's beadwork
- Cross-references to user-beadwork by ticket ID (e.g., `u--7yg.13`) for design-input lookups

## Why a separate repo

Earlier iterations mixed deployable artifacts with substrate definitions, planning docs, and journey tickets in `agent-team-team`. Separating them clarifies which artifacts are deployable (here) versus which are just the team that builds them (`agent-team-team`) versus which capture the user-tier journey (`user-beadwork`).
