"""Lernpfade – geführte Lernwege durch Rätsel und Paradoxe."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/lernpfade")
templates = Jinja2Templates(directory="app/templates")

# ---------------------------------------------------------------------------
# Pfad-Definitionen – curated sequences per topic
# ---------------------------------------------------------------------------

LERNPFADE = [
    {
        "id": "wahrscheinlichkeit",
        "title": "Wahrscheinlichkeit",
        "subtitle": "Von Türen zu Paradoxen – Intuition vs. Mathematik",
        "icon": "🎲",
        "color": "blue",
        "level": "Einsteiger → Fortgeschritten",
        "dauer": "ca. 30 min",
        "beschreibung": (
            "Dein Gehirn ist ein schlechter Wahrscheinlichkeitsrechner – und das hat evolutionäre Gründe. "
            "Dieser Pfad zeigt dir anhand klassischer Paradoxe, wo deine Intuition versagt und warum."
        ),
        "was_du_lernst": [
            "Warum Wechseln beim Monty-Hall-Problem besser ist",
            "Weshalb 23 Menschen für 50% Geburtstags-Überschneidung genügen",
            "Wie unabhängige Zufallsereignisse funktionieren (Spielerfehlschluss)",
            "Warum ‚zufällig' präziser Definition bedarf (Bertrand)",
        ],
        "puzzles": [
            {"id": "geburtstag",         "name": "Geburtstagsparadoxon",          "icon": "🎂",  "dauer": "3 min", "schwierigkeit": "Einstieg"},
            {"id": "spielerfehlschluss", "name": "Der Spielerfehlschluss",         "icon": "🎰",  "dauer": "3 min", "schwierigkeit": "Einstieg"},
            {"id": "monty-hall",         "name": "Monty Hall Problem",             "icon": "🚪",  "dauer": "3 min", "schwierigkeit": "Mittel"},
            {"id": "hundert-gefangene",  "name": "100-Gefangenen-Problem",         "icon": "📦",  "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "coupon-sammler",     "name": "Coupon-Sammler-Problem",         "icon": "🎟️", "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "bertrand-paradoxon", "name": "Bertrand-Paradoxon",             "icon": "⭕",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "schlafendes-maedchen","name": "Schlafendes-Mädchen",           "icon": "😴",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
        ],
    },
    {
        "id": "statistik",
        "title": "Statistik & Daten",
        "subtitle": "Zahlen lügen nicht – aber sie können täuschen",
        "icon": "📊",
        "color": "emerald",
        "level": "Einsteiger → Fortgeschritten",
        "dauer": "ca. 35 min",
        "beschreibung": (
            "Statistik ist die Sprache der Wissenschaft – aber auch das beliebteste Werkzeug zur Täuschung. "
            "Lerne, wie aggregierte Zahlen lügen, Tests täuschen und Muster verschwinden können."
        ),
        "was_du_lernst": [
            "Das Falsch-Positiv-Paradoxon (Bayes'sches Denken)",
            "Wie gleiche Zahlen verschiedene Schlüsse erlauben (Simpson)",
            "Warum Sieger immer wieder zur Mitte tendieren (Regression)",
            "Den Survivorship Bias: wir sehen nur was überlebt hat",
        ],
        "puzzles": [
            {"id": "falsch-positiv",        "name": "Falsch-Positiv-Paradoxon",  "icon": "🔬", "dauer": "4 min", "schwierigkeit": "Einstieg"},
            {"id": "bayes-theorem",         "name": "Das Bayes-Theorem",         "icon": "📐", "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "gesetz-grosse-zahlen",  "name": "Gesetz der großen Zahlen",  "icon": "📈", "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "survivorship-bias",     "name": "Survivorship Bias",         "icon": "✈️", "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "regression-zur-mitte",  "name": "Regression zur Mitte",      "icon": "📊", "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "simpson",               "name": "Simpson-Paradoxon",         "icon": "📊", "dauer": "4 min", "schwierigkeit": "Fortgeschritten"},
        ],
    },
    {
        "id": "mathematik",
        "title": "Mathematik & Unendlichkeit",
        "subtitle": "Dort wo Intuition endet – beginnt echte Mathematik",
        "icon": "📐",
        "color": "violet",
        "level": "Einsteiger → Experte",
        "dauer": "ca. 40 min",
        "beschreibung": (
            "Unendlichkeit ist kein Konzept – sie ist ein Werkzeug. "
            "Dieser Pfad führt dich von einfachen Paradoxen bis zu Erkenntnissen, die die Grundlagen der Mathematik erschüttert haben."
        ),
        "was_du_lernst": [
            "Warum unendlich viele Schritte endliche Zeit brauchen (Achilles)",
            "Dass unendliche Reihen konvergieren und divergieren können",
            "Wie Hilbert unendliche Hotels verwaltet",
            "Was Ramanujan über die Summe aller natürlichen Zahlen behauptete",
            "Warum die Collatz-Vermutung seit 1937 unbewiesen ist",
        ],
        "puzzles": [
            {"id": "geschwindigkeit",   "name": "Durchschnittsgeschwindigkeit",  "icon": "🚗", "dauer": "4 min", "schwierigkeit": "Einstieg"},
            {"id": "achilles",          "name": "Achilles & die Schildkröte",   "icon": "🐢", "dauer": "5 min", "schwierigkeit": "Einstieg"},
            {"id": "hilberts-hotel",    "name": "Hilberts Hotel",               "icon": "🏨", "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "grandis-serie",     "name": "Grandis Serie",                "icon": "∞",  "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "harmonische-reihe", "name": "Die Harmonische Reihe",        "icon": "🌊", "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "collatz-vermutung", "name": "Collatz-Vermutung",            "icon": "🔄", "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "gabriels-trompete", "name": "Gabriels Trompete",            "icon": "🎺", "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "ramanujan-summe",   "name": "1+2+3+… = −1/12",             "icon": "🔢", "dauer": "5 min", "schwierigkeit": "Experte"},
        ],
    },
    {
        "id": "logik",
        "title": "Logik & Rätsel",
        "subtitle": "Scharf denken – streng folgern",
        "icon": "🧩",
        "color": "amber",
        "level": "Einsteiger → Fortgeschritten",
        "dauer": "ca. 40 min",
        "beschreibung": (
            "Logik ist die Grammatik des Denkens. "
            "Diese Rätsel trainieren präzises Schlussfolgern – und zeigen, wo selbst formale Logik an ihre Grenzen stößt."
        ),
        "was_du_lernst": [
            "Systematisches Schlussfolgern aus wenigen Informationen",
            "Kombinatorische Optimierung (Josephus, Vergiftete Fässer)",
            "Wie Sprache Logik verzerren kann (Wason-Test)",
            "Wo selbst Logik paradox wird (Barbier, Henker)",
        ],
        "puzzles": [
            {"id": "wasserkrug",         "name": "Das Wasserkrug-Problem",    "icon": "🫙",  "dauer": "5 min", "schwierigkeit": "Einstieg"},
            {"id": "muenzwaegen",        "name": "Die falsche Münze",         "icon": "🪙",  "dauer": "5 min", "schwierigkeit": "Einstieg"},
            {"id": "vergiftete-faesser", "name": "Vergiftete Fässer",         "icon": "🪣",  "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "huete-spiel",        "name": "Das Hüte-Rätsel",           "icon": "🎩",  "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "wason",              "name": "Wason-Auswahlaufgabe",      "icon": "🃏",  "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "josephus",           "name": "Das Josephus-Problem",      "icon": "⚔️", "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "barbier-paradoxon",  "name": "Das Barbier-Paradoxon",     "icon": "✂️", "dauer": "4 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "piraten",            "name": "Das Piratenspiel",          "icon": "🏴‍☠️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "henker",             "name": "Das Henkerparadoxon",       "icon": "⚖️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
        ],
    },
    {
        "id": "kognition",
        "title": "Kognition & Psychologie",
        "subtitle": "Warum dein Gehirn systematisch irrt",
        "icon": "🧠",
        "color": "rose",
        "level": "Einsteiger → Mittel",
        "dauer": "ca. 25 min",
        "beschreibung": (
            "Kognitive Verzerrungen sind keine Fehler – sie sind Features, die in der Evolution nützlich waren. "
            "Dieser Pfad macht deine blinden Flecken sichtbar."
        ),
        "was_du_lernst": [
            "Wie willkürliche Zahlen deine Urteile verzerren (Anker-Effekt)",
            "Warum Formulierungen Entscheidungen ändern (Framing)",
            "Weshalb wir Bestätigung suchen statt Widerlegung (Konfirmationsfehler)",
            "Das Dunning-Kruger-Paradox: Unwissenheit und Selbstüberschätzung",
        ],
        "puzzles": [
            {"id": "anker-experiment",    "name": "Der Anker-Effekt",          "icon": "⚓",  "dauer": "4 min", "schwierigkeit": "Einstieg"},
            {"id": "framing",             "name": "Framing-Effekt",            "icon": "🖼️", "dauer": "4 min", "schwierigkeit": "Einstieg"},
            {"id": "konfirmationsfehler", "name": "Der Konfirmationsfehler",   "icon": "🔍",  "dauer": "4 min", "schwierigkeit": "Einstieg"},
            {"id": "dunning-kruger",      "name": "Dunning-Kruger-Effekt",     "icon": "📉",  "dauer": "5 min", "schwierigkeit": "Mittel"},
        ],
    },
    {
        "id": "spieltheorie",
        "title": "Spieltheorie-Paradoxe",
        "subtitle": "Entscheidungen, die sich selbst widersprechen",
        "icon": "♟️",
        "color": "indigo",
        "level": "Mittel → Experte",
        "dauer": "ca. 50 min",
        "beschreibung": (
            "Spieltheorie erklärt rationale Entscheidungen – doch was tun, wenn Rationalität paradox wird? "
            "Dieser Pfad zeigt klassische Entscheidungsparadoxe, die Ökonomen und Philosophen bis heute beschäftigen."
        ),
        "was_du_lernst": [
            "Warum rationale Nutzenmaximierung scheitert (Allais, Ellsberg)",
            "Das Newcomb-Dilemma: Kausalität vs. Evidenz",
            "Wenn Nash-Gleichgewichte schlecht für alle sind (Braess, Hotelling)",
            "Optimales Stoppen und soziale Wahlparadoxe",
        ],
        "puzzles": [
            {"id": "hotelling",        "name": "Hotelling-Gesetz",          "icon": "🏖️", "dauer": "3 min", "schwierigkeit": "Einstieg"},
            {"id": "st-petersburg",    "name": "St. Petersburger Paradoxon","icon": "🎲",  "dauer": "4 min", "schwierigkeit": "Mittel"},
            {"id": "allais",           "name": "Allais-Paradoxon",          "icon": "🎰",  "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "ellsberg",         "name": "Ellsberg-Paradoxon",        "icon": "🪬",  "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "zwei-umschlag",    "name": "Zwei-Umschlag-Problem",     "icon": "✉️", "dauer": "5 min", "schwierigkeit": "Mittel"},
            {"id": "newcomb",          "name": "Newcomb-Paradoxon",         "icon": "📦",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "reisenden-dilemma","name": "Reisenden-Dilemma",         "icon": "🧳",  "dauer": "4 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "braess",           "name": "Braess-Paradoxon",          "icon": "🛣️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "condorcet",        "name": "Condorcet-Paradoxon",       "icon": "🗳️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
            {"id": "sekretaerin",      "name": "Sekretärinnen-Problem",     "icon": "📋",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten"},
        ],
    },
]

PFADE_BY_ID = {p["id"]: p for p in LERNPFADE}

COLOR_MAP = {
    "blue":    {"bg": "bg-blue-500",    "light": "bg-blue-50",    "border": "border-blue-200",    "text": "text-blue-700",    "badge": "bg-blue-100 text-blue-800",    "btn": "bg-blue-600 hover:bg-blue-700",    "ring": "ring-blue-400"},
    "emerald": {"bg": "bg-emerald-500", "light": "bg-emerald-50", "border": "border-emerald-200", "text": "text-emerald-700", "badge": "bg-emerald-100 text-emerald-800","btn": "bg-emerald-600 hover:bg-emerald-700","ring": "ring-emerald-400"},
    "violet":  {"bg": "bg-violet-500",  "light": "bg-violet-50",  "border": "border-violet-200",  "text": "text-violet-700",  "badge": "bg-violet-100 text-violet-800",  "btn": "bg-violet-600 hover:bg-violet-700",  "ring": "ring-violet-400"},
    "amber":   {"bg": "bg-amber-500",   "light": "bg-amber-50",   "border": "border-amber-200",   "text": "text-amber-700",   "badge": "bg-amber-100 text-amber-800",   "btn": "bg-amber-600 hover:bg-amber-700",   "ring": "ring-amber-400"},
    "rose":    {"bg": "bg-rose-500",    "light": "bg-rose-50",    "border": "border-rose-200",    "text": "text-rose-700",    "badge": "bg-rose-100 text-rose-800",    "btn": "bg-rose-600 hover:bg-rose-700",    "ring": "ring-rose-400"},
    "indigo":  {"bg": "bg-indigo-500",  "light": "bg-indigo-50",  "border": "border-indigo-200",  "text": "text-indigo-700",  "badge": "bg-indigo-100 text-indigo-800",  "btn": "bg-indigo-600 hover:bg-indigo-700",  "ring": "ring-indigo-400"},
}


@router.get("", response_class=HTMLResponse)
def lernpfade_overview(request: Request):
    return templates.TemplateResponse(
        request,
        "lernpfade.html",
        {"active_page": "lernpfade", "pfade": LERNPFADE, "color_map": COLOR_MAP},
    )


@router.get("/{pfad_id}", response_class=HTMLResponse)
def lernpfad_detail(pfad_id: str, request: Request):
    pfad = PFADE_BY_ID.get(pfad_id)
    if not pfad:
        return HTMLResponse("Lernpfad nicht gefunden", status_code=404)
    c = COLOR_MAP[pfad["color"]]
    return templates.TemplateResponse(
        request,
        "lernpfad_detail.html",
        {"active_page": "lernpfade", "pfad": pfad, "c": c},
    )
