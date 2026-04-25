/* Pages: Konzepte, Lernpfade, Fortschritt */

function KonzeptePage() {
  const t = useT();
  const lang = window.__lang || "de";
  const [active, setActive] = React.useState(0);

  const examples = [
    { name: "Gefangenendilemma", en: "Prisoner's Dilemma",
      rows: ["Koop.","Verrat"], rows_en:["Coop.","Defect"],
      cols: ["Koop.","Verrat"], cols_en:["Coop.","Defect"],
      payoffs: [[[3,3],[0,5]],[[5,0],[1,1]]],
      nash: [[1,1]],
      info_de: "Beide haben eine dominante Strategie zu verraten. Das einzige Nash-Gleichgewicht ist (Verrat, Verrat) — obwohl beide bei Kooperation mehr verdienen würden.",
      info_en: "Both players have a dominant strategy to defect. The only Nash equilibrium is (Defect, Defect) — though both would earn more by cooperating." },
    { name: "Hirschjagd", en: "Stag Hunt",
      rows:["Hirsch","Hase"], rows_en:["Stag","Hare"],
      cols:["Hirsch","Hase"], cols_en:["Stag","Hare"],
      payoffs: [[[5,5],[0,3]],[[3,0],[3,3]]],
      nash: [[0,0],[1,1]],
      info_de: "Zwei Nash-Gleichgewichte: (Hirsch, Hirsch) ist auszahlungsdominant, (Hase, Hase) ist risikodominant.",
      info_en: "Two Nash equilibria: (Stag, Stag) is payoff-dominant, (Hare, Hare) is risk-dominant." },
    { name: "Chicken", en: "Chicken",
      rows:["Geradeaus","Ausweichen"], rows_en:["Straight","Swerve"],
      cols:["Geradeaus","Ausweichen"], cols_en:["Straight","Swerve"],
      payoffs: [[[0,0],[4,1]],[[1,4],[2,2]]],
      nash: [[0,1],[1,0]],
      info_de: "Zwei reine Nash-Gleichgewichte in asymmetrischen Outcomes — plus ein gemischtes.",
      info_en: "Two pure Nash equilibria in asymmetric outcomes — plus a mixed one." },
  ];

  return (
    <div className="page wrap">
      <section style={{padding: "64px 0 40px"}}>
        <div className="eyebrow" style={{marginBottom: 24}}>※ {lang==="de"?"Theorie":"Theory"}</div>
        <h1 className="display" style={{fontSize: "clamp(48px, 7vw, 96px)", margin: 0, maxWidth: 920}}>
          {t.konzepte_title[0]}<br/>
          <span className="display-italic" style={{color:"var(--accent)"}}>{t.konzepte_title[1]}</span> {t.konzepte_title[2]}
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-soft)", maxWidth: 640, marginTop: 32, lineHeight: 1.55}}>{t.konzepte_lede}</p>
      </section>

      {/* Nash finder */}
      <section style={{padding: "48px 0", borderTop:"1px solid var(--ink)"}}>
        <div style={{display:"grid", gridTemplateColumns:"320px 1fr", gap: 56, alignItems:"start"}}>
          <div>
            <div className="eyebrow" style={{color:"var(--accent)", marginBottom:10}}>01 / Interaktiv</div>
            <h2 className="display" style={{fontSize:34, margin:0, lineHeight:1.1, marginBottom: 18}}>
              Der <span className="display-italic">Nash‑</span>Finder.
            </h2>
            <p style={{fontSize:14.5, color:"var(--ink-soft)", lineHeight:1.6, marginBottom: 24}}>
              {lang==="de"
                ? "Wähle ein Spiel und sieh, wo die Gleichgewichte liegen. Markierte Felder sind Strategien, von denen kein Spieler einseitig abweichen will."
                : "Pick a game and see where the equilibria lie. Highlighted cells are strategies from which no player wants to deviate unilaterally."}
            </p>
            <div style={{display:"flex", flexDirection:"column", gap: 4}}>
              {examples.map((e,i)=>(
                <button key={i} onClick={()=>setActive(i)} style={{
                  textAlign:"left", padding:"12px 14px", borderRadius:8, border:"1px solid "+(active===i?"var(--ink)":"transparent"),
                  background: active===i?"var(--bg-elev)":"transparent",
                  color: active===i?"var(--ink)":"var(--ink-soft)", cursor:"pointer", fontSize:14
                }}>
                  <div style={{display:"flex", justifyContent:"space-between"}}>
                    <span>{lang==="de"?e.name:e.en}</span>
                    <span className="mono" style={{fontSize:11,color:"var(--ink-mute)"}}>{e.nash.length}× NE</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
          <div>
            <NashMatrix ex={examples[active]} lang={lang}/>
            <div className="card" style={{padding:18, marginTop: 18, background:"var(--bg-sunk)", borderColor:"var(--line-soft)"}}>
              <p style={{margin:0, fontSize:14, color:"var(--ink-soft)", lineHeight:1.55}}>
                <strong style={{color:"var(--ink)"}}>{lang==="de"?"Erklärung. ":"Explanation. "}</strong>
                {lang==="de"?examples[active].info_de:examples[active].info_en}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Concept map */}
      <section style={{padding: "48px 0", borderTop:"1px solid var(--line)"}}>
        <div className="eyebrow" style={{color:"var(--accent)", marginBottom:10}}>02 / {lang==="de"?"Karte":"Map"}</div>
        <h2 className="display" style={{fontSize:34, margin:"0 0 32px"}}>{lang==="de"?"Die Konzeptkarte":"The concept map"}.</h2>
        <div style={{display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:16}}>
          {[
            { de:"Fundamente", en:"Foundations", icon:"scales", items:["Nash-Gleichgewicht","Dominante Strategie","Pareto-Effizienz","Rückwärtsinduktion","Gemischte Strategien"], items_en:["Nash equilibrium","Dominant strategy","Pareto efficiency","Backward induction","Mixed strategies"]},
            { de:"Kooperation", en:"Cooperation", icon:"handshake", items:["Tit-for-Tat","Wiederholte Spiele","Grim Trigger","Reputation","Folk-Theorem"], items_en:["Tit-for-Tat","Repeated games","Grim Trigger","Reputation","Folk theorem"]},
            { de:"Information", en:"Information", icon:"feather", items:["Adverse Selektion","Signaling","Screening","Cheap Talk","Bayesianische Spiele"], items_en:["Adverse selection","Signaling","Screening","Cheap talk","Bayesian games"]},
            { de:"Fortgeschritten", en:"Advanced", icon:"sparkle", items:["Mechanismus-Design","Shapley-Wert","ESS","Auktionstheorie","Matching"], items_en:["Mechanism design","Shapley value","ESS","Auction theory","Matching"]},
          ].map((g,i)=>(
            <div key={i} className="card" style={{padding:22, display:"flex", flexDirection:"column", gap:14, minHeight: 280}}>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
                <span style={{color:"var(--ink-mute)"}}><Icon name={g.icon} size={20}/></span>
                <span className="mono" style={{fontSize:11, color:"var(--ink-faint)"}}>0{i+1}</span>
              </div>
              <div className="display" style={{fontSize:22, lineHeight:1.1}}>{lang==="de"?g.de:g.en}</div>
              <div style={{display:"flex", flexDirection:"column", gap:6}}>
                {(lang==="de"?g.items:g.items_en).map((it,j)=>(
                  <a key={j} href="#" style={{fontSize:13.5, color:"var(--ink-soft)", display:"flex", justifyContent:"space-between", padding:"4px 0", borderBottom: j<4?"1px dashed var(--line-soft)":"none"}}>
                    <span>{it}</span>
                    <span style={{color:"var(--ink-faint)"}}>→</span>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Nobel timeline */}
      <section style={{padding: "48px 0", borderTop:"1px solid var(--line)"}}>
        <div className="eyebrow" style={{color:"var(--accent)", marginBottom:10}}>03 / Nobel</div>
        <h2 className="display" style={{fontSize:34, margin:"0 0 32px"}}>
          {lang==="de"?"Die Köpfe hinter":"The minds behind"} <span className="display-italic">{lang==="de"?"der Theorie":"the theory"}</span>.
        </h2>
        <div style={{borderLeft:"1px solid var(--line)", marginLeft: 20}}>
          {[
            {y:"1994", n:"Nash · Harsanyi · Selten", w:lang==="de"?"Nicht-kooperative Spieltheorie":"Non-cooperative game theory"},
            {y:"2002", n:"Kahneman · Smith", w:lang==="de"?"Verhaltensökonomik & Experimente":"Behavioral economics & experiments"},
            {y:"2005", n:"Aumann · Schelling", w:lang==="de"?"Konflikt & Kooperation":"Conflict & cooperation"},
            {y:"2007", n:"Hurwicz · Maskin · Myerson", w:"Mechanism design"},
            {y:"2012", n:"Roth · Shapley", w:lang==="de"?"Stabile Allokation & Markt-Design":"Stable allocation & market design"},
            {y:"2020", n:"Milgrom · Wilson", w:lang==="de"?"Auktionstheorie":"Auction theory"},
          ].map((e,i)=>(
            <div key={i} style={{padding:"22px 0 22px 32px", position:"relative", borderBottom: i<5?"1px solid var(--line-soft)":"none"}}>
              <span style={{position:"absolute", left:-5, top:30, width:9, height:9, background:"var(--gold)", borderRadius:"50%", border:"2px solid var(--bg)"}}></span>
              <div style={{display:"grid", gridTemplateColumns:"80px 1fr 1fr", gap:24, alignItems:"baseline"}}>
                <div className="mono" style={{fontSize:14, color:"var(--gold)", fontWeight:600}}>{e.y}</div>
                <div className="display" style={{fontSize:20}}>{e.n}</div>
                <div style={{fontSize:14, color:"var(--ink-soft)"}}>{e.w}</div>
              </div>
            </div>
          ))}
        </div>
      </section>
      <div style={{height: 80}}/>
    </div>
  );
}

function NashMatrix({ ex, lang }) {
  const rows = lang==="de"?ex.rows:ex.rows_en;
  const cols = lang==="de"?ex.cols:ex.cols_en;
  return (
    <div className="card" style={{padding: 24, background:"var(--bg-elev)"}}>
      <div className="matrix" style={{gridTemplateColumns: `auto repeat(${cols.length}, 1fr)`}}>
        <div className="matrix-cell matrix-header" style={{background:"transparent", borderRight:0, borderBottom:0}}></div>
        {cols.map((c,i)=>(<div key={i} className="matrix-cell matrix-header">B: {c}</div>))}
        {rows.map((r,ri)=>(
          <React.Fragment key={ri}>
            <div className="matrix-cell matrix-header">A: {r}</div>
            {ex.payoffs[ri].map((p,ci)=>{
              const isNash = ex.nash.some(n=>n[0]===ri&&n[1]===ci);
              return (
                <div key={ci} className={"matrix-cell matrix-payoff" + (isNash?" matrix-nash":"")}>
                  {p[0]}, {p[1]}
                  {isNash && <span className="matrix-nash-tag">NE</span>}
                </div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

window.KonzeptePage = KonzeptePage;
