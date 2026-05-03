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
    # ── Neue multi-modale Pfade ────────────────────────────────────────────────
    {
        "id": "spieltheorie-einstieg",
        "title": "Einstieg: Spieltheorie kennenlernen",
        "subtitle": "Theorie, Spiele und Paradoxe im Mix",
        "icon": "♟️",
        "color": "indigo",
        "level": "Einsteiger",
        "dauer": "ca. 45 min",
        "beschreibung": (
            "Der perfekte Start: Spieltheorie live erleben – mit Theorie, einem echten Spiel und klassischen Paradoxen. "
            "Du verstehst danach, was Nash-Gleichgewichte sind und warum Kooperation so schwierig ist."
        ),
        "was_du_lernst": [
            "Was Spieltheorie ist und warum sie überall auftaucht",
            "Das Gefangenendilemma – das wichtigste Spiel der Theorie",
            "Das Monty-Hall-Problem – Intuition schlägt Logik",
            "Das Nash-Gleichgewicht: kein Spieler will abweichen",
        ],
        "steps": [
            {"typ": "theorie", "titel": "Was ist Spieltheorie?",     "icon": "📖", "dauer": "8 min", "schwierigkeit": "Einstieg",  "url": "/grundlagen",           "beschreibung": "Grundkonzepte: Auszahlungsmatrizen, Strategien, Gleichgewichte"},
            {"typ": "spiel",   "titel": "Gefangenendilemma",          "icon": "🎮", "dauer": "5 min", "schwierigkeit": "Einstieg",  "url": "/spiele/gefangenendilemma", "beschreibung": "Kooperieren oder Verraten? Das Kernspiel der Spieltheorie"},
            {"typ": "raetsel", "titel": "Monty Hall Problem",         "icon": "🚪", "dauer": "3 min", "schwierigkeit": "Einstieg",  "id": "monty-hall",             "beschreibung": "Wechseln oder bleiben? Deine Intuition täuscht dich"},
            {"typ": "spiel",   "titel": "Ultimatumspiel",             "icon": "🎮", "dauer": "5 min", "schwierigkeit": "Einstieg",  "url": "/spiele/ultimatum",     "beschreibung": "Faire Angebote vs. rationale Maximierung"},
            {"typ": "raetsel", "titel": "Newcomb-Paradoxon",          "icon": "📦", "dauer": "5 min", "schwierigkeit": "Fortgeschritten", "id": "newcomb",         "beschreibung": "Kausalität vs. Evidenz – ein philosophisches Dilemma"},
            {"typ": "theorie", "titel": "Nash-Gleichgewicht vertiefen","icon": "📖", "dauer": "8 min", "schwierigkeit": "Mittel",   "url": "/grundlagen",           "beschreibung": "Nash-Finder, Gleichgewichtstypen und ihre Anwendungen"},
        ],
    },
    {
        "id": "entscheidung-unsicherheit",
        "title": "Entscheidungen unter Unsicherheit",
        "subtitle": "Prospect Theory, Paradoxe und Auktionen",
        "icon": "🎲",
        "color": "amber",
        "level": "Mittel",
        "dauer": "ca. 60 min",
        "beschreibung": (
            "Warum handeln Menschen nicht wie rationale Nutzenmaximierer? "
            "Dieser Pfad verbindet Prospect Theory mit klassischen Entscheidungsparadoxen und zeigt, "
            "wie du unter echter Unsicherheit besser entscheidest."
        ),
        "was_du_lernst": [
            "Prospect Theory: Verluste wiegen schwerer als Gewinne",
            "Allais- und Ellsberg-Paradoxon: rationale Theorie scheitert",
            "Warum Auktionsgewinner oft zu viel zahlen",
            "Bounded Rationality: optimale Entscheidungen mit begrenztem Wissen",
        ],
        "steps": [
            {"typ": "theorie", "titel": "Prospect Theory",            "icon": "📖", "dauer": "8 min", "schwierigkeit": "Mittel",   "url": "/grundlagen",            "beschreibung": "Kahneman & Tversky: wie Menschen Risiken wirklich bewerten"},
            {"typ": "raetsel", "titel": "Allais-Paradoxon",           "icon": "🎰", "dauer": "5 min", "schwierigkeit": "Mittel",   "id": "allais",                  "beschreibung": "Erwartungsnutzen-Theorie bricht zusammen"},
            {"typ": "raetsel", "titel": "Ellsberg-Paradoxon",         "icon": "🪬", "dauer": "5 min", "schwierigkeit": "Mittel",   "id": "ellsberg",                "beschreibung": "Ambiguitätsaversion vs. kalkuliertes Risiko"},
            {"typ": "spiel",   "titel": "Der Fluch des Gewinners",    "icon": "🎮", "dauer": "5 min", "schwierigkeit": "Fortgeschritten", "url": "/spiele/gewinner-fluch", "beschreibung": "Wer gewinnt, zahlt meist zu viel"},
            {"typ": "raetsel", "titel": "St. Petersburger Paradoxon", "icon": "🎲", "dauer": "4 min", "schwierigkeit": "Mittel",   "id": "st-petersburg",           "beschreibung": "Unendlicher Erwartungswert, endliche Zahlungsbereitschaft"},
            {"typ": "theorie", "titel": "Bounded Rationality",        "icon": "📖", "dauer": "8 min", "schwierigkeit": "Mittel",   "url": "/grundlagen",            "beschreibung": "Simon: Satisficing statt Optimierung"},
        ],
    },
    {
        "id": "verhandlung-meistern",
        "title": "Verhandlung meistern",
        "subtitle": "BATNA, Signaling und Informationsasymmetrie",
        "icon": "🤝",
        "color": "teal",
        "level": "Mittel",
        "dauer": "ca. 60 min",
        "beschreibung": (
            "Verhandlung ist angewandte Spieltheorie. "
            "Dieser Pfad zeigt dir die wichtigsten Konzepte – von BATNA über Ankereffekte bis zu Marktversagen durch Informationsasymmetrie."
        ),
        "was_du_lernst": [
            "BATNA: Verhandlungsmacht kommt aus der besten Alternative",
            "Ankereffekte: der erste Wert prägt das gesamte Ergebnis",
            "Signaling: glaubwürdige Signale in asymmetrischer Information",
            "Markt für Zitronen: wie Informationsasymmetrie Märkte zerstört",
        ],
        "steps": [
            {"typ": "theorie", "titel": "Verhandlungstheorie & BATNA", "icon": "📖", "dauer": "8 min", "schwierigkeit": "Einstieg",  "url": "/grundlagen",            "beschreibung": "BATNA, ZOPA, Rubinstein Bargaining"},
            {"typ": "raetsel", "titel": "Der Anker-Effekt",            "icon": "⚓", "dauer": "4 min", "schwierigkeit": "Einstieg",  "id": "anker-experiment",        "beschreibung": "Wie willkürliche Zahlen Urteile verzerren"},
            {"typ": "spiel",   "titel": "Verhandlungssimulation",      "icon": "🎮", "dauer": "6 min", "schwierigkeit": "Fortgeschritten", "url": "/spiele/verhandlung",  "beschreibung": "Mehrrunden-Verhandlung mit realen Szenarien"},
            {"typ": "raetsel", "titel": "Markt für Zitronen",          "icon": "🍋", "dauer": "5 min", "schwierigkeit": "Mittel",   "id": "marktverlust",            "beschreibung": "Akerlof: Informationsasymmetrie zerstört Märkte"},
            {"typ": "raetsel", "titel": "BATNA – Verhandlungsmacht",   "icon": "🤝", "dauer": "5 min", "schwierigkeit": "Einstieg",  "id": "batna",                   "beschreibung": "Wann solltest du abbrechen?"},
            {"typ": "theorie", "titel": "Signaling & Screening",       "icon": "📖", "dauer": "8 min", "schwierigkeit": "Fortgeschritten", "url": "/grundlagen",         "beschreibung": "Spence-Modell: wie glaubwürdige Signale funktionieren"},
        ],
    },
    {
        "id": "soziale-dynamiken",
        "title": "Soziale Dynamiken",
        "subtitle": "Kooperation, Herdenverhalten und Evolution",
        "icon": "🌐",
        "color": "emerald",
        "level": "Fortgeschritten",
        "dauer": "ca. 60 min",
        "beschreibung": (
            "Wie entstehen kollektive Muster aus individuellen Entscheidungen? "
            "Von Informationskaskaden über Public Goods bis zur evolutionären Spieltheorie."
        ),
        "was_du_lernst": [
            "Informationskaskaden: warum Herden irren können",
            "Public Goods: das Trittbrettfahrerproblem in der Praxis",
            "Evolutionäre Spieltheorie: welche Strategien überleben?",
            "Das Braess-Paradoxon: mehr Kapazität kann alle schlechter stellen",
        ],
        "steps": [
            {"typ": "raetsel", "titel": "Informationskaskade",         "icon": "🫧", "dauer": "5 min", "schwierigkeit": "Mittel",          "id": "informationskaskade",     "beschreibung": "Warum rationale Individuen kollektiv irren"},
            {"typ": "spiel",   "titel": "Öffentliche-Güter-Spiel",     "icon": "🎮", "dauer": "5 min", "schwierigkeit": "Einstieg",         "url": "/spiele/public-goods",   "beschreibung": "Trittbrettfahrer vs. Kooperation im Gruppenspiel"},
            {"typ": "raetsel", "titel": "Stag Hunt – Hirschjagd",      "icon": "🦌", "dauer": "5 min", "schwierigkeit": "Mittel",          "id": "hirschjagd",              "beschreibung": "Koordinationsdilemma: Sicherheit vs. hoher Lohn"},
            {"typ": "theorie", "titel": "Evolutionäre Spieltheorie",   "icon": "📖", "dauer": "8 min", "schwierigkeit": "Fortgeschritten",  "url": "/grundlagen",            "beschreibung": "ESS, Replikator-Dynamik und evolutionäre Stabilität"},
            {"typ": "spiel",   "titel": "Iterated Prisoner's Dilemma", "icon": "🎮", "dauer": "5 min", "schwierigkeit": "Mittel",          "url": "/spiele/gefangenendilemma", "beschreibung": "Tit-for-Tat und die Macht der Wiederholung"},
            {"typ": "raetsel", "titel": "Braess-Paradoxon",            "icon": "🛣️","dauer": "5 min", "schwierigkeit": "Fortgeschritten",  "id": "braess",                  "beschreibung": "Eine neue Straße macht alle langsamer – warum?"},
        ],
    },
    # ── Bestehende Rätsel-Pfade ────────────────────────────────────────────────
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
        "steps": [
            {"typ": "raetsel", "id": "geburtstag",          "titel": "Geburtstagsparadoxon",          "icon": "🎂",  "dauer": "3 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "spielerfehlschluss",  "titel": "Der Spielerfehlschluss",         "icon": "🎰",  "dauer": "3 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "monty-hall",          "titel": "Monty Hall Problem",             "icon": "🚪",  "dauer": "3 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "hundert-gefangene",   "titel": "100-Gefangenen-Problem",         "icon": "📦",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "coupon-sammler",      "titel": "Coupon-Sammler-Problem",         "icon": "🎟️", "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "bertrand-paradoxon",  "titel": "Bertrand-Paradoxon",             "icon": "⭕",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "schlafendes-maedchen","titel": "Schlafendes-Mädchen",            "icon": "😴",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
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
        "steps": [
            {"typ": "raetsel", "id": "falsch-positiv",       "titel": "Falsch-Positiv-Paradoxon",  "icon": "🔬", "dauer": "4 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "bayes-theorem",        "titel": "Das Bayes-Theorem",         "icon": "📐", "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "gesetz-grosse-zahlen", "titel": "Gesetz der großen Zahlen",  "icon": "📈", "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "survivorship-bias",    "titel": "Survivorship Bias",         "icon": "✈️", "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "regression-zur-mitte", "titel": "Regression zur Mitte",      "icon": "📊", "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "simpson",              "titel": "Simpson-Paradoxon",         "icon": "📊", "dauer": "4 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
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
        "steps": [
            {"typ": "raetsel", "id": "geschwindigkeit",   "titel": "Durchschnittsgeschwindigkeit",  "icon": "🚗", "dauer": "4 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "achilles",          "titel": "Achilles & die Schildkröte",   "icon": "🐢", "dauer": "5 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "hilberts-hotel",    "titel": "Hilberts Hotel",               "icon": "🏨", "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "grandis-serie",     "titel": "Grandis Serie",                "icon": "∞",  "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "harmonische-reihe", "titel": "Die Harmonische Reihe",        "icon": "🌊", "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "collatz-vermutung", "titel": "Collatz-Vermutung",            "icon": "🔄", "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "gabriels-trompete", "titel": "Gabriels Trompete",            "icon": "🎺", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "parrondo",          "titel": "Parrondo-Paradoxon",           "icon": "🪙", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "ramanujan-summe",   "titel": "1+2+3+… = −1/12",             "icon": "🔢", "dauer": "5 min", "schwierigkeit": "Experte",        "beschreibung": ""},
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
        "steps": [
            {"typ": "raetsel", "id": "wasserkrug",         "titel": "Das Wasserkrug-Problem",    "icon": "🫙",  "dauer": "5 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "muenzwaegen",        "titel": "Die falsche Münze",         "icon": "🪙",  "dauer": "5 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "vergiftete-faesser", "titel": "Vergiftete Fässer",         "icon": "🪣",  "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "huete-spiel",        "titel": "Das Hüte-Rätsel",           "icon": "🎩",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "wason",              "titel": "Wason-Auswahlaufgabe",      "icon": "🃏",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "josephus",           "titel": "Das Josephus-Problem",      "icon": "⚔️", "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "barbier-paradoxon",  "titel": "Das Barbier-Paradoxon",     "icon": "✂️", "dauer": "4 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "piraten",            "titel": "Das Piratenspiel",          "icon": "🏴‍☠️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "henker",             "titel": "Das Henkerparadoxon",       "icon": "⚖️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
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
        "steps": [
            {"typ": "raetsel", "id": "anker-experiment",    "titel": "Der Anker-Effekt",          "icon": "⚓",  "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "framing",             "titel": "Framing-Effekt",            "icon": "🖼️", "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "konfirmationsfehler", "titel": "Der Konfirmationsfehler",   "icon": "🔍",  "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "dunning-kruger",      "titel": "Dunning-Kruger-Effekt",     "icon": "📉",  "dauer": "5 min", "schwierigkeit": "Mittel", "beschreibung": ""},
        ],
    },
    {
        "id": "psychologie",
        "title": "Psychologie & Verhalten",
        "subtitle": "Warum Menschen handeln, wie sie handeln",
        "icon": "🧬",
        "color": "pink",
        "level": "Einsteiger → Mittel",
        "dauer": "ca. 35 min",
        "beschreibung": (
            "Sozialpsychologie erklärt Verhalten, das Ökonomie nicht erklären kann. "
            "Von Priming über Dissonanz bis zu Herdenverhalten – dieser Pfad zeigt, "
            "wie unsichtbare Kräfte unsere Urteile und Entscheidungen formen."
        ),
        "was_du_lernst": [
            "Wie Priming Gedanken beeinflusst, bevor wir denken (Bargh 1996)",
            "Warum wir Überzeugungen ändern, statt Verhalten (Festinger 1959)",
            "Wie rationale Individuen kollektiv irren (Informationskaskade)",
            "Den Konfirmationsfehler: Wir suchen Bestätigung, nicht Widerlegung",
            "Dunning-Kruger: Unwissenheit über die eigene Unwissenheit",
        ],
        "steps": [
            {"typ": "raetsel", "id": "priming",              "titel": "Das Priming-Experiment",    "icon": "💡",  "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "kognitive-dissonanz",  "titel": "Kognitive Dissonanz",       "icon": "🔄",  "dauer": "5 min", "schwierigkeit": "Mittel", "beschreibung": ""},
            {"typ": "raetsel", "id": "informationskaskade",  "titel": "Informationskaskade",       "icon": "🫧",  "dauer": "5 min", "schwierigkeit": "Mittel", "beschreibung": ""},
            {"typ": "raetsel", "id": "konfirmationsfehler",  "titel": "Der Konfirmationsfehler",   "icon": "🔍",  "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "dunning-kruger",       "titel": "Dunning-Kruger-Effekt",     "icon": "📉",  "dauer": "5 min", "schwierigkeit": "Mittel", "beschreibung": ""},
            {"typ": "raetsel", "id": "framing",              "titel": "Framing-Effekt",            "icon": "🖼️", "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "anker-experiment",     "titel": "Der Anker-Effekt",          "icon": "⚓",  "dauer": "4 min", "schwierigkeit": "Einstieg","beschreibung": ""},
            {"typ": "raetsel", "id": "survivorship-bias",    "titel": "Survivorship Bias",         "icon": "✈️", "dauer": "5 min", "schwierigkeit": "Mittel", "beschreibung": ""},
        ],
    },
    {
        "id": "kommunikation",
        "title": "Kommunikation & Verhandlung",
        "subtitle": "Überzeugend argumentieren – rational verhandeln",
        "icon": "💬",
        "color": "teal",
        "level": "Einsteiger → Fortgeschritten",
        "dauer": "ca. 40 min",
        "beschreibung": (
            "Verhandlung ist angewandte Spieltheorie. "
            "Dieser Pfad verbindet BATNA-Kalkulation, Trugschluss-Erkennung und "
            "klassische Entscheidungsparadoxe zu einem kohärenten Kommunikations-Toolkit."
        ),
        "was_du_lernst": [
            "BATNA: deine Verhandlungsmacht kommt aus deiner besten Alternative",
            "Die 5 häufigsten Trugschlüsse erkennen und kontern",
            "Warum rationale Akteure systematisch zu wenig kooperieren",
            "Informationsasymmetrie als Verhandlungsvorteil (Akerlof, Spence)",
            "Anker setzen: der erste Wert prägt das gesamte Ergebnis",
        ],
        "steps": [
            {"typ": "raetsel", "id": "batna",            "titel": "BATNA – Verhandlungsmacht",   "icon": "🤝",  "dauer": "5 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "trugschluesse",    "titel": "Trugschlüsse erkennen",       "icon": "🧩",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "marktverlust",     "titel": "Markt für Zitronen",          "icon": "🍋",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "anker-experiment", "titel": "Der Anker-Effekt",            "icon": "⚓",  "dauer": "4 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "reisenden-dilemma","titel": "Reisenden-Dilemma",           "icon": "🧳",  "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "hotelling",        "titel": "Hotelling-Gesetz",            "icon": "🏖️", "dauer": "3 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "allais",           "titel": "Allais-Paradoxon",            "icon": "🎰",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "condorcet",        "titel": "Condorcet-Paradoxon",         "icon": "🗳️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
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
        "steps": [
            {"typ": "raetsel", "id": "hotelling",        "titel": "Hotelling-Gesetz",          "icon": "🏖️", "dauer": "3 min", "schwierigkeit": "Einstieg",       "beschreibung": ""},
            {"typ": "raetsel", "id": "st-petersburg",    "titel": "St. Petersburger Paradoxon","icon": "🎲",  "dauer": "4 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "allais",           "titel": "Allais-Paradoxon",          "icon": "🎰",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "ellsberg",         "titel": "Ellsberg-Paradoxon",        "icon": "🪬",  "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "zwei-umschlag",    "titel": "Zwei-Umschlag-Problem",     "icon": "✉️", "dauer": "5 min", "schwierigkeit": "Mittel",         "beschreibung": ""},
            {"typ": "raetsel", "id": "newcomb",          "titel": "Newcomb-Paradoxon",         "icon": "📦",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "reisenden-dilemma","titel": "Reisenden-Dilemma",         "icon": "🧳",  "dauer": "4 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "braess",           "titel": "Braess-Paradoxon",          "icon": "🛣️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "condorcet",        "titel": "Condorcet-Paradoxon",       "icon": "🗳️", "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
            {"typ": "raetsel", "id": "sekretaerin",      "titel": "Sekretärinnen-Problem",     "icon": "📋",  "dauer": "5 min", "schwierigkeit": "Fortgeschritten","beschreibung": ""},
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
    "pink":    {"bg": "bg-pink-500",    "light": "bg-pink-50",    "border": "border-pink-200",    "text": "text-pink-700",    "badge": "bg-pink-100 text-pink-800",    "btn": "bg-pink-600 hover:bg-pink-700",    "ring": "ring-pink-400"},
    "teal":    {"bg": "bg-teal-500",    "light": "bg-teal-50",    "border": "border-teal-200",    "text": "text-teal-700",    "badge": "bg-teal-100 text-teal-800",    "btn": "bg-teal-600 hover:bg-teal-700",    "ring": "ring-teal-400"},
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
