// Non-v2 display data for The Stoa — skills and meta-aspects.
//
// v2 (planning §11) only models the rank ladder + agents + the human
// PRINCIPAL. Skills and meta-aspects are pre-v2 display concerns that
// didn't graduate into the v2 schema. They live here until their own
// v2 modeling arc lands (LIEUTENANT data is Arc 13 territory; meta-
// aspects probably later).

export interface Skill {
  name: string;
  kind: "skill" | "subagent" | "script" | "module";
  description: string;
  callable_by: string[];
}

export interface MetaAspect {
  name: string;
  title: string;
  summary: string;
}

export const skills: Skill[] = [
  {
    name: "runner",
    kind: "skill",
    description:
      "Tool-mediated probe execution. Invoked at design time + verify time to run a §4 probe against the actual tool. Returns a structured pass/fail record with output captured.",
    callable_by: ["DAEDALUS", "ARGUS", "VERA"],
  },
  {
    name: "dispatch-lieutenant",
    kind: "skill",
    description:
      "The dispatcher protocol. Agents post a request bead; PLINY runs the lieutenant; the artifact is read on the next wake.",
    callable_by: [],
  },
  {
    name: "format-validate",
    kind: "skill",
    description:
      "Schema-conformance check on structured artifacts (frontmatter markdown, JSON, YAML).",
    callable_by: ["DAEDALUS", "ADA", "VERA"],
  },
  {
    name: "tier2-project-onboarding",
    kind: "skill",
    description:
      "First-session onboarding routine for a freshly-deployed project team. Three phases: project survey, DAEDALUS inventory, PRINCIPAL review.",
    callable_by: ["MAJOR_PLINY"],
  },
  {
    name: "1password-secrets",
    kind: "skill",
    description:
      "Reference template for handling project secrets via the 1Password CLI. Vault-backed pattern: secrets live in a managed vault, never on disk.",
    callable_by: [],
  },
  {
    name: "team-status",
    kind: "skill",
    description:
      "Cross-ticket status report; what is the team doing right now, what's blocked, what's ready.",
    callable_by: ["MAJOR_PLINY"],
  },
  {
    name: "pulse-review",
    kind: "skill",
    description:
      "Mid-flight check on an in-progress ticket; returns a short health verdict.",
    callable_by: ["MAJOR_PLINY"],
  },
  {
    name: "scout",
    kind: "subagent",
    description:
      "Repo-local reconnaissance; returns file:line citations for a focused query.",
    callable_by: ["DAEDALUS", "ADA", "VERA", "CATO"],
  },
  {
    name: "edit-json",
    kind: "skill",
    description: "Path-anchored JSON mutation by RFC-6901 pointer.",
    callable_by: ["DAEDALUS", "ADA"],
  },
  {
    name: "save-verdict",
    kind: "module",
    description:
      "Bash-only verdict-write module (printf author + sha256 + bw-attach)",
    callable_by: ["VERA", "CATO", "ARGUS"],
  },
];

export const metaAspects: MetaAspect[] = [
  {
    name: "envelope-lifecycle",
    title: "Three-layer model + envelope-gap rule",
    summary:
      "Envelope/letter/skill three-layer model. The envelope-gap rule: return a gap flag rather than improvising.",
  },
  {
    name: "inter-agent-comms",
    title: "bw beadwork as message bus",
    summary:
      "How agents communicate: durable message bus, async re-check at gates, three-channel rules.",
  },
  {
    name: "fix-now-discipline",
    title: "The universal fix-now rule",
    summary:
      "Per-role duty split, the handwave detector, the preservation discipline.",
  },
  {
    name: "discipline-catalog",
    title: "Canonical T/P/X/M discipline index",
    summary:
      "T = team-internal, P = pair-programmer, X = cross-cutting, M = meta-install.",
  },
];

