// Reusable components for the character-builder UI kit.
// All colors come from CSS variables defined in colors_and_type.css,
// so the UI follows :root[data-theme="dark"] toggles automatically.

const v = name => `var(--${name})`;

// Archetype accent colors. Each has a [light, dark] pair.
const archColors = {
  orchestrator: ["#5B4D86", "#9D8FCB"],
  architect:    ["#2E6E63", "#6FB5A8"],
  verifier:     ["#785637", "#C29A75"],
  executor:     ["#4A6E2E", "#8FB575"],
  reviewer:     ["#6E2E4A", "#C7889F"],
  "plan-critic":["#6E4A2E", "#C29A75"],
  researcher:   ["#2E4A6E", "#7CA1D4"],
  curator:      ["#4A2E6E", "#A88FCB"],
  intake:       ["#6E6E2E", "#C2C275"],
  scout:        ["#2E6E4A", "#75C29A"],
};

function useDark() {
  const [dark, setDark] = React.useState(() =>
    document.documentElement.getAttribute("data-theme") === "dark");
  React.useEffect(() => {
    const obs = new MutationObserver(() => {
      setDark(document.documentElement.getAttribute("data-theme") === "dark");
    });
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => obs.disconnect();
  }, []);
  return dark;
}

function archColorFor(archetype, dark) {
  const pair = archColors[archetype] || ["#76736B", "#A6A39B"];
  return pair[dark ? 1 : 0];
}

function Icon({ name, size = 16, stroke = 2, style = {} }) {
  const props = { width: size, height: size, viewBox: "0 0 24 24", fill: "none",
    stroke: "currentColor", strokeWidth: stroke, strokeLinecap: "round", strokeLinejoin: "round", style };
  const paths = {
    "users": <><path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/></>,
    "search": <><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></>,
    "edit": <><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4Z"/></>,
    "copy": <><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></>,
    "code": <><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></>,
    "plus": <><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>,
    "settings": <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></>,
    "sun": <><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></>,
    "moon": <><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></>,
  };
  return <svg {...props}>{paths[name]}</svg>;
}

function Mark({ size = 28 }) {
  return (
    <svg width={size * 0.5} height={size} viewBox="0 0 64 96" style={{ color: v("fg-1") }}>
      <g fill="currentColor">
        <rect x="6" y="14" width="52" height="6"/>
        <path d="M10 20 Q10 24 14 24 L50 24 Q54 24 54 20 Z"/>
        <rect x="16" y="24" width="32" height="56"/>
        <rect x="12" y="80" width="40" height="4"/>
        <rect x="6" y="84" width="52" height="6"/>
      </g>
    </svg>
  );
}

function Button({ variant = "primary", size = "md", children, onClick, leading, style = {} }) {
  const base = { fontFamily:"var(--font-sans)", fontWeight:500, borderRadius:6, cursor:"pointer", lineHeight:1.2,
    border:"1px solid transparent", display:"inline-flex", alignItems:"center", gap:6, transition:"all 180ms" };
  const sizes = { sm:{ fontSize:12, padding:"4px 10px" }, md:{ fontSize:13, padding:"7px 13px" }, lg:{ fontSize:14, padding:"9px 16px" }};
  const variants = {
    primary:{ background: v("accent"), color: v("fg-on-accent"), borderColor: v("accent") },
    secondary:{ background:"transparent", color: v("fg-1"), borderColor: v("border-2") },
    ghost:{ background:"transparent", color: v("fg-1") },
    danger:{ background: v("danger"), color: "#fff", borderColor: v("danger") },
  };
  return <button onClick={onClick} style={{ ...base, ...sizes[size], ...variants[variant], ...style }}>{leading}{children}</button>;
}

function RankPill({ rank }) {
  const map = {
    major:      { fg: v("rank-major"),      bg: v("rank-major-bg"),      border: v("border-2") },
    captain:    { fg: v("rank-captain"),    bg: v("rank-captain-bg"),    border: v("border-2") },
    lieutenant: { fg: v("rank-lieutenant"), bg: v("rank-lieutenant-bg"), border: v("border-2") },
  }[rank];
  return <span style={{ fontFamily:"var(--font-mono)", fontSize:10, fontWeight:600, letterSpacing:"0.06em",
    textTransform:"uppercase", padding:"2px 7px", borderRadius:999, border:`1px solid ${map.border}`,
    background: map.bg, color: map.fg, whiteSpace:"nowrap" }}>{rank}</span>;
}

function ArchetypeText({ archetype }) {
  const dark = useDark();
  return <span style={{ fontFamily:"var(--font-mono)", fontSize:10.5,
    color: archColorFor(archetype, dark), textTransform:"lowercase" }}>{archetype}-archetype</span>;
}

function Chip({ children, variant = "tool", onClick }) {
  const variants = {
    tool: { bg: v("bg-inset"), fg: v("fg-2"), border: v("border-1") },
    skill:{ bg: v("accent-soft"), fg: v("accent"), border: v("border-2") },
    meta: { bg: v("accent-soft-2"), fg: v("fg-1"), border: v("border-2") },
  };
  const x = variants[variant] || variants.tool;
  return <span onClick={onClick} style={{ display:"inline-flex", alignItems:"center", gap:6,
    fontFamily:"var(--font-mono)", fontSize:11, fontWeight:500,
    padding:"3px 9px", borderRadius:4, background: x.bg, color: x.fg, border:`1px solid ${x.border}`,
    cursor: onClick ? "pointer" : "default" }}>{children}</span>;
}

function OfficerCard({ officer, onClick }) {
  const [hover, setHover] = React.useState(false);
  const dark = useDark();
  const accent = archColorFor(officer.archetype, dark);
  return (
    <div onClick={onClick} onMouseEnter={()=>setHover(true)} onMouseLeave={()=>setHover(false)}
      style={{ background: hover ? v("bg-inset") : v("bg-surface"),
        border:`1px solid ${v("border-1")}`, borderLeft:`3px solid ${accent}`,
        borderRadius:10, padding:"16px 18px 14px", cursor:"pointer",
        boxShadow: v("shadow-1"), display:"flex", flexDirection:"column", gap:8,
        transition:"background 180ms" }}>
      <div style={{ display:"flex", alignItems:"center", gap:8, flexWrap:"wrap" }}>
        <RankPill rank={officer.rank}/>
        <ArchetypeText archetype={officer.archetype}/>
      </div>
      <div style={{ fontFamily:"var(--font-mono)", fontWeight:700, fontSize:14.5,
        letterSpacing:"0.02em", color: v("fg-1") }}>{officer.name}</div>
      <div style={{ fontFamily:"var(--font-sans)", fontSize:12.5, color: v("fg-2"),
        lineHeight:1.45, textWrap:"pretty" }}>{officer.role}</div>
    </div>
  );
}

function SkillCard({ skill, onClick }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div onClick={onClick} onMouseEnter={()=>setHover(true)} onMouseLeave={()=>setHover(false)}
      style={{ background: hover ? v("bg-inset") : v("bg-surface"),
        border:`1px solid ${v("border-1")}`, borderRadius:10, padding:"16px 18px",
        cursor:"pointer", boxShadow: v("shadow-1"),
        display:"flex", flexDirection:"column", gap:8, transition:"background 180ms" }}>
      <div style={{ display:"flex", alignItems:"center", gap:8, justifyContent:"space-between" }}>
        <div style={{ fontFamily:"var(--font-mono)", fontWeight:600, fontSize:14, color: v("fg-1") }}>{skill.name}</div>
        <span style={{ fontFamily:"var(--font-mono)", fontSize:10, color: v("fg-3"),
          textTransform:"uppercase", letterSpacing:"0.08em" }}>{skill.kind}</span>
      </div>
      <div style={{ fontFamily:"var(--font-sans)", fontSize:12.5, color: v("fg-2"),
        lineHeight:1.45, display:"-webkit-box", WebkitLineClamp:3, WebkitBoxOrient:"vertical",
        overflow:"hidden" }}>{skill.description}</div>
      {skill.callable_by.length > 0 && (
        <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginTop:2 }}>
          <span style={{ fontFamily:"var(--font-sans)", fontSize:10.5, color: v("fg-3"), marginRight:2 }}>callable by</span>
          {skill.callable_by.map(o => <Chip key={o} variant="tool">{o}</Chip>)}
        </div>
      )}
    </div>
  );
}

function CommandPalette({ open, onClose, officers, skills, onPickOfficer }) {
  const [q, setQ] = React.useState("");
  React.useEffect(() => {
    if (!open) setQ("");
    const onKey = e => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  const norm = q.toLowerCase();
  const oMatches = officers.filter(o => o.name.toLowerCase().includes(norm) || o.role.toLowerCase().includes(norm)).slice(0, 5);
  const sMatches = skills.filter(s => s.name.toLowerCase().includes(norm) || s.description.toLowerCase().includes(norm)).slice(0, 4);
  return (
    <div onClick={onClose} style={{ position:"fixed", inset:0, background:"rgba(20,18,12,0.45)",
      backdropFilter:"blur(12px)", WebkitBackdropFilter:"blur(12px)", zIndex:50,
      display:"flex", alignItems:"flex-start", justifyContent:"center", paddingTop:120 }}>
      <div onClick={e=>e.stopPropagation()} style={{ width:560, background: v("bg-surface"),
        border:`1px solid ${v("border-1")}`, borderRadius:10,
        boxShadow: v("shadow-3"), overflow:"hidden" }}>
        <div style={{ padding:"14px 16px", borderBottom:`1px solid ${v("border-1")}`, display:"flex", alignItems:"center", gap:10 }}>
          <Icon name="search" size={16} style={{ color: v("fg-3") }}/>
          <input autoFocus value={q} onChange={e=>setQ(e.target.value)} placeholder="Search officers, skills, meta-aspects…"
            style={{ flex:1, border:"none", outline:"none", fontFamily:"var(--font-sans)", fontSize:14, color: v("fg-1"), background:"transparent" }}/>
          <span style={{ fontFamily:"var(--font-mono)", fontSize:10, background: v("bg-inset"),
            border:`1px solid ${v("border-1")}`, padding:"1px 6px", borderRadius:3, color: v("fg-3") }}>esc</span>
        </div>
        {oMatches.length > 0 && <>
          <div style={{ fontFamily:"var(--font-sans)", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
            textTransform:"uppercase", color: v("fg-4"), padding:"10px 16px 4px" }}>Officers</div>
          {oMatches.map(o => (
            <div key={o.name} onClick={()=>{ onPickOfficer(o); onClose(); }}
              style={{ padding:"7px 16px", display:"flex", alignItems:"center", gap:10, cursor:"pointer" }}
              onMouseEnter={e => e.currentTarget.style.background = "var(--accent-soft)"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
              <span style={{ fontFamily:"var(--font-mono)", fontSize:13, fontWeight:500, color: v("fg-1") }}>{o.name}</span>
              <span style={{ marginLeft:"auto", fontFamily:"var(--font-mono)", fontSize:10.5, color: v("fg-3") }}>
                {o.rank} · {o.archetype}
              </span>
            </div>
          ))}
        </>}
        {sMatches.length > 0 && <>
          <div style={{ fontFamily:"var(--font-sans)", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
            textTransform:"uppercase", color: v("fg-4"), padding:"10px 16px 4px",
            borderTop:`1px solid ${v("border-1")}` }}>Skills</div>
          {sMatches.map(s => (
            <div key={s.name} style={{ padding:"7px 16px", display:"flex", alignItems:"center", gap:10, cursor:"pointer" }}
              onMouseEnter={e => e.currentTarget.style.background = "var(--accent-soft)"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
              <span style={{ fontFamily:"var(--font-mono)", fontSize:13, fontWeight:500, color: v("fg-1") }}>{s.name}</span>
              <span style={{ marginLeft:"auto", fontFamily:"var(--font-mono)", fontSize:10.5, color: v("fg-3") }}>{s.kind}</span>
            </div>
          ))}
        </>}
      </div>
    </div>
  );
}

function ThemeToggle({ dark, onToggle }) {
  return (
    <button onClick={onToggle} title={dark ? "Switch to light" : "Switch to dark"}
      style={{ background:"transparent", border:`1px solid ${v("border-1")}`,
        borderRadius:6, padding:"5px 8px", cursor:"pointer", color: v("fg-2"),
        display:"inline-flex", alignItems:"center" }}>
      <Icon name={dark ? "sun" : "moon"} size={14}/>
    </button>
  );
}

Object.assign(window, { Icon, Mark, Button, RankPill, ArchetypeText, Chip,
  OfficerCard, SkillCard, CommandPalette, ThemeToggle, useDark, archColorFor, v });
