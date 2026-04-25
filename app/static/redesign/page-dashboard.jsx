/* Page: Dashboard */
const { useState: useStateD, useEffect: useEffectD } = React;

function useDashboardStats() {
  const [stats, setStats] = useStateD(null);
  useEffectD(() => {
    fetch("/api/redesign/stats")
      .then(r => r.json())
      .then(setStats)
      .catch(() => {});
  }, []);
  return stats;
}

function Hero() {
  const t = useT();
  return (
    <section style={{padding: "72px 0 56px"}}>
      <div className="eyebrow" style={{marginBottom: 28}}>※ {t.eyebrow_intro}</div>
      <h1 className="display" style={{fontSize: "clamp(56px, 8vw, 112px)", margin: 0, maxWidth: 980}}>
        {t.hero_title[0]}<br/>
        <span className="display-italic" style={{color: "var(--accent)"}}>{t.hero_title[1]}</span><br/>
        {t.hero_title[2]}
      </h1>
      <div className="hero-cta-row" style={{display:"grid", gridTemplateColumns:"1.1fr 1fr", gap:48, marginTop: 44, alignItems:"end"}}>
        <p style={{fontSize: 18, lineHeight: 1.55, color: "var(--ink-soft)", maxWidth: 560, margin: 0}}>{t.hero_lede}</p>
        <div style={{display:"flex", gap:10, justifyContent:"flex-end", flexWrap:"wrap"}}>
          <a href="#" className="btn btn-primary btn-large">
            <Icon name="play" size={13}/> {t.cta_start}
          </a>
          <a href="#" className="btn btn-ghost btn-large">{t.cta_browse}<Icon name="arrow-right" size={14}/></a>
        </div>
      </div>
    </section>
  );
}

function StatStrip({ apiStats }) {
  const t = useT();
  const d = apiStats;
  const stats = [
    { label: t.stat_games,   value: d ? String(d.total_games) : "…",
      spark: d ? [1,2,3,4,5,6,7,8,9,d.total_games] : [] },
    { label: t.stat_score,   value: d ? d.total_score.toLocaleString("de-DE") : "…",
      spark: d ? [10,20,30,40,50,60,70,80,90,d.total_score/50] : [] },
    { label: t.stat_lessons, value: d ? `${d.lessons_viewed} / ${d.total_lessons}` : "…",
      spark: d ? [1,2,3,4,5,6,7,8,9,d.lessons_viewed] : [] },
    { label: t.stat_badges,  value: d ? `${d.unlocked_achievements} / ${d.total_achievements}` : "…",
      spark: d ? [1,2,3,4,5,6,7,8,9,d.unlocked_achievements] : [] },
  ];
  return (
    <section style={{borderTop: "1px solid var(--ink)", borderBottom: "1px solid var(--line)", margin:"0 -28px"}}>
      <div className="wrap stat-strip-grid" style={{gridTemplateColumns: "repeat(4, 1fr)", padding: 0}}>
        {stats.map((s,i) => (
          <div key={i} style={{padding: "28px 24px", borderRight: i<3?"1px solid var(--line)":"none", display:"flex", flexDirection:"column", gap:8}}>
            <div className="eyebrow">{s.label}</div>
            <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end"}}>
              <div className="display" style={{fontSize: 44}}>{s.value}</div>
              <Sparkline data={s.spark}/>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function Sparkline({ data, w=64, h=22 }) {
  const max = Math.max(...data), min = Math.min(...data);
  const dx = w / (data.length - 1);
  const pts = data.map((v,i) => `${i*dx},${h - ((v-min)/(max-min||1))*h}`).join(" ");
  return (
    <svg width={w} height={h} className="spark">
      <polyline points={pts} fill="none" stroke="var(--ink-mute)" strokeWidth="1.2"/>
      <circle cx={w} cy={h - ((data[data.length-1]-min)/(max-min||1))*h} r="2" fill="var(--accent)"/>
    </svg>
  );
}

function Recommended({ setPage, setActiveGame }) {
  const t = useT();
  const lang = window.__lang || "de";
  const featured = GAMES[0];
  return (
    <section style={{padding: "56px 0"}}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", marginBottom: 28}}>
        <h2 className="display" style={{fontSize: 36, margin:0}}>{t.section_recommended}</h2>
        <div className="eyebrow">— Tag 4 / 28</div>
      </div>
      <div className="card recommended-grid" style={{display:"grid", gridTemplateColumns:"1.2fr 1fr", overflow:"hidden"}}>
        <div style={{padding: 36, display:"flex", flexDirection:"column", justifyContent:"space-between", borderRight:"1px solid var(--line)"}}>
          <div>
            <div style={{display:"flex", gap:8, marginBottom:18}}>
              <span className="tag tag-accent">Lektion 04</span>
              <span className="tag">Wiederholte Spiele</span>
            </div>
            <h3 className="display" style={{fontSize: 38, margin: "0 0 16px", maxWidth: 420}}>
              Warum <span className="display-italic">Tit‑for‑Tat</span> Axelrods Turnier gewann.
            </h3>
            <p style={{color:"var(--ink-soft)", margin:0, maxWidth: 480, fontSize: 15.5}}>
              {lang==="de"
                ? "Eine Strategie aus vier Zeilen Code schlug 1980 die ausgeklügeltsten Algorithmen der Welt. Wir spielen sie nach — und du siehst, warum nice, retaliating, forgiving und clear gewinnen."
                : "A four-line strategy beat the world's most sophisticated algorithms in 1980. We replay it — and you'll see why nice, retaliating, forgiving and clear wins."}
            </p>
          </div>
          <div style={{display:"flex", gap:12, alignItems:"center", marginTop: 28}}>
            <a href="#" className="btn btn-primary">{t.read_more}<Icon name="arrow-right" size={14}/></a>
            <span style={{fontSize:13, color:"var(--ink-mute)"}}>≈ 7 min</span>
          </div>
        </div>
        <div style={{background:"var(--bg-sunk)", padding: 36, display:"flex", flexDirection:"column", gap: 16}}>
          <div className="eyebrow">{t.payoff_matrix}</div>
          <PayoffMatrix small/>
          <div className="eyebrow" style={{marginTop:8}}>Score · Axelrod 1980</div>
          <div style={{display:"flex", flexDirection:"column", gap: 8}}>
            {[
              {n:"Tit-for-Tat", v:504, w:100, hl:true},
              {n:"Tideman & Chieruzzi", v:500, w:99},
              {n:"Nydegger", v:486, w:96},
              {n:"Grofman", v:482, w:96},
              {n:"Random", v:276, w:55, mute:true},
            ].map((r,i) => (
              <div key={i} style={{display:"grid", gridTemplateColumns:"1fr 40px", gap:10, alignItems:"center"}}>
                <div>
                  <div className="mono" style={{fontSize:11, color: r.mute?"var(--ink-faint)":"var(--ink-soft)", marginBottom:3}}>{r.n}</div>
                  <div className="progress"><div className={"progress-fill" + (r.hl?" gold":"")} style={{width: r.w+"%"}}/></div>
                </div>
                <div className="mono" style={{fontSize:12, textAlign:"right", color: r.hl?"var(--gold)":"var(--ink-mute)", fontWeight: r.hl?600:400}}>{r.v}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function PayoffMatrix({ small }) {
  const t = useT();
  const lang = window.__lang || "de";
  return (
    <div className="matrix" style={{borderRadius: 8, overflow: "hidden", border:"1px solid var(--line)", fontSize: small?12:14}}>
      <div className="matrix-cell matrix-header"></div>
      <div className="matrix-cell matrix-header">B: {lang==="de"?"Koop.":"Coop."}</div>
      <div className="matrix-cell matrix-header">B: {lang==="de"?"Verrat":"Defect"}</div>
      <div className="matrix-row" style={{display:"contents"}}>
        <div className="matrix-cell matrix-header">A: {lang==="de"?"Koop.":"Coop."}</div>
        <div className="matrix-cell matrix-payoff">3, 3</div>
        <div className="matrix-cell matrix-payoff" style={{color:"var(--ink-mute)"}}>0, 5</div>
      </div>
      <div className="matrix-row" style={{display:"contents"}}>
        <div className="matrix-cell matrix-header">A: {lang==="de"?"Verrat":"Defect"}</div>
        <div className="matrix-cell matrix-payoff" style={{color:"var(--ink-mute)"}}>5, 0</div>
        <div className="matrix-cell matrix-payoff matrix-nash">
          1, 1
          <span className="matrix-nash-tag">NASH</span>
        </div>
      </div>
    </div>
  );
}

function ConceptsInFocus() {
  const t = useT();
  const lang = window.__lang || "de";
  const items = [
    { n: "Nash-Gleichgewicht", en: "Nash equilibrium", y: "1951", a: "John F. Nash", icon:"scales" },
    { n: "Tit-for-Tat", en: "Tit-for-Tat", y: "1984", a: "Robert Axelrod", icon:"handshake" },
    { n: "Prospect Theory", en: "Prospect theory", y: "1979", a: "Kahneman & Tversky", icon:"chart" },
    { n: "Brinkmanship", en: "Brinkmanship", y: "1960", a: "Thomas Schelling", icon:"crosshair" },
  ];
  return (
    <section style={{padding: "56px 0", borderTop: "1px solid var(--line)"}}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", marginBottom: 28}}>
        <h2 className="display" style={{fontSize: 36, margin: 0}}>{t.section_concepts}</h2>
        <a href="#" className="arrow-link">{lang==="de"?"Alle Konzepte":"All concepts"}<Icon name="arrow-up-right" size={13}/></a>
      </div>
      <div className="concepts-grid" style={{gridTemplateColumns:"repeat(4, 1fr)", gap: 16}}>
        {items.map((c,i)=>(
          <a key={i} href="#" className="card card-hover" style={{padding: 22, display:"flex", flexDirection:"column", gap: 16, minHeight: 200}}>
            <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
              <span style={{color:"var(--ink-mute)"}}><Icon name={c.icon} size={20}/></span>
              <span className="mono" style={{fontSize: 11, color:"var(--gold)"}}>{c.y}</span>
            </div>
            <div>
              <div className="display" style={{fontSize: 22, marginBottom: 6, lineHeight: 1.15}}>{lang==="de"?c.n:c.en}</div>
              <div style={{fontSize: 12.5, color:"var(--ink-mute)"}}>{c.a}</div>
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}

function RecentSessions({ apiStats }) {
  const t = useT();
  const lang = window.__lang || "de";
  const sessions = apiStats ? apiStats.recent_sessions : [];
  return (
    <section style={{padding: "56px 0", borderTop: "1px solid var(--line)"}}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", marginBottom: 24}}>
        <h2 className="display" style={{fontSize: 36, margin: 0}}>{t.section_recent}</h2>
        <a href="#" className="arrow-link">{lang==="de"?"Vollständig":"All sessions"}<Icon name="arrow-up-right" size={13}/></a>
      </div>
      <div className="card" style={{overflow: "hidden"}}>
        {sessions.length === 0 && (
          <div style={{padding:"32px 24px", color:"var(--ink-mute)", fontSize:14}}>
            {lang==="de" ? "Noch keine Spiele gespielt." : "No games played yet."}
          </div>
        )}
        {sessions.map((s,i)=>{
          const resColor = s.result==="win"?"var(--cooperate)":s.result==="loss"?"var(--accent)":"var(--ink-mute)";
          const resLabel = lang==="de"
            ? (s.result==="win"?"Gewonnen":s.result==="loss"?"Verloren":"Unentschieden")
            : (s.result==="win"?"Won":s.result==="loss"?"Lost":"Draw");
          return (
            <div key={i} style={{display:"grid", gridTemplateColumns:"36px 1fr auto auto", padding:"16px 20px", alignItems:"center", borderBottom: i<sessions.length-1?"1px solid var(--line)":"none", gap:14}}>
              <span style={{fontSize:20, lineHeight:1}}>{s.game_icon}</span>
              <div>
                <div style={{fontSize: 15, fontWeight: 500}}>{s.game_name}</div>
                <div className="mono" style={{fontSize:11, color:"var(--ink-mute)", marginTop:2}}>{s.date}</div>
              </div>
              <div className="mono" style={{fontSize: 13, color: resColor}}>{resLabel}</div>
              <div className="mono" style={{fontSize: 14, textAlign:"right"}}>{s.score} <span style={{color:"var(--ink-mute)", fontSize:11}}>{lang==="de"?"Pkt.":"pts"}</span></div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function Dashboard({ setPage, setActiveGame }) {
  const apiStats = useDashboardStats();
  return (
    <div className="page wrap">
      <Hero/>
      <StatStrip apiStats={apiStats}/>
      <Recommended setPage={setPage} setActiveGame={setActiveGame}/>
      <ConceptsInFocus/>
      <RecentSessions apiStats={apiStats}/>
      <div style={{height: 80}}/>
    </div>
  );
}

window.Dashboard = Dashboard;
window.PayoffMatrix = PayoffMatrix;
