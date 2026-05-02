// Type definitions for The Stoa data model.
// Field names align with the design handoff bundle's data.jsx schema.
//
// NOTE: agent-team-team's actual JSON definitions use slightly different
// field names (model_tier, callable_lieutenants, required_reading); a future
// adapter (src/data/adapter.ts) will map between the two when wiring to
// real data. For v0.1 we ship inline sample data matching the design's
// expected shape so the prototype renders.

export type Rank = "major" | "captain" | "lieutenant";

export type Archetype =
  | "orchestrator"
  | "architect"
  | "verifier"
  | "executor"
  | "reviewer"
  | "plan-critic"
  | "researcher"
  | "curator"
  | "intake"
  | "scout";

export interface Officer {
  name: string;
  rank: Rank;
  archetype: Archetype;
  nickname: string;
  role: string;
  tools: string[];
  lieutenants: string[];
  reading: string[];
  tier: string;
}

export interface Skill {
  name: string;
  kind: "skill" | "subagent" | "script";
  description: string;
  callable_by: string[];
}

export interface MetaAspect {
  name: string;
  title: string;
  summary: string;
}

export type ArchetypeColors = Record<Archetype, string>;

export interface StoaData {
  officers: Officer[];
  skills: Skill[];
  metaAspects: MetaAspect[];
  archetypes: ArchetypeColors;
  bodyPreview: string;
}
