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
  ArchetypeText,
  Button,
  Chip,
  Mark,
  OfficerCard,
  RankPill,
  SkillCard,
  ThemeToggle,
  archColorFor,
} from "./Components";
import { Plus, Search, Settings, Edit, Copy, Code } from "lucide-react";
import { SAMPLE_DATA } from "./data/sample";
import { useTheme } from "./hooks/useTheme";
import type {
  Archetype,
  ArchetypeColors,
  MetaAspect,
  Officer,
  Skill,
} from "./data/types";

// ---------------------------------------------------------------------------
// URL helpers (acb-009)
// ---------------------------------------------------------------------------

type RosterId = "default" | "minimal" | "user-level" | "custom";

const ROSTER_IDS: RosterId[] = ["default", "minimal", "user-level", "custom"];

/**
 * Derive the current top-level tab from the URL pathname.
 * `/` and `/officer/...` → "team"; `/skills` and `/skill/...` → "skills";
 * `/meta` and `/meta/...` → "meta"; otherwise "team" (fallback for `*`).
 */
function tabFromPath(pathname: string): Tab {
  if (pathname === "/skills" || pathname.startsWith("/skill/")) return "skills";
  if (pathname === "/meta" || pathname.startsWith("/meta/")) return "meta";
  return "team";
}

function parseRosterParam(s: string | null): RosterId {
  if (s && (ROSTER_IDS as string[]).includes(s)) return s as RosterId;
  return "default";
}

function parseArchetypeParam(
  s: string | null,
  archetypes: ArchetypeColors
): Archetype | null {
  if (!s) return null;
  if (Object.prototype.hasOwnProperty.call(archetypes, s)) return s as Archetype;
  return null;
}

/**
 * Build a canonical query-string suffix from the current search params,
 * stripping defaults so the common case (`?roster=default`, no archetype)
 * produces an empty string. Used at navigate sites to preserve the active
 * filter when changing path.
 */
function buildPreservedQuery(searchParams: URLSearchParams): string {
  const next = new URLSearchParams();
  const r = searchParams.get("roster");
  if (r && r !== "default" && (ROSTER_IDS as string[]).includes(r)) {
    next.set("roster", r);
  }
  const a = searchParams.get("archetype");
  if (a) next.set("archetype", a);
  const s = next.toString();
  return s ? `?${s}` : "";
}

/**
 * Returns a copy of `params` with default-valued entries removed
 * (`roster=default`, empty `archetype=`). Used at navigate sites to keep the
 * URL canonically minimal — `?roster=default` is implicit, so omitting it
 * makes deep-links stable across roster picker tweaks.
 *
 * Subtlety (acb-009 spec §9.7): if a user types `?roster=default` manually,
 * the app honors it on initial load; on the next setSearchParams call (e.g.,
 * toggling archetype), `roster=default` gets stripped — URL converges to
 * canonical-minimal form. Documented; not a bug.
 */
function stripDefaultSearchParams(params: URLSearchParams): URLSearchParams {
  const next = new URLSearchParams(params);
  if (next.get("roster") === "default") next.delete("roster");
  const a = next.get("archetype");
  if (!a) next.delete("archetype");
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
// Filter sidebar
// ---------------------------------------------------------------------------

function FilterSidebar({
  rosterId,
  setRoster,
  archetypeFilter,
  setArchetype,
  archetypes,
}: {
  rosterId: RosterId;
  setRoster: (r: RosterId) => void;
  archetypeFilter: Archetype | null;
  setArchetype: (a: Archetype | null) => void;
  archetypes: ArchetypeColors;
}) {
  const { dark } = useTheme();
  const rosters: { id: RosterId; label: string }[] = [
    { id: "default", label: "default · 12 officers" },
    { id: "minimal", label: "minimal · 4 officers" },
    { id: "user-level", label: "user-level · 8 officers" },
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
      <div style={labelStyle}>Archetype</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <div
          data-testid="filter-clear"
          onClick={() => setArchetype(null)}
          style={itemStyle(!archetypeFilter)}
        >
          All
        </div>
        {(Object.keys(archetypes) as Archetype[]).map((a) => (
          <div
            key={a}
            data-testid={`filter-archetype-${a}`}
            onClick={() => setArchetype(a)}
            style={{
              ...itemStyle(archetypeFilter === a),
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span
              style={{
                width: 8,
                height: 8,
                background: archColorFor(a, dark),
                borderRadius: 1,
              }}
            />
            {a}
          </div>
        ))}
      </div>
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Team view
// ---------------------------------------------------------------------------

function TeamView({
  officers,
  onPick,
}: {
  officers: Officer[];
  onPick: (o: Officer) => void;
}) {
  const order: Record<string, number> = { major: 0, captain: 1, lieutenant: 2 };
  const sorted = [...officers].sort((a, b) => order[a.rank] - order[b.rank]);
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
          Team Overview
        </h1>
        <span
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            color: "var(--fg-3)",
          }}
        >
          {officers.length} officers · default roster
        </span>
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
          gap: 14,
        }}
      >
        {sorted.map((o) => (
          <OfficerCard key={o.name} officer={o} onClick={() => onPick(o)} />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Officer detail (with markdown body renderer)
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

function DetailSidebar({ officer }: { officer: Officer }) {
  const sectionLabel: React.CSSProperties = {
    fontFamily: "Inter, sans-serif",
    fontSize: 10.5,
    fontWeight: 600,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "var(--fg-3)",
    marginBottom: 8,
  };
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
          {officer.tools.length}
        </span>
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
        {officer.tools.map((t) => (
          <Chip key={t}>{t}</Chip>
        ))}
      </div>
      {officer.lieutenants.length > 0 && (
        <>
          <div style={sectionLabel}>Callable lieutenants</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
            {officer.lieutenants.map((l) => (
              <span key={l} data-testid={`lieutenant-chip-${l}`} style={{ display: "inline-flex" }}>
                <Chip variant="skill">{l}</Chip>
              </span>
            ))}
          </div>
        </>
      )}
      {officer.reading.length > 0 && (
        <>
          <div style={sectionLabel}>Required reading</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 5, marginBottom: 20 }}>
            {officer.reading.map((r) => (
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
        {officer.tier}
      </div>
      <div style={sectionLabel}>Body path</div>
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          color: "var(--fg-2)",
          wordBreak: "break-all",
          lineHeight: 1.5,
        }}
      >
        definitions/bodies/{officer.name.toLowerCase()}.md
      </div>
    </aside>
  );
}

function OfficerDetail({
  officer,
  onBack,
  body,
}: {
  officer: Officer;
  onBack: () => void;
  body: string;
}) {
  const renderedBody = body
    .replace(/\{\{OFFICER_NAME\}\}/g, officer.name)
    .replace(/\{\{NICKNAME\}\}/g, officer.nickname);
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
          <RankPill rank={officer.rank} />
          <ArchetypeText archetype={officer.archetype} />
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
          {officer.name}
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
          {officer.role}
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
          <BodyMarkdown text={renderedBody} />
        </div>
      </div>
      <DetailSidebar officer={officer} />
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
  officers,
  skills,
  onPickOfficer,
  onPickSkill,
}: {
  open: boolean;
  onClose: () => void;
  officers: Officer[];
  skills: Skill[];
  onPickOfficer: (o: Officer) => void;
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
  const oMatches = officers
    .filter(
      (o) =>
        o.name.toLowerCase().includes(norm) || o.role.toLowerCase().includes(norm)
    )
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
            placeholder="Search officers, skills, meta-aspects…"
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
        {oMatches.length > 0 && (
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
              Officers
            </div>
            {oMatches.map((o) => (
              <div
                key={o.name}
                data-testid={`palette-result-officer-${o.name}`}
                onClick={() => {
                  onPickOfficer(o);
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
                  {o.name}
                </span>
                <span
                  style={{
                    marginLeft: "auto",
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 10.5,
                    color: "var(--fg-3)",
                  }}
                >
                  {o.rank} · {o.archetype}
                </span>
              </div>
            ))}
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

function filterOfficers(
  officers: Officer[],
  roster: RosterId,
  archetypeFilter: Archetype | null
): Officer[] {
  return officers.filter((o) => {
    if (archetypeFilter && o.archetype !== archetypeFilter) return false;
    if (roster === "default") return true;
    if (roster === "minimal")
      return ["MAJOR_PLINY", "DAEDALUS", "ADA", "VERA"].includes(o.name);
    if (roster === "user-level")
      return !["CAPTAIN_PLINY", "CURATOR", "HERALD", "SCOUT"].includes(o.name);
    return false; // custom: empty start
  });
}

function TeamRoute({
  officers,
  archetypes,
}: {
  officers: Officer[];
  archetypes: ArchetypeColors;
}) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const roster = parseRosterParam(searchParams.get("roster"));
  const archetypeFilter = parseArchetypeParam(searchParams.get("archetype"), archetypes);
  const filtered = filterOfficers(officers, roster, archetypeFilter);

  // Set/clear filter params with default-stripping. Reads current params
  // freshly via the closure of `searchParams` (re-resolved each render);
  // no useCallback churn (acb-009 ARGUS Override 2).
  function setRoster(r: RosterId) {
    const next = new URLSearchParams(searchParams);
    next.set("roster", r);
    setSearchParams(stripDefaultSearchParams(next));
  }
  function setArchetype(a: Archetype | null) {
    const next = new URLSearchParams(searchParams);
    if (a) next.set("archetype", a);
    else next.delete("archetype");
    setSearchParams(stripDefaultSearchParams(next));
  }

  return (
    <>
      <FilterSidebar
        rosterId={roster}
        setRoster={setRoster}
        archetypeFilter={archetypeFilter}
        setArchetype={setArchetype}
        archetypes={archetypes}
      />
      <TeamView
        officers={filtered}
        onPick={(o) => navigate(`/officer/${o.name}${buildPreservedQuery(searchParams)}`)}
      />
    </>
  );
}

function OfficerRoute({
  officers,
  body,
}: {
  officers: Officer[];
  body: string;
}) {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const officer = officers.find((o) => o.name === name);

  if (!officer) {
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
          Officer <code>{name}</code> not found.
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
    <OfficerDetail
      officer={officer}
      onBack={() => navigate(`/${buildPreservedQuery(searchParams)}`)}
      body={body}
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
  const data = SAMPLE_DATA;
  const { dark } = useTheme();
  const [paletteOpen, setPaletteOpen] = useState(false);

  // URL-driven state — single source of truth (acb-009).
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const tab: Tab = tabFromPath(location.pathname);
  const roster: RosterId = parseRosterParam(searchParams.get("roster"));
  const archetypeFilter: Archetype | null = parseArchetypeParam(
    searchParams.get("archetype"),
    data.archetypes
  );

  // Resolve `selected` from the URL pathname for STOA_STATE bridge purposes.
  // `useParams()` only populates inside routed children; resolving here via
  // a regex against the pathname keeps the bridge value-correct at the App
  // level. (See acb-009 design §6 / R7.) Returns the same Officer reference
  // across renders for the same URL — effect deps stay identity-stable.
  const officerNameMatch = location.pathname.match(/^\/officer\/([^/?]+)/);
  const selected: Officer | null = officerNameMatch
    ? data.officers.find((o) => o.name === officerNameMatch[1]) ?? null
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
   * Shape:
   *   {
   *     dark: boolean,                        // theme mode, from useTheme()
   *     currentTab: "team" | "skills" | "meta",
   *     selectedOfficer: Officer | null,      // null when on the team grid
   *     roster: RosterId,                     // active roster filter
   *     archetypeFilter: Archetype | null,    // active archetype chip, or null
   *   }
   *
   * Source of truth (post-acb-009): URL is canonical for currentTab,
   *   selectedOfficer, roster, and archetypeFilter — read via useLocation,
   *   useSearchParams, and a pathname-regex resolution for selectedOfficer
   *   (since useParams only populates inside routed children). `dark`
   *   continues to come from useTheme(). The exposed shape and contract
   *   surfaces below are unchanged from acb-008.
   *
   * Contract:
   *   • Read-only by convention. Consumers MUST NOT mutate the object;
   *     mutations would be silently overwritten on the next render anyway.
   *     If a future arc needs a write API, that's a separate dispatch
   *     (`window.STOA_DISPATCH`); explicitly out of scope for acb-008/009.
   *   • Single-object replace per render — observers can detect changes via
   *     reference equality (`prev !== window.STOA_STATE`). We do not mutate
   *     in place. Each effect run produces a fresh object literal.
   *   • Timing: this effect runs after React's commit phase, so consumers
   *     reading STOA_STATE synchronously immediately after dispatching a UI
   *     event (e.g., right after `element.click()`) will see the prior
   *     snapshot. Wait one microtask (`await Promise.resolve()` or
   *     `setTimeout(0)`) — or observe for reference inequality on the next
   *     tick — before reading.
   *
   * The `(window as any)` cast is intentional v1; consumers read this from
   * plain JS where TS typing is not needed. Adding an ambient declaration
   * (`declare global { interface Window { STOA_STATE: ... } }`) is
   * explicitly out of scope per acb-008 §4 — follow-up if a TS consumer
   * emerges.
   */
  useEffect(() => {
    (window as any).STOA_STATE = {
      dark,
      currentTab: tab,
      selectedOfficer: selected,
      roster,
      archetypeFilter,
    };
  }, [dark, tab, selected, roster, archetypeFilter]);

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
          team: data.officers.length,
          skills: data.skills.length,
          meta: data.metaAspects.length,
        }}
      />
      <div style={{ display: "flex", alignItems: "stretch" }}>
        <Routes>
          <Route
            path="/"
            element={<TeamRoute officers={data.officers} archetypes={data.archetypes} />}
          />
          <Route
            path="/officer/:name"
            element={<OfficerRoute officers={data.officers} body={data.bodyPreview} />}
          />
          <Route
            path="/skills"
            element={
              <SkillsView
                skills={data.skills}
                onPick={(s) => navigate(`/skill/${s.name}`)}
              />
            }
          />
          <Route path="/skill/:name" element={<SkillPlaceholder />} />
          <Route
            path="/meta"
            element={
              <MetaView
                items={data.metaAspects}
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
        officers={data.officers}
        skills={data.skills}
        onPickOfficer={(o) =>
          navigate(`/officer/${o.name}${buildPreservedQuery(searchParams)}`)
        }
        onPickSkill={(s) => navigate(`/skill/${s.name}`)}
      />
    </div>
  );
}

export default App;
