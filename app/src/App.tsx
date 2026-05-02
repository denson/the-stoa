import { useEffect, useState } from "react";
import {
  Link,
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router";
import {
  AgentCard,
  Button,
  Chip,
  HumanCard,
  Mark,
  RankPill,
  ReservedColonelCard,
  RoleText,
  SkillCard,
  ThemeToggle,
} from "./Components";
import { Plus, Search, Settings, Edit, Copy, Code } from "lucide-react";
import { stoaData } from "./data/generated/agents";
import { metaAspects, skills } from "./data/display-extras";
import { agentSlug, deriveRoleSummary } from "./data/derive";
import { roleColorFor } from "./data/colors";
import { useTheme } from "./hooks/useTheme";
import type {
  Agent,
  Human,
  RosterSlot,
  StoaDataV2,
} from "./data/types-v2";
import type { MetaAspect, Skill } from "./data/display-extras";

// ---------------------------------------------------------------------------
// Constants — the human's name source (Arc 12 Colonel-call: hardcoded).
// ---------------------------------------------------------------------------

/**
 * The PRINCIPAL's name as displayed in the HUMAN slot. Hardcoded for the
 * single-user localhost-only posture. To swap to a derived value, replace
 * this with a build-time read of `git config user.name` (e.g., expose it
 * via Vite's `define` config) or a small `~/.config/the-stoa/name.txt`
 * lookup at startup.
 */
const PRINCIPAL_NAME = "Denson";

/**
 * Roster preset slugs (filename minus `.md`) — used by the FilterSidebar's
 * roster picker. These are agent identifiers, not display strings.
 */
const MINIMAL_AGENTS = [
  "MAJOR_PLINY",
  "CAPTAIN_DAEDALUS",
  "CAPTAIN_ADA",
  "CAPTAIN_VERA",
];
const USER_LEVEL_EXCLUDE = [
  "CAPTAIN_PLINY",
  "CAPTAIN_CURATOR",
  "CAPTAIN_HERALD",
  "CAPTAIN_STRABO",
];

// ---------------------------------------------------------------------------
// Roster + role helpers
// ---------------------------------------------------------------------------

type RosterId = "default" | "minimal" | "user-level" | "custom";

const ROSTER_IDS: RosterId[] = ["default", "minimal", "user-level", "custom"];

function parseRosterParam(s: string | null): RosterId {
  if (s && (ROSTER_IDS as string[]).includes(s)) return s as RosterId;
  return "default";
}

function parseRoleParam(s: string | null, allRoles: string[]): string | null {
  if (!s) return null;
  return allRoles.includes(s) ? s : null;
}

/**
 * The HUMAN-rank slot, augmented with the hardcoded PRINCIPAL name. The
 * generated v2 data leaves `name` unset (gen-data has no source for it);
 * we attach it at the App layer per Arc 12 Colonel call.
 */
function humanWithName(slot: RosterSlot): RosterSlot {
  if (slot.rank !== "HUMAN") return slot;
  return {
    ...slot,
    agents: slot.agents.map((h) =>
      ({ ...(h as Human), name: PRINCIPAL_NAME } as Human),
    ),
  };
}

/**
 * Hydrate the v2 roster with the human name. The generated data is
 * deliberately name-free; this single point hydrates it before the
 * ladder, palette, and detail routes consume it.
 */
function hydrateRoster(data: StoaDataV2): StoaDataV2 {
  return { ...data, roster: data.roster.map(humanWithName) };
}

/**
 * Returns the unique descriptive roles in the roster, in canonical
 * rank-ladder encounter order (HUMAN → COLONEL → MAJOR → CAPTAIN → LIEUTENANT;
 * within rank, the order they appear in the data — alphabetical-by-mnemonic
 * per gen-data's emit order).
 */
function uniqueRoles(roster: RosterSlot[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const slot of roster) {
    for (const inhabitant of slot.agents) {
      const role = inhabitant.descriptiveRole;
      if (!seen.has(role)) {
        seen.add(role);
        out.push(role);
      }
    }
  }
  return out;
}

/**
 * Returns true when the roster preset includes this agent slug.
 */
function rosterIncludes(rosterId: RosterId, slug: string): boolean {
  if (rosterId === "default") return true;
  if (rosterId === "minimal") return MINIMAL_AGENTS.includes(slug);
  if (rosterId === "user-level") return !USER_LEVEL_EXCLUDE.includes(slug);
  return false; // custom: empty start
}

/**
 * Apply roster + role filters to the v2 roster. Returns a filtered roster
 * preserving slot identity (so all five ranks remain visible as structural
 * sections, even when their agent list is empty after filtering). The
 * COLONEL slot is hidden when a role filter is active (it has no agents
 * so role filtering would always exclude it; explicit hiding keeps the
 * ladder coherent under a filter).
 */
function filterRoster(
  roster: RosterSlot[],
  rosterId: RosterId,
  roleFilter: string | null,
): RosterSlot[] {
  const out: RosterSlot[] = [];
  for (const slot of roster) {
    if (slot.rank === "HUMAN") {
      if (roleFilter && roleFilter !== "PRINCIPAL") continue;
      out.push(slot);
    } else if (slot.rank === "COLONEL") {
      if (roleFilter) continue;
      out.push(slot);
    } else {
      // MAJOR | CAPTAIN | LIEUTENANT — slot is structurally AgentSlot.
      // TS does not collapse the RankSlot base `agents` type
      // (ReadonlyArray<Agent | Human>) intersected with AgentSlot's
      // `agents: Agent[]` down to `Agent[]` automatically, so we narrow
      // the agents array via assertion before filtering.
      const slotAgents = slot.agents as Agent[];
      const filtered = slotAgents.filter((a) => {
        const slug = agentSlug(a);
        if (!rosterIncludes(rosterId, slug)) return false;
        if (roleFilter && a.descriptiveRole !== roleFilter) return false;
        return true;
      });
      out.push({ ...slot, agents: filtered } as RosterSlot);
    }
  }
  return out;
}

/**
 * Flat list of agents from a (filtered) roster — used by the command palette
 * and counts. Excludes HUMAN and reserved-COLONEL slots.
 */
function flattenAgents(roster: RosterSlot[]): Agent[] {
  const out: Agent[] = [];
  for (const slot of roster) {
    if (slot.rank === "HUMAN" || slot.rank === "COLONEL") continue;
    for (const a of slot.agents) out.push(a);
  }
  return out;
}

// ---------------------------------------------------------------------------
// URL helpers (acb-009)
// ---------------------------------------------------------------------------

/**
 * Derive the current top-level tab from the URL pathname.
 * `/` and `/agent/...` → "team"; `/skills` and `/skill/...` → "skills";
 * `/meta` and `/meta/...` → "meta"; otherwise "team" (fallback for `*`).
 */
function tabFromPath(pathname: string): Tab {
  if (pathname === "/skills" || pathname.startsWith("/skill/")) return "skills";
  if (pathname === "/meta" || pathname.startsWith("/meta/")) return "meta";
  return "team";
}

/**
 * Build a canonical query-string suffix from the current search params,
 * stripping defaults so the common case (`?roster=default`, no role)
 * produces an empty string. Used at navigate sites to preserve the active
 * filter when changing path.
 */
function buildPreservedQuery(searchParams: URLSearchParams): string {
  const next = new URLSearchParams();
  const r = searchParams.get("roster");
  if (r && r !== "default" && (ROSTER_IDS as string[]).includes(r)) {
    next.set("roster", r);
  }
  const role = searchParams.get("role");
  if (role) next.set("role", role);
  const s = next.toString();
  return s ? `?${s}` : "";
}

/**
 * Returns a copy of `params` with default-valued entries removed
 * (`roster=default`, empty `role=`). Used at navigate sites to keep the
 * URL canonically minimal — `?roster=default` is implicit, so omitting it
 * makes deep-links stable across roster picker tweaks.
 *
 * Subtlety (acb-009 spec §9.7): if a user types `?roster=default` manually,
 * the app honors it on initial load; on the next setSearchParams call (e.g.,
 * toggling role), `roster=default` gets stripped — URL converges to
 * canonical-minimal form. Documented; not a bug.
 */
function stripDefaultSearchParams(params: URLSearchParams): URLSearchParams {
  const next = new URLSearchParams(params);
  if (next.get("roster") === "default") next.delete("roster");
  const r = next.get("role");
  if (!r) next.delete("role");
  return next;
}

// ---------------------------------------------------------------------------
// Header
// ---------------------------------------------------------------------------

type Tab = "team" | "skills" | "meta";

function Header({
  tab,
  onTab,
  onSearch,
  counts,
}: {
  tab: Tab;
  onTab: (t: Tab) => void;
  onSearch: () => void;
  counts: { team: number; skills: number; meta: number };
}) {
  const tabs: { id: Tab; label: string; count: number }[] = [
    { id: "team", label: "Team", count: counts.team },
    { id: "skills", label: "Skills", count: counts.skills },
    { id: "meta", label: "Meta-aspects", count: counts.meta },
  ];
  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 10,
        background: "var(--bg-surface)",
        borderBottom: "1px solid var(--border-1)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", padding: "10px 24px 0" }}>
        <Mark size={28} />
        <span
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 15,
            fontWeight: 600,
            marginLeft: 10,
            color: "var(--fg-1)",
          }}
        >
          The Stoa
        </span>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 11,
            color: "var(--fg-3)",
            marginLeft: 10,
            padding: "2px 8px",
            background: "var(--bg-inset)",
            borderRadius: 4,
          }}
        >
          character-builder
        </span>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 10 }}>
          <button
            data-testid="search-trigger"
            onClick={onSearch}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "var(--bg-sunken)",
              border: "1px solid var(--border-1)",
              borderRadius: 6,
              padding: "5px 10px",
              fontFamily: "Inter, sans-serif",
              fontSize: 12,
              color: "var(--fg-3)",
              cursor: "pointer",
            }}
          >
            <Search size={14} />
            <span>Search…</span>
            <span
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 10,
                background: "var(--bg-surface)",
                border: "1px solid var(--border-1)",
                padding: "1px 5px",
                borderRadius: 3,
                marginLeft: 14,
              }}
            >
              ⌘K
            </span>
          </button>
          <span data-testid="new-agent-button" style={{ display: "inline-flex" }}>
            <Button variant="primary" size="sm" leading={<Plus size={13} />}>
              New agent
            </Button>
          </span>
          <ThemeToggle />
          <span data-testid="settings-button" style={{ display: "inline-flex", alignItems: "center" }}>
            <Settings
              size={16}
              style={{ color: "var(--fg-3)", cursor: "pointer", marginLeft: 4 }}
            />
          </span>
        </div>
      </div>
      <div style={{ display: "flex", padding: "4px 24px 0", gap: 0, marginTop: 6 }}>
        {tabs.map((t) => (
          <div
            key={t.id}
            data-testid={`tab-${t.id}`}
            onClick={() => onTab(t.id)}
            style={{
              padding: "12px 14px",
              marginBottom: -1,
              cursor: "pointer",
              fontFamily: "Inter, sans-serif",
              fontSize: 13,
              fontWeight: 500,
              color: tab === t.id ? "var(--fg-1)" : "var(--fg-3)",
              borderBottom:
                tab === t.id ? "2px solid var(--accent)" : "2px solid transparent",
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span>{t.label}</span>
            <span
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 11,
                color: tab === t.id ? "var(--fg-3)" : "var(--fg-4)",
              }}
            >
              {t.count}
            </span>
          </div>
        ))}
      </div>
    </header>
  );
}

// ---------------------------------------------------------------------------
// Filter sidebar — roster preset + role filter (replaces v1's archetype filter
// per Arc 11 hand-back #1 / Arc 12 §5).
// ---------------------------------------------------------------------------

function FilterSidebar({
  rosterId,
  setRoster,
  roleFilter,
  setRole,
  allRoles,
}: {
  rosterId: RosterId;
  setRoster: (r: RosterId) => void;
  roleFilter: string | null;
  setRole: (r: string | null) => void;
  allRoles: string[];
}) {
  const { dark } = useTheme();
  const rosters: { id: RosterId; label: string }[] = [
    { id: "default", label: "default · 12 agents" },
    { id: "minimal", label: "minimal · 4 agents" },
    { id: "user-level", label: "user-level · 8 agents" },
    { id: "custom", label: "custom · start from scratch" },
  ];
  const labelStyle: React.CSSProperties = {
    fontFamily: "Inter, sans-serif",
    fontSize: 11,
    fontWeight: 600,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "var(--fg-3)",
    marginBottom: 8,
  };
  const itemStyle = (active: boolean): React.CSSProperties => ({
    fontFamily: "Inter, sans-serif",
    fontSize: 12.5,
    padding: "6px 10px",
    borderRadius: 6,
    cursor: "pointer",
    background: active ? "var(--accent-soft)" : "transparent",
    color: active ? "var(--accent)" : "var(--fg-2)",
    fontWeight: active ? 500 : 400,
  });
  return (
    <aside
      style={{
        width: 220,
        padding: "24px 16px",
        borderRight: "1px solid var(--border-1)",
        background: "var(--bg-sunken)",
        minHeight: "calc(100vh - 110px)",
      }}
    >
      <div style={labelStyle}>Roster</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 2, marginBottom: 24 }}>
        {rosters.map((r) => (
          <div key={r.id} onClick={() => setRoster(r.id)} style={itemStyle(rosterId === r.id)}>
            {r.label}
          </div>
        ))}
      </div>
      <div style={labelStyle}>Role</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <div
          data-testid="filter-clear"
          onClick={() => setRole(null)}
          style={itemStyle(!roleFilter)}
        >
          All
        </div>
        {allRoles.map((role) => (
          <div
            key={role}
            data-testid={`filter-role-${role}`}
            onClick={() => setRole(role)}
            style={{
              ...itemStyle(roleFilter === role),
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span
              style={{
                width: 8,
                height: 8,
                background: roleColorFor(role, dark),
                borderRadius: 1,
              }}
            />
            {role.toLowerCase()}
          </div>
        ))}
      </div>
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Rank ladder view — replaces v1's TeamView. Renders all five ranks
// (HUMAN → COLONEL → MAJOR → CAPTAIN → LIEUTENANT) as stacked sections
// per planning v2 §11. Section headers carry the rank pill + a count;
// empty sections show a "no inhabitants" placeholder so the ladder's
// shape is visible even under filters.
// ---------------------------------------------------------------------------

function RankSectionHeader({
  rank,
  count,
}: {
  rank: RosterSlot["rank"];
  count: number;
}) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 10,
        margin: "20px 0 10px",
        paddingBottom: 6,
        borderBottom: "1px solid var(--border-1)",
      }}
    >
      <RankPill rank={rank} />
      <span
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          color: "var(--fg-3)",
        }}
      >
        {count}
      </span>
    </div>
  );
}

function RankLadderView({
  roster,
  rosterId,
  onPickAgent,
  totalAgentCount,
}: {
  roster: RosterSlot[];
  rosterId: RosterId;
  onPickAgent: (agent: Agent) => void;
  totalAgentCount: number;
}) {
  return (
    <div style={{ flex: 1, padding: "24px 28px", overflow: "auto" }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 6 }}>
        <h1
          style={{
            margin: 0,
            fontFamily: "Inter, sans-serif",
            fontSize: 24,
            fontWeight: 600,
            letterSpacing: "-0.02em",
            color: "var(--fg-1)",
          }}
        >
          Team Overview
        </h1>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            color: "var(--fg-3)",
          }}
        >
          {totalAgentCount} agents · {rosterId} roster
        </span>
      </div>
      {roster.map((slot) => (
        <RankSection key={slot.rank} slot={slot} onPickAgent={onPickAgent} />
      ))}
    </div>
  );
}

function RankSection({
  slot,
  onPickAgent,
}: {
  slot: RosterSlot;
  onPickAgent: (agent: Agent) => void;
}) {
  if (slot.rank === "HUMAN") {
    const humans = slot.agents as Human[];
    return (
      <section data-testid="rank-section-HUMAN">
        <RankSectionHeader rank="HUMAN" count={humans.length} />
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: 14,
          }}
        >
          {humans.map((h) => (
            <HumanCard key={h.descriptiveRole} human={h} />
          ))}
        </div>
      </section>
    );
  }
  if (slot.rank === "COLONEL") {
    return (
      <section data-testid="rank-section-COLONEL">
        <RankSectionHeader rank="COLONEL" count={0} />
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: 14,
          }}
        >
          <ReservedColonelCard />
        </div>
      </section>
    );
  }
  // MAJOR | CAPTAIN | LIEUTENANT
  const agents = slot.agents as Agent[];
  return (
    <section data-testid={`rank-section-${slot.rank}`}>
      <RankSectionHeader rank={slot.rank} count={agents.length} />
      {agents.length === 0 ? (
        <div
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 13,
            color: "var(--fg-3)",
            padding: "12px 0",
          }}
        >
          {slot.rank === "LIEUTENANT"
            ? "No skills authored yet."
            : "No agents at this rank under the current filter."}
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: 14,
          }}
        >
          {agents.map((a) => (
            <AgentCard
              key={agentSlug(a)}
              agent={a}
              onClick={() => onPickAgent(a)}
            />
          ))}
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Agent detail (with markdown body renderer)
// ---------------------------------------------------------------------------

function InlineMD({ text }: { text: string }) {
  const parts: React.ReactNode[] = [];
  let buf = "";
  let i = 0;
  while (i < text.length) {
    if (text[i] === "`") {
      if (buf) {
        parts.push(buf);
        buf = "";
      }
      const end = text.indexOf("`", i + 1);
      if (end === -1) {
        buf += text[i];
        i++;
        continue;
      }
      parts.push(
        <code
          key={`c${i}`}
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: "0.88em",
            background: "var(--bg-inset)",
            border: "1px solid var(--border-1)",
            padding: "1px 5px",
            borderRadius: 3,
            color: "var(--fg-1)",
          }}
        >
          {text.slice(i + 1, end)}
        </code>
      );
      i = end + 1;
    } else if (text.slice(i, i + 2) === "**") {
      if (buf) {
        parts.push(buf);
        buf = "";
      }
      const end = text.indexOf("**", i + 2);
      if (end === -1) {
        buf += text[i];
        i++;
        continue;
      }
      parts.push(
        <strong key={`b${i}`} style={{ color: "var(--fg-1)", fontWeight: 600 }}>
          {text.slice(i + 2, end)}
        </strong>
      );
      i = end + 2;
    } else {
      buf += text[i];
      i++;
    }
  }
  if (buf) parts.push(buf);
  return <>{parts}</>;
}

function BodyMarkdown({ text }: { text: string }) {
  const lines = text.split("\n");
  const out: React.ReactNode[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("# ")) {
      out.push(
        <h2
          key={i}
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 24,
            fontWeight: 600,
            letterSpacing: "-0.02em",
            color: "var(--fg-1)",
            marginTop: 24,
            marginBottom: 10,
          }}
        >
          {line.slice(2)}
        </h2>
      );
    } else if (line.startsWith("## ")) {
      out.push(
        <h3
          key={i}
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 18,
            fontWeight: 600,
            color: "var(--fg-1)",
            marginTop: 22,
            marginBottom: 8,
          }}
        >
          {line.slice(3)}
        </h3>
      );
    } else if (/^\d+\. /.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\. /, ""));
        i++;
      }
      out.push(
        <ol
          key={i}
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 14.5,
            color: "var(--fg-2)",
            lineHeight: 1.65,
            paddingLeft: 22,
            maxWidth: "68ch",
          }}
        >
          {items.map((t, j) => (
            <li key={j} style={{ marginBottom: 4 }}>
              <InlineMD text={t} />
            </li>
          ))}
        </ol>
      );
      continue;
    } else if (line.trim() === "") {
      // skip
    } else {
      out.push(
        <p
          key={i}
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 14.5,
            color: "var(--fg-2)",
            lineHeight: 1.65,
            maxWidth: "68ch",
            margin: "0 0 12px",
            textWrap: "pretty",
          }}
        >
          <InlineMD text={line} />
        </p>
      );
    }
    i++;
  }
  return <div>{out}</div>;
}

function DetailSidebar({ agent }: { agent: Agent }) {
  const sectionLabel: React.CSSProperties = {
    fontFamily: "Inter, sans-serif",
    fontSize: 10.5,
    fontWeight: 600,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "var(--fg-3)",
    marginBottom: 8,
  };
  const lieutenants = agent.callableLieutenants ?? [];
  const reading = agent.requiredReading ?? [];
  const tier = agent.modelTier ?? "opus";
  return (
    <aside
      style={{
        width: 260,
        padding: "24px 24px 24px 16px",
        borderLeft: "1px solid var(--border-1)",
        background: "var(--bg-surface)",
        position: "sticky",
        top: 110,
        alignSelf: "flex-start",
        height: "calc(100vh - 110px)",
        overflow: "auto",
        flexShrink: 0,
      }}
    >
      <div style={sectionLabel}>
        Tools{" "}
        <span style={{ fontFamily: "'JetBrains Mono', monospace", color: "var(--fg-4)" }}>
          {agent.tools.length}
        </span>
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
        {agent.tools.map((t) => (
          <Chip key={t}>{t}</Chip>
        ))}
      </div>
      {lieutenants.length > 0 && (
        <>
          <div style={sectionLabel}>Callable lieutenants</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
            {lieutenants.map((l) => (
              <span key={l} data-testid={`lieutenant-chip-${l}`} style={{ display: "inline-flex" }}>
                <Chip variant="skill">{l}</Chip>
              </span>
            ))}
          </div>
        </>
      )}
      {reading.length > 0 && (
        <>
          <div style={sectionLabel}>Required reading</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
            {reading.map((r) => (
              <Chip key={r} variant="meta">
                {r}
              </Chip>
            ))}
          </div>
        </>
      )}
      <div style={sectionLabel}>Model tier</div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 13,
          color: "var(--fg-1)",
          marginBottom: 20,
        }}
      >
        {tier}
      </div>
      <div style={sectionLabel}>Body source</div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          color: "var(--fg-2)",
          wordBreak: "break-all",
          lineHeight: 1.5,
        }}
      >
        substrate/{agent.filename}
      </div>
    </aside>
  );
}

function AgentDetail({
  agent,
  onBack,
}: {
  agent: Agent;
  onBack: () => void;
}) {
  const summary = deriveRoleSummary(agent.body);
  return (
    <div style={{ flex: 1, display: "flex", overflow: "auto" }}>
      <div style={{ flex: 1, padding: "24px 32px", maxWidth: 920, overflow: "auto" }}>
        <div
          data-testid="back-to-team"
          onClick={onBack}
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 12,
            color: "var(--fg-3)",
            cursor: "pointer",
            display: "inline-flex",
            alignItems: "center",
            gap: 5,
            marginBottom: 14,
          }}
        >
          ← Back to Team
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            flexWrap: "wrap",
            marginBottom: 6,
          }}
        >
          <RankPill rank={agent.rank} />
          <RoleText role={agent.descriptiveRole} />
        </div>
        <h1
          style={{
            margin: "4px 0 4px",
            fontFamily: "'JetBrains Mono', monospace",
            fontWeight: 700,
            fontSize: 30,
            letterSpacing: "0.01em",
            color: "var(--fg-1)",
          }}
        >
          {agent.mnemonic}
        </h1>
        <div
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 15,
            color: "var(--fg-2)",
            lineHeight: 1.55,
            maxWidth: "68ch",
            marginBottom: 14,
            textWrap: "pretty",
          }}
        >
          {summary}
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
          <Button variant="secondary" size="sm" leading={<Edit size={13} />}>
            Edit
          </Button>
          <Button variant="secondary" size="sm" leading={<Copy size={13} />}>
            Clone
          </Button>
          <Button variant="secondary" size="sm" leading={<Code size={13} />}>
            View JSON
          </Button>
          <Button variant="primary" size="sm" leading={<Plus size={13} />}>
            Add to roster
          </Button>
        </div>
        <div style={{ borderTop: "1px solid var(--border-1)", paddingTop: 20 }}>
          <BodyMarkdown text={agent.body} />
        </div>
      </div>
      <DetailSidebar agent={agent} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Skills view
// ---------------------------------------------------------------------------

function SkillsView({
  skills,
  onPick,
}: {
  skills: Skill[];
  onPick?: (s: Skill) => void;
}) {
  return (
    <div style={{ flex: 1, padding: "24px 28px", overflow: "auto" }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 18 }}>
        <h1
          style={{
            margin: 0,
            fontFamily: "Inter, sans-serif",
            fontSize: 24,
            fontWeight: 600,
            letterSpacing: "-0.02em",
            color: "var(--fg-1)",
          }}
        >
          Skill Library
        </h1>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            color: "var(--fg-3)",
          }}
        >
          {skills.length} skills
        </span>
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
          gap: 14,
        }}
      >
        {skills.map((s) => (
          <SkillCard
            key={s.name}
            skill={s}
            onClick={onPick ? () => onPick(s) : undefined}
          />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Meta-aspects view
// ---------------------------------------------------------------------------

function MetaView({
  items,
  onPick,
}: {
  items: MetaAspect[];
  onPick?: (m: MetaAspect) => void;
}) {
  return (
    <div style={{ flex: 1, padding: "24px 28px", overflow: "auto" }}>
      <h1
        style={{
          margin: "0 0 18px",
          fontFamily: "Inter, sans-serif",
          fontSize: 24,
          fontWeight: 600,
          letterSpacing: "-0.02em",
          color: "var(--fg-1)",
        }}
      >
        Meta-aspects
      </h1>
      <div style={{ display: "flex", flexDirection: "column", gap: 8, maxWidth: 760 }}>
        {items.map((m) => (
          <div
            key={m.name}
            data-testid={`meta-card-${m.name}`}
            onClick={onPick ? () => onPick(m) : undefined}
            style={{
              background: "var(--bg-surface)",
              border: "1px solid var(--border-1)",
              borderRadius: 10,
              padding: "16px 18px",
              cursor: onPick ? "pointer" : "default",
            }}
          >
            <div
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontWeight: 600,
                fontSize: 13,
                color: "var(--fg-1)",
                marginBottom: 4,
              }}
            >
              {m.name}
            </div>
            <div
              style={{
                fontFamily: "Inter, sans-serif",
                fontSize: 14,
                color: "var(--fg-1)",
                fontWeight: 500,
                marginBottom: 6,
              }}
            >
              {m.title}
            </div>
            <div
              style={{
                fontFamily: "Inter, sans-serif",
                fontSize: 13,
                color: "var(--fg-2)",
                lineHeight: 1.55,
                textWrap: "pretty",
              }}
            >
              {m.summary}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Command palette (⌘K)
// ---------------------------------------------------------------------------

function CommandPalette({
  open,
  onClose,
  agents,
  skills,
  onPickAgent,
  onPickSkill,
}: {
  open: boolean;
  onClose: () => void;
  agents: Agent[];
  skills: Skill[];
  onPickAgent: (a: Agent) => void;
  onPickSkill: (s: Skill) => void;
}) {
  const [q, setQ] = useState("");
  useEffect(() => {
    if (!open) setQ("");
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  const norm = q.toLowerCase();
  const aMatches = agents
    .filter((a) => {
      const slug = agentSlug(a).toLowerCase();
      const role = a.descriptiveRole.toLowerCase();
      const summary = deriveRoleSummary(a.body).toLowerCase();
      return (
        slug.includes(norm) ||
        role.includes(norm) ||
        summary.includes(norm)
      );
    })
    .slice(0, 5);
  const sMatches = skills
    .filter(
      (s) =>
        s.name.toLowerCase().includes(norm) || s.description.toLowerCase().includes(norm)
    )
    .slice(0, 4);
  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(20,18,12,0.35)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        zIndex: 50,
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        paddingTop: 120,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: 560,
          background: "var(--bg-surface)",
          border: "1px solid var(--border-1)",
          borderRadius: 10,
          boxShadow: "var(--shadow-3)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            padding: "14px 16px",
            borderBottom: "1px solid var(--border-1)",
            display: "flex",
            alignItems: "center",
            gap: 10,
          }}
        >
          <Search size={16} style={{ color: "var(--fg-3)" }} />
          <input
            data-testid="palette-input"
            autoFocus
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search agents, skills, meta-aspects…"
            style={{
              flex: 1,
              border: "none",
              outline: "none",
              fontFamily: "Inter, sans-serif",
              fontSize: 14,
              color: "var(--fg-1)",
              background: "transparent",
            }}
          />
          <span
            style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
              background: "var(--bg-inset)",
              border: "1px solid var(--border-1)",
              padding: "1px 6px",
              borderRadius: 3,
              color: "var(--fg-3)",
            }}
          >
            esc
          </span>
        </div>
        {aMatches.length > 0 && (
          <>
            <div
              style={{
                fontFamily: "Inter, sans-serif",
                fontSize: 10.5,
                fontWeight: 600,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                color: "var(--fg-4)",
                padding: "10px 16px 4px",
              }}
            >
              Agents
            </div>
            {aMatches.map((a) => {
              const slug = agentSlug(a);
              return (
                <div
                  key={slug}
                  data-testid={`palette-result-agent-${slug}`}
                  onClick={() => {
                    onPickAgent(a);
                    onClose();
                  }}
                  style={{
                    padding: "7px 16px",
                    display: "flex",
                    alignItems: "center",
                    gap: 10,
                    cursor: "pointer",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "var(--accent-soft)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                >
                  <span
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 13,
                      fontWeight: 500,
                      color: "var(--fg-1)",
                    }}
                  >
                    {a.mnemonic}
                  </span>
                  <span
                    style={{
                      marginLeft: "auto",
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 10.5,
                      color: "var(--fg-3)",
                    }}
                  >
                    {a.rank} · {a.descriptiveRole.toLowerCase()}
                  </span>
                </div>
              );
            })}
          </>
        )}
        {sMatches.length > 0 && (
          <>
            <div
              style={{
                fontFamily: "Inter, sans-serif",
                fontSize: 10.5,
                fontWeight: 600,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                color: "var(--fg-4)",
                padding: "10px 16px 4px",
                borderTop: "1px solid var(--border-1)",
              }}
            >
              Skills
            </div>
            {sMatches.map((s) => (
              <div
                key={s.name}
                data-testid={`palette-result-skill-${s.name}`}
                onClick={() => {
                  onPickSkill(s);
                  onClose();
                }}
                style={{
                  padding: "7px 16px",
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  cursor: "pointer",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = "var(--accent-soft)")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
              >
                <span
                  style={{
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 13,
                    fontWeight: 500,
                    color: "var(--fg-1)",
                  }}
                >
                  {s.name}
                </span>
                <span
                  style={{
                    marginLeft: "auto",
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 10.5,
                    color: "var(--fg-3)",
                  }}
                >
                  {s.kind}
                </span>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Route components (acb-009)
// ---------------------------------------------------------------------------

function TeamRoute({
  data,
  allRoles,
}: {
  data: StoaDataV2;
  allRoles: string[];
}) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const rosterId = parseRosterParam(searchParams.get("roster"));
  const roleFilter = parseRoleParam(searchParams.get("role"), allRoles);
  const filtered = filterRoster(data.roster, rosterId, roleFilter);
  const totalAgentCount = flattenAgents(filtered).length;

  // Set/clear filter params with default-stripping. Reads current params
  // freshly via the closure of `searchParams` (re-resolved each render);
  // no useCallback churn (acb-009 ARGUS Override 2).
  function setRoster(r: RosterId) {
    const next = new URLSearchParams(searchParams);
    next.set("roster", r);
    setSearchParams(stripDefaultSearchParams(next));
  }
  function setRole(r: string | null) {
    const next = new URLSearchParams(searchParams);
    if (r) next.set("role", r);
    else next.delete("role");
    setSearchParams(stripDefaultSearchParams(next));
  }

  return (
    <>
      <FilterSidebar
        rosterId={rosterId}
        setRoster={setRoster}
        roleFilter={roleFilter}
        setRole={setRole}
        allRoles={allRoles}
      />
      <RankLadderView
        roster={filtered}
        rosterId={rosterId}
        totalAgentCount={totalAgentCount}
        onPickAgent={(a) =>
          navigate(`/agent/${agentSlug(a)}${buildPreservedQuery(searchParams)}`)
        }
      />
    </>
  );
}

function AgentRoute({ data }: { data: StoaDataV2 }) {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const allAgents = flattenAgents(data.roster);
  const agent = allAgents.find((a) => agentSlug(a) === slug);

  if (!agent) {
    return (
      <div style={{ flex: 1, padding: "32px 28px" }}>
        <div
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 14,
            color: "var(--fg-2)",
            marginBottom: 12,
          }}
        >
          Agent <code>{slug}</code> not found.
        </div>
        <Link
          to="/"
          style={{
            fontFamily: "Inter, sans-serif",
            fontSize: 13,
            color: "var(--accent)",
          }}
        >
          ← Back to Team
        </Link>
      </div>
    );
  }

  return (
    <AgentDetail
      agent={agent}
      onBack={() => navigate(`/${buildPreservedQuery(searchParams)}`)}
    />
  );
}

function SkillPlaceholder() {
  const { name } = useParams<{ name: string }>();
  return (
    <div style={{ flex: 1, padding: "32px 28px" }}>
      <h1
        style={{
          margin: "0 0 8px",
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
          fontSize: 22,
          color: "var(--fg-1)",
        }}
      >
        Skill: {name}
      </h1>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 13,
          color: "var(--fg-3)",
          marginBottom: 14,
        }}
      >
        Skill detail not yet implemented.
      </div>
      <Link
        to="/skills"
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 13,
          color: "var(--accent)",
        }}
      >
        ← Back to Skills
      </Link>
    </div>
  );
}

function MetaPlaceholder() {
  const { name } = useParams<{ name: string }>();
  return (
    <div style={{ flex: 1, padding: "32px 28px" }}>
      <h1
        style={{
          margin: "0 0 8px",
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 700,
          fontSize: 22,
          color: "var(--fg-1)",
        }}
      >
        Meta-aspect: {name}
      </h1>
      <div
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 13,
          color: "var(--fg-3)",
          marginBottom: 14,
        }}
      >
        Meta-aspect detail not yet implemented.
      </div>
      <Link
        to="/meta"
        style={{
          fontFamily: "Inter, sans-serif",
          fontSize: 13,
          color: "var(--accent)",
        }}
      >
        ← Back to Meta-aspects
      </Link>
    </div>
  );
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------

function App() {
  const data = hydrateRoster(stoaData);
  const allAgents = flattenAgents(data.roster);
  const allRoles = uniqueRoles(data.roster);
  const { dark } = useTheme();
  const [paletteOpen, setPaletteOpen] = useState(false);

  // URL-driven state — single source of truth (acb-009).
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const tab: Tab = tabFromPath(location.pathname);
  const rosterId: RosterId = parseRosterParam(searchParams.get("roster"));
  const roleFilter: string | null = parseRoleParam(
    searchParams.get("role"),
    allRoles,
  );

  // Resolve `selectedAgent` from the URL pathname for STOA_STATE bridge
  // purposes. `useParams()` only populates inside routed children;
  // resolving here via a regex against the pathname keeps the bridge
  // value-correct at the App level. (See acb-009 design §6 / R7.)
  // Returns the same Agent reference across renders for the same URL —
  // effect deps stay identity-stable.
  const slugMatch = location.pathname.match(/^\/agent\/([^/?]+)/);
  const selectedAgent: Agent | null = slugMatch
    ? allAgents.find((a) => agentSlug(a) === slugMatch[1]) ?? null
    : null;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setPaletteOpen(true);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  /**
   * window.STOA_STATE — read-only-by-convention runtime state bridge for
   * downstream Claude Code skill consumers (acb-007 agent-design-tutor and
   * future Chrome MCP scripts). Mirrors the small set of top-level React
   * state fields the skill needs to drive the app deterministically without
   * DOM-scraping inline styles.
   *
   * Shape (Arc 12, v2):
   *   {
   *     dark: boolean,                        // theme mode, from useTheme()
   *     currentTab: "team" | "skills" | "meta",
   *     selectedAgent: Agent | null,          // null when on the team grid
   *     roster: RosterId,                     // active roster preset
   *     roleFilter: string | null,            // active role chip, or null
   *   }
   *
   * Migration note: pre-Arc-12 the bridge exposed `selectedOfficer` (v1
   * Officer shape) and `archetypeFilter`. Both renamed to v2 vocabulary.
   * The shape is otherwise unchanged.
   *
   * Source of truth (post-acb-009): URL is canonical for currentTab,
   *   selectedAgent, roster, and roleFilter — read via useLocation,
   *   useSearchParams, and a pathname-regex resolution for selectedAgent
   *   (since useParams only populates inside routed children). `dark`
   *   continues to come from useTheme().
   *
   * Contract:
   *   • Read-only by convention. Consumers MUST NOT mutate the object;
   *     mutations would be silently overwritten on the next render anyway.
   *   • Single-object replace per render — observers can detect changes via
   *     reference equality (`prev !== window.STOA_STATE`). We do not mutate
   *     in place.
   *   • Timing: this effect runs after React's commit phase, so consumers
   *     reading STOA_STATE synchronously immediately after dispatching a UI
   *     event (e.g., right after `element.click()`) will see the prior
   *     snapshot. Wait one microtask before reading.
   */
  useEffect(() => {
    (window as any).STOA_STATE = {
      dark,
      currentTab: tab,
      selectedAgent,
      roster: rosterId,
      roleFilter,
    };
  }, [dark, tab, selectedAgent, rosterId, roleFilter]);

  return (
    <div style={{ background: "var(--bg-app)", minHeight: "100vh", color: "var(--fg-1)" }}>
      <Header
        tab={tab}
        onTab={(t) => {
          const path = t === "team" ? "/" : `/${t}`;
          navigate(`${path}${buildPreservedQuery(searchParams)}`);
        }}
        onSearch={() => setPaletteOpen(true)}
        counts={{
          team: allAgents.length,
          skills: skills.length,
          meta: metaAspects.length,
        }}
      />
      <div style={{ display: "flex", alignItems: "stretch" }}>
        <Routes>
          <Route
            path="/"
            element={<TeamRoute data={data} allRoles={allRoles} />}
          />
          <Route
            path="/agent/:slug"
            element={<AgentRoute data={data} />}
          />
          <Route
            path="/skills"
            element={
              <SkillsView
                skills={skills}
                onPick={(s) => navigate(`/skill/${s.name}`)}
              />
            }
          />
          <Route path="/skill/:name" element={<SkillPlaceholder />} />
          <Route
            path="/meta"
            element={
              <MetaView
                items={metaAspects}
                onPick={(m) => navigate(`/meta/${m.name}`)}
              />
            }
          />
          <Route path="/meta/:name" element={<MetaPlaceholder />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        agents={allAgents}
        skills={skills}
        onPickAgent={(a) =>
          navigate(`/agent/${agentSlug(a)}${buildPreservedQuery(searchParams)}`)
        }
        onPickSkill={(s) => navigate(`/skill/${s.name}`)}
      />
    </div>
  );
}

export default App;
