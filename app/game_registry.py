"""Central game registry — single source of truth for all game metadata.

Each entry defines:
  game_type  — the key stored in GameSession.game_type (DB)
  slug       — the URL path segment used in /spiele/{slug}
  name       — German display name
  icon       — emoji icon
  mechanic   — core game theory concept
  literature — canonical reference(s)
  lesson_slug — linked /lektionen/{slug}
  level      — difficulty level (1–6)
"""

GAMES: list[dict] = [
    # ── Level 1: Einstieg ──────────────────────────────────────────────────
    {
        "game_type": "gefangenendilemma",
        "slug": "gefangenendilemma",
        "name": "Gefangenendilemma",
        "icon": "🔒",
        "mechanic": "Dominante Strategien / Nash-GGW",
        "literature": "Tucker (1950), Axelrod (1984)",
        "lesson_slug": "dominante-strategien",
        "level": 1,
    },
    {
        "game_type": "ultimatum",
        "slug": "ultimatum",
        "name": "Ultimatumspiel",
        "icon": "⚖️",
        "mechanic": "Fairness & Rationalität",
        "literature": "Güth, Schmittberger & Schwarze (1982)",
        "lesson_slug": "fairness-effekte",
        "level": 1,
    },
    {
        "game_type": "vertrauen",
        "slug": "vertrauen",
        "name": "Vertrauensspiel",
        "icon": "🤝",
        "mechanic": "Soziale Präferenzen",
        "literature": "Berg, Dickhaut & McCabe (1995)",
        "lesson_slug": "wiederholte-spiele-reputation",
        "level": 1,
    },
    {
        "game_type": "verhandlung",
        "slug": "verhandlung",
        "name": "Verhandlungssimulation",
        "icon": "💼",
        "mechanic": "Rubinstein Bargaining",
        "literature": "Rubinstein (1982)",
        "lesson_slug": "rubinstein-bargaining",
        "level": 1,
    },
    # ── Level 2: Konflikt & Koordination ───────────────────────────────────
    {
        "game_type": "chicken",
        "slug": "chicken",
        "name": "Feiglingsspiel",
        "icon": "🚗",
        "mechanic": "Anti-Koordination / gemischte NE",
        "literature": "Rapoport & Chammah (1966)",
        "lesson_slug": "feiglingsspiel-chicken-game",
        "level": 2,
    },
    {
        "game_type": "stag_hunt",
        "slug": "stag-hunt",
        "name": "Hirschjagd",
        "icon": "🦌",
        "mechanic": "Koordination unter Risiko",
        "literature": "Rousseau (1755), Skyrms (2004)",
        "lesson_slug": "koordinationsspiele",
        "level": 2,
    },
    {
        "game_type": "koordination",
        "slug": "koordination",
        "name": "Koordinationsspiel",
        "icon": "🎯",
        "mechanic": "Nash-GGW / Focal Points",
        "literature": "Schelling (1960)",
        "lesson_slug": "koordinationsspiele",
        "level": 2,
    },
    {
        "game_type": "rps",
        "slug": "rps",
        "name": "Schere-Stein-Papier",
        "icon": "✂️",
        "mechanic": "Gemischte Strategien / Minimax",
        "literature": "von Neumann (1928)",
        "lesson_slug": "gemischte-strategien",
        "level": 2,
    },
    # ── Level 3: Gruppen & Märkte ───────────────────────────────────────────
    {
        "game_type": "public_goods",
        "slug": "public-goods",
        "name": "Öffentliche Güter",
        "icon": "🏛️",
        "mechanic": "Kollektivgut / Trittbrettfahrer",
        "literature": "Olson (1965), Fehr & Gächter (2000)",
        "lesson_slug": "oeffentliche-gueter-kollektivgut",
        "level": 3,
    },
    {
        "game_type": "beauty_contest",
        "slug": "beauty-contest",
        "name": "Schönheitswettbewerb",
        "icon": "🧠",
        "mechanic": "K-Level Thinking / iterated dominance",
        "literature": "Keynes (1936), Nagel (1995)",
        "lesson_slug": "k-level-thinking",
        "level": 3,
    },
    {
        "game_type": "centipede",
        "slug": "centipede",
        "name": "Centipede-Spiel",
        "icon": "🐛",
        "mechanic": "Rückwärtsinduktion",
        "literature": "Rosenthal (1981)",
        "lesson_slug": "rueckwaertsinduktion",
        "level": 3,
    },
    {
        "game_type": "auktion",
        "slug": "auktion",
        "name": "Vickrey-Auktion",
        "icon": "🔨",
        "mechanic": "Dominante Strategie / Wahrheitsoffenbarung",
        "literature": "Vickrey (1961)",
        "lesson_slug": "spieltheorie-grundlagen",
        "level": 3,
    },
    {
        "game_type": "diktator",
        "slug": "diktator",
        "name": "Diktatorspiel",
        "icon": "👑",
        "mechanic": "Soziale Präferenzen / Altruismus",
        "literature": "Forsythe et al. (1994)",
        "lesson_slug": "fairness-effekte",
        "level": 3,
    },
    # ── Level 4: Auktionen & Information ───────────────────────────────────
    {
        "game_type": "dollarauktion",
        "slug": "dollarauktion",
        "name": "Dollarauktion",
        "icon": "💸",
        "mechanic": "Eskalation & Sunk Cost",
        "literature": "Shubik (1971)",
        "lesson_slug": "wiederholte-spiele-reputation",
        "level": 4,
    },
    {
        "game_type": "hollaendische-auktion",
        "slug": "hollaendische-auktion",
        "name": "Holländische Auktion",
        "icon": "🌷",
        "mechanic": "Absteigende Auktion / Bietstrategien",
        "literature": "Klemperer (1999)",
        "lesson_slug": "spieltheorie-grundlagen",
        "level": 4,
    },
    {
        "game_type": "englische-auktion",
        "slug": "englische-auktion",
        "name": "Englische Auktion",
        "icon": "🔔",
        "mechanic": "Aufsteigende Auktion / Dominante Strategie",
        "literature": "Vickrey (1961), Klemperer (1999)",
        "lesson_slug": "spieltheorie-grundlagen",
        "level": 4,
    },
    {
        "game_type": "minderheit",
        "slug": "minderheit",
        "name": "Minderheitsspiel",
        "icon": "🔢",
        "mechanic": "El Farol / Anti-Koordination",
        "literature": "Challet & Zhang (1997)",
        "lesson_slug": "informationsasymmetrie-signaling",
        "level": 4,
    },
    # ── Level 5: Signaling & Wettbewerb ────────────────────────────────────
    {
        "game_type": "gewinner-fluch",
        "slug": "gewinner-fluch",
        "name": "Fluch des Gewinners",
        "icon": "🏆",
        "mechanic": "Winner's Curse / Informationsasymmetrie",
        "literature": "Capen et al. (1971), Thaler (1988)",
        "lesson_slug": "informationsasymmetrie-signaling",
        "level": 5,
    },
    {
        "game_type": "cournot",
        "slug": "cournot",
        "name": "Cournot-Duopol",
        "icon": "🏭",
        "mechanic": "Oligopol / Nash-GGW in Mengen",
        "literature": "Cournot (1838), Nash (1950)",
        "lesson_slug": "dominante-strategien",
        "level": 5,
    },
    # ── Level 6: Evolutionäre & Gemischte Strategien ───────────────────────
    {
        "game_type": "habicht-taube",
        "slug": "habicht-taube",
        "name": "Habicht-Taube-Spiel",
        "icon": "🦅",
        "mechanic": "ESS / Evolutionäre Spieltheorie",
        "literature": "Maynard Smith & Price (1973)",
        "lesson_slug": "gemischte-strategien",
        "level": 6,
    },
    {
        "game_type": "geschlechter-kampf",
        "slug": "geschlechter-kampf",
        "name": "Battle of the Sexes",
        "icon": "🎭",
        "mechanic": "Koordinationsdilemma / gemischte NE",
        "literature": "Luce & Raiffa (1957)",
        "lesson_slug": "gemischte-strategien",
        "level": 6,
    },
    {
        "game_type": "freiwilligen-dilemma",
        "slug": "freiwilligen-dilemma",
        "name": "Freiwilligen-Dilemma",
        "icon": "🙋",
        "mechanic": "Volunteer's Dilemma / gemischte NE",
        "literature": "Diekmann (1985)",
        "lesson_slug": "oeffentliche-gueter-kollektivgut",
        "level": 6,
    },
    {
        "game_type": "gleiche-muenzen",
        "slug": "gleiche-muenzen",
        "name": "Gleiche Münzen",
        "icon": "🎲",
        "mechanic": "Minimax / Nullsummenspiel",
        "literature": "von Neumann (1928)",
        "lesson_slug": "gemischte-strategien",
        "level": 6,
    },
]

# ── Lookup helpers ────────────────────────────────────────────────────────────

# game_type (DB key) → full metadata dict
GAME_BY_TYPE: dict[str, dict] = {g["game_type"]: g for g in GAMES}

# URL slug → full metadata dict
GAME_BY_SLUG: dict[str, dict] = {g["slug"]: g for g in GAMES}

# game_type → display name  (replaces GAME_LABELS in fortschritt.py)
GAME_LABELS: dict[str, str] = {g["game_type"]: g["name"] for g in GAMES}

# game_type → icon emoji
GAME_ICONS: dict[str, str] = {g["game_type"]: g["icon"] for g in GAMES}

# URL slug → game_type  (for routes that only have the slug)
SLUG_TO_TYPE: dict[str, str] = {g["slug"]: g["game_type"] for g in GAMES}

# game_type → URL slug
TYPE_TO_SLUG: dict[str, str] = {g["game_type"]: g["slug"] for g in GAMES}
