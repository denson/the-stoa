# agent-substrate

The deployable substrate for the three-role recursive agent architecture. Contains the role files (`MAJOR_POLYBIUS.md`, `MAJOR_PLINY.md`), the install script, and supporting deliverables that get deployed to user-tier and project-tier directories.

**Author:** Denson Smith.

## What this repo is

This is the *source of truth for the deployable*. The architecture spec — what gets deployed and why — lives in:

- **Architecture spec:** [user-beadwork/plans/three-role-recursive-architecture.md](https://github.com/denson/user-beadwork/blob/main/plans/three-role-recursive-architecture.md)
- **Design inputs:** [user-beadwork epic u--7yg](https://github.com/denson/user-beadwork/blob/beadwork/issues/u--7yg.json) and its children (the empirical observations + disciplines that produced the architecture)

This repo is not the spec. It is the implementation of the spec.

## What gets deployed

When a user runs the install script, this repo's contents get distributed to the appropriate tier:

- **`MAJOR_POLYBIUS.md`** — Chief-of-Staff role file. The seat that converses with humans, holds durable memory via beadwork, writes instructions for the orchestrator. Contains the executable onboarding procedure POLYBIUS runs when first activated.
- **`MAJOR_PLINY.md`** — Orchestrator role file. The seat that runs the team via Agent-tool dispatch.
- **`install.sh`** — Template install script. POLYBIUS customizes the actual run-time install per user feedback.
- **`templates/`** — substitution-slot artifacts POLYBIUS uses during onboarding (paste-instruction template, interview questions, consent prompts).
- **`ONBOARDING.md`** — narrative walkthrough of what onboarding looks like; doubles as a tabletop test harness for fresh POLYBIUS sessions.
- **Supporting files** — anything else POLYBIUS or MAJOR_PLINY needs at runtime (skills, additional templates, default configs).

## Status

**Arc 3 landed.** The 10 CAPTAIN envelopes ship with the substrate; `install.sh` deploys them. Deliverables on `main`:

- [`MAJOR_POLYBIUS.md`](./MAJOR_POLYBIUS.md) — Chief-of-Staff role file (Arc 1; extended in Arc 2 with the executable onboarding procedure in §4)
- [`MAJOR_PLINY.md`](./MAJOR_PLINY.md) — Orchestrator role file (Arc 1)
- [`install.sh`](./install.sh) — template installer (Arc 1; extended in Arc 3 to deploy CAPTAIN envelopes via `{{NAME_SUFFIX}}` substitution)
- [`templates/paste-instruction-template.md`](./templates/paste-instruction-template.md) — MAJOR_PLINY activation template (Arc 2; settles spec §10 open question 1 on string-substitution)
- [`templates/onboarding-questions.md`](./templates/onboarding-questions.md) — interview floor + rationale (Arc 2)
- [`templates/consent-prompts.md`](./templates/consent-prompts.md) — wording for sensitive-action consent (Arc 2)
- [`ONBOARDING.md`](./ONBOARDING.md) — end-to-end narrative walkthrough across four scenarios (Arc 2)
- The 10 CAPTAIN envelopes (Arc 3) — see roster below

Per the planning doc §12, work is broken into small incremental arcs:

- **Arc 1 (done):** Core deployable — `MAJOR_POLYBIUS.md` + `MAJOR_PLINY.md` + minimal `install.sh`
- **Arc 2 (done):** POLYBIUS's interactive onboarding flow + templates + walkthrough
- **Arc 3 (done):** 10 CAPTAIN envelopes + `install.sh` extension to deploy them
- (next) Refactor existing wrong-shape deploys in `agent-team-team` and `agent-character-builder` (was Arc 3 in original §12)
- Sub-project spawning mechanism (was Arc 4)
- Officer body refresh — role-name reassignments and rank prefix consistency in existing project deploys (was Arc 5)

Each arc is small enough to ship cleanly. See planning doc §12 for the original sequencing rationale; arc numbering was revisited after Arc 2 to insert CAPTAIN envelope authoring before the project-deploy refactors.

## The 10 CAPTAIN roster

The CAPTAINs are the team MAJOR_PLINY dispatches via the `Agent` tool. Each is a sub-agent envelope at `.claude/agents/`. Each has exactly one job (`u--7yg.17`); merging seats reliably drops jobs.

| File | Mnemonic | Role | What they do |
|---|---|---|---|
| [`CAPTAIN_DAEDALUS.md`](./CAPTAIN_DAEDALUS.md) | DAEDALUS | ARCHITECT | writes design specs from briefs; flags self-assessed weak points |
| [`CAPTAIN_ARGUS.md`](./CAPTAIN_ARGUS.md) | ARGUS | PLAN-CRITIC | cold-audits designs; surfaces load-bearing risks; **does not propose fixes** (no `Write`/`Edit` tools, structurally) |
| [`CAPTAIN_ADA.md`](./CAPTAIN_ADA.md) | ADA | EXECUTOR | builds — code, file edits, scripted work; does not self-verify or self-review |
| [`CAPTAIN_VERA.md`](./CAPTAIN_VERA.md) | VERA | VERIFIER | designs verification strategy from the design's probes; runs them against the build; returns falsification verdict |
| [`CAPTAIN_CATO.md`](./CAPTAIN_CATO.md) | CATO | REVIEWER | cold-reads the diff for craft, hygiene, consistency, security, scope; meta-verifier of VERA |
| [`CAPTAIN_STRABO.md`](./CAPTAIN_STRABO.md) | STRABO | SCOUT | external/web search and research; produces cited research artifact for design input |
| [`CAPTAIN_BARTLEBY.md`](./CAPTAIN_BARTLEBY.md) | BARTLEBY | FILE-CLERK | internal repo recon; returns `file:line` citations without interpretation |
| [`CAPTAIN_HERALD.md`](./CAPTAIN_HERALD.md) | HERALD | INTAKE | turns a vague request into a structured brief draft with named ambiguities |
| [`CAPTAIN_CURATOR.md`](./CAPTAIN_CURATOR.md) | CURATOR | SYNTHESIST | cross-ticket synthesis, retrospectives, plan revisions |
| [`CAPTAIN_PLINY.md`](./CAPTAIN_PLINY.md) | PLINY | SPEC-CHECKER | embedded mechanical spec-vs-result check; **distinct from MAJOR_PLINY** orchestrator (different ranks, different jobs) |

Note on naming: CAPTAIN_PLINY shares a mnemonic with MAJOR_PLINY by design — the architect spec keeps them as separate seats per the one-job-per-agent discipline. NESTOR (the would-be sub-agent dispatcher in earlier designs) does not appear; the role moves to MAJOR_PLINY at the top-level session tier (sub-agents cannot dispatch sub-agents — `u--7yg.12`).

`install.sh` deploys these envelopes at install time:

- At project-tier: `<project>/.claude/agents/CAPTAIN_<MNEMONIC>_<sanitized-project>.md`, with the `name:` field's `{{NAME_SUFFIX}}` slot substituted with `_<sanitized-project>`.
- At user-tier: `~/.claude/agents/CAPTAIN_<MNEMONIC>.md`, with `{{NAME_SUFFIX}}` substituted with empty string.
- `--no-captains` skips deployment (POLYBIUS may want to deploy CAPTAINs interactively in some onboarding flows).

## Testing the install

`install.sh` is the template POLYBIUS customizes per session at deploy time; it does only the non-conversational mechanical deploy. To exercise it manually on a throwaway directory before any real install:

```bash
# 1. Show usage
./install.sh --help

# 2. Dry-run against a throwaway project directory (no writes)
TMP=$(mktemp -d)
./install.sh --target project --project-dir "$TMP" --modify-claude-md --dry-run

# 3. Real install into the throwaway directory
./install.sh --target project --project-dir "$TMP" --modify-claude-md
ls "$TMP/.claude/"           # MAJOR_POLYBIUS.md, MAJOR_PLINY.md, agents/
ls "$TMP/.claude/agents/"    # 10 CAPTAIN_*_<slug>.md files
cat "$TMP/CLAUDE.md"         # POLYBIUS reference appended

# 4. Verify CAPTAIN frontmatter substitution worked
head -3 "$TMP/.claude/agents/CAPTAIN_DAEDALUS_$(basename $TMP | tr '.-' '__').md"
# expected: name: CAPTAIN_DAEDALUS_<slug>

# 5. Idempotency check — running again is a no-op for the CLAUDE.md append
./install.sh --target project --project-dir "$TMP" --modify-claude-md
cat "$TMP/CLAUDE.md"         # unchanged (marker check skipped the append)
ls "$TMP/.claude/agents/" | wc -l  # still 10

# 6. Skip CAPTAIN deployment if needed
./install.sh --target project --project-dir "$TMP" --no-captains --dry-run

# 7. Clean up
rm -rf "$TMP"
```

User-tier installs target `~/.claude/` and deploy CAPTAINs as `CAPTAIN_*.md` (unsuffixed). The `--modify-claude-md` flag is opt-in; without it, the script drops the role files but leaves `CLAUDE.md` untouched. The `--no-captains` flag opts out of CAPTAIN deployment.

## Repo conventions

- `main` branch: stable deliverables ready to deploy
- `beadwork` branch: per-arc journey tickets (initialized in Arc 1 with `bw init --prefix as-`)
- Each Arc files its own ticket chain in this repo's beadwork
- Cross-references to user-beadwork by ticket ID (e.g., `u--7yg.13`) for design-input lookups

## Why a separate repo

Earlier iterations mixed deployable artifacts with substrate definitions, planning docs, and journey tickets in `agent-team-team`. Separating them clarifies which artifacts are deployable (here) versus which are just the team that builds them (`agent-team-team`) versus which capture the user-tier journey (`user-beadwork`).
