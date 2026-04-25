/* Game data — shared across pages */

const GAMES = [
  { id: "gefangenendilemma", de: "Gefangenendilemma", en: "Prisoner's Dilemma", group: "coop", icon: "lock",
    de_blurb: "Schweigen oder verraten — der Klassiker der Kooperationsforschung.",
    en_blurb: "Silence or betrayal — the classic of cooperation research.",
    rounds: 10, level_de: "Einstieg", level_en: "Beginner",
    concept_de: "Nash-Gleichgewicht · Tit-for-Tat",
    concept_en: "Nash equilibrium · Tit-for-Tat" },
  { id: "ultimatum", de: "Ultimatumspiel", en: "Ultimatum Game", group: "coop", icon: "scales",
    de_blurb: "Wie viel ist fair? Anbieten, ablehnen, lernen.",
    en_blurb: "How much is fair? Offer, reject, learn.",
    rounds: 8, level_de: "Einstieg", level_en: "Beginner",
    concept_de: "Fairness · Prospect Theory",
    concept_en: "Fairness · Prospect theory" },
  { id: "vertrauen", de: "Vertrauensspiel", en: "Trust Game", group: "coop", icon: "handshake",
    de_blurb: "Investieren ohne Garantie. Zahlt sich Vertrauen aus?",
    en_blurb: "Invest without a guarantee. Does trust pay off?",
    rounds: 6, level_de: "Einstieg", level_en: "Beginner",
    concept_de: "Reziprozität · Berg/Dickhaut/McCabe",
    concept_en: "Reciprocity · Berg/Dickhaut/McCabe" },
  { id: "stag-hunt", de: "Hirschjagd", en: "Stag Hunt", group: "coop", icon: "tree",
    de_blurb: "Großer Hirsch oder sicherer Hase? Risikodominanz vs. Auszahlungsdominanz.",
    en_blurb: "Big stag or safe hare? Risk vs. payoff dominance.",
    rounds: 8, level_de: "Mittel", level_en: "Intermediate",
    concept_de: "Koordination · Rousseau",
    concept_en: "Coordination · Rousseau" },
  { id: "habicht-taube", de: "Habicht‑Taube", en: "Hawk‑Dove", group: "coord", icon: "feather",
    de_blurb: "Aggression oder Rückzug — evolutionär stabile Strategien.",
    en_blurb: "Aggression or retreat — evolutionarily stable strategies.",
    rounds: 12, level_de: "Mittel", level_en: "Intermediate",
    concept_de: "ESS · Maynard Smith",
    concept_en: "ESS · Maynard Smith" },
  { id: "chicken", de: "Chicken", en: "Chicken", group: "coord", icon: "crosshair",
    de_blurb: "Wer weicht zuerst aus? Brinkmanship in Reinform.",
    en_blurb: "Who swerves first? Brinkmanship distilled.",
    rounds: 6, level_de: "Mittel", level_en: "Intermediate",
    concept_de: "Brinkmanship · Schelling",
    concept_en: "Brinkmanship · Schelling" },
  { id: "beauty-contest", de: "Beauty Contest", en: "Beauty Contest", group: "info", icon: "users",
    de_blurb: "Rate 2/3 vom Durchschnitt aller Schätzungen. Wie tief denkst du?",
    en_blurb: "Guess 2/3 of the average guess. How deep do you reason?",
    rounds: 5, level_de: "Fortgeschritten", level_en: "Advanced",
    concept_de: "K‑Level Thinking · Keynes",
    concept_en: "K‑level thinking · Keynes" },
  { id: "centipede", de: "Tausendfüßler", en: "Centipede", group: "info", icon: "infinity",
    de_blurb: "Weitergeben oder kassieren? Rückwärtsinduktion gegen Kooperation.",
    en_blurb: "Pass or take? Backward induction vs. cooperation.",
    rounds: 10, level_de: "Fortgeschritten", level_en: "Advanced",
    concept_de: "Rückwärtsinduktion · Rosenthal",
    concept_en: "Backward induction · Rosenthal" },
  { id: "auktion", de: "Erstpreisauktion", en: "First‑Price Auction", group: "market", icon: "auction",
    de_blurb: "Bieten gegen private Werte. Optimale Bietfunktion gesucht.",
    en_blurb: "Bid against private values. Find the optimal bid function.",
    rounds: 8, level_de: "Mittel", level_en: "Intermediate",
    concept_de: "Vickrey · BNE",
    concept_en: "Vickrey · BNE" },
  { id: "gewinner-fluch", de: "Fluch des Gewinners", en: "Winner's Curse", group: "market", icon: "auction",
    de_blurb: "Gemeinsamer Wert, private Schätzungen. Wer gewinnt, hat überzahlt.",
    en_blurb: "Common value, private signals. The winner overpaid.",
    rounds: 6, level_de: "Mittel", level_en: "Intermediate",
    concept_de: "Capen, Clapp & Campbell",
    concept_en: "Capen, Clapp & Campbell" },
  { id: "cournot", de: "Cournot‑Duopol", en: "Cournot Duopoly", group: "market", icon: "chart",
    de_blurb: "Mengenwettbewerb zweier Firmen. Wo liegt das Gleichgewicht?",
    en_blurb: "Two firms compete on quantity. Where's the equilibrium?",
    rounds: 8, level_de: "Fortgeschritten", level_en: "Advanced",
    concept_de: "Cournot · Reaktionsfunktion",
    concept_en: "Cournot · reaction function" },
  { id: "rps", de: "Schere‑Stein‑Papier", en: "Rock‑Paper‑Scissors", group: "coord", icon: "grid",
    de_blurb: "Reine Mischstrategie — der Lehrbuchfall für 1/3, 1/3, 1/3.",
    en_blurb: "Pure mixed strategy — the textbook 1/3, 1/3, 1/3 case.",
    rounds: 12, level_de: "Einstieg", level_en: "Beginner",
    concept_de: "Gemischte Strategien",
    concept_en: "Mixed strategies" },
];

const GROUPS = {
  de: { coop: "Kooperation & Fairness", coord: "Koordination & Konflikt", info: "Strategie & Information", market: "Auktionen & Märkte" },
  en: { coop: "Cooperation & Fairness", coord: "Coordination & Conflict", info: "Strategy & Information", market: "Auctions & Markets" }
};

const GROUP_BLURB = {
  de: {
    coop: "Wann kooperieren wir mit Fremden — und warum?",
    coord: "Wann koordinieren wir uns — und wann nicht?",
    info: "Komplexe Entscheidungen mit unvollständigem Wissen.",
    market: "Preisfindung in Märkten, Auktionen und Bietverfahren."
  },
  en: {
    coop: "When do we cooperate with strangers — and why?",
    coord: "When do we coordinate — and when do we fail?",
    info: "Complex decisions under incomplete information.",
    market: "Price discovery in markets, auctions and bidding."
  }
};

window.GAMES = GAMES;
window.GROUPS = GROUPS;
window.GROUP_BLURB = GROUP_BLURB;
