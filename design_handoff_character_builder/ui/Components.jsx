// Reusable components for the character-builder UI kit.
// All inline styles are unique-named to avoid scope collisions.

const ccPalette = {
  bgApp:"#FAF9F6", bgSurface:"#FFFFFF", bgSunken:"#F2F0EB", bgInset:"#ECE9E1",
  fg1:"#1B1A17", fg2:"#45433E", fg3:"#76736B", fg4:"#A6A39B",
  border1:"#E4E1D8", border2:"#D4D0C5", border3:"#BFBAAD",
  accent:"#2B4A7F", accentHover:"#233C68", accentSoft:"#E6EBF3",
  rankMaj:"#8A6B2C", rankMajBg:"#F5EBD3", rankMajBorder:"#E5D6A8",
  rankCap:"#5C5F66", rankCapBg:"#ECEDEF", rankCapBorder:"#D9DBDF",
  rankLt:"#8A4A2C", rankLtBg:"#F2E2D5", rankLtBorder:"#E5C9B3",
};

function Icon({ name, size = 16, stroke = 2, style = {} }) {
  const props = { width: size, height: size, viewBox: "0 0 24 24", fill: "none",
    stroke: "currentColor", strokeWidth: stroke, strokeLinecap: "round", strokeLinejoin: "round", style };
  const paths = {
    "users": <><path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/></>,
    "package": <><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></>,
    "file": <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></>,
    "search": <><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></>,
    "edit": <><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4Z"/></>,
    "copy": <><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></>,
    "code": <><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></>,
    "plus": <><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>,
    "arrow-right": <><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></>,
    "x": <><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></>,
    "filter": <><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></>,
    "settings": <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></>,
    "check": <><polyline points="20 6 9 17 4 12"/></>,
  };
  return <svg {...props}>{paths[name]}</svg>;
}

function Mark({ size = 28 }) {
  return (
    <svg width={size * 0.5} height={size} viewBox="0 0 64 96" style={{ color: ccPalette.fg1 }}>
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
  const base = { fontFamily:"Inter, sans-serif", fontWeight:500, borderRadius:6, cursor:"pointer", lineHeight:1.2,
    border:"1px solid transparent", display:"inline-flex", alignItems:"center", gap:6, transition:"all 180ms" };
  const sizes = { sm:{ fontSize:12, padding:"4px 10px" }, md:{ fontSize:13, padding:"7px 13px" }, lg:{ fontSize:14, padding:"9px 16px" }};
  const variants = {
    primary:{ background: ccPalette.accent, color:"#fff", borderColor: ccPalette.accent },
    secondary:{ background:"transparent", color: ccPalette.fg1, borderColor: ccPalette.border2 },
    ghost:{ background:"transparent", color: ccPalette.fg1 },
    danger:{ background:"#9B3A3A", color:"#fff", borderColor:"#9B3A3A" },
  };
  return <button onClick={onClick} style={{ ...base, ...sizes[size], ...variants[variant], ...style }}>{leading}{children}</button>;
}

function RankPill({ rank }) {
  const styles = {
    major:{ bg: ccPalette.rankMajBg, fg: ccPalette.rankMaj, border: ccPalette.rankMajBorder },
    captain:{ bg: ccPalette.rankCapBg, fg: ccPalette.rankCap, border: ccPalette.rankCapBorder },
    lieutenant:{ bg: ccPalette.rankLtBg, fg: ccPalette.rankLt, border: ccPalette.rankLtBorder },
  }[rank];
  return <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:10, fontWeight:600, letterSpacing:"0.06em",
    textTransform:"uppercase", padding:"2px 7px", borderRadius:999, border:`1px solid ${styles.border}`,
    background: styles.bg, color: styles.fg, whiteSpace:"nowrap" }}>{rank}</span>;
}

function ArchetypeText({ archetype, color }) {
  return <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:10.5, color, textTransform:"lowercase" }}>{archetype}-archetype</span>;
}

function Chip({ children, variant = "tool", onClick }) {
  const variants = {
    tool:{ bg: ccPalette.bgInset, fg: ccPalette.fg2, border: ccPalette.border1 },
    skill:{ bg: ccPalette.accentSoft, fg: ccPalette.accent, border:"#B7C5DA" },
    meta:{ bg:"#F1EEF7", fg:"#5B4D86", border:"#E0DAEC" },
  };
  const v = variants[variant] || variants.tool;
  return <span onClick={onClick} style={{ display:"inline-flex", alignItems:"center", gap:6,
    fontFamily:"'JetBrains Mono', monospace", fontSize:11, fontWeight:500,
    padding:"3px 9px", borderRadius:4, background:v.bg, color:v.fg, border:`1px solid ${v.border}`,
    cursor: onClick ? "pointer" : "default" }}>{children}</span>;
}

function OfficerCard({ officer, archColor, onClick }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div onClick={onClick} onMouseEnter={()=>setHover(true)} onMouseLeave={()=>setHover(false)}
      style={{ background: hover ? ccPalette.bgApp : ccPalette.bgSurface,
        border:`1px solid ${ccPalette.border1}`, borderLeft:`3px solid ${archColor}`,
        borderRadius:10, padding:"16px 18px 14px", cursor:"pointer",
        boxShadow:"0 1px 2px rgba(20,18,12,0.04)", display:"flex", flexDirection:"column", gap:8,
        transition:"background 180ms" }}>
      <div style={{ display:"flex", alignItems:"center", gap:8, flexWrap:"wrap" }}>
        <RankPill rank={officer.rank}/>
        <ArchetypeText archetype={officer.archetype} color={archColor}/>
      </div>
      <div style={{ fontFamily:"'JetBrains Mono', monospace", fontWeight:700, fontSize:14.5,
        letterSpacing:"0.02em", color: ccPalette.fg1 }}>{officer.name}</div>
      <div style={{ fontFamily:"Inter, sans-serif", fontSize:12.5, color: ccPalette.fg2,
        lineHeight:1.45, textWrap:"pretty" }}>{officer.role}</div>
    </div>
  );
}

function SkillCard({ skill, onClick }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div onClick={onClick} onMouseEnter={()=>setHover(true)} onMouseLeave={()=>setHover(false)}
      style={{ background: hover ? ccPalette.bgApp : ccPalette.bgSurface,
        border:`1px solid ${ccPalette.border1}`, borderRadius:10, padding:"16px 18px",
        cursor:"pointer", boxShadow:"0 1px 2px rgba(20,18,12,0.04)",
        display:"flex", flexDirection:"column", gap:8, transition:"background 180ms" }}>
      <div style={{ display:"flex", alignItems:"center", gap:8, justifyContent:"space-between" }}>
        <div style={{ fontFamily:"'JetBrains Mono', monospace", fontWeight:600, fontSize:14, color: ccPalette.fg1 }}>{skill.name}</div>
        <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:10, color: ccPalette.fg3,
          textTransform:"uppercase", letterSpacing:"0.08em" }}>{skill.kind}</span>
      </div>
      <div style={{ fontFamily:"Inter, sans-serif", fontSize:12.5, color: ccPalette.fg2,
        lineHeight:1.45, display:"-webkit-box", WebkitLineClamp:3, WebkitBoxOrient:"vertical",
        overflow:"hidden" }}>{skill.description}</div>
      {skill.callable_by.length > 0 && (
        <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginTop:2 }}>
          <span style={{ fontFamily:"Inter, sans-serif", fontSize:10.5, color: ccPalette.fg3, marginRight:2 }}>callable by</span>
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
    <div onClick={onClose} style={{ position:"fixed", inset:0, background:"rgba(20,18,12,0.35)",
      backdropFilter:"blur(12px)", WebkitBackdropFilter:"blur(12px)", zIndex:50,
      display:"flex", alignItems:"flex-start", justifyContent:"center", paddingTop:120 }}>
      <div onClick={e=>e.stopPropagation()} style={{ width:560, background: ccPalette.bgSurface,
        border:`1px solid ${ccPalette.border1}`, borderRadius:10,
        boxShadow:"0 4px 12px rgba(20,18,12,0.07), 0 12px 32px rgba(20,18,12,0.05)", overflow:"hidden" }}>
        <div style={{ padding:"14px 16px", borderBottom:`1px solid ${ccPalette.border1}`, display:"flex", alignItems:"center", gap:10 }}>
          <Icon name="search" size={16} style={{ color: ccPalette.fg3 }}/>
          <input autoFocus value={q} onChange={e=>setQ(e.target.value)} placeholder="Search officers, skills, meta-aspects…"
            style={{ flex:1, border:"none", outline:"none", fontFamily:"Inter, sans-serif", fontSize:14, color: ccPalette.fg1, background:"transparent" }}/>
          <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:10, background: ccPalette.bgInset,
            border:`1px solid ${ccPalette.border1}`, padding:"1px 6px", borderRadius:3, color: ccPalette.fg3 }}>esc</span>
        </div>
        {oMatches.length > 0 && <>
          <div style={{ fontFamily:"Inter, sans-serif", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
            textTransform:"uppercase", color: ccPalette.fg4, padding:"10px 16px 4px" }}>Officers</div>
          {oMatches.map(o => (
            <div key={o.name} onClick={()=>{ onPickOfficer(o); onClose(); }}
              style={{ padding:"7px 16px", display:"flex", alignItems:"center", gap:10, cursor:"pointer" }}
              onMouseEnter={e => e.currentTarget.style.background = ccPalette.accentSoft}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
              <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:13, fontWeight:500, color: ccPalette.fg1 }}>{o.name}</span>
              <span style={{ marginLeft:"auto", fontFamily:"'JetBrains Mono', monospace", fontSize:10.5, color: ccPalette.fg3 }}>
                {o.rank} · {o.archetype}
              </span>
            </div>
          ))}
        </>}
        {sMatches.length > 0 && <>
          <div style={{ fontFamily:"Inter, sans-serif", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
            textTransform:"uppercase", color: ccPalette.fg4, padding:"10px 16px 4px",
            borderTop:`1px solid ${ccPalette.border1}` }}>Skills</div>
          {sMatches.map(s => (
            <div key={s.name} style={{ padding:"7px 16px", display:"flex", alignItems:"center", gap:10, cursor:"pointer" }}
              onMouseEnter={e => e.currentTarget.style.background = ccPalette.accentSoft}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
              <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:13, fontWeight:500, color: ccPalette.fg1 }}>{s.name}</span>
              <span style={{ marginLeft:"auto", fontFamily:"'JetBrains Mono', monospace", fontSize:10.5, color: ccPalette.fg3 }}>{s.kind}</span>
            </div>
          ))}
        </>}
      </div>
    </div>
  );
}

Object.assign(window, { Icon, Mark, Button, RankPill, ArchetypeText, Chip, OfficerCard, SkillCard, CommandPalette, ccPalette });
