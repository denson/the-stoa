// v2 type definitions for The Stoa data model.
//
// Encodes the v2 rank ladder (planning v2 §2) and the PRINCIPAL framework
// (planning v2 §3). Authority: ~/claude_projects/user-beadwork/plans/
// three-role-recursive-architecture.md.
//
// Additive: coexists with the v1 types in ./types.ts. Nothing imports these
// yet. Arc 10 wires the gen-data adapter against this shape; Arc 11 swaps
// sample data; Arc 12 swaps display.

/**
 * The five ranks in the v2 architecture (planning v2 §2).
 *
 * Ordered from top to bottom of authority:
 *
 * - `HUMAN`       — actual humans. The top role; agents do not get
 *                   HUMAN-tier titles. The human's descriptive role is
 *                   `PRINCIPAL` (see {@link Human}).
 * - `COLONEL`     — **reserved future agent rank.** Sits between MAJOR
 *                   and HUMAN: more autonomous than MAJOR, still below
 *                   HUMAN. No agent currently occupies this rank. v1 used
 *                   COLONEL to mean "the human"; v2 corrects that error.
 *                   See {@link ColonelSlot} for type-level enforcement
 *                   that the slot is empty.
 * - `MAJOR`       — current top agent rank. Top-level Claude Code session.
 *                   Has the `Agent` tool; can dispatch CAPTAINs.
 *                   Two MAJOR seats per tier: `POLYBIUS` (CHIEF-OF-STAFF)
 *                   and `PLINY` (ORCHESTRATOR).
 * - `CAPTAIN`     — sub-agent in `.claude/agents/<NAME>.md`. Cannot
 *                   dispatch further sub-agents (runtime constraint
 *                   `u--7yg.12`). Reports up to a MAJOR.
 * - `LIEUTENANT`  — skill in `skills/<name>/`. Reusable helper invoked
 *                   by any rank.
 */
export type Rank = "HUMAN" | "COLONEL" | "MAJOR" | "CAPTAIN" | "LIEUTENANT";

/**
 * Ranks that an agent can hold. HUMAN is excluded — HUMANs are not agents.
 * COLONEL is included in the type but no agent currently carries it; the
 * COLONEL slot is enforced empty at the slot level (see {@link ColonelSlot}).
 */
export type AgentRank = Exclude<Rank, "HUMAN">;

/**
 * An agent record (planning v2 §3).
 *
 * Agents have three identifying pieces:
 * - {@link rank}            — structural; what the agent can do
 * - {@link mnemonic}        — for human memory; e.g. "POLYBIUS", "DAEDALUS"
 * - {@link descriptiveRole} — what the agent does in plain words; e.g.
 *                             "CHIEF-OF-STAFF", "ARCHITECT"
 *
 * Different ranks identify different agents — the type system treats
 * (rank, mnemonic) as the agent identity, so distinct ranks always produce
 * distinct agents.
 */
export type Agent = {
  /** The agent's rank. Always non-HUMAN. */
  rank: AgentRank;

  /** Mnemonic name in canonical UPPERCASE form, e.g. "POLYBIUS", "PLINY". */
  mnemonic: string;

  /**
   * Plain-words description of the seat's job, in canonical
   * SCREAMING-KEBAB-CASE, e.g. "CHIEF-OF-STAFF", "ORCHESTRATOR",
   * "ARCHITECT", "PLAN-CRITIC", "EXECUTOR", "VERIFIER", "REVIEWER".
   */
  descriptiveRole: string;

  /** Markdown body of the role file (everything after frontmatter, if any). */
  body: string;

  /** Tools available to the agent (typically from frontmatter `tools:`). */
  tools: string[];

  /**
   * Canonical filename without project suffix, e.g. `MAJOR_PLINY.md` or
   * `CAPTAIN_DAEDALUS.md`. The `_<project>` suffix used at deploy time
   * is *not* part of the canonical filename — see {@link projectScope}.
   */
  filename: string;

  /**
   * Project suffix when this agent is deployed against a specific project
   * (e.g. `"the-stoa"` for `MAJOR_POLYBIUS_the-stoa.md`). Omit for
   * user-tier deploys.
   */
  projectScope?: string;

  /**
   * LIEUTENANT (skill) names this agent is wired to dispatch.
   * Mirrors the `callable_lieutenants` field used in role-file authoring.
   */
  callableLieutenants?: string[];

  /**
   * Files this agent is expected to read at session start.
   * Mirrors the `required_reading` field used in role-file authoring.
   */
  requiredReading?: string[];

  /**
   * Model tier the agent runs on (e.g. `"opus"`, `"sonnet"`, `"haiku"`).
   * Mirrors the `model_tier` field used in role-file authoring.
   */
  modelTier?: string;
};

/**
 * A human record (planning v2 §3 — PRINCIPAL framework).
 *
 * Humans rank above agents. The descriptive role is hardcoded `PRINCIPAL`
 * — that is the only role a human occupies in the system. The human's
 * actual {@link name} is learned through onboarding and is not assumed.
 *
 * Note: v1 used "Colonel" to mean the human. v2 corrects that. The human
 * is `PRINCIPAL`; `COLONEL` is a reserved future *agent* rank.
 */
export type Human = {
  /** Always `"HUMAN"`. */
  rank: "HUMAN";

  /** The human's actual name, learned through onboarding. */
  name?: string;

  /** Hardcoded — `PRINCIPAL` is the only descriptive role for a human. */
  descriptiveRole: "PRINCIPAL";
};

/**
 * A slot in the rank ladder, used by The Stoa's display layer
 * (planning v2 §11) to show all ranks including the reserved-empty
 * COLONEL rank.
 *
 * For the rank-specific specializations that carry stronger type-level
 * guarantees, see {@link HumanSlot}, {@link ColonelSlot}, and
 * {@link AgentSlot}. {@link RosterSlot} is the discriminated union over
 * those three.
 */
export type RankSlot = {
  rank: Rank;

  /**
   * `true` for ranks that are visible in the ladder but not yet occupied
   * by any agent. Currently only the COLONEL slot uses this.
   */
  reserved?: boolean;

  /**
   * Inhabitants of the slot. For the HUMAN rank this is a list of
   * {@link Human}s; for agent ranks it is a list of {@link Agent}s; for
   * COLONEL it is an empty tuple.
   */
  agents: ReadonlyArray<Agent | Human>;
};

/**
 * The HUMAN rank slot. PRINCIPALs only; never agents.
 */
export type HumanSlot = RankSlot & {
  rank: "HUMAN";
  reserved?: false;
  agents: Human[];
};

/**
 * The COLONEL rank slot.
 *
 * COLONEL is a **reserved future agent rank** — visible in the ladder
 * (planning v2 §11) so the architecture's shape is legible, but no agent
 * currently inhabits it. The empty-tuple type below enforces at compile
 * time that no agent is assigned to this slot. When/if a future agent is
 * promoted to COLONEL, this type will be relaxed; until then, attempts to
 * push an agent into the slot are a TypeScript error.
 *
 * Do **not** use this slot for the human PRINCIPAL — that was the v1
 * mistake. The human lives in {@link HumanSlot} with descriptive role
 * `PRINCIPAL`.
 */
export type ColonelSlot = RankSlot & {
  rank: "COLONEL";
  reserved: true;
  /** Empty tuple — type-level enforcement that COLONEL has no agents. */
  agents: readonly [];
};

/**
 * A non-COLONEL agent rank slot (MAJOR, CAPTAIN, or LIEUTENANT).
 */
export type AgentSlot = RankSlot & {
  rank: "MAJOR" | "CAPTAIN" | "LIEUTENANT";
  reserved?: false;
  agents: Agent[];
};

/**
 * Discriminated union of all slot kinds. The ladder's display layer
 * (Arc 12) iterates over an array of these in canonical top-to-bottom
 * order: HUMAN, COLONEL, MAJOR, CAPTAIN, LIEUTENANT.
 */
export type RosterSlot = HumanSlot | ColonelSlot | AgentSlot;

/**
 * Top-level v2 data shape: the ranked roster plus any document-level
 * extras the display layer needs. Extends naturally as Arcs 10–12
 * add adapter-derived fields (skills index, meta-aspects, etc.).
 */
export type StoaDataV2 = {
  /**
   * Slots in canonical top-to-bottom order:
   * HUMAN → COLONEL → MAJOR → CAPTAIN → LIEUTENANT.
   */
  roster: RosterSlot[];
};
