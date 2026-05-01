// Top-level shell.

function Header({ tab, onTab, onSearch }) {
  const tabs = [
    { id:"team", label:"Team", count: window.STOA_DATA.officers.length },
    { id:"skills", label:"Skills", count: window.STOA_DATA.skills.length },
    { id:"meta", label:"Meta-aspects", count: window.STOA_DATA.metaAspects.length },
  ];
  return (
    <header style={{ position:"sticky", top:0, zIndex:10, background: ccPalette.bgSurface,
      borderBottom:`1px solid ${ccPalette.border1}` }}>
      <div style={{ display:"flex", alignItems:"center", padding:"10px 24px 0" }}>
        <Mark size={28}/>
        <span style={{ fontFamily:"Inter, sans-serif", fontSize:15, fontWeight:600, marginLeft:10, color: ccPalette.fg1 }}>The Stoa</span>
        <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:11, color: ccPalette.fg3, marginLeft:10,
          padding:"2px 8px", background: ccPalette.bgInset, borderRadius:4 }}>character-builder</span>
        <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap:10 }}>
          <button onClick={onSearch} style={{ display:"flex", alignItems:"center", gap:8,
            background: ccPalette.bgSunken, border:`1px solid ${ccPalette.border1}`, borderRadius:6,
            padding:"5px 10px", fontFamily:"Inter, sans-serif", fontSize:12, color: ccPalette.fg3, cursor:"pointer" }}>
            <Icon name="search" size={14}/>
            <span>Search…</span>
            <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:10, background: ccPalette.bgSurface,
              border:`1px solid ${ccPalette.border1}`, padding:"1px 5px", borderRadius:3, marginLeft:14 }}>⌘K</span>
          </button>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13}/>}>New agent</Button>
          <Icon name="settings" size={16} style={{ color: ccPalette.fg3, cursor:"pointer", marginLeft:4 }}/>
        </div>
      </div>
      <div style={{ display:"flex", padding:"4px 24px 0", gap:0, marginTop:6 }}>
        {tabs.map(t => (
          <div key={t.id} onClick={()=>onTab(t.id)} style={{
            padding:"12px 14px", marginBottom:-1, cursor:"pointer",
            fontFamily:"Inter, sans-serif", fontSize:13, fontWeight:500,
            color: tab === t.id ? ccPalette.fg1 : ccPalette.fg3,
            borderBottom: tab === t.id ? `2px solid ${ccPalette.accent}` : "2px solid transparent",
            display:"flex", alignItems:"center", gap:6 }}>
            <span>{t.label}</span>
            <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:11,
              color: tab === t.id ? ccPalette.fg3 : ccPalette.fg4 }}>{t.count}</span>
          </div>
        ))}
      </div>
    </header>
  );
}

function FilterSidebar({ rosterId, setRoster, archetypeFilter, setArchetype, archetypes }) {
  const rosters = [
    { id:"default", label:"default · 12 officers" },
    { id:"minimal", label:"minimal · 4 officers" },
    { id:"user-level", label:"user-level · 8 officers" },
    { id:"custom", label:"custom · start from scratch" },
  ];
  const labelStyle = { fontFamily:"Inter, sans-serif", fontSize:11, fontWeight:600, letterSpacing:"0.08em",
    textTransform:"uppercase", color: ccPalette.fg3, marginBottom:8 };
  const itemStyle = active => ({ fontFamily:"Inter, sans-serif", fontSize:12.5,
    padding:"6px 10px", borderRadius:6, cursor:"pointer",
    background: active ? ccPalette.accentSoft : "transparent",
    color: active ? ccPalette.accent : ccPalette.fg2,
    fontWeight: active ? 500 : 400 });
  return (
    <aside style={{ width:220, padding:"24px 16px", borderRight:`1px solid ${ccPalette.border1}`,
      background: ccPalette.bgSunken, minHeight:"calc(100vh - 110px)" }}>
      <div style={labelStyle}>Roster</div>
      <div style={{ display:"flex", flexDirection:"column", gap:2, marginBottom:24 }}>
        {rosters.map(r => <div key={r.id} onClick={()=>setRoster(r.id)} style={itemStyle(rosterId === r.id)}>{r.label}</div>)}
      </div>
      <div style={labelStyle}>Archetype</div>
      <div style={{ display:"flex", flexDirection:"column", gap:2 }}>
        <div onClick={()=>setArchetype(null)} style={itemStyle(!archetypeFilter)}>All</div>
        {Object.entries(archetypes).map(([a, c]) =>
          <div key={a} onClick={()=>setArchetype(a)} style={{ ...itemStyle(archetypeFilter === a),
            display:"flex", alignItems:"center", gap:8 }}>
            <span style={{ width:8, height:8, background:c, borderRadius:1 }}/>{a}
          </div>)}
      </div>
    </aside>
  );
}

function TeamView({ officers, archetypes, onPick }) {
  const sorted = [...officers].sort((a, b) => {
    const order = { major:0, captain:1, lieutenant:2 };
    return order[a.rank] - order[b.rank];
  });
  return (
    <div style={{ flex:1, padding:"24px 28px", overflow:"auto" }}>
      <div style={{ display:"flex", alignItems:"baseline", gap:12, marginBottom:18 }}>
        <h1 style={{ margin:0, fontFamily:"Inter, sans-serif", fontSize:24, fontWeight:600,
          letterSpacing:"-0.02em", color: ccPalette.fg1 }}>Team Overview</h1>
        <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:12, color: ccPalette.fg3 }}>
          {officers.length} officers · default roster
        </span>
      </div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(240px, 1fr))", gap:14 }}>
        {sorted.map(o => <OfficerCard key={o.name} officer={o} archColor={archetypes[o.archetype]} onClick={()=>onPick(o)}/>)}
      </div>
    </div>
  );
}

function OfficerDetail({ officer, archColor, onBack, body }) {
  const renderedBody = body
    .replace(/\{\{OFFICER_NAME\}\}/g, officer.name)
    .replace(/\{\{NICKNAME\}\}/g, officer.nickname);
  return (
    <div style={{ flex:1, display:"flex", overflow:"auto" }}>
      <div style={{ flex:1, padding:"24px 32px", maxWidth:920, overflow:"auto" }}>
        <div onClick={onBack} style={{ fontFamily:"Inter, sans-serif", fontSize:12,
          color: ccPalette.fg3, cursor:"pointer", display:"inline-flex", alignItems:"center", gap:5, marginBottom:14 }}>
          ← Back to Team
        </div>
        <div style={{ display:"flex", alignItems:"center", gap:10, flexWrap:"wrap", marginBottom:6 }}>
          <RankPill rank={officer.rank}/>
          <ArchetypeText archetype={officer.archetype} color={archColor}/>
        </div>
        <h1 style={{ margin:"4px 0 4px", fontFamily:"'JetBrains Mono', monospace", fontWeight:700,
          fontSize:30, letterSpacing:"0.01em", color: ccPalette.fg1 }}>{officer.name}</h1>
        <div style={{ fontFamily:"Inter, sans-serif", fontSize:15, color: ccPalette.fg2,
          lineHeight:1.55, maxWidth:"68ch", marginBottom:14, textWrap:"pretty" }}>{officer.role}</div>
        <div style={{ display:"flex", gap:8, marginBottom:24, flexWrap:"wrap" }}>
          <Button variant="secondary" size="sm" leading={<Icon name="edit" size={13}/>}>Edit</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="copy" size={13}/>}>Clone</Button>
          <Button variant="secondary" size="sm" leading={<Icon name="code" size={13}/>}>View JSON</Button>
          <Button variant="primary" size="sm" leading={<Icon name="plus" size={13}/>}>Add to roster</Button>
        </div>
        <div style={{ borderTop:`1px solid ${ccPalette.border1}`, paddingTop:20 }}>
          <BodyMarkdown text={renderedBody}/>
        </div>
      </div>
      <DetailSidebar officer={officer}/>
    </div>
  );
}

function DetailSidebar({ officer }) {
  const sectionLabel = { fontFamily:"Inter, sans-serif", fontSize:10.5, fontWeight:600, letterSpacing:"0.08em",
    textTransform:"uppercase", color: ccPalette.fg3, marginBottom:8 };
  return (
    <aside style={{ width:260, padding:"24px 24px 24px 16px", borderLeft:`1px solid ${ccPalette.border1}`,
      background: ccPalette.bgSurface, position:"sticky", top:110, alignSelf:"flex-start",
      height:"calc(100vh - 110px)", overflow:"auto", flexShrink:0 }}>
      <div style={sectionLabel}>Tools <span style={{ fontFamily:"'JetBrains Mono', monospace", color: ccPalette.fg4 }}>{officer.tools.length}</span></div>
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
      <div style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:13, color: ccPalette.fg1, marginBottom:20 }}>{officer.tier}</div>
      <div style={sectionLabel}>Body path</div>
      <div style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:11, color: ccPalette.fg2,
        wordBreak:"break-all", lineHeight:1.5 }}>definitions/bodies/{officer.name.toLowerCase()}.md</div>
    </aside>
  );
}

function BodyMarkdown({ text }) {
  // Tiny renderer: H1, H2, paragraphs, inline code, bold.
  const lines = text.split("\n");
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("# ")) {
      out.push(<h2 key={i} style={{ fontFamily:"Inter, sans-serif", fontSize:24, fontWeight:600,
        letterSpacing:"-0.02em", color: ccPalette.fg1, marginTop:24, marginBottom:10 }}>{line.slice(2)}</h2>);
    } else if (line.startsWith("## ")) {
      out.push(<h3 key={i} style={{ fontFamily:"Inter, sans-serif", fontSize:18, fontWeight:600,
        color: ccPalette.fg1, marginTop:22, marginBottom:8 }}>{line.slice(3)}</h3>);
    } else if (line.match(/^\d+\. /)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^\d+\. /)) { items.push(lines[i].replace(/^\d+\. /, "")); i++; }
      out.push(<ol key={i} style={{ fontFamily:"Inter, sans-serif", fontSize:14.5,
        color: ccPalette.fg2, lineHeight:1.65, paddingLeft:22, maxWidth:"68ch" }}>
        {items.map((t, j) => <li key={j} style={{ marginBottom:4 }}><InlineMD text={t}/></li>)}
      </ol>);
      continue;
    } else if (line.trim() === "") {
      // skip
    } else {
      out.push(<p key={i} style={{ fontFamily:"Inter, sans-serif", fontSize:14.5,
        color: ccPalette.fg2, lineHeight:1.65, maxWidth:"68ch", margin:"0 0 12px", textWrap:"pretty" }}>
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
      parts.push(<code key={"c"+i} style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:"0.88em",
        background: ccPalette.bgInset, border:`1px solid ${ccPalette.border1}`, padding:"1px 5px", borderRadius:3, color: ccPalette.fg1 }}>{text.slice(i + 1, end)}</code>);
      i = end + 1;
    } else if (text.slice(i, i + 2) === "**") {
      if (buf) { parts.push(buf); buf = ""; }
      const end = text.indexOf("**", i + 2);
      if (end === -1) { buf += text[i]; i++; continue; }
      parts.push(<strong key={"b"+i} style={{ color: ccPalette.fg1, fontWeight:600 }}>{text.slice(i + 2, end)}</strong>);
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
        <h1 style={{ margin:0, fontFamily:"Inter, sans-serif", fontSize:24, fontWeight:600,
          letterSpacing:"-0.02em", color: ccPalette.fg1 }}>Skill Library</h1>
        <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:12, color: ccPalette.fg3 }}>
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
      <h1 style={{ margin:"0 0 18px", fontFamily:"Inter, sans-serif", fontSize:24, fontWeight:600,
        letterSpacing:"-0.02em", color: ccPalette.fg1 }}>Meta-aspects</h1>
      <div style={{ display:"flex", flexDirection:"column", gap:8, maxWidth:760 }}>
        {items.map(m => (
          <div key={m.name} style={{ background: ccPalette.bgSurface, border:`1px solid ${ccPalette.border1}`,
            borderRadius:10, padding:"16px 18px" }}>
            <div style={{ fontFamily:"'JetBrains Mono', monospace", fontWeight:600, fontSize:13, color: ccPalette.fg1, marginBottom:4 }}>{m.name}</div>
            <div style={{ fontFamily:"Inter, sans-serif", fontSize:14, color: ccPalette.fg1, fontWeight:500, marginBottom:6 }}>{m.title}</div>
            <div style={{ fontFamily:"Inter, sans-serif", fontSize:13, color: ccPalette.fg2, lineHeight:1.55, textWrap:"pretty" }}>{m.summary}</div>
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
    <div style={{ background: ccPalette.bgApp, minHeight:"100vh", color: ccPalette.fg1 }}>
      <Header tab={tab} onTab={t => { setTab(t); setSelected(null); }} onSearch={()=>setPaletteOpen(true)}/>
      <div style={{ display:"flex", alignItems:"stretch" }}>
        {tab === "team" && !selected && <FilterSidebar rosterId={roster} setRoster={setRoster}
          archetypeFilter={archetypeFilter} setArchetype={setArchetypeFilter} archetypes={data.archetypes}/>}
        {tab === "team" && !selected && <TeamView officers={officers} archetypes={data.archetypes} onPick={setSelected}/>}
        {tab === "team" && selected && <OfficerDetail officer={selected} archColor={data.archetypes[selected.archetype]}
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
