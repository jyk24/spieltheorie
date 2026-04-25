"""Rätsel & Paradoxe – einmalige spieltheoretische Denkexperimente."""
import datetime as _dt
import json
import random as _random

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/raetsel")
templates = Jinja2Templates(directory="app/templates")

RAETSEL_META = [
    # ── Wahrscheinlichkeit & Zufall ────────────────────────────────────────────
    {
        "id": "monty-hall",
        "name": "Monty Hall Problem",
        "icon": "🚪",
        "beschreibung": "Du wählst eine von drei Türen. Der Moderator öffnet eine falsche. Wechselst du? Die Antwort überrascht fast jeden.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "geburtstag",
        "name": "Geburtstagsparadoxon",
        "icon": "🎂",
        "beschreibung": "Wie viele Menschen braucht es, damit die Wahrscheinlichkeit eines gemeinsamen Geburtstags über 50 % liegt? Weit weniger als du denkst.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "spielerfehlschluss",
        "name": "Der Spielerfehlschluss",
        "icon": "🎰",
        "beschreibung": "1913, Monte Carlo: Die Roulette-Kugel fiel 26 Mal auf Schwarz. Spieler setzten Millionen auf Rot – und verloren alles. Warum vergangene Zufallsereignisse nichts über die Zukunft sagen.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "hundert-gefangene",
        "name": "Das 100-Gefangenen-Problem",
        "icon": "📦",
        "beschreibung": "100 Gefangene, 100 Boxen mit Nummern. Jeder darf 50 öffnen. Zufällig überleben fast 0% – mit einer cleveren Strategie plötzlich 30%. Wie?",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "coupon-sammler",
        "name": "Das Coupon-Sammler-Problem",
        "icon": "🎟️",
        "beschreibung": "6 verschiedene Figuren im Überraschungsei. Wie viele Eier braucht man im Schnitt, um alle zu haben? Intuitiv sagt man 6 – die Mathematik antwortet: 14,7. Warum?",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "schlafendes-maedchen",
        "name": "Das Schlafendes-Mädchen-Paradoxon",
        "icon": "😴",
        "beschreibung": "Vor dem Schlafen: P(Kopf) = ½. Nach dem Aufwachen – ohne neue Information – sagen manche Mathematiker: P(Kopf) = ⅓. Wer hat recht? Das Paradoxon spaltet Philosophen und Statistiker.",
        "typ": "Wahrscheinlichkeits-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    {
        "id": "bertrand-paradoxon",
        "name": "Das Bertrand-Paradoxon",
        "icon": "⭕",
        "beschreibung": "Ziehe eine zufällige Sehne in einem Kreis. Ist sie länger als die Dreiecksseite? Je nach Definition von 'zufällig' lautet die Antwort ⅓, ½ oder ¼. Bertrand (1889) zeigte: Wahrscheinlichkeit braucht Präzision.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Wahrscheinlichkeit",
    },
    # ── Statistik & Kognition ──────────────────────────────────────────────────
    {
        "id": "simpson",
        "name": "Simpson-Paradoxon",
        "icon": "📊",
        "beschreibung": "Medikament A ist in jeder Untergruppe besser – trotzdem gewinnt Medikament B in der Gesamtstatistik. Warum?",
        "typ": "Statistik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Statistik",
    },
    {
        "id": "falsch-positiv",
        "name": "Das Falsch-Positiv-Paradoxon",
        "icon": "🔬",
        "beschreibung": "Ein 99%-genauer Test für eine Krankheit mit 0,1% Häufigkeit. Du testest positiv. Wie groß ist die Wahrscheinlichkeit, wirklich krank zu sein? Die Antwort schockiert Ärzte und Patienten.",
        "typ": "Statistik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Statistik",
    },
    {
        "id": "bayes-theorem",
        "name": "Das Bayes-Theorem",
        "icon": "📐",
        "beschreibung": "Wie aktualisieren wir Überzeugungen rational auf Basis neuer Beweise? Bayes (1763) lieferte die Formel. Drei interaktive Szenarien: Medizintest, Spam-Filter, und eigene Parameter.",
        "typ": "Statistik-Interaktiv",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Statistik",
    },
    {
        "id": "gesetz-grosse-zahlen",
        "name": "Gesetz der großen Zahlen",
        "icon": "📈",
        "beschreibung": "Je mehr Würfe, desto näher am Erwartungswert – aber nie garantiert genau. Bernoulli bewies das 1713. Und was unterscheidet dieses Gesetz vom Spielerfehlschluss?",
        "typ": "Statistik-Interaktiv",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Statistik",
    },
    {
        "id": "anker-experiment",
        "name": "Der Anker-Effekt",
        "icon": "⚓",
        "beschreibung": "Sieh eine zufällige Zahl – und schätze dann etwas völlig anderes. Am Ende siehst du, wie stark der Anker deine Schätzungen verzerrt hat. Das Experiment an dir selbst.",
        "typ": "Verhaltens-Experiment",
        "schwierigkeit": "Einsteiger",
        "dauer": "4 min",
        "kategorie": "Kognition",
    },
    {
        "id": "framing",
        "name": "Framing-Effekt",
        "icon": "🖼️",
        "beschreibung": "600 Menschen sind in Gefahr. Zwei Programme, zwei Formulierungen. Kahneman & Tversky zeigten 1981: Wie eine Entscheidung beschrieben wird, ändert das Ergebnis – auch wenn die Zahlen identisch sind.",
        "typ": "Verhaltens-Experiment",
        "schwierigkeit": "Einsteiger",
        "dauer": "4 min",
        "kategorie": "Kognition",
    },
    {
        "id": "wason",
        "name": "Wason-Auswahlaufgabe",
        "icon": "🃏",
        "beschreibung": "Vier Karten, eine Regel. Welche musst du umdrehen? Nur ~10% lösen die abstrakte Version – aber fast alle die soziale Version. Cosmides (1989) entdeckte: Unser Gehirn ist für soziale Regeln optimiert.",
        "typ": "Logik-Experiment",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    # ── Mathematik & Unendlichkeit ─────────────────────────────────────────────
    {
        "id": "achilles",
        "name": "Achilles und die Schildkröte",
        "icon": "🐢",
        "beschreibung": "Achilles läuft 10× schneller als eine Schildkröte. Dennoch behauptete Zenon (~450 v.Chr.), er könne sie nie einholen – wegen unendlich vieler Zwischenschritte. Wer hat recht?",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "geschwindigkeit",
        "name": "Durchschnittsgeschwindigkeit-Paradoxon",
        "icon": "🚗",
        "beschreibung": "Du fährst die erste Hälfte einer Strecke mit 50 km/h. Wie schnell muss die zweite Hälfte sein, damit du 100 km/h Durchschnitt erreichst? Die Antwort ist unmöglich – und mathematisch beweisbar.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Einsteiger",
        "dauer": "4 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "grandis-serie",
        "name": "Grandis Serie",
        "icon": "∞",
        "beschreibung": "1 − 1 + 1 − 1 + … Was ergibt das? Grandi behauptete 1703: ½. Die Partialsummen schwingen zwischen 0 und 1. Trotzdem lässt sich ½ mathematisch exakt rechtfertigen – mit Cesàro-Summation.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "harmonische-reihe",
        "name": "Die Harmonische Reihe",
        "icon": "🌊",
        "beschreibung": "1 + ½ + ⅓ + ¼ + … – jedes Glied wird kleiner, trotzdem divergiert die Reihe. Oresme bewies das 1350. Wie viele Glieder braucht man, um 10 zu überschreiten? Die Antwort: 12.367.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "ramanujan-summe",
        "name": "1 + 2 + 3 + … = −1/12",
        "icon": "🔢",
        "beschreibung": "Ramanujan schrieb 1913 an Hardy: Die Summe aller natürlichen Zahlen ist −1/12. Hardy hielt ihn für einen Betrüger – bis er die Beweise sah. Wie ist das möglich?",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "gabriels-trompete",
        "name": "Gabriels Trompete",
        "icon": "🎺",
        "beschreibung": "Ein Körper mit unendlicher Oberfläche – aber endlichem Volumen. Er kann mit Farbe gefüllt, aber nicht angestrichen werden. Torricelli (1643) entdeckte das erste mathematische Objekt dieser Art.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "hilberts-hotel",
        "name": "Hilberts Hotel",
        "icon": "🏨",
        "beschreibung": "Ein Hotel mit unendlich vielen Zimmern – alle belegt. Trotzdem gibt es immer Platz für neue Gäste. Hilbert (1924) zeigt: Unendlichkeit spielt nach anderen Regeln als Endlichkeit.",
        "typ": "Mathematik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "josephus",
        "name": "Das Josephus-Problem",
        "icon": "⚔️",
        "beschreibung": "10 Soldaten stehen im Kreis. Jeder zweite wird eliminiert. Wo musst du stehen, um zu überleben? Die Antwort folgt einem überraschenden Muster.",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Mathematik",
    },
    # ── Logik & Rätsel ─────────────────────────────────────────────────────────
    {
        "id": "piraten",
        "name": "Das Piratenspiel",
        "icon": "🏴‍☠️",
        "beschreibung": "5 Piraten teilen 100 Goldstücke. Wie viel bekommt der Anführer laut Rückwärtsinduktion? Die Antwort schockiert fast jeden.",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    {
        "id": "henker",
        "name": "Das Henkerparadoxon",
        "icon": "⚖️",
        "beschreibung": "Der Richter verspricht eine überraschende Hinrichtung nächste Woche. Der Gefangene beweist mit Rückwärtsinduktion, dass sie unmöglich stattfinden kann – und wird trotzdem überrascht.",
        "typ": "Logik-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    {
        "id": "vergiftete-faesser",
        "name": "Die vergifteten Fässer",
        "icon": "🪣",
        "beschreibung": "1000 Fässer, eines vergiftet. Das Gift wirkt nach einer Nacht. Wie viele Tester brauchst du mindestens, um das vergiftete Fass in einer Nacht zu identifizieren?",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Logik",
    },
    {
        "id": "huete-spiel",
        "name": "Das Hüte-Rätsel",
        "icon": "🎩",
        "beschreibung": "Drei Gefangene tragen Hüte (3 weiß, 2 rot). C sagt 'ich weiß nicht', B sagt 'ich weiß nicht'. Was schlussfolgert Gefangener A über seinen eigenen Hut?",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    {
        "id": "muenzwaegen",
        "name": "Die falsche Münze",
        "icon": "🪙",
        "beschreibung": "9 Münzen – eine ist schwerer als die anderen. Du hast eine Balkenwaage und genau 2 Wägungen. Kannst du die schwere Münze immer finden?",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Einsteiger",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    {
        "id": "wasserkrug",
        "name": "Das Wasserkrug-Problem",
        "icon": "🫙",
        "beschreibung": "Zwei Krüge: 3 Liter und 5 Liter. Kein Maßstrich. Wie misst du exakt 4 Liter ab? Interaktiv – fülle und leere die Krüge selbst.",
        "typ": "Logik-Puzzle",
        "schwierigkeit": "Einsteiger",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    {
        "id": "zerrissene-karte",
        "name": "Die zerrissene Karte",
        "icon": "🃏",
        "beschreibung": "Du hast 5 rote Karten (Monopol), 5 andere je eine blaue. Ein Paar = 1 €. Welche Strategie bringt mehr: Alle annehmen? Hart verhandeln? Oder eine Karte öffentlich zerreißen?",
        "typ": "Monopol-Experiment",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Logik",
    },
    # ── Spieltheorie & Entscheidung ────────────────────────────────────────────
    {
        "id": "allais",
        "name": "Allais-Paradoxon",
        "icon": "🎰",
        "beschreibung": "Zwei Lotterie-Entscheidungen, kein Feedback dazwischen. Am Ende zeigt sich: deine Wahl widerspricht sich selbst – wie bei fast allen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "ellsberg",
        "name": "Ellsberg-Paradoxon",
        "icon": "🪬",
        "beschreibung": "Eine Urne, 90 Kugeln – 30 rot, 60 schwarz oder gelb (Verhältnis unbekannt). Zwei Wetten. Deine Wahl widerspricht der Erwartungsnutzentheorie – und zeigt, dass Ambiguität anders wirkt als Risiko.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "newcomb",
        "name": "Newcomb-Paradoxon",
        "icon": "📦",
        "beschreibung": "Eine Box oder zwei? Ein nahezu unfehlbarer Vorhersager hat bereits entschieden – und beide Entscheidungen lassen sich rational begründen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "st-petersburg",
        "name": "St. Petersburger Paradoxon",
        "icon": "🎲",
        "beschreibung": "Ein Spiel mit theoretisch unendlichem Erwartungswert – und doch würde kaum jemand mehr als 30€ dafür zahlen. Warum?",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "zwei-umschlag",
        "name": "Zwei-Umschlag-Problem",
        "icon": "✉️",
        "beschreibung": "Du hast einen Umschlag mit Geld. Der andere enthält doppelt oder halb so viel. Tauschen? Das Argument sagt immer ja – aber das kann nicht stimmen.",
        "typ": "Entscheidungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "reisenden-dilemma",
        "name": "Reisenden-Dilemma",
        "icon": "🧳",
        "beschreibung": "Wähle eine Zahl von 2–100. Nash-Gleichgewicht sagt: 2. Aber fast alle Menschen spielen 95+ und verdienen mehr.",
        "typ": "Strategieparadox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "condorcet",
        "name": "Condorcet-Paradoxon",
        "icon": "🗳️",
        "beschreibung": "Drei Wähler, drei Optionen – und die Mehrheitswahl dreht im Kreis. Das Fundament der Social-Choice-Theorie.",
        "typ": "Abstimmungsparadox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "sekretaerin",
        "name": "Sekretärinnen-Problem",
        "icon": "📋",
        "beschreibung": "Du bewertest Kandidaten nacheinander, ohne zurückgehen zu können. Wann hörst du auf zu suchen? Die optimale Strategie basiert auf der Zahl e.",
        "typ": "Optimierungsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "braess",
        "name": "Braess-Paradoxon",
        "icon": "🛣️",
        "beschreibung": "Eine neue Straße hinzufügen kann den Verkehr für alle verlangsamen. Das Nash-Gleichgewicht ist nicht das gesellschaftliche Optimum.",
        "typ": "Spieltheorie-Paradox",
        "schwierigkeit": "Fortgeschritten",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "hotelling",
        "name": "Hotelling-Gesetz",
        "icon": "🏖️",
        "beschreibung": "Zwei Eiswagen auf einem Strand – wo stellst du dich auf? Die Nash-Logik treibt beide in die Mitte, zum Schaden aller Kunden.",
        "typ": "Wettbewerbsparadox",
        "schwierigkeit": "Einsteiger",
        "dauer": "3 min",
        "kategorie": "Spieltheorie",
    },
    {
        "id": "el-farol",
        "name": "El Farol Bar Problem",
        "icon": "🍺",
        "beschreibung": "Die Bar macht Spaß, solange weniger als 60 von 100 Stammgästen kommen. Aber wenn alle so rechnen – was passiert dann?",
        "typ": "Koordinationsparadox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Spieltheorie",
    },
    # ── Kognition & Psychologie ────────────────────────────────────────────────
    {
        "id": "konfirmationsfehler",
        "name": "Der Konfirmationsfehler",
        "icon": "🔍",
        "beschreibung": "Du siehst Zahlen in einer Sequenz. Dein Ziel: die Regel herausfinden. Wason (1960) zeigte, dass Menschen fast immer bestätigen statt widerlegen – auch wenn Widerlegung viel schneller zur Lösung führt.",
        "typ": "Kognitions-Experiment",
        "schwierigkeit": "Einsteiger",
        "dauer": "4 min",
        "kategorie": "Kognition",
    },
    {
        "id": "dunning-kruger",
        "name": "Dunning-Kruger-Effekt",
        "icon": "📉",
        "beschreibung": "Schätze dein Wissen in verschiedenen Bereichen ein – dann vergleiche mit dem Durchschnitt. Dunning & Kruger (1999) fanden: Inkompetente überschätzen sich, Experten unterschätzen sich. Das Paradox des Nicht-Wissens.",
        "typ": "Selbsteinschätzungs-Experiment",
        "schwierigkeit": "Einsteiger",
        "dauer": "5 min",
        "kategorie": "Kognition",
    },
    {
        "id": "survivorship-bias",
        "name": "Survivorship Bias",
        "icon": "✈️",
        "beschreibung": "Wo soll man Bomber im WWII panzerplatten? Dort, wo die Einschüsse sind? Abraham Wald (1943) dachte anders – und rettete damit tausende Leben. Der klassische Fehler: nur die Überlebenden zu beobachten.",
        "typ": "Statistik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Statistik",
    },
    {
        "id": "regression-zur-mitte",
        "name": "Regression zur Mitte",
        "icon": "📊",
        "beschreibung": "Warum schneiden Sportler nach dem Titelblatt schlechter ab? Warum wirken Strafen besser als Lob? Galton (1886) entdeckte: extreme Ergebnisse neigen zur Mitte – ganz ohne kausale Erklärung.",
        "typ": "Statistik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Statistik",
    },
    {
        "id": "collatz-vermutung",
        "name": "Die Collatz-Vermutung",
        "icon": "🔄",
        "beschreibung": "Nimm eine beliebige Zahl. Gerade? Halbiere. Ungerade? Mal 3 plus 1. Wiederhole. Lothar Collatz (1937) behauptete: du landest immer bei 1. Klingt einfach – kein Mensch hat es bisher bewiesen.",
        "typ": "Mathematik-Vermutung",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Mathematik",
    },
    {
        "id": "barbier-paradoxon",
        "name": "Das Barbier-Paradoxon",
        "icon": "✂️",
        "beschreibung": "Ein Barbier rasiert alle, die sich nicht selbst rasieren. Rasiert er sich selbst? Bertrand Russell (1901) zeigte: Diese Frage hat keine konsistente Antwort – und erschütterte damit die Grundlagen der Mathematik.",
        "typ": "Logik-Paradox",
        "schwierigkeit": "Mittel",
        "dauer": "4 min",
        "kategorie": "Logik",
    },
    {
        "id": "informationskaskade",
        "name": "Informationskaskade",
        "icon": "🫧",
        "beschreibung": "Drei Personen vor dir wählten alle Urne A. Deine private Kugel sagt etwas anderes. Wem vertraust du – der Masse oder dir selbst? Bikhchandani (1992) zeigte: Es kann rational sein, die eigene Information zu ignorieren.",
        "typ": "Entscheidungsexperiment",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Kognition",
    },
    {
        "id": "marktverlust",
        "name": "Der Markt für Zitronen",
        "icon": "🍋",
        "beschreibung": "10 Gebrauchtwagen, Qualität 1–10. Nur der Verkäufer kennt die echte Qualität. Beobachte Runde für Runde, wie der Markt kollabiert – das Akerlof-Paradoxon (Nobelpreis 2001) interaktiv simuliert.",
        "typ": "Marktmechanismus",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Spieltheorie",
    },
    # ── Psychologie & Sozialverhalten ─────────────────────────────────────────
    {
        "id": "priming",
        "name": "Das Priming-Experiment",
        "icon": "💡",
        "beschreibung": "Fünf Wörter – und deine nächste Assoziation verschiebt sich messbar. Erlebe Priming am eigenen Beispiel: Beeinflusst ein unsichtbarer Kontext deine spontanen Gedanken?",
        "typ": "Psychologie-Experiment",
        "schwierigkeit": "Einsteiger",
        "dauer": "4 min",
        "kategorie": "Psychologie",
    },
    {
        "id": "kognitive-dissonanz",
        "name": "Kognitive Dissonanz",
        "icon": "🔄",
        "beschreibung": "Festinger 1959: Wer eine langweilige Aufgabe für 1 Dollar als interessant bezeichnet, glaubt das hinterher wirklich – mehr als jemand mit 20 Dollar. Warum ändern wir Überzeugungen statt Verhalten?",
        "typ": "Psychologie-Quiz",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Psychologie",
    },
    # ── Kommunikation & Rhetorik ──────────────────────────────────────────────
    {
        "id": "batna",
        "name": "BATNA – Die Verhandlungsmacht",
        "icon": "🤝",
        "beschreibung": "Deine Stärke in Verhandlungen hängt nicht davon ab, wie sehr du willst – sondern wie gut deine Alternative ist. Kalkuliere deinen BATNA und visualisiere die Verhandlungszone interaktiv.",
        "typ": "Verhandlungs-Simulation",
        "schwierigkeit": "Einsteiger",
        "dauer": "5 min",
        "kategorie": "Kommunikation",
    },
    {
        "id": "trugschluesse",
        "name": "Trugschlüsse erkennen",
        "icon": "🧩",
        "beschreibung": "5 Argumente, die überzeugend klingen – aber logisch fehlerhaft sind. Ad Hominem, Strohmann, Falsche Dichotomie, Slippery Slope, Appeal to Authority. Erkennst du sie alle?",
        "typ": "Logik-Quiz",
        "schwierigkeit": "Mittel",
        "dauer": "5 min",
        "kategorie": "Kommunikation",
    },
]


# ---------------------------------------------------------------------------
# Übersicht
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
def raetsel_overview(request: Request):
    day_num = _dt.date.today().timetuple().tm_yday
    featured = RAETSEL_META[day_num % len(RAETSEL_META)]
    return templates.TemplateResponse(
        request, "raetsel.html", {
            "active_page": "raetsel",
            "raetsel": RAETSEL_META,
            "featured_raetsel": featured,
            "total_raetsel": len(RAETSEL_META),
        }
    )


# ---------------------------------------------------------------------------
# Monty Hall Problem
# ---------------------------------------------------------------------------

@router.get("/monty-hall", response_class=HTMLResponse)
def monty_hall_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/monty_hall.html", {"active_page": "raetsel"}
    )


@router.post("/monty-hall/reveal", response_class=HTMLResponse)
def monty_hall_reveal(request: Request, chosen: int = Form(...)):
    """Spieler hat Tür gewählt – Moderator öffnet eine Ziegentür."""
    winning = _random.randint(1, 3)
    options = [d for d in [1, 2, 3] if d != chosen and d != winning]
    revealed = _random.choice(options)
    switch_door = next(d for d in [1, 2, 3] if d != chosen and d != revealed)
    return templates.TemplateResponse(
        request,
        "partials/monty_reveal.html",
        {
            "chosen": chosen,
            "winning": winning,
            "revealed": revealed,
            "switch_door": switch_door,
        },
    )


@router.post("/monty-hall/result", response_class=HTMLResponse)
def monty_hall_result(
    request: Request,
    chosen: int = Form(...),
    winning: int = Form(...),
    decision: str = Form(...),
    switch_door: int = Form(...),
):
    final_door = chosen if decision == "stay" else switch_door
    won = final_door == winning
    # Deterministische Simulation (analytisch exakt)
    sim_n = 10000
    sim_stay_wins = round(sim_n / 3)
    sim_switch_wins = sim_n - sim_stay_wins
    return templates.TemplateResponse(
        request,
        "partials/monty_result.html",
        {
            "chosen": chosen,
            "winning": winning,
            "final_door": final_door,
            "decision": decision,
            "switch_door": switch_door,
            "won": won,
            "sim_n": sim_n,
            "sim_stay_wins": sim_stay_wins,
            "sim_switch_wins": sim_switch_wins,
            "sim_stay_rate": round(sim_stay_wins / sim_n * 100),
            "sim_switch_rate": round(sim_switch_wins / sim_n * 100),
        },
    )


# ---------------------------------------------------------------------------
# Allais-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/allais", response_class=HTMLResponse)
def allais_page(request: Request):
    order1 = _random.sample(["A", "B"], 2)
    return templates.TemplateResponse(
        request, "raetsel/allais.html", {"active_page": "raetsel", "order1": order1}
    )


@router.post("/allais/phase2", response_class=HTMLResponse)
def allais_phase2(request: Request, choice1: str = Form(...)):
    order2 = _random.sample(["C", "D"], 2)
    return templates.TemplateResponse(
        request, "partials/allais_phase2.html", {"choice1": choice1, "order2": order2}
    )


@router.post("/allais/result", response_class=HTMLResponse)
def allais_result(
    request: Request,
    choice1: str = Form(...),
    choice2: str = Form(...),
):
    # A + D  oder  B + C  sind inkonsistent (verletzen Unabhängigkeitsaxiom)
    # A + C  oder  B + D  sind konsistent
    inconsistent = (choice1 == "A" and choice2 == "D") or (choice1 == "B" and choice2 == "C")
    choice1_label = "A (sichere Million)" if choice1 == "A" else "B (Risiko mit höherem Erwartungswert)"
    choice2_label = "D (höherer Erwartungswert)" if choice2 == "D" else "C (kleinere sichere Chance)"
    return templates.TemplateResponse(
        request,
        "partials/allais_result.html",
        {
            "choice1": choice1,
            "choice2": choice2,
            "choice1_label": choice1_label,
            "choice2_label": choice2_label,
            "inconsistent": inconsistent,
        },
    )


# ---------------------------------------------------------------------------
# Piratenspiel
# ---------------------------------------------------------------------------

# Rückwärtsinduktions-Schritte (für die Erklärung)
PIRATE_STEPS = [
    {
        "n": 2,
        "pirates": "P4 + P5",
        "proposal": [None, None, None, 100, 0],
        "votes": "P4 stimmt ja (50% = Mehrheit mit Tie-Breaking). Angenommen.",
        "reasoning": "P4 braucht nur die eigene Stimme.",
    },
    {
        "n": 3,
        "pirates": "P3 + P4 + P5",
        "proposal": [None, None, 99, 0, 1],
        "votes": "P3 + P5 stimmen ja (2/3).",
        "reasoning": "P4 würde bei 2 Piraten 100 bekommen → nicht zu bestechen. P5 würde 0 bekommen → 1 Münze reicht.",
    },
    {
        "n": 4,
        "pirates": "P2 + P3 + P4 + P5",
        "proposal": [None, 99, 0, 1, 0],
        "votes": "P2 + P4 stimmen ja (2/4 = 50%).",
        "reasoning": "P3 würde 99 bekommen → zu teuer. P4 würde 0 bekommen → 1 Münze reicht. P5 würde 1 bekommen → bräuchte 2 Münzen → teurer.",
    },
    {
        "n": 5,
        "pirates": "P1 + P2 + P3 + P4 + P5",
        "proposal": [98, 0, 1, 0, 1],
        "votes": "P1 + P3 + P5 stimmen ja (3/5).",
        "reasoning": "P2 würde 99 bekommen → nicht zu bestechen. P3 würde 0 bekommen → 1 Münze reicht. P4 würde 1 bekommen → bräuchte 2 Münzen. P5 würde 0 bekommen → 1 Münze reicht. Günstigste Option: P3 + P5 je 1 Münze.",
    },
]

PIRATE_SOLUTION = [98, 0, 1, 0, 1]


@router.get("/piraten", response_class=HTMLResponse)
def piraten_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/piraten.html", {"active_page": "raetsel"}
    )


@router.post("/piraten/result", response_class=HTMLResponse)
def piraten_result(
    request: Request,
    p1: int = Form(...),
    p2: int = Form(...),
    p3: int = Form(...),
    p4: int = Form(...),
    p5: int = Form(...),
):
    player_guess = [p1, p2, p3, p4, p5]
    total = sum(player_guess)
    diff = sum(abs(player_guess[i] - PIRATE_SOLUTION[i]) for i in range(5))
    exact = player_guess == PIRATE_SOLUTION
    close = diff <= 15 and not exact
    return templates.TemplateResponse(
        request,
        "partials/piraten_result.html",
        {
            "player_guess": player_guess,
            "solution": PIRATE_SOLUTION,
            "total": total,
            "exact": exact,
            "close": close,
            "diff": diff,
            "steps": PIRATE_STEPS,
        },
    )


# ---------------------------------------------------------------------------
# St. Petersburger Paradoxon
# ---------------------------------------------------------------------------

@router.get("/st-petersburg", response_class=HTMLResponse)
def st_petersburg_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/st_petersburg.html", {"active_page": "raetsel"}
    )


@router.post("/st-petersburg/result", response_class=HTMLResponse)
def st_petersburg_result(
    request: Request,
    wtp: int = Form(...),
):
    # Expected value after N flips = sum of 2^n * (1/2)^n = sum of 1 → infinite
    # Bernoulli's log utility: U = log2(wtp) → fair price ≈ log2(wealth)
    # Typical WTP in studies: 10-30€
    import math
    ev_10 = sum(2**n * (0.5**n) for n in range(1, 11))  # truncated at 10 flips
    ev_20 = sum(2**n * (0.5**n) for n in range(1, 21))
    log_utility_price = round(math.log2(max(wtp, 1)) * 2)

    if wtp <= 10:
        reaction = "sehr_niedrig"
    elif wtp <= 30:
        reaction = "typisch"
    elif wtp <= 100:
        reaction = "hoch"
    else:
        reaction = "sehr_hoch"

    return templates.TemplateResponse(
        request,
        "partials/st_petersburg_result.html",
        {
            "wtp": wtp,
            "ev_10": round(ev_10, 1),
            "ev_20": round(ev_20, 1),
            "log_utility_price": log_utility_price,
            "reaction": reaction,
        },
    )


# ---------------------------------------------------------------------------
# Reisenden-Dilemma
# ---------------------------------------------------------------------------

@router.get("/reisenden-dilemma", response_class=HTMLResponse)
def reisenden_dilemma_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/reisenden_dilemma.html", {"active_page": "raetsel"}
    )


@router.post("/reisenden-dilemma/result", response_class=HTMLResponse)
def reisenden_dilemma_result(
    request: Request,
    claim: int = Form(...),
):
    # Nash equilibrium: claim = 2 (iterated dominance argument)
    # Against Nash player: if you claim X, Nash player claims 2
    # You get max(2, claim) - 2 = 0 if claim >= 3, or 4 if claim = 2
    # Wait - let's recalculate:
    # Rules: lower claimant gets their value + 2, higher gets lower value - 2
    # If claim=100, Nash=2: you get 2-2=0, Nash gets 2+2=4 → Nash wins
    # If claim=2, Nash=2: both get 2 → tie
    # Against high human players (avg ~90): claim=97 → you get 97+2=99, they get 97-2=95 → you win!
    nash_claim = 2
    if claim == nash_claim:
        your_payoff = claim
        nash_payoff = nash_claim
    elif claim < nash_claim:
        your_payoff = claim + 2
        nash_payoff = claim - 2
    else:  # claim > nash_claim
        your_payoff = nash_claim - 2
        nash_payoff = nash_claim + 2

    # Against a typical human (claim ~90)
    human_avg = 90
    if claim == human_avg:
        vs_human_you = claim
        vs_human_other = human_avg
    elif claim < human_avg:
        vs_human_you = claim + 2
        vs_human_other = claim - 2
    else:
        vs_human_you = human_avg - 2
        vs_human_other = human_avg + 2

    # Nash iteration explanation
    dominance_steps = [
        {"from": 100, "to": 99, "reason": "Wenn du 100 bietest und der andere auch – wechsle zu 99: du bekommst 99+2=101 statt 100"},
        {"from": 99, "to": 98, "reason": "Wenn du 99 bietest und der andere auch – wechsle zu 98: 98+2=100 > 99"},
        {"from": 98, "to": "...", "reason": "Dieses Argument wiederholt sich... bis zum Boden"},
        {"from": 3, "to": 2, "reason": "Der letzte Schritt: von 3 zu 2. Nash-Gleichgewicht = 2"},
    ]

    return templates.TemplateResponse(
        request,
        "partials/reisenden_dilemma_result.html",
        {
            "claim": claim,
            "your_payoff_vs_nash": your_payoff,
            "nash_payoff": nash_payoff,
            "vs_human_you": vs_human_you,
            "vs_human_other": vs_human_other,
            "human_avg": human_avg,
            "dominance_steps": dominance_steps,
        },
    )


# ---------------------------------------------------------------------------
# Condorcet-Paradoxon
# ---------------------------------------------------------------------------

CONDORCET_VOTERS = [
    {"name": "Wähler 1", "icon": "👤", "prefs": ["A", "B", "C"], "label": "A > B > C"},
    {"name": "Wähler 2", "icon": "👥", "prefs": ["B", "C", "A"], "label": "B > C > A"},
    {"name": "Wähler 3", "icon": "🧑", "prefs": ["C", "A", "B"], "label": "C > A > B"},
]

# Pairwise results
CONDORCET_DUELS = [
    {
        "match": "A vs. B",
        "winner": "A",
        "votes": {"A": 2, "B": 1},
        "voters_for_A": ["Wähler 1 (A>B)", "Wähler 3 (A>B)"],
        "voters_for_B": ["Wähler 2 (B>A)"],
    },
    {
        "match": "B vs. C",
        "winner": "B",
        "votes": {"B": 2, "C": 1},
        "voters_for_A": ["Wähler 1 (B>C)", "Wähler 2 (B>C)"],
        "voters_for_B": ["Wähler 3 (C>B)"],
    },
    {
        "match": "C vs. A",
        "winner": "C",
        "votes": {"C": 2, "A": 1},
        "voters_for_A": ["Wähler 2 (C>A)", "Wähler 3 (C>A)"],
        "voters_for_B": ["Wähler 1 (A>C)"],
    },
]


@router.get("/condorcet", response_class=HTMLResponse)
def condorcet_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/condorcet.html",
        {"active_page": "raetsel", "voters": CONDORCET_VOTERS},
    )


@router.post("/condorcet/result", response_class=HTMLResponse)
def condorcet_result(request: Request):
    return templates.TemplateResponse(
        request,
        "partials/condorcet_result.html",
        {
            "voters": CONDORCET_VOTERS,
            "duels": CONDORCET_DUELS,
        },
    )


# ---------------------------------------------------------------------------
# Newcomb-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/newcomb", response_class=HTMLResponse)
def newcomb_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/newcomb.html", {"active_page": "raetsel"}
    )


@router.post("/newcomb/result", response_class=HTMLResponse)
def newcomb_result(
    request: Request,
    choice: str = Form(...),   # "b_only" or "both"
):
    # Expected value calculation
    accuracy = 0.95
    ev_b_only = round(accuracy * 1_000_000)          # 950.000
    ev_both   = round(1_000 + (1 - accuracy) * 1_000_000)  # 51.000
    return templates.TemplateResponse(
        request,
        "partials/newcomb_result.html",
        {
            "choice": choice,
            "ev_b_only": ev_b_only,
            "ev_both": ev_both,
            "accuracy": int(accuracy * 100),
        },
    )


# ---------------------------------------------------------------------------
# Simpson-Paradoxon
# ---------------------------------------------------------------------------

# Klassisches Nierenstein-Beispiel (Charig et al. 1986)
SIMPSON_DATA = {
    "overall": {
        "A": {"success": 273, "total": 350, "rate": 78},
        "B": {"success": 289, "total": 350, "rate": 83},
        "winner": "B",
    },
    "small_stones": {
        "label": "Kleine Nierensteine",
        "A": {"success": 81, "total": 87, "rate": 93},
        "B": {"success": 234, "total": 270, "rate": 87},
        "winner": "A",
    },
    "large_stones": {
        "label": "Große Nierensteine",
        "A": {"success": 192, "total": 263, "rate": 73},
        "B": {"success": 55, "total": 80, "rate": 69},
        "winner": "A",
    },
}


@router.get("/simpson", response_class=HTMLResponse)
def simpson_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/simpson.html",
        {
            "active_page": "raetsel",
            "overall": SIMPSON_DATA["overall"],
        },
    )


@router.post("/simpson/result", response_class=HTMLResponse)
def simpson_result(
    request: Request,
    choice: str = Form(...),  # "A" or "B"
):
    return templates.TemplateResponse(
        request,
        "partials/simpson_result.html",
        {
            "choice": choice,
            "data": SIMPSON_DATA,
        },
    )


# ---------------------------------------------------------------------------
# Geburtstagsparadoxon
# ---------------------------------------------------------------------------

import math as _math

_birthday_table = []
for _n in range(1, 51):
    _p_no_match = 1.0
    for _k in range(_n):
        _p_no_match *= (365 - _k) / 365
    _birthday_table.append({"n": _n, "prob": round((1 - _p_no_match) * 100, 1)})


@router.get("/geburtstag", response_class=HTMLResponse)
def geburtstag_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/geburtstag.html", {"active_page": "raetsel"}
    )


@router.post("/geburtstag/result", response_class=HTMLResponse)
def geburtstag_result(
    request: Request,
    guess: int = Form(...),   # player's guess for how many people needed for 50%
):
    # Correct answer: 23 people → 50.7%
    correct = 23
    diff = abs(guess - correct)
    if diff == 0:
        reaction = "exakt"
    elif diff <= 5:
        reaction = "nah"
    elif diff <= 15:
        reaction = "mittel"
    else:
        reaction = "weit"

    # Prob for player's guess
    p_no_match = 1.0
    for k in range(min(guess, 365)):
        p_no_match *= (365 - k) / 365
    p_guess = round((1 - p_no_match) * 100, 1)

    # Highlight a few milestones
    milestones = [
        {"n": 10, "prob": 11.7},
        {"n": 23, "prob": 50.7},
        {"n": 30, "prob": 70.6},
        {"n": 50, "prob": 97.0},
        {"n": 70, "prob": 99.9},
    ]
    return templates.TemplateResponse(
        request,
        "partials/geburtstag_result.html",
        {
            "guess": guess,
            "correct": correct,
            "diff": diff,
            "reaction": reaction,
            "p_guess": p_guess,
            "milestones": milestones,
            "table": _birthday_table,
        },
    )


# ---------------------------------------------------------------------------
# Zwei-Umschlag-Problem
# ---------------------------------------------------------------------------

@router.get("/zwei-umschlag", response_class=HTMLResponse)
def zwei_umschlag_page(request: Request):
    amount = _random.choice([10, 20, 50, 100, 200])
    return templates.TemplateResponse(
        request,
        "raetsel/zwei_umschlag.html",
        {"active_page": "raetsel", "amount": amount},
    )


@router.post("/zwei-umschlag/result", response_class=HTMLResponse)
def zwei_umschlag_result(
    request: Request,
    decision: str = Form(...),   # "stay" or "switch"
    amount: int = Form(...),
):
    # If player switches: 50% chance double (2*amount), 50% chance half (amount/2)
    ev_switch = 0.5 * (2 * amount) + 0.5 * (amount / 2)
    ev_stay = amount
    # The paradox: expected value calculation seems to say always switch
    # But this is wrong because the setup constrains the other envelope
    # If amount=X, other is either X/2 or 2X, so either you have the small or large one
    # True EV if amount is the small envelope: switch gives 2X (100% gain)
    # True EV if amount is the large envelope: switch gives X/2 (50% loss)
    # Without knowing which, EV=X always
    return templates.TemplateResponse(
        request,
        "partials/zwei_umschlag_result.html",
        {
            "decision": decision,
            "amount": amount,
            "ev_switch": round(ev_switch, 2),
            "ev_stay": ev_stay,
        },
    )


# ---------------------------------------------------------------------------
# Sekretärinnen-Problem (Optimal Stopping)
# ---------------------------------------------------------------------------

_sekr_candidates = [
    {"id": 1, "quality": 62, "rank_hint": "Gut"},
    {"id": 2, "quality": 85, "rank_hint": "Sehr gut"},
    {"id": 3, "quality": 41, "rank_hint": "Mittel"},
    {"id": 4, "quality": 93, "rank_hint": "Ausgezeichnet"},
    {"id": 5, "quality": 57, "rank_hint": "Gut"},
    {"id": 6, "quality": 78, "rank_hint": "Sehr gut"},
    {"id": 7, "quality": 34, "rank_hint": "Schwach"},
    {"id": 8, "quality": 89, "rank_hint": "Ausgezeichnet"},
    {"id": 9, "quality": 71, "rank_hint": "Sehr gut"},
    {"id": 10, "quality": 48, "rank_hint": "Mittel"},
]


@router.get("/sekretaerin", response_class=HTMLResponse)
def sekretaerin_page(request: Request):
    candidates = _sekr_candidates.copy()
    _random.shuffle(candidates)
    # Only show relative rank info (better/worse than seen so far), not absolute quality
    return templates.TemplateResponse(
        request,
        "raetsel/sekretaerin.html",
        {"active_page": "raetsel", "total": len(candidates)},
    )


@router.post("/sekretaerin/result", response_class=HTMLResponse)
def sekretaerin_result(
    request: Request,
    chosen_at: int = Form(...),    # which position player stopped at (1-10)
    chosen_quality: int = Form(...),  # quality of chosen candidate
    best_quality: int = Form(default=93),  # best available
):
    import math as _m
    n = 10
    # Optimal cutoff: stop after first 1/e ≈ 37% → round(10/e) = 4
    optimal_cutoff = round(n / _m.e)
    # Probability of success with optimal strategy ~= 1/e ≈ 36.8%
    optimal_prob = round(100 / _m.e, 1)

    got_best = chosen_quality == best_quality
    rank_fraction = round(chosen_quality / best_quality * 100)

    if got_best:
        outcome = "optimal"
    elif chosen_quality >= 85:
        outcome = "gut"
    elif chosen_quality >= 70:
        outcome = "mittel"
    else:
        outcome = "schlecht"

    return templates.TemplateResponse(
        request,
        "partials/sekretaerin_result.html",
        {
            "chosen_at": chosen_at,
            "chosen_quality": chosen_quality,
            "best_quality": best_quality,
            "got_best": got_best,
            "rank_fraction": rank_fraction,
            "outcome": outcome,
            "optimal_cutoff": optimal_cutoff,
            "optimal_prob": optimal_prob,
            "n": n,
        },
    )


# ---------------------------------------------------------------------------
# Braess-Paradoxon
# ---------------------------------------------------------------------------

# Network scenarios: without new road vs. with new road
BRAESS_NETWORK = {
    "without_road": {
        "label": "Ohne neue Straße",
        "routes": [
            {"name": "Oben (A→X→B)", "cost_formula": "t/100 + 45", "desc": "Variable Fahrtzeit + feste 45 min"},
            {"name": "Unten (A→Y→B)", "cost_formula": "45 + t/100", "desc": "Feste 45 min + variable Fahrtzeit"},
        ],
        "nash_time": 65,
        "optimal_time": 65,
        "is_paradox": False,
    },
    "with_road": {
        "label": "Mit neuer Straße A→Y und X→B direkt",
        "routes": [
            {"name": "Oben (A→X→B)", "cost_formula": "t/100 + 45", "desc": "Variable + 45 min"},
            {"name": "Unten (A→Y→B)", "cost_formula": "45 + t/100", "desc": "45 min + Variable"},
            {"name": "Neue Route (A→X→Y→B)", "cost_formula": "t/100 + 0 + t/100", "desc": "Nur variable Kosten – verlockend!"},
        ],
        "nash_time": 80,
        "optimal_time": 65,
        "is_paradox": True,
    },
}


@router.get("/braess", response_class=HTMLResponse)
def braess_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/braess.html",
        {"active_page": "raetsel", "network": BRAESS_NETWORK},
    )


@router.post("/braess/result", response_class=HTMLResponse)
def braess_result(
    request: Request,
    choice: str = Form(...),   # "yes_new_road" or "no_new_road"
):
    return templates.TemplateResponse(
        request,
        "partials/braess_result.html",
        {
            "choice": choice,
            "network": BRAESS_NETWORK,
        },
    )


# ---------------------------------------------------------------------------
# Die zerrissene Karte (Monopol-Verhandlungsexperiment)
# ---------------------------------------------------------------------------
# Setup: You hold 5 red cards (monopoly). 5 players each hold 1 blue card.
# Each red+blue pair is worth 1 €. Players make initial offers.
# You choose a strategy. The commitment device: tearing a card.

_KARTE_PLAYERS = [
    {"id": 1, "icon": "🧑‍💼", "name": "Spieler A", "offer": 0.30, "note": "Niedrigstes Angebot"},
    {"id": 2, "icon": "👩‍💼", "name": "Spieler B", "offer": 0.40, "note": "Unter fairem Wert"},
    {"id": 3, "icon": "🧔",   "name": "Spieler C", "offer": 0.50, "note": "Faire 50/50-Aufteilung"},
    {"id": 4, "icon": "👩",   "name": "Spieler D", "offer": 0.35, "note": "Etwas unter fair"},
    {"id": 5, "icon": "🧑",   "name": "Spieler E", "offer": 0.25, "note": "Sehr niedriges Angebot"},
]

# Per-player outcome for each strategy.
# "accepted": deal happens | "excluded": card torn/player passed over | your_share in €
_KARTE_STRATEGIES = {
    "accept_all": {
        "label": "Alle Angebote annehmen",
        "icon": "🤝",
        "color": "slate",
        "description": "Du nimmst jeden Deal so an, wie er dir angeboten wird – kein Widerspruch.",
        "results": [
            {"accepted": True,  "excluded": False, "your_share": 0.30, "note": "Angenommen"},
            {"accepted": True,  "excluded": False, "your_share": 0.40, "note": "Angenommen"},
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Angenommen"},
            {"accepted": True,  "excluded": False, "your_share": 0.35, "note": "Angenommen"},
            {"accepted": True,  "excluded": False, "your_share": 0.25, "note": "Angenommen"},
        ],
    },
    "equal_split": {
        "label": "Gleichteilung fordern (50/50)",
        "icon": "⚖️",
        "color": "indigo",
        "description": "Du forderst von jedem Spieler eine faire 50/50-Aufteilung. BATNA aller = 0, also akzeptieren alle.",
        "results": [
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Akzeptiert (50¢ > 0¢ BATNA)"},
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Akzeptiert"},
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Akzeptiert (war schon fair)"},
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Akzeptiert"},
            {"accepted": True,  "excluded": False, "your_share": 0.50, "note": "Akzeptiert"},
        ],
    },
    "aggressive": {
        "label": "Aggressiv verhandeln – 70/30, kein Zerreißen",
        "icon": "💪",
        "color": "amber",
        "description": "Du verlangst 70% ohne Commitment-Signal. Fairness-Normen schlagen zurück.",
        "results": [
            {"accepted": False, "excluded": False, "your_share": 0.00, "note": "Abgelehnt – Fairness-Reflex (bot dir 30¢, bekommt jetzt 30¢ = Demütigung)"},
            {"accepted": True,  "excluded": False, "your_share": 0.70, "note": "Akzeptiert (rational: 30¢ > 0¢)"},
            {"accepted": True,  "excluded": False, "your_share": 0.70, "note": "Akzeptiert – war schon kooperativ"},
            {"accepted": False, "excluded": False, "your_share": 0.00, "note": "Abgelehnt – kein Vertrauen ohne Commitment"},
            {"accepted": False, "excluded": False, "your_share": 0.00, "note": "Abgelehnt – 25¢ Angebot + 70/30 Forderung = Widerspruch"},
        ],
    },
    "tear_one": {
        "label": "Eine Karte zerreißen + 65/35 fordern",
        "icon": "✂️",
        "color": "emerald",
        "description": "Du zerreißt öffentlich eine Karte. Nur noch 4 Deals möglich. Die verbleibenden 4 sehen: Ausschluss ist real.",
        "results": [
            {"accepted": True,  "excluded": False, "your_share": 0.65, "note": "Akzeptiert – Ausschluss ist glaubwürdig"},
            {"accepted": True,  "excluded": False, "your_share": 0.65, "note": "Akzeptiert"},
            {"accepted": True,  "excluded": False, "your_share": 0.65, "note": "Akzeptiert"},
            {"accepted": True,  "excluded": False, "your_share": 0.65, "note": "Akzeptiert"},
            {"accepted": False, "excluded": True,  "your_share": 0.00, "note": "Ausgeschlossen – Karte zerrissen"},
        ],
    },
    "tear_two": {
        "label": "Zwei Karten zerreißen + 75/25 fordern",
        "icon": "✂️✂️",
        "color": "red",
        "description": "Maximale Verknappung: Nur noch 3 Deals. Restliche Spieler akzeptieren widerwillig 25¢.",
        "results": [
            {"accepted": True,  "excluded": False, "your_share": 0.75, "note": "Akzeptiert – keine Alternative"},
            {"accepted": True,  "excluded": False, "your_share": 0.75, "note": "Akzeptiert"},
            {"accepted": True,  "excluded": False, "your_share": 0.75, "note": "Akzeptiert"},
            {"accepted": False, "excluded": True,  "your_share": 0.00, "note": "Ausgeschlossen"},
            {"accepted": False, "excluded": True,  "your_share": 0.00, "note": "Ausgeschlossen"},
        ],
    },
}


@router.get("/zerrissene-karte", response_class=HTMLResponse)
def zerrissene_karte_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/zerrissene_karte.html",
        {
            "active_page": "raetsel",
            "players": _KARTE_PLAYERS,
            "strategies": list(_KARTE_STRATEGIES.items()),
        },
    )


@router.post("/zerrissene-karte/result", response_class=HTMLResponse)
def zerrissene_karte_result(
    request: Request,
    strategy: str = Form(...),
):
    if strategy not in _KARTE_STRATEGIES:
        strategy = "accept_all"

    chosen = _KARTE_STRATEGIES[strategy]
    results = chosen["results"]

    # Compute totals
    your_total = round(sum(r["your_share"] for r in results), 2)
    deals_closed = sum(1 for r in results if r["accepted"] and not r["excluded"])
    cards_torn = sum(1 for r in results if r["excluded"])

    # Per-player combined view
    player_results = []
    for p, r in zip(_KARTE_PLAYERS, results):
        their_share = round(1.0 - r["your_share"], 2) if r["accepted"] else 0.0
        player_results.append({**p, **r, "their_share": their_share})

    # Build comparison across all strategies
    comparison = []
    best_strat = None
    best_total = -1
    for sid, sdata in _KARTE_STRATEGIES.items():
        total = round(sum(r["your_share"] for r in sdata["results"]), 2)
        torn = sum(1 for r in sdata["results"] if r["excluded"])
        closed = sum(1 for r in sdata["results"] if r["accepted"] and not r["excluded"])
        comparison.append({
            "id": sid,
            "label": sdata["label"],
            "icon": sdata["icon"],
            "total": total,
            "deals": closed,
            "torn": torn,
            "is_chosen": sid == strategy,
        })
        if total > best_total:
            best_total = total
            best_strat = sid

    return templates.TemplateResponse(
        request,
        "partials/zerrissene_karte_result.html",
        {
            "strategy": strategy,
            "chosen": chosen,
            "player_results": player_results,
            "your_total": your_total,
            "deals_closed": deals_closed,
            "cards_torn": cards_torn,
            "comparison": comparison,
            "best_strat": best_strat,
            "best_total": best_total,
        },
    )


# ---------------------------------------------------------------------------
# Hotelling-Gesetz (Vendor Positioning)
# ---------------------------------------------------------------------------

_HOTELLING_A = 25   # fixed position of Vendor A


@router.get("/hotelling", response_class=HTMLResponse)
def hotelling_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/hotelling.html",
        {"active_page": "raetsel", "vendor_a": _HOTELLING_A},
    )


@router.post("/hotelling/result", response_class=HTMLResponse)
def hotelling_result(
    request: Request,
    position_b: int = Form(...),
):
    import math as _m

    vendor_a = _HOTELLING_A
    beach_size = 101   # positions 0–100, 1 customer per position

    # Customer split: each customer goes to the nearer vendor
    if vendor_a == position_b:
        customers_b = beach_size // 2
        customers_a = beach_size - customers_b
    else:
        a_pos = min(vendor_a, position_b)
        b_pos = max(vendor_a, position_b)
        boundary = _m.floor((a_pos + b_pos) / 2)
        # customers 0..boundary go to left vendor, boundary+1..100 to right
        left_customers = boundary + 1
        right_customers = beach_size - left_customers
        if vendor_a < position_b:
            customers_a = left_customers
            customers_b = right_customers
        else:
            customers_b = left_customers
            customers_a = right_customers

    # Find optimal B position (maximise B customers)
    best_b_pos = position_b
    best_b_customers = 0
    for pos in range(0, 101):
        if pos == vendor_a:
            continue
        if vendor_a == pos:
            bc = beach_size // 2
        else:
            ap = min(vendor_a, pos)
            bp = max(vendor_a, pos)
            bnd = _m.floor((ap + bp) / 2)
            lc = bnd + 1
            rc = beach_size - lc
            bc = rc if vendor_a < pos else lc
        if bc > best_b_customers:
            best_b_customers = bc
            best_b_pos = pos

    # Nash equilibrium note
    if position_b < 50:
        nash_pressure = f"A würde jetzt auf {position_b + 1} wandern → Beide driften zur Mitte."
    elif position_b > 50:
        nash_pressure = f"A würde jetzt auf {position_b - 1} wandern → Beide driften zur Mitte."
    else:
        nash_pressure = "Nash-Gleichgewicht erreicht! Beide stehen bei 50 – niemand kann profitieren, indem er sich bewegt."

    # Social optimum: vendors at 25 and 75 (minimize total travel distance)
    social_opt_a = 25
    social_opt_b = 75
    avg_travel_player = sum(
        min(abs(i - vendor_a), abs(i - position_b)) for i in range(101)
    ) / 101
    avg_travel_optimal = sum(
        min(abs(i - social_opt_a), abs(i - social_opt_b)) for i in range(101)
    ) / 101

    return templates.TemplateResponse(
        request,
        "partials/hotelling_result.html",
        {
            "position_b": position_b,
            "vendor_a": vendor_a,
            "customers_a": customers_a,
            "customers_b": customers_b,
            "beach_size": beach_size,
            "best_b_pos": best_b_pos,
            "best_b_customers": best_b_customers,
            "nash_pressure": nash_pressure,
            "avg_travel_player": round(avg_travel_player, 1),
            "avg_travel_optimal": round(avg_travel_optimal, 1),
            "social_opt_b": social_opt_b,
        },
    )


# ---------------------------------------------------------------------------
# El Farol Bar Problem
# ---------------------------------------------------------------------------

_ELFAROL_HISTORY = [72, 45, 68, 55, 63, 48, 71, 52]   # last 8 weeks
_ELFAROL_THRESHOLD = 60
_ELFAROL_TOTAL = 100


@router.get("/el-farol", response_class=HTMLResponse)
def el_farol_page(request: Request):
    return templates.TemplateResponse(
        request,
        "raetsel/el_farol.html",
        {
            "active_page": "raetsel",
            "history": _ELFAROL_HISTORY,
            "threshold": _ELFAROL_THRESHOLD,
            "total": _ELFAROL_TOTAL,
        },
    )


@router.post("/el-farol/result", response_class=HTMLResponse)
def el_farol_result(
    request: Request,
    prediction: int = Form(...),
    decision: str = Form(...),   # "go" | "stay"
):
    threshold = _ELFAROL_THRESHOLD

    # Simulate the 99 other regulars:
    # Each forms their own prediction based on history (mean ~60, sd ~12).
    # Those who predict < threshold go; those predicting ≥ threshold stay.
    others_going = 0
    for _ in range(99):
        their_pred = _random.gauss(58, 12)
        if their_pred < threshold:
            if _random.random() < 0.85:
                others_going += 1
        else:
            if _random.random() < 0.15:
                others_going += 1

    player_goes = decision == "go"
    total_attendance = others_going + (1 if player_goes else 0)
    bar_fun = total_attendance <= threshold

    if player_goes and bar_fun:
        outcome_key = "toll"
    elif player_goes and not bar_fun:
        outcome_key = "schlecht"
    elif not player_goes and bar_fun:
        outcome_key = "verpasst"
    else:
        outcome_key = "klug"

    prediction_error = abs(prediction - total_attendance)
    prediction_quality = (
        "sehr_gut" if prediction_error <= 5
        else "gut" if prediction_error <= 12
        else "mittel" if prediction_error <= 20
        else "schlecht"
    )

    # Illustrate the self-defeating-prediction paradox:
    # If everyone predicts < 60 → all 100 go → 100 > 60 → bar ruined → prediction wrong
    # If everyone predicts ≥ 60 → nobody goes → 0 < 60 → bar would have been fun → also wrong

    return templates.TemplateResponse(
        request,
        "partials/el_farol_result.html",
        {
            "prediction": prediction,
            "decision": decision,
            "others_going": others_going,
            "total_attendance": total_attendance,
            "threshold": threshold,
            "bar_fun": bar_fun,
            "outcome_key": outcome_key,
            "prediction_error": prediction_error,
            "prediction_quality": prediction_quality,
            "player_goes": player_goes,
        },
    )


# ---------------------------------------------------------------------------
# Henkerparadoxon (Unexpected Hanging Paradox)
# ---------------------------------------------------------------------------

HENKER_STEPS = [
    {
        "tag": "Freitag",
        "tagkurz": "Fr",
        "reasoning": "Wenn ich Donnerstagabend noch lebe, ist Freitag der einzige verbleibende Tag. Ich würde es wissen → keine Überraschung → der Richter hätte gelogen → Freitag ist ausgeschlossen.",
    },
    {
        "tag": "Donnerstag",
        "tagkurz": "Do",
        "reasoning": "Da Freitag ausgeschlossen ist: Wenn ich Mittwochabend noch lebe, bleibt nur Donnerstag. Ich würde es wissen → keine Überraschung → auch Donnerstag ausgeschlossen.",
    },
    {
        "tag": "Mittwoch",
        "tagkurz": "Mi",
        "reasoning": "Da Fr + Do ausgeschlossen sind: Wenn ich Dienstagabend noch lebe, bleibt nur Mittwoch. Ich würde es wissen → auch Mittwoch ausgeschlossen.",
    },
    {
        "tag": "Dienstag",
        "tagkurz": "Di",
        "reasoning": "Da Fr + Do + Mi ausgeschlossen sind: Wenn ich Montagabend noch lebe, bleibt nur Dienstag. Auch Dienstag ausgeschlossen.",
    },
    {
        "tag": "Montag",
        "tagkurz": "Mo",
        "reasoning": "Da alle anderen Tage ausgeschlossen sind, bleibt nur Montag. Aber dann wäre Montag vorhersehbar → keine Überraschung → auch Montag ausgeschlossen.",
    },
]


@router.get("/henker", response_class=HTMLResponse)
def henker_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/henker.html", {"active_page": "raetsel"}
    )


@router.post("/henker/result", response_class=HTMLResponse)
def henker_result(request: Request, choice: str = Form(...)):
    # choices: "unmoeglich" | "montag" | "freitag" | "zufaellig"
    is_correct_deduction = choice == "unmoeglich"
    choice_labels = {
        "unmoeglich": "Die Hinrichtung kann logisch unmöglich stattfinden.",
        "montag": "Er wird am Montag hingerichtet – dem ersten möglichen Tag.",
        "freitag": "Er wird am Freitag hingerichtet – dem letzten möglichen Tag.",
        "zufaellig": "Er kann keinen Tag ausschließen – der Richter hat einfach Recht.",
    }
    return templates.TemplateResponse(
        request,
        "partials/henker_result.html",
        {
            "choice": choice,
            "choice_label": choice_labels.get(choice, ""),
            "is_correct_deduction": is_correct_deduction,
            "steps": HENKER_STEPS,
        },
    )


# ---------------------------------------------------------------------------
# 100-Gefangenen-Problem
# ---------------------------------------------------------------------------

@router.get("/hundert-gefangene", response_class=HTMLResponse)
def hundert_gefangene_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/hundert_gefangene.html", {"active_page": "raetsel"}
    )


@router.post("/hundert-gefangene/result", response_class=HTMLResponse)
def hundert_gefangene_result(request: Request, strategy: str = Form(...)):
    n_trials = 2000
    loop_wins = 0
    for _ in range(n_trials):
        boxes = list(range(1, 101))
        _random.shuffle(boxes)
        all_found = True
        for prisoner in range(1, 101):
            found = False
            current = prisoner
            for _ in range(50):
                if boxes[current - 1] == prisoner:
                    found = True
                    break
                current = boxes[current - 1]
            if not found:
                all_found = False
                break
        if all_found:
            loop_wins += 1
    loop_rate = round(loop_wins / n_trials * 100, 1)
    theoretical = round((1 - sum(1 / k for k in range(51, 101))) * 100, 2)
    return templates.TemplateResponse(
        request,
        "partials/hundert_gefangene_result.html",
        {"strategy": strategy, "loop_rate": loop_rate, "theoretical": theoretical, "n_trials": n_trials},
    )


# ---------------------------------------------------------------------------
# Vergiftete Fässer
# ---------------------------------------------------------------------------

@router.get("/vergiftete-faesser", response_class=HTMLResponse)
def vergiftete_faesser_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/vergiftete_faesser.html", {"active_page": "raetsel"}
    )


@router.post("/vergiftete-faesser/result", response_class=HTMLResponse)
def vergiftete_faesser_result(request: Request, guess: int = Form(...)):
    correct = 10
    return templates.TemplateResponse(
        request,
        "partials/vergiftete_faesser_result.html",
        {"guess": guess, "correct": correct, "is_correct": guess == correct},
    )


# ---------------------------------------------------------------------------
# Wasserkrug-Problem
# ---------------------------------------------------------------------------

def _water_pour(a: int, b: int, action: str, cap_a: int = 3, cap_b: int = 5):
    if action == "fill_a":
        a = cap_a
    elif action == "fill_b":
        b = cap_b
    elif action == "empty_a":
        a = 0
    elif action == "empty_b":
        b = 0
    elif action == "pour_ab":
        t = min(a, cap_b - b); a -= t; b += t
    elif action == "pour_ba":
        t = min(b, cap_a - a); b -= t; a += t
    return a, b


@router.get("/wasserkrug", response_class=HTMLResponse)
def wasserkrug_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/wasserkrug.html",
        {"active_page": "raetsel", "jug_a": 0, "jug_b": 0, "cap_a": 3, "cap_b": 5, "moves": 0, "won": False, "history": [], "history_str": ""},
    )


@router.post("/wasserkrug/pour", response_class=HTMLResponse)
def wasserkrug_pour(
    request: Request,
    jug_a: int = Form(...),
    jug_b: int = Form(...),
    moves: int = Form(...),
    history: str = Form(default=""),
    action: str = Form(...),
):
    cap_a, cap_b, goal = 3, 5, 4
    new_a, new_b = _water_pour(jug_a, jug_b, action, cap_a, cap_b)
    new_moves = moves + 1
    won = (new_b == goal or new_a == goal)
    action_labels = {
        "fill_a": "Krug A (3L) füllen", "fill_b": "Krug B (5L) füllen",
        "empty_a": "Krug A leeren", "empty_b": "Krug B leeren",
        "pour_ab": "A → B umfüllen", "pour_ba": "B → A umfüllen",
    }
    hist = [e for e in history.split("|") if e]
    hist.append(f"{action_labels.get(action, action)}: A={new_a}L, B={new_b}L")
    new_history_str = "|".join(hist[-10:])
    return templates.TemplateResponse(
        request,
        "partials/wasserkrug_state.html",
        {
            "jug_a": new_a, "jug_b": new_b, "cap_a": cap_a, "cap_b": cap_b,
            "moves": new_moves, "won": won, "goal": goal,
            "history": hist, "history_str": new_history_str,
        },
    )


# ---------------------------------------------------------------------------
# Josephus-Problem
# ---------------------------------------------------------------------------

def _josephus(n: int, k: int = 2):
    people = list(range(1, n + 1))
    order = []
    idx = 0
    while len(people) > 1:
        idx = (idx + k - 1) % len(people)
        order.append(people.pop(idx))
        if idx == len(people):
            idx = 0
    return people[0], order


@router.get("/josephus", response_class=HTMLResponse)
def josephus_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/josephus.html",
        {"active_page": "raetsel", "n": 10, "positions": list(range(1, 11))},
    )


@router.post("/josephus/result", response_class=HTMLResponse)
def josephus_result(request: Request, position: int = Form(...)):
    n = 10
    survivor, order = _josephus(n)
    return templates.TemplateResponse(
        request,
        "partials/josephus_result.html",
        {"position": position, "survivor": survivor, "order": order, "n": n, "is_correct": position == survivor},
    )


# ---------------------------------------------------------------------------
# Hüte-Rätsel
# ---------------------------------------------------------------------------

@router.get("/huete-spiel", response_class=HTMLResponse)
def huete_spiel_page(request: Request):
    choices = [
        ("weiß", "weiß"), ("weiß", "rot"), ("rot", "weiß"), ("rot", "rot"),
    ]
    hat_b, hat_c = _random.choice(choices)
    return templates.TemplateResponse(
        request, "raetsel/huete_spiel.html",
        {"active_page": "raetsel", "hat_b": hat_b, "hat_c": hat_c},
    )


@router.post("/huete-spiel/result", response_class=HTMLResponse)
def huete_spiel_result(
    request: Request,
    guess: str = Form(...),
    hat_b: str = Form(...),
    hat_c: str = Form(...),
):
    is_correct = guess == "weiß"
    return templates.TemplateResponse(
        request,
        "partials/huete_result.html",
        {"guess": guess, "hat_b": hat_b, "hat_c": hat_c, "is_correct": is_correct},
    )


# ---------------------------------------------------------------------------
# Münzenwägen (9 Münzen, 1 schwerer, 2 Wägungen)
# ---------------------------------------------------------------------------

@router.get("/muenzwaegen", response_class=HTMLResponse)
def muenzwaegen_page(request: Request):
    heavy = _random.randint(1, 9)
    return templates.TemplateResponse(
        request, "raetsel/muenzwaegen.html",
        {"active_page": "raetsel", "heavy": heavy, "bags": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
    )


@router.post("/muenzwaegen/weigh1", response_class=HTMLResponse)
def muenzwaegen_weigh1(
    request: Request,
    heavy: int = Form(...),
    left_bag: int = Form(...),   # 0,1,2 = bag index
    right_bag: int = Form(...),
):
    bags = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    aside_bag = [i for i in range(3) if i not in (left_bag, right_bag)][0]
    left_coins = bags[left_bag]
    right_coins = bags[right_bag]
    aside_coins = bags[aside_bag]
    left_heavy = heavy in left_coins
    right_heavy = heavy in right_coins
    if left_heavy:
        result, candidates = "left", left_coins
    elif right_heavy:
        result, candidates = "right", right_coins
    else:
        result, candidates = "equal", aside_coins
    return templates.TemplateResponse(
        request,
        "partials/muenzwaegen_weigh1.html",
        {
            "heavy": heavy, "result": result, "candidates": candidates,
            "left_coins": left_coins, "right_coins": right_coins, "aside_coins": aside_coins,
        },
    )


@router.post("/muenzwaegen/weigh2", response_class=HTMLResponse)
def muenzwaegen_weigh2(
    request: Request,
    heavy: int = Form(...),
    left_coin: int = Form(...),
    right_coin: int = Form(...),
    aside_coin: int = Form(...),
):
    if heavy == left_coin:
        result, found = "left", left_coin
    elif heavy == right_coin:
        result, found = "right", right_coin
    else:
        result, found = "equal", aside_coin
    return templates.TemplateResponse(
        request,
        "partials/muenzwaegen_result.html",
        {"heavy": heavy, "found": found, "result": result, "is_correct": found == heavy},
    )


# ---------------------------------------------------------------------------
# Anker-Experiment
# ---------------------------------------------------------------------------

ANKER_FRAGEN = [
    {
        "id": 0,
        "frage": "Wie viel Prozent der Weltbevölkerung lebt in Asien?",
        "einheit": "%",
        "wahrheit": 59,
        "erklaerung": "Etwa 59 % der Weltbevölkerung (ca. 4,7 Mrd.) leben in Asien – China und Indien allein machen über 35 % aus.",
        "anker_lo": [8, 15, 22],
        "anker_hi": [72, 80, 88],
    },
    {
        "id": 1,
        "frage": "Wie viele Länder sind Mitglied der Vereinten Nationen?",
        "einheit": "Länder",
        "wahrheit": 193,
        "erklaerung": "Die UN hat 193 Mitgliedstaaten (Stand 2024). Fast alle souveränen Staaten der Erde.",
        "anker_lo": [35, 42, 58],
        "anker_hi": [230, 248, 265],
    },
    {
        "id": 2,
        "frage": "In welchem Jahr wurde das erste Smartphone (iPhone) vorgestellt?",
        "einheit": "Jahr",
        "wahrheit": 2007,
        "erklaerung": "Steve Jobs stellte das erste iPhone am 9. Januar 2007 auf der Macworld Conference vor.",
        "anker_lo": [1988, 1993, 1998],
        "anker_hi": [2013, 2016, 2019],
    },
    {
        "id": 3,
        "frage": "Wie hoch ist der Frauenanteil in nationalen Parlamenten weltweit (%)? ",
        "einheit": "%",
        "wahrheit": 26,
        "erklaerung": "Laut IPU-Daten 2023 betrug der globale Frauenanteil in Parlamenten ca. 26 %.",
        "anker_lo": [4, 7, 11],
        "anker_hi": [48, 55, 63],
    },
    {
        "id": 4,
        "frage": "Wie viele km ist der Äquator lang (gerundet auf 1.000 km)?",
        "einheit": "km",
        "wahrheit": 40075,
        "erklaerung": "Der Erdumfang am Äquator beträgt exakt 40.075 km.",
        "anker_lo": [12000, 18000, 24000],
        "anker_hi": [52000, 61000, 74000],
    },
]


def _anker_generate(frage_idx: int) -> tuple[dict, int]:
    """Gibt Frage + zufälligen Anker zurück."""
    frage = ANKER_FRAGEN[frage_idx]
    use_hi = _random.random() < 0.5
    pool = frage["anker_hi"] if use_hi else frage["anker_lo"]
    anchor = _random.choice(pool)
    return frage, anchor


@router.get("/anker-experiment", response_class=HTMLResponse)
def anker_experiment_page(request: Request):
    frage, anchor = _anker_generate(0)
    return templates.TemplateResponse(
        request,
        "raetsel/anker_experiment.html",
        {
            "active_page": "raetsel",
            "frage": frage,
            "anchor": anchor,
            "frage_num": 1,
            "total": len(ANKER_FRAGEN),
            "answers_json": "[]",
        },
    )


@router.post("/anker-experiment/naechste", response_class=HTMLResponse)
def anker_experiment_naechste(
    request: Request,
    frage_idx: int = Form(...),
    anchor: int = Form(...),
    schaetzung: int = Form(...),
    answers_json: str = Form(default="[]"),
):
    answers = json.loads(answers_json)
    frage = ANKER_FRAGEN[frage_idx]
    answers.append({
        "frage": frage["frage"],
        "einheit": frage["einheit"],
        "wahrheit": frage["wahrheit"],
        "erklaerung": frage["erklaerung"],
        "anchor": anchor,
        "schaetzung": schaetzung,
    })

    next_idx = frage_idx + 1
    if next_idx >= len(ANKER_FRAGEN):
        # Auswertung
        return templates.TemplateResponse(
            request,
            "partials/anker_result.html",
            {"answers": answers},
        )

    next_frage, next_anchor = _anker_generate(next_idx)
    return templates.TemplateResponse(
        request,
        "partials/anker_frage.html",
        {
            "frage": next_frage,
            "anchor": next_anchor,
            "frage_num": next_idx + 1,
            "total": len(ANKER_FRAGEN),
            "answers_json": json.dumps(answers, ensure_ascii=False),
        },
    )


# ---------------------------------------------------------------------------
# Ellsberg-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/ellsberg", response_class=HTMLResponse)
def ellsberg_page(request: Request):
    order1 = _random.sample(["A", "B"], 2)
    return templates.TemplateResponse(
        request, "raetsel/ellsberg.html", {"active_page": "raetsel", "order1": order1}
    )


@router.post("/ellsberg/phase2", response_class=HTMLResponse)
def ellsberg_phase2(request: Request, choice1: str = Form(...)):
    order2 = _random.sample(["C", "D"], 2)
    return templates.TemplateResponse(
        request, "partials/ellsberg_phase2.html", {"choice1": choice1, "order2": order2}
    )


@router.post("/ellsberg/result", response_class=HTMLResponse)
def ellsberg_result(
    request: Request,
    choice1: str = Form(...),
    choice2: str = Form(...),
):
    # A+D und B+C verletzen die Erwartungsnutzentheorie (Ambiguitätsaversion)
    # A+C oder B+D sind konsistent mit EU
    inconsistent = (choice1 == "A" and choice2 == "D") or (choice1 == "B" and choice2 == "C")
    choice1_label = "A (Rote Kugel – 1/3 bekannt)" if choice1 == "A" else "B (Schwarze Kugel – Wahrscheinlichkeit unbekannt)"
    choice2_label = "D (Schwarz oder Gelb – 2/3 bekannt)" if choice2 == "D" else "C (Rot oder Gelb – Wahrscheinlichkeit unbekannt)"
    return templates.TemplateResponse(
        request,
        "partials/ellsberg_result.html",
        {
            "choice1": choice1,
            "choice2": choice2,
            "choice1_label": choice1_label,
            "choice2_label": choice2_label,
            "inconsistent": inconsistent,
        },
    )


# ---------------------------------------------------------------------------
# Framing-Effekt (Kahneman & Tversky 1981, Science 211)
# ---------------------------------------------------------------------------

@router.get("/framing", response_class=HTMLResponse)
def framing_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/framing.html", {"active_page": "raetsel"}
    )


@router.post("/framing/phase2", response_class=HTMLResponse)
def framing_phase2(request: Request, choice1: str = Form(...)):
    return templates.TemplateResponse(
        request, "partials/framing_phase2.html", {"choice1": choice1}
    )


@router.post("/framing/result", response_class=HTMLResponse)
def framing_result(
    request: Request,
    choice1: str = Form(...),
    choice2: str = Form(...),
):
    # A=C (200 saved = 400 die) and B=D (1/3 all / 2/3 none = same)
    # Typical: 72% choose A (gain frame), 78% choose D (loss frame) → A+D inconsistent
    inconsistent = (choice1 == "A" and choice2 == "D") or (choice1 == "B" and choice2 == "C")
    choice1_label = "A – 200 Menschen sicher gerettet" if choice1 == "A" else "B – Risiko: 1/3 alle gerettet, 2/3 niemand"
    choice2_label = "D – Risiko: 1/3 niemand stirbt, 2/3 alle sterben" if choice2 == "D" else "C – 400 Menschen sterben sicher"
    return templates.TemplateResponse(
        request,
        "partials/framing_result.html",
        {
            "choice1": choice1,
            "choice2": choice2,
            "choice1_label": choice1_label,
            "choice2_label": choice2_label,
            "inconsistent": inconsistent,
        },
    )


# ---------------------------------------------------------------------------
# Achilles und die Schildkröte (Zenon, ~450 v.Chr.)
# ---------------------------------------------------------------------------

_ACHILLES_STEPS = []
_time = 0.0
_achilles_pos = 0.0
_turtle_pos = 100.0
_achilles_speed = 10.0
_turtle_speed = 1.0
for _i in range(7):
    _gap = _turtle_pos - _achilles_pos
    _step_dt = _gap / _achilles_speed
    _time += _step_dt
    _achilles_pos = _turtle_pos
    _turtle_pos += _step_dt * _turtle_speed
    _ACHILLES_STEPS.append({
        "step": _i + 1,
        "gap": round(_gap, 4),
        "dt": round(_step_dt, 4),
        "total_time": round(_time, 4),
        "achilles_pos": round(_achilles_pos, 4),
        "turtle_pos": round(_turtle_pos, 4),
    })

_ACHILLES_MEETING_TIME = round(100 / 9, 4)    # = 100/(v_a - v_t) * v_a/v_a ... exact: 100/9
_ACHILLES_MEETING_POS = round(1000 / 9, 4)    # = v_a * t_meet


@router.get("/achilles", response_class=HTMLResponse)
def achilles_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/achilles.html", {"active_page": "raetsel"}
    )


@router.post("/achilles/result", response_class=HTMLResponse)
def achilles_result(
    request: Request,
    prediction: str = Form(...),   # "niemals" | "schliesslich" | "unentscheidbar"
):
    correct = prediction == "schliesslich"
    return templates.TemplateResponse(
        request,
        "partials/achilles_result.html",
        {
            "prediction": prediction,
            "correct": correct,
            "steps": _ACHILLES_STEPS,
            "meeting_time": _ACHILLES_MEETING_TIME,
            "meeting_pos": _ACHILLES_MEETING_POS,
        },
    )


# ---------------------------------------------------------------------------
# Wason-Auswahlaufgabe (Wason 1968 + Cosmides 1989)
# ---------------------------------------------------------------------------

_WASON_ABSTRACT = {
    "cards": ["E", "K", "4", "7"],
    "rule": "Wenn eine Karte auf einer Seite einen Vokal zeigt, zeigt sie auf der anderen Seite eine gerade Zahl.",
    "correct": ["E", "7"],
    "explanation": {
        "E": "Muss umgedreht werden – wenn keine gerade Zahl auf der Rückseite, ist die Regel verletzt.",
        "K": "Muss NICHT umgedreht werden – K ist kein Vokal, egal was auf der Rückseite ist.",
        "4": "Muss NICHT umgedreht werden – selbst wenn ein Vokal auf der Rückseite: Vokal → gerade ist erfüllt.",
        "7": "Muss umgedreht werden – wenn ein Vokal auf der Rückseite, wäre die Regel verletzt (Vokal → gerade, aber 7 ist ungerade).",
    },
}

_WASON_SOCIAL = {
    "cards": ["Bier", "Cola", "16", "25"],
    "rule": "Wer Alkohol trinkt, muss mindestens 18 Jahre alt sein.",
    "correct": ["Bier", "16"],
    "explanation": {
        "Bier": "Muss umgedreht werden – das Alter auf der Rückseite muss ≥ 18 sein.",
        "Cola": "Muss NICHT umgedreht werden – Cola ist kein Alkohol, Alter irrelevant.",
        "16": "Muss umgedreht werden – wenn auf der Rückseite Alkohol steht, ist die Regel verletzt.",
        "25": "Muss NICHT umgedreht werden – Person ist volljährig, darf Alkohol trinken.",
    },
}


@router.get("/wason", response_class=HTMLResponse)
def wason_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/wason.html",
        {"active_page": "raetsel", "task": _WASON_ABSTRACT}
    )


@router.post("/wason/result", response_class=HTMLResponse)
def wason_result(
    request: Request,
    cards: str = Form(default=""),
):
    selected = [c.strip() for c in cards.split(",") if c.strip()] if cards else []
    correct_set = set(_WASON_ABSTRACT["correct"])
    selected_set = set(selected)
    is_correct = selected_set == correct_set
    return templates.TemplateResponse(
        request,
        "partials/wason_result.html",
        {
            "selected": selected,
            "task": _WASON_ABSTRACT,
            "is_correct": is_correct,
            "social_task": _WASON_SOCIAL,
        },
    )


@router.post("/wason/social", response_class=HTMLResponse)
def wason_social(
    request: Request,
    cards: str = Form(default=""),
):
    selected = [c.strip() for c in cards.split(",") if c.strip()] if cards else []
    correct_set = set(_WASON_SOCIAL["correct"])
    selected_set = set(selected)
    is_correct = selected_set == correct_set
    return templates.TemplateResponse(
        request,
        "partials/wason_social_result.html",
        {
            "selected": selected,
            "task": _WASON_SOCIAL,
            "is_correct": is_correct,
        },
    )


# ---------------------------------------------------------------------------
# Durchschnittsgeschwindigkeit-Paradoxon (harmonisches Mittel)
# ---------------------------------------------------------------------------

@router.get("/geschwindigkeit", response_class=HTMLResponse)
def geschwindigkeit_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/geschwindigkeit.html", {"active_page": "raetsel"}
    )


@router.post("/geschwindigkeit/result", response_class=HTMLResponse)
def geschwindigkeit_result(
    request: Request,
    v1: int = Form(...),
    v_target: int = Form(...),
):
    import math as _m
    # v_avg = 2*v1*v2 / (v1 + v2) => v2 = v_avg*v1 / (2*v1 - v_avg)
    denom = 2 * v1 - v_target
    if denom <= 0:
        impossible = True
        v2 = None
        time_first = round(50 / v1, 2)
        time_total_needed = round(100 / v_target, 2)
        time_deficit = round(time_first - time_total_needed, 4)
    else:
        impossible = False
        v2 = round(v_target * v1 / denom, 1)
        time_first = round(50 / v1, 2)
        time_second = round(50 / v2, 2)
        time_total = round(time_first + time_second, 3)
        v_actual = round(100 / time_total, 1)
        time_deficit = None

    return templates.TemplateResponse(
        request,
        "partials/geschwindigkeit_result.html",
        {
            "v1": v1,
            "v_target": v_target,
            "impossible": impossible,
            "v2": v2,
            "time_first": time_first if impossible else time_first,
            "time_second": None if impossible else round(50 / v2, 2),
            "time_total": None if impossible else round(50 / v1 + 50 / v2, 3),
            "v_actual": None if impossible else round(100 / (50 / v1 + 50 / v2), 1),
            "time_deficit": time_deficit,
            "time_total_needed": round(100 / v_target, 2) if impossible else None,
        },
    )


# ---------------------------------------------------------------------------
# Gabriels Trompete (Torricelli 1643)
# ---------------------------------------------------------------------------

@router.get("/gabriels-trompete", response_class=HTMLResponse)
def gabriels_trompete_page(request: Request):
    import math as _m
    # Precompute: volume = pi, surface area diverges
    # V = pi * integral(1/x^2, 1, inf) = pi
    # S = 2*pi * integral(1/x * sqrt(1 + 1/x^4), 1, inf) > 2*pi * integral(1/x, 1, N) -> inf
    # Show partial sums for illustration
    partial_volumes = []
    partial_surfaces = []
    intervals = [2, 5, 10, 50, 100, 1000]
    for N in intervals:
        # V approx = pi*(1 - 1/N)
        v = round(_m.pi * (1 - 1/N), 6)
        # S lower bound = 2*pi*ln(N)
        s_lower = round(2 * _m.pi * _m.log(N), 3)
        partial_volumes.append({"N": N, "volume": v, "surface_lower": s_lower})
    return templates.TemplateResponse(
        request,
        "raetsel/gabriels_trompete.html",
        {
            "active_page": "raetsel",
            "partial_volumes": partial_volumes,
            "pi": round(_m.pi, 6),
        },
    )


@router.post("/gabriels-trompete/result", response_class=HTMLResponse)
def gabriels_trompete_result(
    request: Request,
    intuition: str = Form(...),   # "endlich_beide" | "unendlich_beide" | "paradox" | "weiss_nicht"
):
    return templates.TemplateResponse(
        request,
        "partials/gabriels_trompete_result.html",
        {"intuition": intuition},
    )


# ---------------------------------------------------------------------------
# Hilberts Hotel (David Hilbert, 1924 / popularised by Gamow 1947)
# ---------------------------------------------------------------------------

@router.get("/hilberts-hotel", response_class=HTMLResponse)
def hilberts_hotel_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/hilberts_hotel.html", {"active_page": "raetsel"}
    )


@router.post("/hilberts-hotel/result", response_class=HTMLResponse)
def hilberts_hotel_result(
    request: Request,
    scenario: str = Form(...),   # "one_guest" | "inf_guests" | "inf_buses"
    answer: str = Form(...),     # "yes" | "no" | "impossible"
):
    correct = {
        "one_guest": "yes",
        "inf_guests": "yes",
        "inf_buses": "yes",
    }
    is_correct = answer == correct.get(scenario, "")
    return templates.TemplateResponse(
        request,
        "partials/hilberts_hotel_result.html",
        {
            "scenario": scenario,
            "answer": answer,
            "is_correct": is_correct,
        },
    )


# ---------------------------------------------------------------------------
# Schlafendes Mädchen (Sleeping Beauty Problem)
# ---------------------------------------------------------------------------

@router.get("/schlafendes-maedchen", response_class=HTMLResponse)
def schlafendes_maedchen_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/schlafendes_maedchen.html", {"active_page": "raetsel"}
    )


@router.post("/schlafendes-maedchen/result", response_class=HTMLResponse)
def schlafendes_maedchen_result(request: Request, answer: str = Form(...)):
    return templates.TemplateResponse(
        request,
        "partials/schlafendes_maedchen_result.html",
        {"answer": answer},
    )


# ---------------------------------------------------------------------------
# Grandis Serie
# ---------------------------------------------------------------------------

@router.get("/grandis-serie", response_class=HTMLResponse)
def grandis_serie_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/grandis_serie.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Ramanujan-Summe
# ---------------------------------------------------------------------------

@router.get("/ramanujan-summe", response_class=HTMLResponse)
def ramanujan_summe_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/ramanujan_summe.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Harmonische Reihe
# ---------------------------------------------------------------------------

@router.get("/harmonische-reihe", response_class=HTMLResponse)
def harmonische_reihe_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/harmonische_reihe.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Falsch-Positiv-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/falsch-positiv", response_class=HTMLResponse)
def falsch_positiv_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/falsch_positiv.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Spielerfehlschluss (Gambler's Fallacy)
# ---------------------------------------------------------------------------

@router.get("/spielerfehlschluss", response_class=HTMLResponse)
def spielerfehlschluss_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/spielerfehlschluss.html", {"active_page": "raetsel"}
    )


@router.post("/spielerfehlschluss/result", response_class=HTMLResponse)
def spielerfehlschluss_result(request: Request, answer: str = Form(...)):
    return templates.TemplateResponse(
        request,
        "partials/spielerfehlschluss_result.html",
        {"answer": answer},
    )


# ---------------------------------------------------------------------------
# Bayes-Theorem
# ---------------------------------------------------------------------------

@router.get("/bayes-theorem", response_class=HTMLResponse)
def bayes_theorem_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/bayes_theorem.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Gesetz der großen Zahlen
# ---------------------------------------------------------------------------

@router.get("/gesetz-grosse-zahlen", response_class=HTMLResponse)
def gesetz_grosse_zahlen_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/gesetz_grosse_zahlen.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Coupon-Sammler-Problem
# ---------------------------------------------------------------------------

@router.get("/coupon-sammler", response_class=HTMLResponse)
def coupon_sammler_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/coupon_sammler.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Bertrand-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/bertrand-paradoxon", response_class=HTMLResponse)
def bertrand_paradoxon_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/bertrand_paradoxon.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Konfirmationsfehler
# ---------------------------------------------------------------------------

@router.get("/konfirmationsfehler", response_class=HTMLResponse)
def konfirmationsfehler_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/konfirmationsfehler.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Dunning-Kruger-Effekt
# ---------------------------------------------------------------------------

@router.get("/dunning-kruger", response_class=HTMLResponse)
def dunning_kruger_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/dunning_kruger.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Survivorship Bias
# ---------------------------------------------------------------------------

@router.get("/survivorship-bias", response_class=HTMLResponse)
def survivorship_bias_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/survivorship_bias.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Regression zur Mitte
# ---------------------------------------------------------------------------

@router.get("/regression-zur-mitte", response_class=HTMLResponse)
def regression_zur_mitte_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/regression_zur_mitte.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Collatz-Vermutung
# ---------------------------------------------------------------------------

@router.get("/collatz-vermutung", response_class=HTMLResponse)
def collatz_vermutung_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/collatz_vermutung.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Barbier-Paradoxon
# ---------------------------------------------------------------------------

@router.get("/barbier-paradoxon", response_class=HTMLResponse)
def barbier_paradoxon_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/barbier_paradoxon.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Informationskaskade
# ---------------------------------------------------------------------------

@router.get("/informationskaskade", response_class=HTMLResponse)
def informationskaskade_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/informationskaskade.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Marktverlust (Akerlof Market for Lemons)
# ---------------------------------------------------------------------------

@router.get("/marktverlust", response_class=HTMLResponse)
def marktverlust_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/marktverlust.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Priming-Experiment
# ---------------------------------------------------------------------------

@router.get("/priming", response_class=HTMLResponse)
def priming_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/priming.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Kognitive Dissonanz
# ---------------------------------------------------------------------------

@router.get("/kognitive-dissonanz", response_class=HTMLResponse)
def kognitive_dissonanz_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/kognitive_dissonanz.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# BATNA – Verhandlungsmacht
# ---------------------------------------------------------------------------

@router.get("/batna", response_class=HTMLResponse)
def batna_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/batna.html", {"active_page": "raetsel"}
    )


# ---------------------------------------------------------------------------
# Trugschlüsse erkennen
# ---------------------------------------------------------------------------

@router.get("/trugschluesse", response_class=HTMLResponse)
def trugschluesse_page(request: Request):
    return templates.TemplateResponse(
        request, "raetsel/trugschluesse.html", {"active_page": "raetsel"}
    )
