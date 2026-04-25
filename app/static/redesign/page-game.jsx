/* Page: Game detail (Gefangenendilemma exemplarisch, klickbar) */

function GamePage({ gameId, setPage }) {
  const t = useT();
  const lang = window.__lang || "de";
  const game = GAMES.find(g => g.id === gameId) || GAMES[0];

  const [round, setRound] = React.useState(1);
  const [hist, setHist] = React.useState([]); // [{p:'C'|'D', ai:'C'|'D'}]
  const [over, setOver] = React.useState(false);

  const playerScore = hist.reduce((s,h) => s + payoff(h.p, h.ai), 0);
  const aiScore = hist.reduce((s,h) => s + payoff(h.ai, h.p), 0);

  function play(move) {
    if (over) return;
    // Tit-for-tat: copy player's last move; cooperate first
    const aiMove = hist.length === 0 ? "C" : hist[hist.length-1].p;
    const next = [...hist, {p: move, ai: aiMove}];
    setHist(next);
    if (next.length >= game.rounds) setOver(true);
    else setRound(r => r+1);
  }

  function reset() {
    setRound(1); setHist([]); setOver(false);
  }

  return (
    <div className="page wrap-narrow">
      <div style={{padding: "32px 0 16px"}}>
        <a href="#" onClick={(e)=>{e.preventDefault();setPage("spiele");}} className="arrow-link" style={{fontSize:12.5}}>
          ← {lang==="de"?"Alle Spiele":"All games"}
        </a>
      </div>

      <section style={{padding: "16px 0 40px", display:"grid", gridTemplateColumns:"1fr auto", alignItems:"end", gap:24}}>
        <div>
          <div style={{display:"flex", gap:10, marginBottom:18, alignItems:"center"}}>
            <span style={{color:"var(--ink-mute)"}}><Icon name={game.icon} size={20}/></span>
            <span className="tag tag-accent">{lang==="de"?"Klassiker · 1950":"Classic · 1950"}</span>
            <span className="tag">{lang==="de"?game.level_de:game.level_en}</span>
          </div>
          <h1 className="display" style={{fontSize: "clamp(40px, 6vw, 72px)", margin: 0, lineHeight: 1.05}}>
            {lang==="de"?game.de:game.en}
          </h1>
          <p style={{fontSize:16, color:"var(--ink-soft)", margin:"20px 0 0", maxWidth: 560, lineHeight:1.55}}>
            {lang==="de"
              ? "Du spielst gegen einen Algorithmus mit verborgener Strategie. Beobachte sein Verhalten Runde für Runde. Nach Spielende wird die Strategie aufgedeckt."
              : "You play against an algorithm with a hidden strategy. Watch its behavior round by round. The strategy is revealed when the game ends."}
          </p>
        </div>
        <div style={{textAlign:"right"}}>
          <div className="eyebrow" style={{marginBottom: 4}}>{t.round}</div>
          <div className="display" style={{fontSize: 56, lineHeight: 1, color:"var(--accent)"}}>
            <span className="mono" style={{fontSize:56}}>{String(Math.min(round,game.rounds)).padStart(2,"0")}</span>
            <span style={{color:"var(--ink-faint)"}}>/{game.rounds}</span>
          </div>
        </div>
      </section>

      <section style={{borderTop:"1px solid var(--ink)", borderBottom:"1px solid var(--line)", display:"grid", gridTemplateColumns:"1fr 1fr", gap: 0, margin: "0 -28px"}}>
        <div style={{padding: "24px 28px", borderRight:"1px solid var(--line)"}}>
          <div className="eyebrow">{t.you}</div>
          <div className="display" style={{fontSize: 56, color:"var(--cooperate)"}}>{playerScore}</div>
        </div>
        <div style={{padding: "24px 28px", textAlign:"right"}}>
          <div className="eyebrow">{t.opponent} · <span style={{color:"var(--accent)"}}>?</span> {t.strategy_hidden}</div>
          <div className="display" style={{fontSize: 56, color:"var(--accent)"}}>{aiScore}</div>
        </div>
      </section>

      <section style={{padding: "48px 0 24px", display:"grid", gridTemplateColumns: "1fr 1fr", gap: 32}}>
        <div>
          <div className="eyebrow" style={{marginBottom: 14}}>{t.payoff_matrix}</div>
          <PayoffMatrix/>
          <p style={{fontSize: 13, color: "var(--ink-mute)", marginTop: 14, lineHeight: 1.5}}>
            {lang==="de"
              ? "Beide kooperieren → 3 Punkte für jeden. Verrat eines Spielers gibt ihm 5 (der andere 0). Beide verraten: 1 Punkt — das Nash-Gleichgewicht. Doch alle würden mehr verdienen, wenn sie kooperieren."
              : "Both cooperate → 3 each. One defects → 5 for them, 0 for the other. Both defect: 1 each — Nash equilibrium. Yet both would earn more by cooperating."}
          </p>
        </div>
        <div>
          <div className="eyebrow" style={{marginBottom: 14}}>{t.history}</div>
          <HistoryGrid hist={hist} total={game.rounds}/>
          {hist.length > 0 && (
            <p style={{fontSize: 12, color:"var(--ink-mute)", marginTop: 12, fontFamily:"var(--font-mono)"}}>
              {lang==="de" ? "Du" : "You"}: {hist.map(h=>h.p).join(" ")} {"\u00A0\u00A0"}
              {lang==="de" ? "KI" : "AI"}: {hist.map(h=>h.ai).join(" ")}
            </p>
          )}
        </div>
      </section>

      {!over && (
        <section style={{padding: "16px 0 48px"}}>
          <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap: 14}}>
            <button className="btn btn-coop btn-large" style={{padding: "22px", justifyContent:"center", fontSize:16}} onClick={()=>play("C")}>
              <Icon name="handshake" size={18}/> {t.cooperate}
            </button>
            <button className="btn btn-accent btn-large" style={{padding: "22px", justifyContent:"center", fontSize:16}} onClick={()=>play("D")}>
              <Icon name="crosshair" size={18}/> {t.defect}
            </button>
          </div>
        </section>
      )}

      {over && (
        <section className="card" style={{padding: 32, marginTop: 8}}>
          <div className="eyebrow" style={{marginBottom:12, color:"var(--gold)"}}>{t.debrief}</div>
          <h3 className="display" style={{fontSize: 30, margin:"0 0 14px"}}>
            {lang==="de"?"Strategie aufgedeckt: ":"Strategy revealed: "}
            <span className="display-italic" style={{color:"var(--accent)"}}>Tit‑for‑Tat</span>
          </h3>
          <p style={{color:"var(--ink-soft)", margin:0, maxWidth: 600, lineHeight:1.6}}>
            {lang==="de"
              ? "Die KI kooperiert in Runde 1 und kopiert dann jeweils deinen letzten Zug. Diese vier Zeilen Code haben Axelrods Turnier 1980 gewonnen — gegen 62 ausgeklügeltere Algorithmen."
              : "The AI cooperates in round 1, then copies your last move. These four lines of code won Axelrod's 1980 tournament — against 62 more sophisticated algorithms."}
          </p>
          <div style={{display:"flex", gap:12, marginTop: 24}}>
            <button onClick={reset} className="btn btn-primary">{lang==="de"?"Nochmal spielen":"Play again"}<Icon name="arrow-right" size={14}/></button>
            <a href="#" onClick={(e)=>{e.preventDefault();setPage("spiele");}} className="btn btn-ghost">{lang==="de"?"Anderes Spiel":"Different game"}</a>
          </div>
        </section>
      )}
      <div style={{height:80}}/>
    </div>
  );
}

function payoff(me, them) {
  if (me === "C" && them === "C") return 3;
  if (me === "C" && them === "D") return 0;
  if (me === "D" && them === "C") return 5;
  return 1;
}

function HistoryGrid({ hist, total }) {
  const cells = Array.from({length: total}, (_,i) => hist[i]);
  return (
    <div style={{display:"grid", gridTemplateColumns:"repeat("+total+", 1fr)", gap:4}}>
      {cells.map((c,i)=>(
        <div key={i} style={{aspectRatio:"1/2", border:"1px solid var(--line)", borderRadius: 4, display:"flex", flexDirection:"column", overflow:"hidden", background: c?"transparent":"var(--bg-sunk)"}}>
          <div style={{flex:1, background: c?(c.p==="C"?"var(--cooperate-soft)":"var(--accent-soft)"):"transparent", display:"grid", placeItems:"center", color: c?(c.p==="C"?"var(--cooperate)":"var(--accent)"):"transparent", fontFamily:"var(--font-mono)", fontSize:12, fontWeight:600}}>{c?.p||""}</div>
          <div style={{flex:1, background: c?(c.ai==="C"?"var(--cooperate-soft)":"var(--accent-soft)"):"transparent", display:"grid", placeItems:"center", color: c?(c.ai==="C"?"var(--cooperate)":"var(--accent)"):"transparent", fontFamily:"var(--font-mono)", fontSize:12, fontWeight:600, borderTop: c?"1px solid var(--bg-elev)":"none"}}>{c?.ai||""}</div>
        </div>
      ))}
    </div>
  );
}

window.GamePage = GamePage;
