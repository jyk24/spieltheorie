/* Page: Spiele (Games library) */

function SpielePage({ setPage, setActiveGame }) {
  const t = useT();
  const lang = window.__lang || "de";
  const [filter, setFilter] = React.useState("all");

  const filtered = filter === "all" ? GAMES : GAMES.filter(g => g.group === filter);
  const groups = ["coop", "coord", "info", "market"];

  return (
    <div className="page wrap">
      <section style={{padding: "64px 0 40px"}}>
        <div className="eyebrow" style={{marginBottom: 24}}>※ 26 {lang==="de"?"Experimente":"Experiments"} · 4 {lang==="de"?"Domänen":"Domains"}</div>
        <h1 className="display" style={{fontSize: "clamp(48px, 7vw, 96px)", margin: 0, maxWidth: 920}}>
          {t.spiele_title[0]}<br/>
          <span className="display-italic" style={{color: "var(--accent)"}}>{t.spiele_title[1]}</span>{t.spiele_title[2]}
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-soft)", maxWidth: 640, marginTop: 32, lineHeight: 1.55}}>{t.spiele_lede}</p>
      </section>

      <section style={{borderTop: "1px solid var(--ink)", padding: "20px 0", display: "flex", gap: 24, alignItems: "center", flexWrap:"wrap", position:"sticky", top: 64, background: "var(--bg)", zIndex: 10}}>
        <span className="eyebrow">{lang==="de"?"Filter":"Filter"}</span>
        <button onClick={()=>setFilter("all")} className={"chip"+(filter==="all"?" chip-on":"")}
          style={chipStyle(filter==="all")}>{t.filter_all} <span className="mono" style={{fontSize:11,opacity:0.6,marginLeft:4}}>{GAMES.length}</span></button>
        {groups.map(g => {
          const count = GAMES.filter(x=>x.group===g).length;
          const on = filter===g;
          return (
            <button key={g} onClick={()=>setFilter(g)} style={chipStyle(on)}>
              {GROUPS[lang][g]} <span className="mono" style={{fontSize:11,opacity:0.6,marginLeft:4}}>{count}</span>
            </button>
          );
        })}
      </section>

      {(filter === "all" ? groups : [filter]).map((grp, gi) => {
        const games = filtered.filter(g => g.group === grp);
        if (!games.length) return null;
        return (
          <section key={grp} style={{padding: "48px 0", borderTop: gi>0?"1px solid var(--line)":"1px solid var(--line)"}}>
            <div style={{display:"grid", gridTemplateColumns:"280px 1fr", gap: 48, marginBottom: 32, alignItems:"start"}}>
              <div>
                <div className="eyebrow" style={{marginBottom: 10, color:"var(--accent)"}}>0{groups.indexOf(grp)+1} / 04</div>
                <h2 className="display" style={{fontSize: 32, margin: 0, lineHeight:1.1}}>{GROUPS[lang][grp]}</h2>
              </div>
              <p style={{color:"var(--ink-soft)", fontSize: 16, margin: 0, paddingTop: 8, maxWidth: 540}}>{GROUP_BLURB[lang][grp]}</p>
            </div>
            <div style={{display:"grid", gridTemplateColumns:"repeat(3, 1fr)", gap: 16}}>
              {games.map(g => (
                <a key={g.id} href="#" onClick={(e)=>{e.preventDefault();setActiveGame(g.id);setPage("game");}}
                   className="card card-hover" style={{padding: 22, display:"flex", flexDirection:"column", minHeight: 220, gap: 14, position:"relative"}}>
                  <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-start"}}>
                    <span style={{color:"var(--ink-mute)"}}><Icon name={g.icon} size={24}/></span>
                    <span className="mono" style={{fontSize: 10.5, letterSpacing: "0.1em", color:"var(--ink-faint)", textTransform:"uppercase"}}>{lang==="de"?g.level_de:g.level_en}</span>
                  </div>
                  <div style={{flex: 1}}>
                    <div className="display" style={{fontSize: 24, lineHeight: 1.1, marginBottom: 8}}>{lang==="de"?g.de:g.en}</div>
                    <p style={{fontSize: 13.5, color:"var(--ink-soft)", margin: 0, lineHeight: 1.5}}>{lang==="de"?g.de_blurb:g.en_blurb}</p>
                  </div>
                  <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", paddingTop: 12, borderTop: "1px solid var(--line-soft)"}}>
                    <span className="mono" style={{fontSize: 11, color:"var(--ink-mute)"}}>{lang==="de"?g.concept_de:g.concept_en}</span>
                    <span className="mono" style={{fontSize: 11, color:"var(--ink-mute)"}}>{g.rounds}r</span>
                  </div>
                </a>
              ))}
            </div>
          </section>
        );
      })}
      <div style={{height:80}}/>
    </div>
  );
}

function chipStyle(on) {
  return {
    padding: "7px 14px",
    fontSize: 13,
    borderRadius: 100,
    border: "1px solid " + (on?"var(--ink)":"var(--line)"),
    background: on ? "var(--ink)" : "var(--bg-elev)",
    color: on ? "var(--bg)" : "var(--ink-soft)",
    transition: "all 0.15s",
    cursor: "pointer"
  };
}

window.SpielePage = SpielePage;
