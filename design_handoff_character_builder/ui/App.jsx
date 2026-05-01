// Top-level shell. All colors via CSS vars (var(--name)) — light/dark just works.

function Header({ tab, onTab, onSearch, dark, onToggleTheme }) {
  const tabs = [
    { id:"team", label:"Team", count: window.STOA_DATA.officers.length },
    { id:"skills", label:"Skills", count: window.STOA_DATA.skills.length },
    { id:"meta", label:"Meta-aspects", count: window.STOA_DATA.metaAspects.length },
  ];
  return (
    <header style={{ position:"sticky", top:0, zIndex:10, background: v("bg-surface"),
      borderBottom:`1px solid ${v("border-1")}` }}>
      <div style={{ display:"flex", alignItems:"center", padding:"10px 24px 0" }}>
        <Mark size={28}/>
        <span style={{ fontFamily:"var(--font-sans)", fontSize:15, fontWeight:600, marginLeft:10, color: v("fg-1") }}>The Stoa</span>
        <span style={{ fontFamily:"var(--font-mono)", fontSize:11, color: v("fg-3"), marginLeft:10,
          padding:"2px 8px", background: v("bg-inset"), borderRadius:4 }}>character-builder</span>
        <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:10 }}>
          <button onClick={onSearch} style={{ display:"flex", alignItems:"center", gap:8,
            background: v("bg-sunken"), border:`1px solid ${v("border-1")}`, borderRadius:6,
            padding:"5px 10px", fontFamily:"var(--font-sans)", fontSize:12, color: v("fg-3"), cursor:"pointer" }}>
            <Icon name="search" size={14}/>
            <span>Search…</span>
            <span style={{ fontFamily:"var(--font-mono)", fontSize:10, background: v("bg-surface"),
              border:`1px solid ${v("border-1")}`, padding:"1px 5px", borderRadius:3, marginLeft:14 }}>⌘K</span>
          </button>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13}/>}>New agent</Button>
          <ThemeToggle dark={dark} onToggle={onToggleTheme}/>
          <Icon name="settings" size={16} style={{ color: v("fg-3"), cursor:"pointer", marginLeft:4 }}/>
        </div>
      </div>
      <div style={{ display:"flex", padding:"4px 24px 0", gap:0, marginTop:6 }}>
        {tabs.map(t => (
          <div key={t.id} onClick={()=>onTab(t.id)} style={{
            padding:"12px 14px", marginBottom:-1, cursor:"pointer",
            fontFamily:"var(--font-sans)", fontSize:13, fontWeight:500,
            color: tab === t.id ? v("fg-1") : v("fg-3"),
            borderBottom: tab === t.id ? `2px solid ${v("accent")}` : "2px solid transparent",
            display:"flex", alignItems:"center", gap:6 }}>
            <span>{t.label}</span>
            <span style={{ fontFamily:"var(--font-mono)", fontSize:11,
              color: tab === t.id ? v("fg-3") : v("fg-4") }}>{t.count}</span>
          </div>
        ))}
      </div>
    </header>
  );
}

function FilterSidebar({ rosterId, setRoster, archetypeFilter, setArchetype, archetypes }) {
  const dark = useDark();
  const rosters = [
    { id:"default", label:"default · 12 officers" },
    { id:"minimal", label:"minimal · 4 officers" },
    { id:"user-level", label:"user-level · 8 officers" },
    { id:"custom", label:"custom · start from scratch" },
  ];
  const labelStyle = { fontFamily:"var(--font-sans)", fontSize:11, fontWeight:600, letterSpacing:"0.08em",
    textTransform:"uppercase", color: v("fg-3"), marginBottom:8 };
  const itemStyle = active => ({ fontFamily:"var(--font-sans)", fontSize:12.5,
    padding:"6px 10px", borderRadius:6, cursor:"pointer",
    background: active ? v("accent-soft") : "transparent",
    color: active ? v("accent") : v("fg-2"),
    fontWeight: active ? 500 : 400 });
  return (
    <aside style={{ width:220, padding:"24px 16px", borderRight:`1px solid ${v("border-1")}`,
      background: v("bg-sunken"), minHeight:"calc(100vh - 110px)" }}>
      <div style={labelStyle}>Roster</div>
      <div style={{ display:"flex", flexDirection:"column", gap:2, marginBottom:24 }}>
        {rosters.map(r => <div key={r.id} onClick={()=>setRoster(r.id)} style={itemStyle(rosterId === r.id)}>{r.label}</div>)}
      </div>
      <div style={labelStyle}>Archetype</div>
      <div style={{ display:"flex", flexDirection:"column", gap:2 }}>
        <div onClick={()=>setArchetype(null)} style={itemStyle(!archetypeFilter)}>All</div>
        {Object.keys(archetypes).map(a =>
          <div key={a} onClick={()=>setArchetype(a)} style={{ ...itemStyle(archetypeFilter === a),
            display:"flex", alignItems:"center", gap:8 }}>
            <span style={{ width:8, height:8, background: archColorFor(a, dark), borderRadius:1 }}/>{a}
          </div>)}
      </div>
    </aside>
  );
}

function TeamView({ officers, onPick }) {
  const sorted = [...officers].sort((a, b) => {
    const order = { major:0, captain:1, lieutenant:2 };
    return order[a.rank] - order[b.rank];
  });
  return (
    <div style={{ flex:1, padding:"24px 28px", overflow:"auto" }}>
      <div style={{ display:"flex", alignItems:"baseline", gap:12, marginBottom:18 }}>
        <h1 style={{ margin:0, fontFamily:"var(--font-sans)", fontSize:24, fontWeight:600,
          letterSpacing:"-0.02em", color: v("fg-1") }}>Team Overview</h1>
        <span style={{ fontFamily:"var(--font-mono)", fontSize:12, color: v("fg-3") }}>
          {officers.length} officers · default roster
        </span>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(240px, 1fr))", gap:14 }}>
        {sorted.map(o => <OfficerCard key={o.name} officer={o} onClick={()=>onPick(o)}/>)}
      </div>
    </div>
  );
}

function OfficerDetail({ officer, onBack, body }) {
  const renderedBody = body
    .replace(/\{\{OFFICER_NAME\}\}/g, officer.name)
    .replace(/\{\{NICKNAME\}\}/g, officer.nickname);
  return (
    <div style={{ flex:1, display:"flex", overflow:"auto" }}>
      <div style={{ flex:1, padding:"24px 32px", maxWidth:920, overflow:"auto" }}>
        <div onClick={onBack} style={{ fontFamily:"var(--font-sans)", fontSize:12,
          color: v("fg-3"), cursor:"pointer", display:"inline-flex", alignItems:"center", gap:5, marginBottom:14 }}>
          ← Back to Team
        </div>
        <div style={{ display:"flex", alignItems:"center", gap:10, flexWrap:"wrap", marginBottom:6 }}>
          <RankPill rank={officer.rank}/>
          <ArchetypeText archetype={officer.archetype}/>
        </div>
        <h1 style={{ margin:"4px 0 4px", fontFamily:"var(--font-mono)", fontWeight:700,
          fontSize:30, letterSpacing:"0.01em", color: v("fg-1") }}>{officer.name}</h1>
        <div style={{ fontFamily:"var(--font-sans)", fontSize:15, color: v("fg-2"),
          lineHeight:1.55, maxWidth:"68ch", marginBottom:14, textWrap:"pretty" }}>{officer.role}</div>
        <div style={{ display:"flex", gap:8, marginBottom:24, flexWrap:"wrap" }}>
          <Button variant="secondary" size="sm" leading={<Icon name="edit" size={13}/>}>Edit</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="copy" size={13}/>}>Clone</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="code" size={13}/>}>View JSON</Button>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13}/>}>Add to roster</Button>
        </div>
        <div style={{ borderTop:`1px solid ${v("border-1")}`, paddingTop:20 }}>
          <BodyMarkdown text={renderedBody}/>
        </div>
      </div>
      <DetailSidebar officer={officer}/>
    </div>
  );
}

function DetailSidebar({ officer }) {
  const sectionLabel = { fontFamily:"var(--font-sans)", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
    textTransform:"uppercase", color: v("fg-3"), marginBottom:8 };
  return (
    <aside style={{ width:260, padding:"24px 24px 24px 16px", borderLeft:`1px solid ${v("border-1")}`,
      background: v("bg-surface"), position:"sticky", top:110, alignSelf:"flex-start",
      height:"calc(100vh - 110px)", overflow:"auto", flexShrink:0 }}>
      <div style={sectionLabel}>Tools <span style={{ fontFamily:"var(--font-mono)", color: v("fg-4") }}>{officer.tools.length}</span></div>
      <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginBottom:20 }}>
        {officer.tools.map(t => <Chip key={t}>{t}</Chip>)}
      </div>
      {officer.lieutenants.length > 0 && <>
        <div style={sectionLabel}>Callable lieutenants</div>
        <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginBottom:20 }}>
          {officer.lieutenants.map(l => <Chip key={l} variant="skill">{l}</Chip>)}
        </div>
      </>}
      {officer.reading.length > 0 && <>
        <div style={sectionLabel}>Required reading</div>
        <div style={{ display:"flex", flexWrap:"wrap", gap:5, marginBottom:20 }}>
          {officer.reading.map(r => <Chip key={r} variant="meta">{r}</Chip>)}
        </div>
      </>}
      <div style={sectionLabel}>Model tier</div>
      <div style={{ fontFamily:"var(--font-mono)", fontSize:13, color: v("fg-1"), marginBottom:20 }}>{officer.tier}</div>
      <div style={sectionLabel}>Body path</div>
      <div style={{ fontFamily:"var(--font-mono)", fontSize:11, color: v("fg-2"),
        wordBreak:"break-all", lineHeight:1.5 }}>definitions/bodies/{officer.name.toLowerCase()}.md</div>
    </aside>
  );
}

function BodyMarkdown({ text }) {
  const lines = text.split("\n");
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("# ")) {
      out.push(<h2 key={i} style={{ fontFamily:"var(--font-sans)", fontSize:24, fontWeight:600,
        letterSpacing:"-0.02em", color: v("fg-1"), marginTop:24, marginBottom:10 }}>{line.slice(2)}</h2>);
    } else if (line.startsWith("## ")) {
      out.push(<h3 key={i} style={{ fontFamily:"var(--font-sans)", fontSize:18, fontWeight:600,
        color: v("fg-1"), marginTop:22, marginBottom:8 }}>{line.slice(3)}</h3>);
    } else if (line.match(/^\d+\. /)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^\d+\. /)) { items.push(lines[i].replace(/^\d+\. /, "")); i++; }
      out.push(<ol key={i} style={{ fontFamily:"var(--font-sans)", fontSize:14.5,
        color: v("fg-2"), lineHeight:1.65, paddingLeft:22, maxWidth:"68ch" }}>
        {items.map((t, j) => <li key={j} style={{ marginBottom:4 }}><InlineMD text={t}/></li>)}
      </ol>);
      continue;
    } else if (line.trim() === "") {
      // skip
    } else {
      out.push(<p key={i} style={{ fontFamily:"var(--font-sans)", fontSize:14.5,
        color: v("fg-2"), lineHeight:1.65, maxWidth:"68ch", margin:"0 0 12px", textWrap:"pretty" }}>
        <InlineMD text={line}/>
      </p>);
    }
    i++;
  }
  return <div>{out}</div>;
}

function InlineMD({ text }) {
  const parts = [];
  let buf = "";
  let i = 0;
  while (i < text.length) {
    if (text[i] === "`") {
      if (buf) { parts.push(buf); buf = ""; }
      const end = text.indexOf("`", i + 1);
      if (end === -1) { buf += text[i]; i++; continue; }
      parts.push(<code key={"c"+i} style={{ fontFamily:"var(--font-mono)", fontSize:"0.88em",
        background: v("bg-inset"), border:`1px solid ${v("border-1")}`, padding:"1px 5px",
        borderRadius:3, color: v("fg-1") }}>{text.slice(i + 1, end)}</code>);
      i = end + 1;
    } else if (text.slice(i, i + 2) === "**") {
      if (buf) { parts.push(buf); buf = ""; }
      const end = text.indexOf("**", i + 2);
      if (end === -1) { buf += text[i]; i++; continue; }
      parts.push(<strong key={"b"+i} style={{ color: v("fg-1"), fontWeight:600 }}>{text.slice(i + 2, end)}</strong>);
      i = end + 2;
    } else { buf += text[i]; i++; }
  }
  if (buf) parts.push(buf);
  return <>{parts}</>;
}

function SkillsView({ skills }) {
  return (
    <div style={{ flex:1, padding:"24px 28px", overflow:"auto" }}>
      <div style={{ display:"flex", alignItems:"baseline", gap:12, marginBottom:18 }}>
        <h1 style={{ margin:0, fontFamily:"var(--font-sans)", fontSize:24, fontWeight:600,
          letterSpacing:"-0.02em", color: v("fg-1") }}>Skill Library</h1>
        <span style={{ fontFamily:"var(--font-mono)", fontSize:12, color: v("fg-3") }}>
          {skills.length} skills
        </span>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(280px, 1fr))", gap:14 }}>
        {skills.map(s => <SkillCard key={s.name} skill={s}/>)}
      </div>
    </div>
  );
}

function MetaView({ items }) {
  return (
    <div style={{ flex:1, padding:"24px 28px", overflow:"auto" }}>
      <h1 style={{ margin:"0 0 18px", fontFamily:"var(--font-sans)", fontSize:24, fontWeight:600,
        letterSpacing:"-0.02em", color: v("fg-1") }}>Meta-aspects</h1>
      <div style={{ display:"flex", flexDirection:"column", gap:8, maxWidth:760 }}>
        {items.map(m => (
          <div key={m.name} style={{ background: v("bg-surface"), border:`1px solid ${v("border-1")}`,
            borderRadius:10, padding:"16px 18px" }}>
            <div style={{ fontFamily:"var(--font-mono)", fontWeight:600, fontSize:13, color: v("fg-1"), marginBottom:4 }}>{m.name}</div>
            <div style={{ fontFamily:"var(--font-sans)", fontSize:14, color: v("fg-1"), fontWeight:500, marginBottom:6 }}>{m.title}</div>
            <div style={{ fontFamily:"var(--font-sans)", fontSize:13, color: v("fg-2"), lineHeight:1.55, textWrap:"pretty" }}>{m.summary}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  const data = window.STOA_DATA;
  const [tab, setTab] = React.useState("team");
  const [selected, setSelected] = React.useState(null);
  const [paletteOpen, setPaletteOpen] = React.useState(false);
  const [roster, setRoster] = React.useState("default");
  const [archetypeFilter, setArchetypeFilter] = React.useState(null);
  const [dark, setDark] = React.useState(() => {
    const saved = localStorage.getItem("stoa-theme");
    if (saved) return saved === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  React.useEffect(() => {
    document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
    localStorage.setItem("stoa-theme", dark ? "dark" : "light");
  }, [dark]);

  React.useEffect(() => {
    const onKey = e => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); setPaletteOpen(true); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const officers = data.officers.filter(o =>
    (!archetypeFilter || o.archetype === archetypeFilter) &&
    (roster === "default" ? true :
     roster === "minimal" ? ["MAJOR_PLINY","DAEDALUS","ADA","VERA"].includes(o.name) :
     roster === "user-level" ? !["CAPTAIN_PLINY","CURATOR","HERALD","SCOUT"].includes(o.name) :
     false));

  return (
    <div style={{ background: v("bg-app"), minHeight:"100vh", color: v("fg-1") }}>
      <Header tab={tab} onTab={t => { setTab(t); setSelected(null); }}
        onSearch={()=>setPaletteOpen(true)}
        dark={dark} onToggleTheme={()=>setDark(d => !d)}/>
      <div style={{ display:"flex", alignItems:"stretch" }}>
        {tab === "team" && !selected && <FilterSidebar rosterId={roster} setRoster={setRoster}
          archetypeFilter={archetypeFilter} setArchetype={setArchetypeFilter} archetypes={data.archetypes}/>}
        {tab === "team" && !selected && <TeamView officers={officers} onPick={setSelected}/>}
        {tab === "team" && selected && <OfficerDetail officer={selected}
          onBack={()=>setSelected(null)} body={data.bodyPreview}/>}
        {tab === "skills" && <SkillsView skills={data.skills}/>}
        {tab === "meta" && <MetaView items={data.metaAspects}/>}
      </div>
      <CommandPalette open={paletteOpen} onClose={()=>setPaletteOpen(false)}
        officers={data.officers} skills={data.skills}
        onPickOfficer={o => { setTab("team"); setSelected(o); }}/>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
