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

**Arc 5 landed.** The 10 CAPTAIN envelopes have been re-authored against the v2 architecture spec, completing the substrate's voice-grounding pass. Combined with Arc 4 (which re-authored the MAJOR role files), the entire deployable substrate now uses **PRINCIPAL** for the human's descriptive role and reserves **COLONEL** for a future high-autonomy agent rank — the terminology debt v1 carried (using "Colonel" as the human's title) is fully retired. The empirical signal that motivated v2 is captured in user-beadwork `u--7yg.20`. v1 role files are preserved for reference at [`v1-historical/`](./v1-historical/).

Deliverables on `main`:

- [`MAJOR_POLYBIUS.md`](./MAJOR_POLYBIUS.md) — Chief-of-Staff role file (re-authored Arc 4 against v2; supersedes [Arc 1 + Arc 2 v1 version](./v1-historical/MAJOR_POLYBIUS.md))
- [`MAJOR_PLINY.md`](./MAJOR_PLINY.md) — Orchestrator role file (re-authored Arc 4 against v2; supersedes [Arc 1 v1 version](./v1-historical/MAJOR_PLINY.md))
- [`install.sh`](./install.sh) — template installer (Arc 1; extended in Arc 3 to deploy CAPTAIN envelopes via `{{NAME_SUFFIX}}` substitution)
- [`templates/paste-instruction-template.md`](./templates/paste-instruction-template.md) — MAJOR_PLINY activation template (Arc 2; settles spec §10 open question 1 on string-substitution)
- [`templates/onboarding-questions.md`](./templates/onboarding-questions.md) — interview floor + rationale (Arc 2)
- [`templates/consent-prompts.md`](./templates/consent-prompts.md) — wording for sensitive-action consent (Arc 2)
- [`ONBOARDING.md`](./ONBOARDING.md) — end-to-end narrative walkthrough across four scenarios (Arc 2)
- The 10 CAPTAIN envelopes (re-authored Arc 5 against v2; supersedes Arc 3 v1 versions preserved at [`v1-historical/CAPTAIN_*.md`](./v1-historical/)) — see roster below

The post-v2 arc sequence (per architecture spec §14):

- **Arc 1 (done, v1):** Core deployable — `MAJOR_POLYBIUS.md` + `MAJOR_PLINY.md` + minimal `install.sh`
- **Arc 2 (done, v1):** POLYBIUS's interactive onboarding flow + templates + walkthrough
- **Arc 3 (done, v1):** 10 CAPTAIN envelopes + `install.sh` extension to deploy them
- **Arc 4 (done, v2):** Re-author `MAJOR_POLYBIUS.md` + `MAJOR_PLINY.md` from v2 spec; PRINCIPAL/HUMAN voice throughout
- **Arc 5 (done, v2):** Re-author the 10 CAPTAIN envelopes from v2 spec; rank-table headers, spec-authority pointers, PRINCIPAL/HUMAN voice grounded throughout; structural tool restrictions per spec §9 (ARGUS / CATO no `Write`/`Edit`; BARTLEBY / HERALD / CAPTAIN_PLINY no `WebSearch`/`WebFetch`; CAPTAIN_PLINY also no `Write`/`Edit`)
- (next) **Arc 6:** Update Arc directives, ONBOARDING.md, templates/ from v2
- **Arc 7:** `install.sh` improvements (Windows portability, deploy `templates/`, next-step guidance after install)
- **Arc 8:** Refactor existing wrong-shape deploys in `agent-team-team` and `agent-character-builder`
- **Arc 9:** The Stoa data-model + display alignment (in `agent-character-builder`)
- **Arc 10:** Sub-project spawning mechanism

Each arc is small enough to ship cleanly. See architecture spec §14 for full sequencing rationale.

## The 10 CAPTAIN roster

The CAPTAINs are the team MAJOR_PLINY dispatches via the `Agent` tool. Each is a sub-agent envelope at `.claude/agents/`. Each has exactly one job (`u--7yg.17`); merging seats reliably drops jobs.

| File | Mnemonic | Role | What they do | Tool restrictions |
|---|---|---|---|---|
| [`CAPTAIN_DAEDALUS.md`](./CAPTAIN_DAEDALUS.md) | DAEDALUS | ARCHITECT | writes design specs from briefs; flags self-assessed weak points | — |
| [`CAPTAIN_ARGUS.md`](./CAPTAIN_ARGUS.md) | ARGUS | PLAN-CRITIC | cold-audits designs; surfaces load-bearing risks; **does not propose fixes** | no `Write`/`Edit` |
| [`CAPTAIN_ADA.md`](./CAPTAIN_ADA.md) | ADA | EXECUTOR | builds — code, file edits, scripted work; does not self-verify or self-review | — |
| [`CAPTAIN_VERA.md`](./CAPTAIN_VERA.md) | VERA | VERIFIER | designs verification strategy from the design's probes; runs them against the build; returns falsification verdict | — |
| [`CAPTAIN_CATO.md`](./CAPTAIN_CATO.md) | CATO | REVIEWER | cold-reads the diff for craft, hygiene, consistency, security, scope; meta-verifier of VERA | no `Write`/`Edit` |
| [`CAPTAIN_STRABO.md`](./CAPTAIN_STRABO.md) | STRABO | SCOUT | external/web search and research; produces cited research artifact for design input | — |
| [`CAPTAIN_BARTLEBY.md`](./CAPTAIN_BARTLEBY.md) | BARTLEBY | FILE_CLERK | internal repo recon; returns `file:line` citations without interpretation | no `WebSearch`/`WebFetch` |
| [`CAPTAIN_HERALD.md`](./CAPTAIN_HERALD.md) | HERALD | INTAKE | turns a vague request into a structured brief draft with named ambiguities | no `WebSearch`/`WebFetch` |
| [`CAPTAIN_CURATOR.md`](./CAPTAIN_CURATOR.md) | CURATOR | SYNTHESIST | cross-ticket synthesis, retrospectives, plan revisions | — |
| [`CAPTAIN_PLINY.md`](./CAPTAIN_PLINY.md) | PLINY | SPEC-CHECKER | embedded mechanical spec-vs-result check; **distinct from MAJOR_PLINY** orchestrator (different ranks, different jobs) | no `Write`/`Edit`, no `WebSearch`/`WebFetch` |

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
