import { useEffect, useState } from "react";
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
          <Button variant="primary" size="sm" leading={<Plus size={13} />}>
            New agent
          </Button>
          <ThemeToggle />
          <Settings
            size={16}
            style={{ color: "var(--fg-3)", cursor: "pointer", marginLeft: 4 }}
          />
        </div>
      </div>
      <div style={{ display: "flex", padding: "4px 24px 0", gap: 0, marginTop: 6 }}>
        {tabs.map((t) => (
          <div
            key={t.id}
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

type RosterId = "default" | "minimal" | "user-level" | "custom";

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
        <div onClick={() => setArchetype(null)} style={itemStyle(!archetypeFilter)}>
          All
        </div>
        {(Object.keys(archetypes) as Archetype[]).map((a) => (
          <div
            key={a}
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
              <Chip key={l} variant="skill">
                {l}
              </Chip>
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

function SkillsView({ skills }: { skills: Skill[] }) {
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
          <SkillCard key={s.name} skill={s} />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Meta-aspects view
// ---------------------------------------------------------------------------

function MetaView({ items }: { items: MetaAspect[] }) {
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
            style={{
              background: "var(--bg-surface)",
              border: "1px solid var(--border-1)",
              borderRadius: 10,
              padding: "16px 18px",
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
}: {
  open: boolean;
  onClose: () => void;
  officers: Officer[];
  skills: Skill[];
  onPickOfficer: (o: Officer) => void;
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
// App
// ---------------------------------------------------------------------------

function App() {
  const data = SAMPLE_DATA;
  const [tab, setTab] = useState<Tab>("team");
  const [selected, setSelected] = useState<Officer | null>(null);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [roster, setRoster] = useState<RosterId>("default");
  const [archetypeFilter, setArchetypeFilter] = useState<Archetype | null>(null);

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

  const officers = data.officers.filter((o) => {
    if (archetypeFilter && o.archetype !== archetypeFilter) return false;
    if (roster === "default") return true;
    if (roster === "minimal")
      return ["MAJOR_PLINY", "DAEDALUS", "ADA", "VERA"].includes(o.name);
    if (roster === "user-level")
      return !["CAPTAIN_PLINY", "CURATOR", "HERALD", "SCOUT"].includes(o.name);
    return false; // custom: empty start
  });

  return (
    <div style={{ background: "var(--bg-app)", minHeight: "100vh", color: "var(--fg-1)" }}>
      <Header
        tab={tab}
        onTab={(t) => {
          setTab(t);
          setSelected(null);
        }}
        onSearch={() => setPaletteOpen(true)}
        counts={{
          team: data.officers.length,
          skills: data.skills.length,
          meta: data.metaAspects.length,
        }}
      />
      <div style={{ display: "flex", alignItems: "stretch" }}>
        {tab === "team" && !selected && (
          <FilterSidebar
            rosterId={roster}
            setRoster={setRoster}
            archetypeFilter={archetypeFilter}
            setArchetype={setArchetypeFilter}
            archetypes={data.archetypes}
          />
        )}
        {tab === "team" && !selected && (
          <TeamView officers={officers} onPick={setSelected} />
        )}
        {tab === "team" && selected && (
          <OfficerDetail
            officer={selected}
            onBack={() => setSelected(null)}
            body={data.bodyPreview}
          />
        )}
        {tab === "skills" && <SkillsView skills={data.skills} />}
        {tab === "meta" && <MetaView items={data.metaAspects} />}
      </div>
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        officers={data.officers}
        skills={data.skills}
        onPickOfficer={(o) => {
          setTab("team");
          setSelected(o);
        }}
      />
    </div>
  );
}

export default App;
