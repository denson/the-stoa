# substrate

> **Note:** This was the standalone `agent-substrate` repo. As of 2026-05-02 (Arc Z) it lives as the `substrate/` subtree of [the-stoa](https://github.com/denson/the-stoa). See the [top-level README](../README.md) for the unified-repo overview. The content below describes the deployable itself and is otherwise unchanged.

---

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
- **`.claude/.gitignore`** — a canonical, idempotent ignore file the installer writes into the target's `.claude/` so a consumer's `git status` is not polluted by the transient runtime state the substrate generates there (Arc 55 / stoa--2i5). The transient paths it ignores (relative to `.claude/`) are: `scheduled_tasks.lock` (cron lock), `worktrees/` (per-arc-build worktree residue), `.substrate-last-check` (check-substrate-updates state), and `__pycache__/` + `*.pyc` (skill bytecode regenerated at consumer runtime). It is rewritten verbatim on every run (full-overwrite idempotent) and honors `--dry-run`. The `.substrate-manifest` deploy artifact is deliberately NOT ignored — it is read by the check-substrate-updates tooling and is meant to stay visible.

## Status

**Arc 7 landed — `install.sh` improvements.** The deployable now ships templates alongside role files (`templates/*.md` → `<target>/.claude/templates/`), prints next-step guidance after a successful install (so the human isn't left staring at a "done" line wondering how to activate), documents Windows-bash portability for PowerShell users, and retires the last reflexive "Colonel" reference from the install script (resolves `as--meq`). Combined with Arcs 4–6 (substrate redesign from v2), the substrate is now both v2-aligned in voice and end-to-end deployable: role files + 10 CAPTAIN envelopes + 3 runtime templates land in one mechanical step, and the human gets clear pointers for what to do next. v1 versions of all re-authored files remain preserved at [`v1-historical/`](./v1-historical/) for reference.

Deliverables on `main`:

- [`MAJOR_POLYBIUS.md`](./MAJOR_POLYBIUS.md) — Chief-of-Staff role file (re-authored Arc 4 against v2; supersedes [Arc 1 + Arc 2 v1 version](./v1-historical/MAJOR_POLYBIUS.md))
- [`MAJOR_PLINY.md`](./MAJOR_PLINY.md) — Orchestrator role file (re-authored Arc 4 against v2; supersedes [Arc 1 v1 version](./v1-historical/MAJOR_PLINY.md))
- [`install.sh`](./install.sh) — template installer (Arc 1; extended in Arc 3 to deploy CAPTAIN envelopes via `{{NAME_SUFFIX}}` substitution; extended again in Arc 7 to deploy `templates/`, print next-step guidance, document Windows portability, and retire residual v1 voice)
- [`templates/paste-instruction-template.md`](./templates/paste-instruction-template.md) — MAJOR_PLINY activation template (re-authored Arc 6 against v2; supersedes [Arc 2 v1 version](./v1-historical/templates/paste-instruction-template.md); string-substitution mechanism settled in spec §8)
- [`templates/onboarding-questions.md`](./templates/onboarding-questions.md) — interview floor + rationale (re-authored Arc 6 against v2; supersedes [Arc 2 v1 version](./v1-historical/templates/onboarding-questions.md))
- [`templates/consent-prompts.md`](./templates/consent-prompts.md) — wording for sensitive-action consent (re-authored Arc 6 against v2; supersedes [Arc 2 v1 version](./v1-historical/templates/consent-prompts.md))
- [`ONBOARDING.md`](./ONBOARDING.md) — end-to-end narrative walkthrough across four scenarios (re-authored Arc 6 against v2; supersedes [Arc 2 v1 version](./v1-historical/ONBOARDING.md))
- The 10 CAPTAIN envelopes (re-authored Arc 5 against v2; supersedes Arc 3 v1 versions preserved at [`v1-historical/CAPTAIN_*.md`](./v1-historical/)) — see roster below

The post-v2 arc sequence (per architecture spec §14):

- **Arc 1 (done, v1):** Core deployable — `MAJOR_POLYBIUS.md` + `MAJOR_PLINY.md` + minimal `install.sh`
- **Arc 2 (done, v1):** POLYBIUS's interactive onboarding flow + templates + walkthrough
- **Arc 3 (done, v1):** 10 CAPTAIN envelopes + `install.sh` extension to deploy them
- **Arc 4 (done, v2):** Re-author `MAJOR_POLYBIUS.md` + `MAJOR_PLINY.md` from v2 spec; PRINCIPAL/HUMAN voice throughout
- **Arc 5 (done, v2):** Re-author the 10 CAPTAIN envelopes from v2 spec; rank-table headers, spec-authority pointers, PRINCIPAL/HUMAN voice grounded throughout; structural tool restrictions per spec §9 (ARGUS / CATO no `Write`/`Edit`; BARTLEBY / HERALD / CAPTAIN_ZENO no `WebSearch`/`WebFetch`; CAPTAIN_ZENO also no `Write`/`Edit`)
- **Arc 6 (done, v2):** Re-author `ONBOARDING.md` + 3 `templates/*.md` files from v2 spec; PRINCIPAL/HUMAN voice grounded throughout including dialogue; substitution slots and consent-prompt structure preserved; v1 versions archived under `v1-historical/`. Substrate-redesign-from-v2 (Arcs 4–6) complete.
- **Arc 7 (done):** `install.sh` improvements — `templates/` deployment alongside role files (default on; `--no-templates` opts out), next-step guidance printed on successful install (suppressed in `--dry-run`), Windows-bash portability documented in this README, and the residual `Colonel` reference at install.sh:17 retired (resolves `as--meq`).
- (next) **Arc 8:** Refactor existing wrong-shape deploys in `agent-team-team` and `agent-character-builder`
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
| [`CAPTAIN_ZENO.md`](./CAPTAIN_ZENO.md) | ZENO | SPEC-CHECKER | embedded mechanical spec-vs-result check | no `Write`/`Edit`, no `WebSearch`/`WebFetch` |

Note on naming: CAPTAIN_ZENO is the embedded spec-checker (this seat was renamed from CAPTAIN_PLINY in Arc 16 to eliminate the role-collapse trap from sharing a mnemonic with MAJOR_PLINY). NESTOR (the would-be sub-agent dispatcher in earlier designs) does not appear; the role moves to MAJOR_PLINY at the top-level session tier (sub-agents cannot dispatch sub-agents — `u--7yg.12`).

`install.sh` deploys these envelopes at install time:

- At project-tier: `<project>/.claude/agents/CAPTAIN_<MNEMONIC>_<sanitized-project>.md`, with the `name:` field's `{{NAME_SUFFIX}}` slot substituted with `_<sanitized-project>`.
- At user-tier: `~/.claude/agents/CAPTAIN_<MNEMONIC>.md`, with `{{NAME_SUFFIX}}` substituted with empty string.
- `--no-captains` skips deployment (POLYBIUS may want to deploy CAPTAINs interactively in some onboarding flows).

It also deploys POLYBIUS's runtime templates:

- The three files under [`templates/`](./templates/) (`paste-instruction-template.md`, `onboarding-questions.md`, `consent-prompts.md`) land at `<target>/.claude/templates/<filename>`. Unsuffixed at both tiers — they are shared tooling, not agent-shaped.
- `--no-templates` skips this step (default: deploy).

## Testing the install

`install.sh` is the template POLYBIUS customizes per session at deploy time; it does only the non-conversational mechanical deploy. To exercise it manually on a throwaway directory before any real install:

```bash
# 1. Show usage (includes --no-captains, --no-templates, --modify-claude-md, --dry-run)
./install.sh --help

# 2. Dry-run against a throwaway project directory (no writes; suppresses
#    next-step guidance because nothing was actually deployed)
TMP=$(mktemp -d)
./install.sh --target project --project-dir "$TMP" --modify-claude-md --dry-run

# 3. Real install into the throwaway directory; prints next-step guidance
#    after the "done" line.
./install.sh --target project --project-dir "$TMP" --modify-claude-md
ls "$TMP/.claude/"           # MAJOR_POLYBIUS.md, MAJOR_PLINY.md, agents/, templates/
ls "$TMP/.claude/agents/"    # 10 CAPTAIN_*_<slug>.md files
ls "$TMP/.claude/templates/" # paste-instruction-template.md, onboarding-questions.md, consent-prompts.md
cat "$TMP/CLAUDE.md"         # POLYBIUS reference appended

# 4. Verify CAPTAIN frontmatter substitution worked
head -3 "$TMP/.claude/agents/CAPTAIN_DAEDALUS_$(basename $TMP | tr '.-' '__').md"
# expected: name: CAPTAIN_DAEDALUS_<slug>

# 5. Idempotency check — running again is a no-op for the CLAUDE.md append,
#    re-overwrites templates/agents in place (no duplicates), still prints
#    next-step guidance.
./install.sh --target project --project-dir "$TMP" --modify-claude-md
cat "$TMP/CLAUDE.md"               # unchanged (marker check skipped the append)
ls "$TMP/.claude/agents/" | wc -l  # still 10
ls "$TMP/.claude/templates/" | wc -l  # still 3

# 6. Skip CAPTAIN deployment if needed
./install.sh --target project --project-dir "$TMP" --no-captains --dry-run

# 7. Skip templates deployment if needed
./install.sh --target project --project-dir "$TMP" --no-templates --dry-run

# 8. Clean up
rm -rf "$TMP"
```

User-tier installs target `~/.claude/` and deploy CAPTAINs as `CAPTAIN_*.md` (unsuffixed) and templates as `~/.claude/templates/<filename>`. The `--modify-claude-md` flag is opt-in; without it, the script drops the role files but leaves `CLAUDE.md` untouched. The `--no-captains` and `--no-templates` flags opt out of those respective steps.

### Windows-bash portability

`install.sh` is a Bash script. On Windows, run it from a real Bash environment — Git Bash works out of the box. Two ways to invoke it:

**Git Bash (recommended).** Open Git Bash, `cd` to the repo, and run as on any Unix shell:

```bash
./install.sh --target project --project-dir "$(pwd)" --modify-claude-md
```

**PowerShell.** PowerShell's bare `bash` may resolve to the WSL relay, which fails when no WSL distro is installed. Invoke Git Bash explicitly to bypass that path:

```powershell
& "C:\Program Files\Git\bin\bash.exe" install.sh --target project --project-dir "$PWD" --modify-claude-md
```

Both invocations produce identical results — the script is the same; only the shell that hosts it differs.

## Repo conventions

- `main` branch: stable deliverables ready to deploy
- `beadwork` branch: per-arc journey tickets (initialized in Arc 1 with `bw init --prefix as-`)
- Each Arc files its own ticket chain in this repo's beadwork
- Cross-references to user-beadwork by ticket ID (e.g., `u--7yg.13`) for design-input lookups

## Why a separate repo

Earlier iterations mixed deployable artifacts with substrate definitions, planning docs, and journey tickets in `agent-team-team`. Separating them clarifies which artifacts are deployable (here) versus which are just the team that builds them (`agent-team-team`) versus which capture the user-tier journey (`user-beadwork`).
