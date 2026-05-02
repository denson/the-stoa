# Data samples

Real data shapes from agent-team-team's `definitions/` tree. Use these to ground the prototype in concrete content instead of lorem-ipsum.

The app's job is to read, display, edit, and write back this data shape.

## File layout

```
data-samples/
├── team.json                    canonical roster + work-class adjustments
├── officers/<NAME>.json         per-officer structural metadata (5 samples)
├── skills/<name>.json           per-skill metadata (4 samples)
├── meta-aspects/<name>.json     per-meta-aspect metadata (3 samples)
└── bodies/<name>.md             natural-language body content (4 samples)
```

## What each looks like

**Officer JSON** (`officers/MAJOR_PLINY.json`) — structural metadata. The `body_path` field references a markdown file with the natural-language voice.

```json
{
  "name": "MAJOR_PLINY",
  "archetype": "orchestrator-archetype",
  "rank": "major",
  "nickname": "Pliny",
  "role_summary": "Session A spec keeper; conversational with the Colonel; orchestrates project-level work via the team in Session B.",
  "body_path": "definitions/bodies/major-pliny.md",
  "tools": ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "Agent", "TodoWrite", "WebSearch", "WebFetch"],
  "callable_lieutenants": [],
  "required_reading": [],
  "consult_on_demand": [],
  "model_tier": "opus"
}
```

**Skill JSON** (`skills/runner.json`) — Anthropic Skills format compatible.

```json
{
  "name": "runner",
  "description": "Tool-mediated probe execution. Invoked at design time + verify time to run a §4 probe...",
  "kind": "skill",
  "callable_by": [],
  "body_path": "definitions/bodies/skill-runner.md"
}
```

**Meta-aspect JSON** — team-wide convention every officer reads.

```json
{
  "name": "envelope-lifecycle",
  "title": "Three-layer model + envelope-gap rule",
  "summary": "...",
  "audience": ["all"],
  "body_path": "definitions/bodies/meta-envelope-lifecycle.md"
}
```

**Body markdown** (`bodies/major-pliny.md`) — long-form natural-language content; the actual "agent voice" / system prompt content. Renders as documentation when shown to the user.

**Team JSON** (`team.json`) — the catalog. Has named rosters (`default`, `minimal`, `user-level`) and `work_class_adjustments`. The full roster has 12 officers; what's in samples here is a subset for design purposes.

## Full canonical roster (for reference)

The 12-officer canonical roster in production:

| Name | Archetype | Rank | Role |
|---|---|---|---|
| MAJOR_PLINY | orchestrator-archetype | major | Session A spec keeper |
| NESTOR | orchestrator-archetype | captain | Session B dispatcher |
| CAPTAIN_PLINY | orchestrator-archetype | captain | Embedded spec checker |
| DAEDALUS | architect-archetype | captain | Designs |
| ARGUS | plan-critic-archetype | captain | Critiques plans |
| STRABO | researcher-archetype | captain | Web research |
| ADA | executor-archetype | captain | Builds |
| VERA | verifier-archetype | captain | Verifies |
| CATO | reviewer-archetype | captain | Reviews diffs |
| CURATOR | curator-archetype | captain | Cross-ticket synthesis |
| HERALD | intake-archetype | lieutenant | Intake routing |
| SCOUT | scout-archetype | lieutenant | Codebase recon |

15 skills (lieutenants) ride along: runner, format-validate, cite-check, pulse-review, dispatch-lieutenant, copy-artifact, transcribe-bw-to-disk, save-verdict, edit-json, team-status, spawn-pair-programmer, arc-management, 1password-secrets, tier2-project-onboarding, tier2-task-routing.

7 meta-aspects: envelope-lifecycle, inter-agent-comms, fix-now-discipline, pliny-dispatch-economy, design-time-tool-validation, discipline-catalog, pair-programmer-disciplines.

## What the samples are missing (for prototype purposes)

Many fields like `callable_lieutenants`, `required_reading`, `consult_on_demand` are empty arrays in these samples — they'd be populated in the full system based on body content analysis. For the design prototype, treat these as scoped fields the user can configure when authoring an officer.

The "fully populated" design state would have officers with rich callable_lieutenants lists (e.g., MAJOR_PLINY callable_lieutenants might list `dispatch-lieutenant`, `team-status`, `pulse-review`, `tier2-task-routing`).
