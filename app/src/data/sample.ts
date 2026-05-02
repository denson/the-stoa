import type { StoaData } from "./types";

// Inline sample data — mirrors the design handoff bundle's data.jsx shape.
// v0.2 will replace this with a fetch from /data.json (built from
// agent-team-team's definitions/ tree by a build-time script).

export const SAMPLE_DATA: StoaData = {
  officers: [
    {
      name: "MAJOR_PLINY", rank: "major", archetype: "orchestrator", nickname: "Pliny",
      role: "Session A spec keeper; conversational with the Colonel; orchestrates project-level work via the team in Session B.",
      tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "Agent", "TodoWrite", "WebSearch", "WebFetch"],
      lieutenants: ["dispatch-lieutenant", "team-status", "pulse-review", "tier2-task-routing"],
      reading: ["envelope-lifecycle", "inter-agent-comms", "fix-now-discipline"],
      tier: "opus",
    },
    {
      name: "NESTOR", rank: "captain", archetype: "orchestrator", nickname: "Nestor",
      role: "Session B dispatcher; runs the build pipeline against PLINY's spec.",
      tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "Agent", "TodoWrite"],
      lieutenants: ["dispatch-lieutenant", "format-validate"],
      reading: ["envelope-lifecycle", "inter-agent-comms"],
      tier: "opus",
    },
    {
      name: "CAPTAIN_PLINY", rank: "captain", archetype: "orchestrator", nickname: "Pliny",
      role: "Embedded spec checker; the spec-mechanical gate inside Session B.",
      tools: ["Read", "Write", "Edit", "Grep", "TodoWrite"],
      lieutenants: [],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "DAEDALUS", rank: "captain", archetype: "architect", nickname: "Daedalus",
      role: "Architect; writes design.md from briefs + research.",
      tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "TodoWrite", "WebSearch", "WebFetch"],
      lieutenants: ["runner", "format-validate", "scout"],
      reading: ["envelope-lifecycle", "inter-agent-comms"],
      tier: "opus",
    },
    {
      name: "ARGUS", rank: "captain", archetype: "plan-critic", nickname: "Argus",
      role: "Plan critic; names risks in DAEDALUS's design without proposing fixes.",
      tools: ["Read", "Grep", "Glob", "TodoWrite"],
      lieutenants: ["runner"],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "STRABO", rank: "captain", archetype: "researcher", nickname: "Strabo",
      role: "Researcher; produces research artifacts to inform design.",
      tools: ["Read", "WebSearch", "WebFetch", "Write", "TodoWrite"],
      lieutenants: [],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "ADA", rank: "captain", archetype: "executor", nickname: "Ada",
      role: "Builder; implements design artifacts as code on a feature branch.",
      tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "TodoWrite"],
      lieutenants: ["runner", "format-validate"],
      reading: ["envelope-lifecycle", "fix-now-discipline"],
      tier: "opus",
    },
    {
      name: "VERA", rank: "captain", archetype: "verifier", nickname: "Vera",
      role: "Verifier; designs verification strategy, runs probes, returns falsification verdict.",
      tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "TodoWrite", "WebSearch", "WebFetch"],
      lieutenants: ["runner", "format-validate"],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "CATO", rank: "captain", archetype: "reviewer", nickname: "Cato",
      role: "Reviewer; audits diffs for craft, safety, and regressions.",
      tools: ["Read", "Grep", "Glob", "TodoWrite"],
      lieutenants: [],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "CURATOR", rank: "captain", archetype: "curator", nickname: "Curator",
      role: "Cross-ticket synthesis; maintains the team's institutional memory.",
      tools: ["Read", "Write", "Grep", "Glob", "TodoWrite"],
      lieutenants: [],
      reading: ["envelope-lifecycle"],
      tier: "opus",
    },
    {
      name: "HERALD", rank: "lieutenant", archetype: "intake", nickname: "Herald",
      role: "Intake lieutenant; turns Colonel requests into structured briefs + bw tickets.",
      tools: ["Bash", "Read", "Write", "Grep", "Glob", "TodoWrite"],
      lieutenants: [],
      reading: [],
      tier: "opus",
    },
    {
      name: "SCOUT", rank: "lieutenant", archetype: "scout", nickname: "Scout",
      role: "Codebase recon lieutenant; focused searches when an officer needs repo-local facts.",
      tools: ["Bash", "Read", "Grep", "Glob", "TodoWrite"],
      lieutenants: [],
      reading: [],
      tier: "opus",
    },
  ],
  skills: [
    { name: "runner", kind: "skill", description: "Tool-mediated probe execution. Invoked at design time + verify time to run a §4 probe against the actual tool. Returns a structured pass/fail record with output captured.", callable_by: ["DAEDALUS", "ARGUS", "VERA"] },
    { name: "dispatch-lieutenant", kind: "skill", description: "The dispatcher protocol. Officers post a request bead; PLINY runs the lieutenant; the artifact is read on the next wake.", callable_by: [] },
    { name: "format-validate", kind: "skill", description: "Schema-conformance check on structured artifacts (frontmatter markdown, JSON, YAML).", callable_by: ["DAEDALUS", "ADA", "VERA"] },
    { name: "tier2-project-onboarding", kind: "skill", description: "First-session onboarding routine for a freshly-deployed project team. Three phases: project survey, DAEDALUS inventory, Colonel review.", callable_by: ["MAJOR_PLINY"] },
    { name: "1password-secrets", kind: "skill", description: "Reference template for handling project secrets via the 1Password CLI. Vault-backed pattern: secrets live in a managed vault, never on disk.", callable_by: [] },
    { name: "team-status", kind: "skill", description: "Cross-ticket status report; what is the team doing right now, what's blocked, what's ready.", callable_by: ["MAJOR_PLINY"] },
    { name: "pulse-review", kind: "skill", description: "Mid-flight check on an in-progress ticket; returns a short health verdict.", callable_by: ["MAJOR_PLINY"] },
    { name: "scout", kind: "subagent", description: "Repo-local reconnaissance; returns file:line citations for a focused query.", callable_by: ["DAEDALUS", "ADA", "VERA", "CATO"] },
    { name: "edit-json", kind: "skill", description: "Path-anchored JSON mutation by RFC-6901 pointer.", callable_by: ["DAEDALUS", "ADA"] },
    { name: "save-verdict", kind: "skill", description: "Writes a structured verdict bead onto the ticket after a gate.", callable_by: ["VERA", "CATO", "ARGUS"] },
  ],
  metaAspects: [
    { name: "envelope-lifecycle", title: "Three-layer model + envelope-gap rule", summary: "Envelope/letter/skill three-layer model. The envelope-gap rule: return a gap flag rather than improvising." },
    { name: "inter-agent-comms", title: "bw beadwork as message bus", summary: "How agents communicate: durable message bus, async re-check at gates, three-channel rules." },
    { name: "fix-now-discipline", title: "The universal fix-now rule", summary: "Per-role duty split, the handwave detector, the preservation discipline." },
    { name: "discipline-catalog", title: "Canonical T/P/X/M discipline index", summary: "T = team-internal, P = pair-programmer, X = cross-cutting, M = meta-install." },
  ],
  archetypes: {
    orchestrator: "#5B4D86",
    architect: "#2E6E63",
    verifier: "#785637",
    executor: "#4A6E2E",
    reviewer: "#6E2E4A",
    "plan-critic": "#6E4A2E",
    researcher: "#2E4A6E",
    curator: "#4A2E6E",
    intake: "#6E6E2E",
    scout: "#2E6E4A",
  },
  bodyPreview: `# {{OFFICER_NAME}} — the architect

You are {{OFFICER_NAME}}, the architect on the gauntlet team. You take a design brief from PLINY, consume the researcher's artifact as input, write a concrete design artifact to disk, flag your own self-assessed weak points for the plan-critic to catch, and return a structured verdict to PLINY.

**Writes plans, not code.** This property is load-bearing. Your output is an artifact on disk, not a change on a feature branch.

## Required reading at session start

1. \`CLAUDE.md\` — the workspace conventions
2. \`agents/aspects/_meta/envelope-lifecycle.md\` — three-layer model
3. \`agents/aspects/_meta/inter-agent-comms.md\` — bw as the message bus
4. \`agents/aspects/_meta/fix-now-discipline.md\` — the universal fix-now rule

## Restatement gate (pre-work, load-bearing)

Before designing, restate the brief's problem in your own words. If the restatement diverges from the brief, return an envelope-gap flag rather than designing against the ambiguity.`,
};
