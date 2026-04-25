/* Shared App Shell — Topbar + Nav + content router */
const { useState, useEffect, useMemo, useRef } = React;

function useT() {
  const lang = window.__lang || "de";
  return T[lang];
}

function Icon({ name, size = 16 }) {
  const s = size;
  const sw = 1.5;
  const props = { width: s, height: s, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: sw, strokeLinecap: "round", strokeLinejoin: "round" };
  switch (name) {
    case "arrow-right": return <svg {...props}><path d="M5 12h14M13 6l6 6-6 6"/></svg>;
    case "arrow-up-right": return <svg {...props}><path d="M7 17 17 7M8 7h9v9"/></svg>;
    case "play": return <svg {...props}><polygon points="6 4 20 12 6 20 6 4" fill="currentColor" stroke="none"/></svg>;
    case "search": return <svg {...props}><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>;
    case "sun": return <svg {...props}><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>;
    case "moon": return <svg {...props}><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/></svg>;
    case "sparkle": return <svg {...props}><path d="M12 3v6M12 15v6M3 12h6M15 12h6M5.6 5.6l4.2 4.2M14.2 14.2l4.2 4.2M5.6 18.4l4.2-4.2M14.2 9.8l4.2-4.2"/></svg>;
    case "book": return <svg {...props}><path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5a2.5 2.5 0 0 0 0 5H20"/></svg>;
    case "map": return <svg {...props}><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21 3 6"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>;
    case "chart": return <svg {...props}><path d="M3 20h18M5 16l4-6 4 4 5-8"/></svg>;
    case "grid": return <svg {...props}><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>;
    case "shield": return <svg {...props}><path d="M12 2 4 6v6c0 5 3.5 9 8 10 4.5-1 8-5 8-10V6l-8-4z"/></svg>;
    case "handshake": return <svg {...props}><path d="m11 17 2 2a1 1 0 0 0 1.4 0l5.6-5.6a2 2 0 0 0 0-2.8L18 8.2 13 13l-2 2-1.4-1.4a1 1 0 0 0-1.4 0L7 14.8M14.5 5.5 13 7l-3-3-2.5 2.5L4 6"/></svg>;
    case "compass": return <svg {...props}><circle cx="12" cy="12" r="10"/><polygon points="16 8 12 14 8 16 12 10 16 8" fill="currentColor"/></svg>;
    case "scales": return <svg {...props}><path d="M12 3v18M5 21h14M5 7h14M5 7l-3 7a4 4 0 0 0 6 0L5 7zM19 7l-3 7a4 4 0 0 0 6 0l-3-7z"/></svg>;
    case "lock": return <svg {...props}><rect x="4" y="11" width="16" height="10" rx="1.5"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>;
    case "crosshair": return <svg {...props}><circle cx="12" cy="12" r="9"/><line x1="12" y1="3" x2="12" y2="7"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="3" y1="12" x2="7" y2="12"/><line x1="17" y1="12" x2="21" y2="12"/></svg>;
    case "globe": return <svg {...props}><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>;
    case "tree": return <svg {...props}><path d="M12 21V11M12 11l-5-5M12 11l5-5M7 6V3M17 6V3"/></svg>;
    case "users": return <svg {...props}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>;
    case "feather": return <svg {...props}><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5l6.74-6.76zM16 8 2 22M17.5 15H9"/></svg>;
    case "infinity": return <svg {...props}><path d="M18.18 8a4.5 4.5 0 0 0-6.36 0L8.18 11.64a4.5 4.5 0 0 1-6.36 0M5.82 8a4.5 4.5 0 0 1 6.36 0l3.64 3.64a4.5 4.5 0 0 0 6.36 0"/></svg>;
    case "auction": return <svg {...props}><path d="m14 13-7.5 7.5a2.12 2.12 0 0 1-3-3L11 10M9 7l5-5 7 7-5 5M5 19h14"/></svg>;
    default: return null;
  }
}

const CLASSIC_URL = {
  dashboard: "/", spiele: "/spiele", game: "/spiele",
  konzepte: "/konzepte", lernpfade: "/lernpfade", fortschritt: "/fortschritt"
};

function switchToClassic(currentPage) {
  localStorage.setItem("app_design", "classic");
  window.location.href = CLASSIC_URL[currentPage] || "/";
}

function Topbar({ page, setPage, tweaks, setTweaks }) {
  const t = useT();
  return (
    <header className="topbar">
      <div className="wrap topbar-inner">
        <a href="#" onClick={(e)=>{e.preventDefault();setPage("dashboard");}} className="brand">
          <span className="brand-mark"></span>
          <span>{t.brand}<span style={{color:"var(--ink-mute)",fontStyle:"italic",marginLeft:8,fontSize:14,fontFamily:"var(--font-display)"}}>·</span><span style={{color:"var(--ink-mute)",fontStyle:"italic",marginLeft:8,fontSize:14,fontFamily:"var(--font-display)"}}>{t.brand_sub}</span></span>
        </a>
        <nav className="nav">
          {["dashboard","spiele","konzepte","lernpfade","fortschritt"].map(k => (
            <a key={k} href="#" onClick={(e)=>{e.preventDefault();setPage(k);}}
               className={"nav-item" + (page===k?" active":"")}>{t.nav[k]}</a>
          ))}
        </nav>
        <div className="topbar-right">
          <button className="icon-btn" onClick={()=>{
            const next = tweaks.theme === "dark" ? "light" : "dark";
            setTweaks({theme: next});
          }} title="Theme">
            <Icon name={tweaks.theme==="dark"?"sun":"moon"} size={15}/>
          </button>
          <button className="icon-btn" style={{width:"auto",padding:"0 12px",fontFamily:"var(--font-mono)",fontSize:11,letterSpacing:"0.1em"}} onClick={()=>{
            setTweaks({lang: tweaks.lang === "de" ? "en" : "de"});
          }}>{tweaks.lang.toUpperCase()}</button>
          <button className="icon-btn" style={{width:"auto",padding:"0 12px",fontFamily:"var(--font-mono)",fontSize:11,letterSpacing:"0.1em",opacity:0.6}} onClick={()=>switchToClassic(page)} title="Zu klassischem Design wechseln">
            ← Klassisch
          </button>
        </div>
      </div>
    </header>
  );
}

window.useT = useT;
window.Icon = Icon;
window.Topbar = Topbar;
