/* Pages: Lernpfade & Fortschritt */

function LernpfadePage({ setPage }) {
  const t = useT();
  const lang = window.__lang || "de";

  const pfade = [
    { id:"start", de:"Erste Schritte", en:"First Steps", icon:"play",
      sub_de:"Vom Dilemma zum Gleichgewicht", sub_en:"From dilemma to equilibrium",
      desc_de:"Vier klassische Spiele, die jede:r einmal gespielt haben sollte. Du lernst, was Nash gemeint hat.",
      desc_en:"Four classic games everyone should play once. You'll learn what Nash actually meant.",
      n: 4, time:"30 min", level_de:"Einstieg", level_en:"Beginner",
      points:["Was ist ein Nash-Gleichgewicht?","Dominante Strategien erkennen","Wann Kooperation rational ist","Pareto vs. Nash"],
      points_en:["What is a Nash equilibrium?","Spot dominant strategies","When cooperation is rational","Pareto vs. Nash"]},
    { id:"axelrod", de:"Axelrods Turnier", en:"Axelrod's Tournament", icon:"infinity",
      sub_de:"Wie Tit-for-Tat die Welt gewann", sub_en:"How Tit-for-Tat won the world",
      desc_de:"Die berühmte Computersimulation von 1980 — und was sie über Kooperation in der Natur verrät.",
      desc_en:"The famous 1980 computer simulation — and what it reveals about cooperation in nature.",
      n: 6, time:"50 min", level_de:"Mittel", level_en:"Intermediate",
      points:["Wiederholte Spiele","Tit-for-Tat & Varianten","Grim Trigger","Nice, retaliating, forgiving, clear"],
      points_en:["Repeated games","Tit-for-Tat & variants","Grim Trigger","Nice, retaliating, forgiving, clear"]},
    { id:"behave", de:"Wenn Menschen irrational sind", en:"When humans are irrational", icon:"feather",
      sub_de:"Kahneman trifft Spieltheorie", sub_en:"Kahneman meets game theory",
      desc_de:"Ultimatum, Diktator, Framing — was passiert, wenn echte Menschen statt Homo Oeconomicus spielen.",
      desc_en:"Ultimatum, dictator, framing — what happens when real people play instead of homo oeconomicus.",
      n: 5, time:"40 min", level_de:"Mittel", level_en:"Intermediate",
      points:["Prospect Theory","Faire Angebote","Loss Aversion","Soziale Präferenzen"],
      points_en:["Prospect theory","Fair offers","Loss aversion","Social preferences"]},
    { id:"market", de:"Märkte & Auktionen", en:"Markets & Auctions", icon:"auction",
      sub_de:"Mechanism Design in Aktion", sub_en:"Mechanism design in action",
      desc_de:"Wie versteckte Werte zum Vorschein kommen — vom eBay-Bid bis zum Spektrum-Auktion.",
      desc_en:"How hidden values come out — from eBay bidding to spectrum auctions.",
      n: 5, time:"45 min", level_de:"Fortgeschritten", level_en:"Advanced",
      points:["Erstpreis vs. Vickrey","Fluch des Gewinners","Optimale Bietfunktion","Revenue Equivalence"],
      points_en:["First-price vs. Vickrey","Winner's curse","Optimal bid functions","Revenue equivalence"]},
    { id:"evo", de:"Evolutionäre Spiele", en:"Evolutionary Games", icon:"tree",
      sub_de:"Strategien, die sich durchsetzen", sub_en:"Strategies that survive",
      desc_de:"Maynard Smith brachte Spieltheorie zur Biologie. Hier siehst du, wie aus Spielen Populationen werden.",
      desc_en:"Maynard Smith brought game theory to biology. Here you see how games become populations.",
      n: 5, time:"55 min", level_de:"Fortgeschritten", level_en:"Advanced",
      points:["ESS","Replicator-Dynamik","Habicht-Taube","Public Goods"],
      points_en:["ESS","Replicator dynamics","Hawk-Dove","Public goods"]},
    { id:"verhandeln", de:"Praktisches Verhandeln", en:"Practical Negotiation", icon:"handshake",
      sub_de:"Vom Modell zur Methode", sub_en:"From model to method",
      desc_de:"Fisher & Ury, BATNA, taktische Empathie — die Brücke von Theorie zu echten Verhandlungen.",
      desc_en:"Fisher & Ury, BATNA, tactical empathy — the bridge from theory to real negotiations.",
      n: 6, time:"60 min", level_de:"Praxis", level_en:"Applied",
      points:["BATNA","Harvard-Konzept","Taktische Empathie","Anker & Konzessionen"],
      points_en:["BATNA","Harvard method","Tactical empathy","Anchors & concessions"]},
  ];

  return (
    <div className="page wrap">
      <section style={{padding: "64px 0 40px"}}>
        <div className="eyebrow" style={{marginBottom: 24}}>※ 6 {lang==="de"?"Routen · 31 Spiele":"Routes · 31 Games"}</div>
        <h1 className="display" style={{fontSize: "clamp(48px, 7vw, 96px)", margin: 0, maxWidth: 920}}>
          {t.pfade_title[0]}<br/>
          <span className="display-italic" style={{color:"var(--accent)"}}>{t.pfade_title[1]}</span>
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-soft)", maxWidth: 640, marginTop: 32, lineHeight: 1.55}}>{t.pfade_lede}</p>
      </section>

      <section style={{padding: "32px 0", borderTop:"1px solid var(--ink)", display:"grid", gridTemplateColumns:"repeat(2, 1fr)", gap:16}}>
        {pfade.map((p, i)=>(
          <a key={p.id} href="#" className="card card-hover" style={{padding: 28, display:"grid", gridTemplateColumns:"56px 1fr", gap: 20, position:"relative"}}>
            <div style={{display:"flex", flexDirection:"column", alignItems:"center", gap:12}}>
              <div style={{width:48,height:48,border:"1px solid var(--line)",borderRadius:"50%",display:"grid",placeItems:"center",color:"var(--ink-soft)"}}>
                <Icon name={p.icon} size={20}/>
              </div>
              <div className="mono" style={{fontSize:11, color:"var(--ink-faint)"}}>0{i+1}</div>
            </div>
            <div>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", gap:12, marginBottom:8}}>
                <div className="display" style={{fontSize:26, lineHeight:1.1}}>{lang==="de"?p.de:p.en}</div>
                <span className="mono" style={{fontSize:11, color:"var(--accent)"}}>{lang==="de"?p.level_de:p.level_en}</span>
              </div>
              <div className="display-italic" style={{fontSize:15, color:"var(--ink-mute)", marginBottom: 12}}>{lang==="de"?p.sub_de:p.sub_en}</div>
              <p style={{fontSize:13.5, color:"var(--ink-soft)", margin:"0 0 16px", lineHeight:1.55}}>{lang==="de"?p.desc_de:p.desc_en}</p>
              <div style={{display:"flex", gap: 16, marginBottom: 16, flexWrap:"wrap"}}>
                <span className="mono" style={{fontSize:11, color:"var(--ink-mute)"}}>{p.n} {lang==="de"?"Spiele":"games"}</span>
                <span className="mono" style={{fontSize:11, color:"var(--ink-mute)"}}>· {p.time}</span>
              </div>
              <div style={{borderTop:"1px dashed var(--line)", paddingTop: 14, display:"flex", flexDirection:"column", gap:5}}>
                {(lang==="de"?p.points:p.points_en).slice(0,3).map((x,j)=>(
                  <div key={j} style={{fontSize:12.5, color:"var(--ink-soft)", display:"flex", gap:8, alignItems:"baseline"}}>
                    <span style={{color:"var(--gold)"}}>·</span> <span>{x}</span>
                  </div>
                ))}
              </div>
            </div>
          </a>
        ))}
      </section>
      <div style={{height: 80}}/>
    </div>
  );
}

function FortschrittPage() {
  const t = useT();
  const lang = window.__lang || "de";
  const stats = [
    { label: t.stat_games, value: 47, sub: lang==="de"?"insgesamt":"total" },
    { label: t.stat_score, value: "2,184", sub: lang==="de"?"über alle Spiele":"all games" },
    { label: t.avg, value: 46, sub: lang==="de"?"pro Spiel":"per game" },
    { label: t.best, value: 52, sub: "Stag Hunt" },
  ];
  const series = [12,18,15,22,19,28,25,32,30,38,42,40,46,44,51,48,52,46,49,52];

  const perGame = [
    { id:"gefangenendilemma", n:14, best:42, avg:34 },
    { id:"ultimatum", n:9, best:28, avg:18 },
    { id:"stag-hunt", n:7, best:52, avg:38 },
    { id:"chicken", n:5, best:24, avg:14 },
    { id:"vertrauen", n:6, best:33, avg:22 },
    { id:"beauty-contest", n:3, best:30, avg:24 },
  ];

  return (
    <div className="page wrap">
      <section style={{padding: "64px 0 40px"}}>
        <div className="eyebrow" style={{marginBottom: 24}}>※ {lang==="de"?"Spielername · Stand heute":"Player · Today"}</div>
        <h1 className="display" style={{fontSize: "clamp(48px, 7vw, 96px)", margin: 0, maxWidth: 920}}>
          {t.fortschritt_title[0]} <span className="display-italic" style={{color:"var(--accent)"}}>{t.fortschritt_title[1]}</span>
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-soft)", maxWidth: 640, marginTop: 32, lineHeight: 1.55}}>{t.fortschritt_lede}</p>
      </section>

      <section style={{borderTop:"1px solid var(--ink)", borderBottom:"1px solid var(--line)", margin:"0 -28px", display:"grid", gridTemplateColumns:"repeat(4,1fr)"}}>
        {stats.map((s,i)=>(
          <div key={i} style={{padding:"28px 24px", borderRight: i<3?"1px solid var(--line)":"none"}}>
            <div className="eyebrow">{s.label}</div>
            <div className="display" style={{fontSize:48, lineHeight:1.05, marginTop: 6}}>{s.value}</div>
            <div className="mono" style={{fontSize:11, color:"var(--ink-mute)", marginTop:4}}>{s.sub}</div>
          </div>
        ))}
      </section>

      <section style={{padding: "48px 0", borderBottom:"1px solid var(--line)"}}>
        <div className="eyebrow" style={{color:"var(--accent)", marginBottom: 14}}>{t.score_history}</div>
        <ScoreChart data={series}/>
      </section>

      <section style={{padding:"48px 0"}}>
        <div className="eyebrow" style={{color:"var(--accent)", marginBottom: 14}}>{lang==="de"?"Pro Spiel":"Per game"}</div>
        <div style={{display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:0, border:"1px solid var(--line)", borderRadius:"var(--r-lg)", overflow:"hidden", background:"var(--bg-elev)"}}>
          {perGame.map((row, i)=>{
            const g = GAMES.find(x=>x.id===row.id);
            return (
              <div key={i} style={{padding:"20px 22px", borderRight: i%2===0?"1px solid var(--line)":"none", borderBottom: i<perGame.length-2?"1px solid var(--line)":"none", display:"grid", gridTemplateColumns:"32px 1fr auto auto", gap: 18, alignItems:"center"}}>
                <span style={{color:"var(--ink-mute)"}}><Icon name={g.icon} size={18}/></span>
                <div>
                  <div style={{fontSize:14.5, fontWeight:500}}>{lang==="de"?g.de:g.en}</div>
                  <div className="mono" style={{fontSize:11, color:"var(--ink-mute)", marginTop:2}}>{row.n} {lang==="de"?"Partien":"sessions"} · {t.avg} {row.avg}</div>
                </div>
                <div style={{textAlign:"right"}}>
                  <div className="mono" style={{fontSize:18, color:"var(--gold)"}}>{row.best}</div>
                  <div className="eyebrow" style={{fontSize:9}}>{t.best}</div>
                </div>
                <Icon name="arrow-right" size={14}/>
              </div>
            );
          })}
        </div>
      </section>
      <div style={{height: 80}}/>
    </div>
  );
}

function ScoreChart({ data }) {
  const w=900, h=160, p=20;
  const max = Math.max(...data), min = Math.min(...data);
  const dx = (w-p*2)/(data.length-1);
  const pts = data.map((v,i)=>[p+i*dx, h-p-((v-min)/(max-min))*(h-p*2)]);
  const path = "M " + pts.map(p=>p.join(" ")).join(" L ");
  const area = path + ` L ${w-p} ${h-p} L ${p} ${h-p} Z`;
  return (
    <svg viewBox={`0 0 ${w} ${h}`} style={{width:"100%", display:"block"}}>
      {[0,1,2,3].map(i => (
        <line key={i} x1={p} x2={w-p} y1={p + i*((h-p*2)/3)} y2={p + i*((h-p*2)/3)} stroke="var(--line-soft)" strokeWidth="1"/>
      ))}
      <path d={area} fill="var(--accent-soft)" opacity="0.5"/>
      <path d={path} fill="none" stroke="var(--accent)" strokeWidth="2"/>
      {pts.map(([x,y],i)=>(<circle key={i} cx={x} cy={y} r="2.5" fill="var(--bg-elev)" stroke="var(--accent)" strokeWidth="1.5"/>))}
    </svg>
  );
}

window.LernpfadePage = LernpfadePage;
window.FortschrittPage = FortschrittPage;
