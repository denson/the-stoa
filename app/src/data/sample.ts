// Sample data for The Stoa.
//
// As of Arc 11 this is a thin v2 -> v1 transform shim: the officer roster
// is sourced from `generated/agents.ts` (Arc 10's adapter output, which
// reads canonical role files from `substrate/`) and reshaped to the v1
// types in `./types.ts` that components currently consume.
//
// Skills, meta-aspects, archetype colors, and the body preview remain
// inline because v2 does not yet carry that data; they ride along
// unchanged. (LIEUTENANT data is Arc 13 territory.)
//
// Arc 12 will migrate components to consume v2 types directly, at which
// point this shim shrinks to a re-export — or disappears.
//
// Voice discipline (planning v2 §6, ticket stoa--ggy): the three v1
// "Colonel"-as-human strings that previously lived inline at lines 11,
// 91, and 110 of this file are gone. The two officer-role strings now
// derive from v2 body content (which is v2-voice clean per Arc 10's
// audit); the skill description at v1 line 110 has been rewritten in
// PRINCIPAL terms.

import { stoaData } from "./generated/agents";
import type { Agent } from "./types-v2";
import type { Archetype, Officer, StoaData } from "./types";

// ---------------------------------------------------------------------------
// v2 descriptive role -> v1 archetype
// ---------------------------------------------------------------------------
//
// Most v2 descriptive roles map to a v1 archetype directly. Three v2 roles
// (CHIEF-OF-STAFF, FILE_CLERK, SPEC-CHECKER) postdate the v1 enum and have
// no clean v1 equivalent; they are mapped to the nearest existing archetype
// for color/grouping purposes. Arc 12 should consume v2 types directly and
// retire the v1 archetype enum.
const ARCHETYPE_BY_DESCRIPTIVE_ROLE: Record<string, Archetype> = {
  ORCHESTRATOR: "orchestrator",
  ARCHITECT: "architect",
  "PLAN-CRITIC": "plan-critic",
  EXECUTOR: "executor",
  VERIFIER: "verifier",
  REVIEWER: "reviewer",
  SCOUT: "scout",
  INTAKE: "intake",
  SYNTHESIST: "curator",
  "CHIEF-OF-STAFF": "orchestrator",
  FILE_CLERK: "scout",
  "SPEC-CHECKER": "reviewer",
};

function v1RankFromV2(rank: Agent["rank"]): Officer["rank"] {
  switch (rank) {
    case "MAJOR":
      return "major";
    case "CAPTAIN":
      return "captain";
    case "LIEUTENANT":
      return "lieutenant";
    case "COLONEL":
      throw new Error(
        "COLONEL slot is reserved-empty; an Agent should never carry it.",
      );
  }
}

function nicknameFromMnemonic(mnemonic: string): string {
  return mnemonic.charAt(0) + mnemonic.slice(1).toLowerCase();
}

// Pull the first prose paragraph that follows the role file's header table.
// v1 Officer.role is a one-line description; the natural v2 source would be
// frontmatter `description`, but Agent does not currently carry that field
// (Arc 10 hand-back §1, deferred to Arc 12). The first body paragraph is a
// faithful approximation until then.
function deriveRoleSummary(body: string): string {
  const lines = body.split(/\r?\n/);
  let sawTable = false;
  let inTable = false;
  const paragraph: string[] = [];
  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith("# ")) continue;
    if (line.startsWith("|")) {
      sawTable = true;
      inTable = true;
      continue;
    }
    if (inTable && line === "") {
      inTable = false;
      continue;
    }
    if (!sawTable) continue;
    if (line === "") {
      if (paragraph.length > 0) break;
      continue;
    }
    if (line.startsWith("---") || line.startsWith("##")) {
      if (paragraph.length > 0) break;
      continue;
    }
    paragraph.push(line);
  }
  return paragraph.join(" ");
}

function transformAgent(agent: Agent): Officer {
  const archetype = ARCHETYPE_BY_DESCRIPTIVE_ROLE[agent.descriptiveRole];
  if (!archetype) {
    throw new Error(
      `No v1 archetype mapping for descriptiveRole="${agent.descriptiveRole}" ` +
        `(agent ${agent.filename}). Extend ARCHETYPE_BY_DESCRIPTIVE_ROLE.`,
    );
  }
  return {
    name: agent.filename.replace(/\.md$/, ""),
    rank: v1RankFromV2(agent.rank),
    archetype,
    nickname: nicknameFromMnemonic(agent.mnemonic),
    role: deriveRoleSummary(agent.body),
    tools: agent.tools,
    lieutenants: agent.callableLieutenants ?? [],
    reading: agent.requiredReading ?? [],
    tier: agent.modelTier ?? "opus",
  };
}

const officers: Officer[] = stoaData.roster.flatMap((slot) => {
  if (slot.rank === "HUMAN" || slot.rank === "COLONEL") return [];
  return slot.agents.map(transformAgent);
});

export const SAMPLE_DATA: StoaData = {
  officers,
  skills: [
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
        "The dispatcher protocol. Officers post a request bead; PLINY runs the lieutenant; the artifact is read on the next wake.",
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
      kind: "skill",
      description:
        "Writes a structured verdict bead onto the ticket after a gate.",
      callable_by: ["VERA", "CATO", "ARGUS"],
    },
  ],
  metaAspects: [
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
