/* Main app — router + tweaks */

function App() {
  const [twValues, setTweak] = useTweaks(window.I18N_DEFAULTS || {theme:"light", lang:"de"});
  const lang = twValues.lang || "de";
  const theme = twValues.theme || "light";

  // expose globally so useT() picks them up
  window.__lang = lang;
  window.__theme = theme;

  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  const [page, setPage] = React.useState("dashboard");
  const [activeGame, setActiveGame] = React.useState("gefangenendilemma");

  // wrapper for Topbar (expects {theme,lang} setter taking partial obj)
  const setTweaksObj = (patch) => {
    Object.keys(patch).forEach(k => setTweak(k, patch[k]));
  };

  const tLabels = (window.T && window.T[lang]) || window.T.de;

  return (
    <>
      <Topbar page={page} setPage={setPage} tweaks={{theme, lang}} setTweaks={setTweaksObj}/>
      {page === "dashboard" && <Dashboard setPage={setPage} setActiveGame={setActiveGame}/>}
      {page === "spiele" && <SpielePage setPage={setPage} setActiveGame={setActiveGame}/>}
      {page === "game" && <GamePage gameId={activeGame} setPage={setPage}/>}
      {page === "konzepte" && <KonzeptePage/>}
      {page === "lernpfade" && <LernpfadePage setPage={setPage}/>}
      {page === "fortschritt" && <FortschrittPage/>}

      <TweaksPanel title="Tweaks">
        <TweakSection label={tLabels.tw_appearance}>
          <TweakRadio label={tLabels.tw_theme}
            value={theme}
            onChange={v=>setTweak("theme", v)}
            options={[
              {value:"light", label: tLabels.tw_light},
              {value:"dark",  label: tLabels.tw_dark}
            ]}/>
          <TweakRadio label={tLabels.tw_lang}
            value={lang}
            onChange={v=>setTweak("lang", v)}
            options={[
              {value:"de", label:"Deutsch"},
              {value:"en", label:"English"}
            ]}/>
        </TweakSection>
      </TweaksPanel>
    </>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
