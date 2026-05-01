"""Rätsel & Paradoxe – einmalige spieltheoretische Denkexperimente."""
import datetime as _dt
import json
import random as _random

from fastapi import APIRouter, Form, HTTPException, Request
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
    # ── Mathematik (neu) ─────────────────────────────────────────────────────
    {"id":"hanoi","name":"Die Türme von Hanoi","icon":"🗼","beschreibung":"3 Türme, n Scheiben – wie viele Züge braucht man mindestens? Die Antwort steckt in einer eleganten Rekursionsformel.","typ":"Logik-Rätsel","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Mathematik"},
    {"id":"koenigsberger-bruecken","name":"Königsberger Brücken","icon":"🌉","beschreibung":"7 Brücken, 4 Landmassen – kann man alle Brücken genau einmal überqueren? Euler löste das Problem 1736 und begründete die Graphentheorie.","typ":"Graphentheorie","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Mathematik"},
    {"id":"vier-farben-satz","name":"Der Vier-Farben-Satz","icon":"🗺️","beschreibung":"Jede Landkarte lässt sich mit 4 Farben so färben, dass keine Nachbarländer die gleiche Farbe haben. Klingt einfach – der Beweis dauerte über 100 Jahre.","typ":"Topologie","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Mathematik"},
    {"id":"magische-quadrate","name":"Magische Quadrate","icon":"🔢","beschreibung":"Ein 3×3-Gitter mit den Zahlen 1–9: alle Zeilen, Spalten und Diagonalen ergeben dieselbe Summe. Wie viele Lösungen gibt es?","typ":"Kombinatorik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Mathematik"},
    {"id":"fibonacci-suche","name":"Fibonacci & Goldener Schnitt","icon":"🌀","beschreibung":"1, 1, 2, 3, 5, 8, 13, 21 … Das Verhältnis benachbarter Glieder strebt gegen einen berühmten Wert – der überall in der Natur auftaucht.","typ":"Mustererkennung","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Mathematik"},
    {"id":"kryptarithmen","name":"Kryptarithmen: SEND+MORE=MONEY","icon":"🔐","beschreibung":"Jeder Buchstabe steht für eine eindeutige Ziffer. Welche Belegung macht SEND+MORE=MONEY wahr? Ein klassisches Constraint-Satisfaction-Problem.","typ":"Algebrapuzzle","schwierigkeit":"Fortgeschritten","dauer":"8 min","kategorie":"Mathematik"},
    {"id":"moebius-band","name":"Das Möbius-Band","icon":"♾️","beschreibung":"Nimm einen Papierstreifen, dreh ein Ende um 180° und klebe die Enden zusammen. Was entsteht – und was passiert, wenn du die Mitte durchschneidest?","typ":"Topologie","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Mathematik"},
    {"id":"ziegenproblem-2","name":"Ziegenproblem 2.0","icon":"🚪","beschreibung":"Das Monty-Hall-Problem mit n Türen: Bei 100 Türen öffnet der Moderator 98. Lohnt sich der Wechsel noch mehr? Die Mathematik überrascht erneut.","typ":"Wahrscheinlichkeits-Paradox","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Mathematik"},
    {"id":"polyeder-check","name":"Polyeder & Euler-Formel","icon":"💠","beschreibung":"Ecken minus Kanten plus Flächen = 2. Diese Formel gilt für jeden konvexen Polyeder. Euler entdeckte sie 1750 – und sie ist bis heute grundlegend.","typ":"Geometrie","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Mathematik"},
    {"id":"banach-tarski","name":"Das Banach-Tarski-Paradoxon","icon":"🧩","beschreibung":"Eine Kugel wird in endlich viele Stücke zerlegt – und nur durch Drehen und Verschieben entstehen daraus zwei Kugeln gleicher Größe. Mathematisch beweisbar, physikalisch unmöglich.","typ":"Mengenlehre","schwierigkeit":"Fortgeschritten","dauer":"5 min","kategorie":"Mathematik"},
    # ── Physik (neu) ──────────────────────────────────────────────────────────
    {"id":"schroedinger-katze","name":"Schrödingers Katze","icon":"🐱","beschreibung":"Eine Katze, eine radioaktive Substanz, ein Giftbehälter – und die seltsamste Frage der Physik: Ist die Katze tot oder lebendig, bevor du nachschaust?","typ":"Quantenmechanik","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Physik"},
    {"id":"maxwells-daemon","name":"Maxwells Dämon","icon":"😈","beschreibung":"Ein winziges Wesen sortiert schnelle und langsame Moleküle – und scheint damit den zweiten Hauptsatz der Thermodynamik zu verletzen. Wie ist das möglich?","typ":"Thermodynamik","schwierigkeit":"Fortgeschritten","dauer":"5 min","kategorie":"Physik"},
    {"id":"zwillingsparadoxon","name":"Das Zwillingsparadoxon","icon":"👯","beschreibung":"Ein Zwilling reist mit 99% Lichtgeschwindigkeit ins All und kehrt zurück. Wer ist älter? Und warum ist das kein echtes Paradoxon?","typ":"Relativitätstheorie","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Physik"},
    {"id":"doppelspalt","name":"Das Doppelspaltexperiment","icon":"🔬","beschreibung":"Elektronen erzeugen ein Interferenzmuster – wie Wellen. Aber sobald man misst, welchen Spalt sie passieren, verhält sich alles anders. Warum?","typ":"Quantenphysik","schwierigkeit":"Fortgeschritten","dauer":"5 min","kategorie":"Physik"},
    {"id":"bernoulli-puzzle","name":"Das Bernoulli-Puzzle","icon":"✈️","beschreibung":"Warum fliegt ein Flugzeug? Und warum saugt ein Duschvorhang nach innen? Bernoullis Prinzip erklärt Druckunterschiede in strömenden Fluiden.","typ":"Strömungslehre","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Physik"},
    {"id":"foucault-pendel","name":"Das Foucaultsche Pendel","icon":"🕰️","beschreibung":"1851 ließ Léon Foucault ein riesiges Pendel im Pariser Panthéon schwingen – und bewies damit ohne Teleskop die Rotation der Erde.","typ":"Mechanik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Physik"},
    {"id":"tensegrity","name":"Tensegrity-Strukturen","icon":"🏗️","beschreibung":"Stäbe, die in der Luft schweben – nur gehalten von Seilen. Keine Stäbe berühren sich. Wie hält diese Konstruktion dem Druck stand?","typ":"Statik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Physik"},
    {"id":"archimedischer-punkt","name":"Der Archimedische Punkt","icon":"⚖️","beschreibung":"\"Gebt mir einen festen Punkt, und ich hebe die Welt aus den Angeln.\" Was sagte Archimedes damit – und wie lang wäre der nötige Hebel wirklich?","typ":"Mechanik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Physik"},
    {"id":"eimer-experiment","name":"Newtons Eimerversuch","icon":"🪣","beschreibung":"Wasser in einem rotierenden Eimer wölbt sich nach außen. Aber – dreht er sich relativ zu was? Newtons Antwort und Machs Kritik spalten die Physik.","typ":"Mechanik","schwierigkeit":"Fortgeschritten","dauer":"5 min","kategorie":"Physik"},
    # ── Spieltheorie (neu) ───────────────────────────────────────────────────
    {"id":"matching-pennies","name":"Matching Pennies","icon":"🪙","beschreibung":"Zwei Spieler legen gleichzeitig eine Münze auf den Tisch. Einer gewinnt bei gleichen Seiten, der andere bei verschiedenen. Gibt es eine optimale Strategie?","typ":"Nullsummenspiel","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Spieltheorie"},
    {"id":"cake-cutting","name":"Cake Cutting","icon":"🎂","beschreibung":"Wie teilt man einen Kuchen zwischen zwei Personen fair auf, ohne eine Instanz als Schiedsrichter? Die Lösung ist so einfach wie elegant.","typ":"Fairness-Algorithmus","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Spieltheorie"},
    # ── Statistik (neu) ──────────────────────────────────────────────────────
    {"id":"berkson","name":"Das Berkson-Paradoxon","icon":"🏥","beschreibung":"Im Krankenhaus scheinen Raucher seltener Lungenkrebs zu haben. Ein scheinbarer Widerspruch – erklärt durch verzerrte Stichproben.","typ":"Statistik-Paradox","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Statistik"},
    {"id":"p-hacking","name":"P-Hacking","icon":"🎰","beschreibung":"Ein Forscher testet 20 Hypothesen und findet eine mit p < 0,05. Ist das ein echter Befund? Die gefährlichste Methode der modernen Wissenschaft.","typ":"Wissenschaftsmethodik","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Statistik"},
    {"id":"stichproben-raetsel","name":"Die Literary-Digest-Katastrophe","icon":"📰","beschreibung":"1936: Zehn Millionen Befragte, und trotzdem die falscheste Wahlprognose der Geschichte. Was ging schief?","typ":"Stichproben-Fehler","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Statistik"},
    {"id":"benfords-gesetz","name":"Benfords Gesetz","icon":"1️⃣","beschreibung":"In echten Datensätzen beginnt ~30% aller Zahlen mit der Ziffer 1. Finanzbetrüger kennen dieses Gesetz nicht – und werden damit überführt.","typ":"Forensik-Statistik","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Statistik"},
    {"id":"will-rogers","name":"Das Will-Rogers-Phänomen","icon":"📈","beschreibung":"Eine Gruppe wandert aus. Der Durchschnitt beider Gruppen steigt. Wie ist das arithmetisch möglich – und was hat das mit Krebsstatistiken zu tun?","typ":"Statistik-Paradox","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Statistik"},
    # ── Wahrscheinlichkeit (neu) ─────────────────────────────────────────────
    {"id":"kelly-kriterium","name":"Das Kelly-Kriterium","icon":"📊","beschreibung":"Du gewinnst 60% aller Wetten zum Kurs 1:1. Wie viel deines Kapitals setzt du pro Wette ein, um langfristig maximal zu wachsen?","typ":"Risikomanagement","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Wahrscheinlichkeit"},
    {"id":"martingale","name":"Das Martingale-System","icon":"🎲","beschreibung":"Verdopple nach jedem Verlust – und du gewinnst immer, oder? Das System klingt narrensicher. Die Mathematik sagt etwas anderes.","typ":"Wahrscheinlichkeits-Paradox","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Wahrscheinlichkeit"},
    {"id":"infinite-monkey","name":"Infinite Monkey Theorem","icon":"🐒","beschreibung":"Ein Affe tippt zufällig. Bei unendlich viel Zeit – tippt er Hamlet? Die Antwort ist theoretisch ja. Aber wie unendlich lang ist \"unendlich\"?","typ":"Unendlichkeit","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Wahrscheinlichkeit"},
    {"id":"drunkards-walk","name":"Der Drunkard's Walk","icon":"🚶","beschreibung":"Ein Betrunkener macht zufällig einen Schritt vor oder zurück. Wie weit ist er nach 100 Schritten vom Start entfernt? Die Antwort ist √100 = 10.","typ":"Zufallspfade","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Wahrscheinlichkeit"},
    {"id":"littlewoods-law","name":"Littlewoods Gesetz der Wunder","icon":"✨","beschreibung":"Littlewood: Ein \"Wunder\" ist ein Ereignis mit Wahrscheinlichkeit 1 zu einer Million. Wie oft erleben wir solche Wunder – und warum sind sie gar nicht überraschend?","typ":"Koinzidenz","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Wahrscheinlichkeit"},
    # ── Kommunikation (neu) ──────────────────────────────────────────────────
    {"id":"johari-fenster","name":"Das Johari-Fenster","icon":"🪟","beschreibung":"Vier Felder beschreiben, was dir und anderen über dich bekannt ist. Welches Feld nennt man den \"Blinden Fleck\" – und wie verkleinert man ihn?","typ":"Selbstreflexion","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Kommunikation"},
    {"id":"vier-ohren-modell","name":"Das Vier-Ohren-Modell","icon":"👂","beschreibung":"\"Das Essen ist fertig\" – vier Botschaften in einem Satz. Schulz von Thun zeigt: Sprecher und Hörer verwenden selten dieselbe Ebene.","typ":"Kommunikationsmodell","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Kommunikation"},
    {"id":"stille-post","name":"Stille Post im Business","icon":"📡","beschreibung":"Eine Anweisung durch 5 Hierarchieebenen: Was am Ende ankommt, unterscheidet sich radikal vom Original. Warum verzerren Informationsketten so stark?","typ":"Kommunikations-Experiment","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"eisbergmodell","name":"Das Eisbergmodell","icon":"🧊","beschreibung":"In Konflikten sehen wir nur 20% – die sichtbaren Positionen. 80% verbergen sich unter der Oberfläche. Was steckt darunter?","typ":"Konfliktmodell","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"transaktionsanalyse","name":"Transaktionsanalyse","icon":"🎭","beschreibung":"\"Wie oft soll ich das noch sagen?\" – aus welchem Ich-Zustand spricht das? Berne (1964) beschreibt drei Grundmuster jeder Kommunikation.","typ":"Kommunikationspsychologie","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Kommunikation"},
    {"id":"aktives-zuhoeren","name":"Aktives Zuhören","icon":"🎧","beschreibung":"Paraphrasieren, Spiegeln, offene Fragen stellen – was unterscheidet aktives von passivem Zuhören? Und warum ist es die unterschätzteste Verhandlungstechnik?","typ":"Kommunikationstechnik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"elevator-pitch","name":"Der Elevator Pitch","icon":"🛗","beschreibung":"60 Sekunden, eine Idee, ein Fremder. Was gehört rein – und was nicht? Die Kunst der radikalen Verdichtung.","typ":"Kommunikationstraining","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"nonverbale-mimikry","name":"Nonverbale Mimikry","icon":"🪞","beschreibung":"Spiegelst du unbewusst die Körpersprache deines Gegenübers, steigt die Sympathie deutlich. Warum – und wie setzt man das gezielt ein?","typ":"Körpersprache","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"feedback-sandwich","name":"Das Feedback-Sandwich","icon":"🥪","beschreibung":"Positiv-Kritik-Positiv: Die beliebteste Feedback-Technik. Doch Studien zeigen: Sie verfehlt häufig ihr Ziel. Was ist das Problem?","typ":"Führungskommunikation","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Kommunikation"},
    {"id":"empathie-mapping","name":"Empathie-Mapping","icon":"🗺️","beschreibung":"Was denkt, fühlt, sieht und hört dein Gegenüber? Die Design-Thinking-Methode für tieferes Verständnis des Verhandlungspartners.","typ":"Perspektivwechsel","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Kommunikation"},
    # ── Rhetorik (neu) ───────────────────────────────────────────────────────
    {"id":"sokratische-methode","name":"Die Sokratische Methode","icon":"🏛️","beschreibung":"Sokrates stellte Fragen, statt Antworten zu geben – und brachte sein Gegenüber dazu, Widersprüche selbst zu erkennen. Wie funktioniert das?","typ":"Dialektik","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Rhetorik"},
    {"id":"ethos-pathos-logos","name":"Ethos, Pathos, Logos","icon":"⚖️","beschreibung":"Aristoteles identifizierte drei Grundformen der Überzeugung: Glaubwürdigkeit, Emotion, Logik. Welche ist am wirkungsvollsten – und wann?","typ":"Rhetorik-Analyse","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Rhetorik"},
    {"id":"steel-manning","name":"Steel-Manning","icon":"🛡️","beschreibung":"Statt das schwächste Argument des Gegners anzugreifen (Strohmann), formulierst du sein stärkstes. Warum ist das intellektuell ehrlicher – und wann schlägt man damit?","typ":"Argumentationstechnik","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Rhetorik"},
    {"id":"slippery-slope","name":"Slippery Slope","icon":"🛷","beschreibung":"\"Wenn wir X erlauben, dann führt das zu Y, dann zu Z, dann zum Untergang.\" Wann ist diese Argumentation legitim – und wann ein Trugschluss?","typ":"Logik-Trugschluss","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Rhetorik"},
    {"id":"red-herring","name":"Red Herring","icon":"🐟","beschreibung":"Ein ablenkender Punkt wird eingebracht, um vom eigentlichen Thema wegzuführen. Wie erkennt man dieses Manöver – und wie reagiert man darauf?","typ":"Argumentationsabwehr","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Rhetorik"},
    {"id":"syllogismen-check","name":"Syllogismen-Check","icon":"🔗","beschreibung":"Alle Menschen sind sterblich. Sokrates ist ein Mensch. Also ist Sokrates sterblich. Wann ist ein Syllogismus gültig – und wann nur scheinbar logisch?","typ":"Logik","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Rhetorik"},
    {"id":"fallacy-hunting","name":"Fallacy Hunting","icon":"🎯","beschreibung":"Ad Hominem, Strohmann, False Dilemma, Appeal to Authority – kannst du die Trugschlüsse in echten Argumenten identifizieren?","typ":"Logik-Quiz","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Rhetorik"},
    {"id":"regel-der-drei","name":"Die Regel der Drei","icon":"3️⃣","beschreibung":"\"Veni, vidi, vici.\" Dreierstrukturen sind einprägsamer, überzeugender und rhythmisch. Warum hat das menschliche Gehirn eine Vorliebe für Dreigruppen?","typ":"Stilistik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Rhetorik"},
    {"id":"euphemismus-jagd","name":"Euphemismus-Jagd","icon":"🎭","beschreibung":"\"Kollateralschäden\", \"Entlassungswelle\", \"Preisanpassung\" – Euphemismen verbergen unangenehme Wahrheiten. Wie entlarvt man manipulative Sprache?","typ":"Sprachkritik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Rhetorik"},
    {"id":"anapher-training","name":"Anapher-Training","icon":"🔁","beschreibung":"\"Wir werden kämpfen… wir werden niemals aufgeben… wir werden siegen.\" Wiederholungen am Satzbeginn erzeugen Rhythmus und emotionale Wucht.","typ":"Stilmittel","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Rhetorik"},
    # ── Verhandlung (neu) ────────────────────────────────────────────────────
    {"id":"zopa","name":"ZOPA – Die Einigungszone","icon":"🎯","beschreibung":"Verkäufer will mindestens 80 000 €, Käufer zahlt maximal 100 000 €. Was ist die ZOPA – und was, wenn sie nicht existiert?","typ":"Verhandlungsstrategie","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Verhandlung"},
    {"id":"logrolling","name":"Logrolling","icon":"🔄","beschreibung":"Du willst Gehalt, dein Chef will Flexibilität. Beide Seiten können gewinnen – wenn man Themen bündelt statt einzeln verhandelt.","typ":"Verhandlungstaktik","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Verhandlung"},
    {"id":"good-cop-bad-cop","name":"Good Cop / Bad Cop","icon":"👮","beschreibung":"Ein Verhandler ist hart, der andere nett. Wie funktioniert diese psychologische Taktik – und wie neutralisiert man sie?","typ":"Verhandlungsabwehr","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Verhandlung"},
    {"id":"interessen-vs-positionen","name":"Interessen vs. Positionen","icon":"🍊","beschreibung":"Zwei Schwestern streiten um eine Orange. Eine will die Schale, die andere den Saft. Was zeigt das über Verhandlungen – und über das Harvard-Konzept?","typ":"Harvard-Methode","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Verhandlung"},
    {"id":"macht-des-schweigens","name":"Die Macht des Schweigens","icon":"🤫","beschreibung":"Du machst ein Angebot. Dann – Stille. Wer als erster spricht, verliert? Die Psychologie hinter strategischen Pausen.","typ":"Verhandlungstaktik","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Verhandlung"},
    {"id":"nibbling","name":"Nibbling","icon":"🐭","beschreibung":"Der Deal ist fast durch – und plötzlich: \"Könntest du noch schnell...?\" Nibbling ist eine der häufigsten Last-Minute-Taktiken. Wie wehrt man sich?","typ":"Verhandlungsabwehr","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Verhandlung"},
    {"id":"salami-taktik","name":"Salami-Taktik","icon":"🥩","beschreibung":"Scheibe für Scheibe – jede Forderung wirkt klein, das Gesamtpaket ist enorm. Wie erkennt man die Salami-Taktik frühzeitig?","typ":"Verhandlungsstrategie","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Verhandlung"},
    {"id":"reframing","name":"Reframing in der Verhandlung","icon":"🖼️","beschreibung":"\"Wir können uns das nicht leisten\" → \"Was müsste sich ändern, damit das möglich wird?\" Reframing verwandelt Sackgassen in Chancen.","typ":"Mediation","schwierigkeit":"Mittel","dauer":"4 min","kategorie":"Verhandlung"},
    # ── Psychologie (neu) ────────────────────────────────────────────────────
    {"id":"marshmallow-test","name":"Der Marshmallow-Test","icon":"🍬","beschreibung":"Ein Kind, ein Marshmallow, ein Versprechen: Wer 15 Minuten wartet, bekommt zwei. Was sagt die Fähigkeit zum Belohnungsaufschub über Lebenserfolg?","typ":"Verhaltenspsychologie","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Psychologie"},
    {"id":"halo-effekt","name":"Der Halo-Effekt","icon":"👼","beschreibung":"Ein attraktiver Mensch gilt automatisch als kompetenter, ehrlicher und intelligenter. Wie stark beeinflusst ein einziges Merkmal das Gesamturteil?","typ":"Wahrnehmungsverzerrung","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Psychologie"},
    {"id":"bystander-effekt","name":"Der Bystander-Effekt","icon":"👥","beschreibung":"1964, New York: Kitty Genovese wird angegriffen – 38 Nachbarn beobachten es, keiner ruft die Polizei. Was erklärt dieses Versagen kollektiver Verantwortung?","typ":"Sozialpsychologie","schwierigkeit":"Einsteiger","dauer":"4 min","kategorie":"Psychologie"},
    {"id":"barnum-effekt","name":"Der Barnum-Effekt","icon":"🎪","beschreibung":"\"Sie haben unausgeschöpfte Potenziale und manchmal zweifeln Sie an sich.\" Warum glauben so viele, dass diese Aussage genau auf sie zutrifft?","typ":"Kognitionspsychologie","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Psychologie"},
    {"id":"flow-analyse","name":"Flow – der optimale Zustand","icon":"🌊","beschreibung":"Zwischen Langeweile und Überforderung liegt ein schmaler Kanal: Flow. Csikszentmihalyi (1990) beschreibt, wann Menschen völlig aufgehen in einer Tätigkeit.","typ":"Motivationspsychologie","schwierigkeit":"Einsteiger","dauer":"3 min","kategorie":"Psychologie"},
    {"id":"milgram-gehorsam","name":"Das Milgram-Experiment","icon":"⚡","beschreibung":"65% der Versuchspersonen verabreichten tödliche Elektroschocks – weil eine Autoritätsperson es verlangte. Was sagt das über moralischen Mut?","typ":"Sozialpsychologie","schwierigkeit":"Mittel","dauer":"5 min","kategorie":"Psychologie"},
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


# ---------------------------------------------------------------------------
# Generic puzzle content (catch-all via /raetsel/{id})
# ---------------------------------------------------------------------------

GENERIC_PUZZLES: dict = {
    # ── Mathematik ────────────────────────────────────────────────────────
    "hanoi": {
        "id": "hanoi", "name": "Die Türme von Hanoi", "icon": "🗼",
        "farbe": "violet", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Drei Türme, n Scheiben (von groß nach klein gestapelt). Regel: Du darfst immer nur eine Scheibe bewegen, und eine größere Scheibe darf nie auf einer kleineren liegen. Ziel: alle Scheiben von Turm A nach Turm C.",
        "frage": "Wie viele Züge braucht man minimal, um <strong>n Scheiben</strong> zu versetzen?",
        "optionen": [
            {"text": "n²", "hinweis": "Quadratisches Wachstum"},
            {"text": "2ⁿ − 1", "hinweis": "Exponentielles Wachstum"},
            {"text": "n · (n+1) / 2", "hinweis": "Gaußsche Summenformel"},
            {"text": "n!", "hinweis": "Faktorielles Wachstum"},
        ],
        "loesung_text": "2ⁿ − 1 Züge",
        "erklaerung": "<p>Die Rekursion ist elegant: Um n Scheiben zu verschieben, verschiebt man erst n−1 Scheiben auf den Hilfsstapel (2ⁿ⁻¹ − 1 Züge), dann die große Scheibe (1 Zug), dann wieder n−1 Scheiben drauf (2ⁿ⁻¹ − 1 Züge). T(n) = 2·T(n−1) + 1 löst sich zu 2ⁿ − 1.</p>",
        "kontext": "<p>Bei n = 64 (die legendäre Brahma-Version) ergibt das 2⁶⁴ − 1 ≈ 1,8 · 10¹⁹ Züge. Bei einem Zug pro Sekunde dauert das rund 585 Milliarden Jahre — weit länger als das Alter des Universums.</p>",
        "erkenntnis": "Exponentielles Wachstum wirkt harmlos bei kleinen n — und erdrückt bei großen. Dasselbe Muster steckt in Zinseszins, Virusvermehrung und algorithmischer Komplexität.",
    },
    "koenigsberger-bruecken": {
        "id": "koenigsberger-bruecken", "name": "Königsberger Brücken", "icon": "🌉",
        "farbe": "cyan", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Königsberg (heute Kaliningrad) liegt an der Pregel. Die Stadt hat 4 Landmassen, verbunden durch 7 Brücken. Euler fragte 1736: Kann man alle 7 Brücken genau einmal überqueren und zum Ausgangspunkt zurückkehren?",
        "frage": "Was ist Eulers Antwort — und warum?",
        "optionen": [
            {"text": "Ja, wenn man die richtige Startposition wählt", "hinweis": "Kommt es auf den Start an?"},
            {"text": "Nein — zu viele Knoten haben ungerade Knotengrade", "hinweis": "Euler-Kriterium für Graphen"},
            {"text": "Ja, aber nur ohne Rückkehr zum Start", "hinweis": "Euler-Weg vs. Euler-Kreis"},
            {"text": "Das Problem ist unentscheidbar", "hinweis": "Gibt es ein klares Kriterium?"},
        ],
        "loesung_text": "Nein — alle 4 Knoten haben ungerade Knotengrade",
        "erklaerung": "<p>Ein Euler-Kreis (alle Kanten genau einmal, Rückkehr) existiert genau dann, wenn <em>jeder</em> Knoten geraden Grad hat. In Königsberg haben alle 4 Landmassen eine ungerade Anzahl Brücken. Selbst ein offener Euler-Weg (ohne Rückkehr) erfordert genau 0 oder 2 Knoten mit ungeradem Grad — nicht 4.</p>",
        "kontext": "<p>Eulers Beweis gilt als Geburtsstunde der Graphentheorie. Das Prinzip steckt heute in Routenplanung (Post-Mann-Problem), Schaltkreisdesign und Netzwerkoptimierung.</p>",
        "erkenntnis": "Ein scheinbar praktisches Spaziergang-Problem führte zu einer der wichtigsten mathematischen Disziplinen. Abstraktion verwandelt Einzelfälle in universelle Strukturen.",
    },
    "vier-farben-satz": {
        "id": "vier-farben-satz", "name": "Der Vier-Farben-Satz", "icon": "🗺️",
        "farbe": "emerald", "kategorie": "Mathematik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Gegeben ist eine beliebige politische Landkarte in der Ebene. Zwei Länder, die eine gemeinsame Grenzlinie teilen, sollen verschiedene Farben erhalten. Punkte zählen nicht als gemeinsame Grenze.",
        "frage": "Wie viele Farben reichen stets aus?",
        "optionen": [
            {"text": "3 Farben", "hinweis": "Für planare Graphen ohne Dreieck"},
            {"text": "4 Farben", "hinweis": "Der bekannte Satz"},
            {"text": "5 Farben", "hinweis": "Ein älteres, leichter beweisbares Ergebnis"},
            {"text": "6 Farben", "hinweis": "Zu viel Spielraum"},
        ],
        "loesung_text": "4 Farben genügen immer",
        "erklaerung": "<p>Der Vier-Farben-Satz wurde 1976 von Appel & Haken bewiesen — als erster großer mathematischer Satz durch Computerhilfe (1936 Fälle geprüft). Dass 5 Farben reichen, war schon 1890 bekannt (Heawood). Dass 4 genügen, war über 100 Jahre offen.</p>",
        "kontext": "<p>Der Beweis ist bis heute umstritten, weil er nicht von Menschen vollständig nachprüfbar ist. Er löste eine Debatte aus: Ist ein Beweis, den kein Mensch vollständig lesen kann, wirklich ein Beweis?</p>",
        "erkenntnis": "Manche Wahrheiten sind einfach zu formulieren, aber extrem schwer zu beweisen. Und manchmal braucht Mathematik Verbündete aus der Informatik.",
    },
    "magische-quadrate": {
        "id": "magische-quadrate", "name": "Magische Quadrate", "icon": "🔢",
        "farbe": "amber", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Ein 3×3-Gitter wird mit den Zahlen 1 bis 9 (jede genau einmal) gefüllt. Jede Zeile, jede Spalte und jede Hauptdiagonale soll dieselbe Summe ergeben.",
        "frage": "Was ist diese magische Summe — und wie viele wesentlich verschiedene Lösungen gibt es?",
        "optionen": [
            {"text": "Summe 15, genau 1 wesentliche Lösung", "hinweis": "Rotationen/Spiegelungen gelten als gleich"},
            {"text": "Summe 15, genau 8 Lösungen", "hinweis": "Zählt man Symmetrien mit?"},
            {"text": "Summe 18, genau 1 Lösung", "hinweis": "Stimmt die Summe?"},
            {"text": "Summe 15, unendlich viele Lösungen", "hinweis": "Ist das bei ganzen Zahlen möglich?"},
        ],
        "loesung_text": "Summe 15, genau 1 wesentliche Lösung",
        "erklaerung": "<p>Die magische Summe ist (1+2+…+9)/3 = 45/3 = 15. Es gibt genau eine wesentliche Lösung (Lo-Shu-Quadrat), alle anderen 8 entstehen durch Rotation oder Spiegelung. Die 5 muss immer in der Mitte stehen.</p>",
        "kontext": "<p>Das Lo-Shu-Quadrat ist über 4000 Jahre alt und gilt in China als Glückssymbol. Magische Quadrate höherer Ordnung existieren in großer Zahl — für n=4 gibt es bereits 880 wesentlich verschiedene.</p>",
        "erkenntnis": "Symmetrie reduziert scheinbare Vielfalt auf das Wesentliche. Ein Ergebnis mit Eindeutigkeit zu beweisen ist oft schwerer als zu erraten.",
    },
    "fibonacci-suche": {
        "id": "fibonacci-suche", "name": "Fibonacci & Goldener Schnitt", "icon": "🌀",
        "farbe": "teal", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Die Fibonacci-Folge: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 … Jede Zahl ist die Summe der beiden Vorgänger.",
        "frage": "Gegen welchen Wert strebt das Verhältnis zweier aufeinanderfolgender Fibonacci-Zahlen (Fₙ₊₁/Fₙ)?",
        "optionen": [
            {"text": "π ≈ 3,14159", "hinweis": "Der Kreisumfang"},
            {"text": "e ≈ 2,71828", "hinweis": "Die Eulersche Zahl"},
            {"text": "φ ≈ 1,61803 (Goldener Schnitt)", "hinweis": "φ = (1+√5)/2"},
            {"text": "√2 ≈ 1,41421", "hinweis": "Pythagoreische Konstante"},
        ],
        "loesung_text": "φ ≈ 1,61803 — der Goldene Schnitt",
        "erklaerung": "<p>φ = (1+√5)/2 ≈ 1,618 ist die einzige positive Zahl mit der Eigenschaft φ² = φ + 1. Das Verhältnis 89/55 = 1,6182… nähert sich bereits stark an. Je größer n, desto genauer die Approximation.</p>",
        "kontext": "<p>φ taucht in Blattstellungen, Blütenblattanordnungen und Spiralen von Sonnenblumen auf — nicht aus ästhetischen Gründen, sondern weil die irrationalste aller irrationalen Zahlen optimale Packungsdichte erzeugt.</p>",
        "erkenntnis": "Zwei scheinbar unverwandte mathematische Objekte — eine rekursive Folge und ein geometrisches Verhältnis — sind tief miteinander verbunden. Das ist das Schönste an Mathematik.",
    },
    "kryptarithmen": {
        "id": "kryptarithmen", "name": "Kryptarithmen: SEND+MORE=MONEY", "icon": "🔐",
        "farbe": "rose", "kategorie": "Mathematik",
        "schwierigkeit": "Fortgeschritten", "dauer": "8 min",
        "setup": "Jeder Buchstabe steht für eine eindeutige Ziffer (0–9). Führende Stellen sind nicht 0. Gesucht: die Belegung, die <strong>SEND + MORE = MONEY</strong> erfüllt.",
        "frage": "Was ist die Ziffer für M?",
        "optionen": [
            {"text": "M = 1", "hinweis": "Der Übertrag aus der höchsten Stelle"},
            {"text": "M = 2", "hinweis": "Wäre ein Übertrag von 2 möglich?"},
            {"text": "M = 0", "hinweis": "Aber M ist eine führende Stelle"},
            {"text": "M = 9", "hinweis": "Maximalwert"},
        ],
        "loesung_text": "M = 1 (Lösung: 9567 + 1085 = 10652)",
        "erklaerung": "<p>Da SEND und MORE vierstellig sind, ist MONEY fünfstellig — der Übertrag aus der höchsten Stelle kann maximal 1 sein, also M = 1. Daraus folgt O = 0. Weiterhin: S = 9 (damit der Übertrag stimmt), E = 5, N = 6, D = 7, R = 8, Y = 2.</p>",
        "kontext": "<p>Kryptarithmen sind klassische Constraint-Satisfaction-Probleme (CSP). Moderne SAT-Solver lösen sie in Millisekunden — für Menschen sind sie ein Training in systematischer Fallunterscheidung.</p>",
        "erkenntnis": "Constraints propagieren sich: ein einziger fixierter Wert kann eine Kettenwirkung auslösen, die das gesamte Problem löst. Das ist das Prinzip hinter Sudoku, Schachanalyse und KI-Planung.",
    },
    "moebius-band": {
        "id": "moebius-band", "name": "Das Möbius-Band", "icon": "♾️",
        "farbe": "indigo", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Nimm einen langen Papierstreifen. Drehe ein Ende um 180° und klebe die Enden zusammen. Das Ergebnis ist das Möbius-Band.",
        "frage": "Was passiert, wenn du das Möbius-Band in der Mitte (längs) durchschneidest?",
        "optionen": [
            {"text": "Zwei getrennte Ringe entstehen", "hinweis": "Wie bei einem normalen Ring"},
            {"text": "Ein doppelt so langer, einmal verwundener Ring", "hinweis": "Topologische Überraschung"},
            {"text": "Das Band zerfällt in viele kleine Stücke", "hinweis": "Physikalisch?"},
            {"text": "Ein Möbius-Band bleibt erhalten", "hinweis": "Unverändert?"},
        ],
        "loesung_text": "Ein doppelt so langer Ring mit zwei Verdrehungen entsteht",
        "erklaerung": "<p>Das Möbius-Band hat nur <em>eine</em> Seite und eine Kante. Beim Durchschneiden in der Mitte folgt die Schere dem einzigen Weg rund um das Band — und landet nach einem vollen Umlauf auf der 'anderen Seite'. Das Ergebnis ist ein Ring doppelter Länge, zweimal verdreht (also ein orientierbarer Ring).</p>",
        "kontext": "<p>Das Möbius-Band ist ein zentrales Objekt der Topologie — der Mathematik der Formen unabhängig von Abstandsmessung. Es taucht in Förderanlagen auf, wo es gleichmäßigen Verschleiß beider Seiten erzeugt.</p>",
        "erkenntnis": "Intuition versagt bei topologischen Objekten. Mathmatisches Denken heißt: Eigenschaften präzise definieren, nicht bildlich vorstellen.",
    },
    "ziegenproblem-2": {
        "id": "ziegenproblem-2", "name": "Ziegenproblem 2.0", "icon": "🚪",
        "farbe": "orange", "kategorie": "Mathematik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Stell dir das klassische Monty-Hall-Problem vor, aber diesmal mit <strong>100 Türen</strong>. Du wählst Tür 1. Der Moderator öffnet 98 der restlichen 99 Türen — alle mit Ziegen. Noch zwei Türen sind geschlossen: deine und eine andere.",
        "frage": "Wie groß ist die Gewinnwahrscheinlichkeit, wenn du wechselst?",
        "optionen": [
            {"text": "50 % — beide Türen sind gleich wahrscheinlich", "hinweis": "Symmetrie-Argument"},
            {"text": "99 % — fast sicher ein Gewinn beim Wechsel", "hinweis": "Informationskonzentration"},
            {"text": "1 % — du hast von Anfang an fast sicher verloren", "hinweis": "Keine Aktualisierung?"},
            {"text": "Gleich wie beim 3-Türen-Problem: 2/3", "hinweis": "Skaliert das Prinzip?"},
        ],
        "loesung_text": "99 % Gewinnchance beim Wechsel",
        "erklaerung": "<p>Beim Wählen hattest du 1/100 Chance. Die anderen 99 Türen zusammen hatten 99/100. Der Moderator konzentriert diese 99/100 auf die eine verbleibende Tür — die andere Tür trägt also 99 % der Wahrscheinlichkeit. Das Prinzip ist dasselbe wie bei 3 Türen (2/3), nur deutlicher sichtbar.</p>",
        "kontext": "<p>Die 100-Türen-Version macht das Monty-Hall-Prinzip intuitiv zugänglich: Wenn du zufällig aus 100 zeigst und der allwissende Moderator 98 falsche aufdeckt, ist die Tür, die er <em>stehen ließ</em>, fast sicher die richtige.</p>",
        "erkenntnis": "Neue Information verändert Wahrscheinlichkeiten nicht symmetrisch. Wer fragt, wie Wissen verteilt wurde, denkt bayesianisch — und gewinnt öfter.",
    },
    "polyeder-check": {
        "id": "polyeder-check", "name": "Polyeder & Euler-Formel", "icon": "💠",
        "farbe": "sky", "kategorie": "Mathematik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Ein Würfel hat 8 Ecken (E), 12 Kanten (K) und 6 Flächen (F). Ein Tetraeder hat 4 Ecken, 6 Kanten, 4 Flächen. Ein Ikosaeder hat 12 Ecken, 30 Kanten, 20 Flächen.",
        "frage": "Was ergibt E − K + F in jedem dieser Fälle?",
        "optionen": [
            {"text": "0", "hinweis": "Würfel: 8−12+6=?"},
            {"text": "1", "hinweis": "Tetraeder: 4−6+4=?"},
            {"text": "2", "hinweis": "Euler-Charakteristik der Sphäre"},
            {"text": "Unterschiedlich je nach Polyeder", "hinweis": "Gibt es eine Invariante?"},
        ],
        "loesung_text": "Immer 2 — Eulers Polyederformel",
        "erklaerung": "<p>Würfel: 8−12+6 = 2. Tetraeder: 4−6+4 = 2. Ikosaeder: 12−30+20 = 2. Euler (1750): Für jeden konvexen Polyeder gilt E − K + F = 2. Die Zahl 2 ist die Euler-Charakteristik der Sphäre.</p>",
        "kontext": "<p>Die Formel versagt bei Polyedern mit Löchern (Torus: E−K+F = 0). Euler-Charakteristik ist ein topologisches Invariant — sie ändert sich nicht beim Biegen, nur beim Schneiden oder Kleben.</p>",
        "erkenntnis": "Hinter der Vielfalt der Formen steckt eine einzige Zahl. Invarianten sind das Werkzeug, mit dem Mathematik Chaos in Ordnung verwandelt.",
    },
    "banach-tarski": {
        "id": "banach-tarski", "name": "Das Banach-Tarski-Paradoxon", "icon": "🧩",
        "farbe": "pink", "kategorie": "Mathematik",
        "schwierigkeit": "Fortgeschritten", "dauer": "5 min",
        "setup": "Banach und Tarski bewiesen 1924: Eine Vollkugel im dreidimensionalen Raum lässt sich in endlich viele disjunkte Teilmengen zerlegen, die sich – nur durch Drehungen und Verschiebungen, ohne Dehnen oder Verzerren – zu <strong>zwei</strong> Vollkugeln zusammensetzen lassen, jede gleich groß wie das Original.",
        "frage": "Wie viele Teilmengen genügen mindestens – und welche zentrale Voraussetzung macht den Beweis möglich?",
        "optionen": [
            {"text": "2 Teile, ohne weitere Annahme – pure Geometrie", "hinweis": "Zerschneide eine Kugel mit einem Schnitt"},
            {"text": "5 Teile, mithilfe des Auswahlaxioms", "hinweis": "Robinsons Verschärfung 1947"},
            {"text": "Unendlich viele Teile – sonst geht es nie", "hinweis": "Banach-Tarski betont „endlich“"},
            {"text": "Es ist gar nicht möglich – nur ein Denkfehler", "hinweis": "Aber das Theorem ist bewiesen"},
        ],
        "loesung_text": "5 Teile genügen – aber nur unter Verwendung des Auswahlaxioms",
        "erklaerung": "<p>Banach & Tarski zeigten 1924 die Zerlegung mit endlich vielen Stücken. Robinson bewies 1947, dass <strong>5</strong> die minimale Anzahl ist (4 reichen nicht). Die Stücke sind allerdings <em>nicht messbar</em> – sie haben weder Volumen noch Oberfläche im klassischen Sinne. Der Beweis stützt sich entscheidend auf das <strong>Auswahlaxiom</strong> (AC): die Annahme, dass man aus jeder Familie nichtleerer Mengen ein Element auswählen kann, selbst aus überabzählbar vielen.</p>",
        "kontext": "<p>Das Paradoxon zeigt einen tiefen Riss zwischen Mathematik und physikalischer Realität: Atome sind diskret, eine Kugel im strengen Sinn ist ein <em>überabzählbares Kontinuum</em>. Ohne dieses Kontinuum kein Banach-Tarski. Manche Mathematiker (Konstruktivisten) verwerfen das Auswahlaxiom genau deshalb. In der Praxis wird AC trotzdem fast überall verwendet – ohne es bricht ein Großteil der Analysis und Topologie zusammen.</p>",
        "erkenntnis": "Was beweisbar ist, muss nicht vorstellbar sein. Mathematik beschreibt nicht die physische Welt, sondern eine logische – und manchmal fallen beide auseinander. Wer „aber das geht doch nicht“ denkt, hat das Theorem verstanden.",
    },
    # ── Physik ───────────────────────────────────────────────────────────
    "schroedinger-katze": {
        "id": "schroedinger-katze", "name": "Schrödingers Katze", "icon": "🐱",
        "farbe": "violet", "kategorie": "Physik",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Eine Katze sitzt in einer geschlossenen Box. Darin: ein radioaktives Atom, ein Geigerzähler, ein Hammer, ein Giftbehälter. Wenn das Atom zerfällt (50 % in 1 Stunde), löst der Geigerzähler den Hammer aus und tötet die Katze.",
        "frage": "Was sagt die Kopenhagener Deutung der Quantenmechanik über den Zustand der Katze vor dem Öffnen?",
        "optionen": [
            {"text": "Die Katze ist tot oder lebendig — wir wissen es nur nicht", "hinweis": "Klassische Unwissenheit"},
            {"text": "Die Katze ist in einer Superposition aus tot UND lebendig", "hinweis": "Quantenmechanische Deutung"},
            {"text": "Das Atom zerfällt deterministisch — kein Paradoxon", "hinweis": "Verborgene Variablen?"},
            {"text": "Quantenmechanik gilt nicht für makroskopische Objekte", "hinweis": "Dekohärenz-Argument"},
        ],
        "loesung_text": "Superposition: tot UND lebendig bis zur Messung",
        "erklaerung": "<p>Die Kopenhagener Deutung: Das Atom ist vor der Messung in Superposition (zerfallen + nicht zerfallen). Diese überträgt sich auf Katze. Erst die Messung 'kollabiert' die Wellenfunktion. Schrödinger entwarf das Gedankenexperiment 1935, um diese Konsequenz als absurd zu enthüllen.</p>",
        "kontext": "<p>Das Gedankenexperiment ist kein echtes Paradoxon, sondern eine Kritik an der Deutung. Heute erklärt Dekohärenz, warum Superposition im Makrobereich nie beobachtet wird: Die Umgebung 'misst' ständig.</p>",
        "erkenntnis": "Quantenmechanik beschreibt keine verborgene Realität, sondern Zustände vor der Messung. Was 'Realität' ohne Beobachter bedeutet, ist keine Physik-, sondern eine Philosophiefrage.",
    },
    "maxwells-daemon": {
        "id": "maxwells-daemon", "name": "Maxwells Dämon", "icon": "😈",
        "farbe": "rose", "kategorie": "Physik",
        "schwierigkeit": "Fortgeschritten", "dauer": "5 min",
        "setup": "Ein Behälter ist durch eine Trennwand mit einer kleinen Klappe geteilt. Ein winziges Wesen (der Dämon) öffnet die Klappe nur für schnelle Moleküle von links nach rechts und für langsame von rechts nach links. Ergebnis: links kühlt ab, rechts erwärmt sich — ohne Energiezufuhr?",
        "frage": "Warum verletzt der Dämon den zweiten Hauptsatz der Thermodynamik dennoch nicht?",
        "optionen": [
            {"text": "Weil er selbst Energie benötigt, um die Klappe zu bewegen", "hinweis": "Mechanische Arbeit?"},
            {"text": "Weil das Speichern und Löschen von Messinformation Entropie erzeugt", "hinweis": "Landauers Prinzip"},
            {"text": "Weil der Dämon keine Moleküle unterscheiden kann", "hinweis": "Messgenauigkeit?"},
            {"text": "Weil schnelle Moleküle nicht konzentrierbar sind", "hinweis": "Statistische Argumentation"},
        ],
        "loesung_text": "Das Löschen von Messinformation erzeugt Entropie (Landauers Prinzip)",
        "erklaerung": "<p>Der Dämon muss Informationen über Molekülgeschwindigkeiten speichern. Sein Gedächtnis füllt sich. Wenn er es löscht (um weiterzumessen), wird Entropie in die Umgebung abgegeben — mindestens k·ln(2) pro gelöschtem Bit (Landauer 1961). Diese Entropie kompensiert exakt die thermodynamische Entropieverringerung.</p>",
        "kontext": "<p>Maxwells Dämon (1867) war 100 Jahre ungelöst. Die Lösung verknüpft Thermodynamik mit Informationstheorie: Information ist physikalisch, und Löschen hat einen thermodynamischen Preis.</p>",
        "erkenntnis": "Information ist keine abstrakte Ressource — sie hat physikalische Kosten. Thermodynamik und Informationstheorie sind zwei Seiten derselben Medaille.",
    },
    "zwillingsparadoxon": {
        "id": "zwillingsparadoxon", "name": "Das Zwillingsparadoxon", "icon": "👯",
        "farbe": "indigo", "kategorie": "Physik",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Zwilling A bleibt auf der Erde. Zwilling B reist mit 99 % Lichtgeschwindigkeit zu einem 10 Lichtjahre entfernten Stern, kehrt zurück. Nach Spezielle Relativitätstheorie vergeht für B weniger Zeit (Zeitdilatation).",
        "frage": "Warum ist das kein echtes Paradoxon — also warum ist nicht auch A jünger als B?",
        "optionen": [
            {"text": "Weil Lichtgeschwindigkeit nie wirklich erreicht wird", "hinweis": "Annäherung vs. Exaktheit"},
            {"text": "Weil B beschleunigt (und bremst) — die Situation ist asymmetrisch", "hinweis": "Inertialsysteme"},
            {"text": "Weil A die schwerere Person ist", "hinweis": "Masse und Zeit?"},
            {"text": "Weil das Paradoxon tatsächlich unlösbar ist", "hinweis": "Steht das in Lehrbüchern?"},
        ],
        "loesung_text": "B beschleunigt — die Situation ist nicht symmetrisch",
        "erklaerung": "<p>Spezielle Relativitätstheorie gilt nur für Inertialsysteme (gleichförmige Bewegung). B wechselt beim Umkehren das Inertialsystem — das bricht die scheinbare Symmetrie. Nur B hat eine absolute Beschleunigung erfahren. Das Ergebnis ist eindeutig: B ist jünger.</p>",
        "kontext": "<p>GPS-Satelliten müssen relativistische Zeitkorrekturen berücksichtigen (~38 Mikrosekunden/Tag), sonst würde die Positionsgenauigkeit täglich um ~10 km driften. Das Zwillingsparadoxon ist also real messbar.</p>",
        "erkenntnis": "Symmetrie-Argumente sind verlockend aber gefährlich: Sie gelten nur, wenn die Situation wirklich symmetrisch ist. Beschleunigung bricht die Symmetrie.",
    },
    "doppelspalt": {
        "id": "doppelspalt", "name": "Das Doppelspaltexperiment", "icon": "🔬",
        "farbe": "cyan", "kategorie": "Physik",
        "schwierigkeit": "Fortgeschritten", "dauer": "5 min",
        "setup": "Elektronen werden einzeln durch eine Platte mit zwei Spalten geschossen. Auf dem Schirm dahinter entsteht ein Interferenzmuster — obwohl jedes Elektron einzeln durch 'einen' Spalt geht. Sobald man einen Detektor anbringt, welchen Spalt das Elektron passiert, verschwindet das Interferenzmuster.",
        "frage": "Was ist die quantenmechanische Erklärung für das Verschwinden des Interferenzmusters?",
        "optionen": [
            {"text": "Der Detektor stört das Elektron physisch (Heisenberg-Störung)", "hinweis": "Klassische Erklärung"},
            {"text": "Die Messung liefert Welcher-Weg-Information — und kollabiert die Superposition", "hinweis": "Quantenmechanische Erklärung"},
            {"text": "Elektronen wechselwirken miteinander am Detektor", "hinweis": "Klassische Wechselwirkung?"},
            {"text": "Das Interferenzmuster bleibt — es ist nur kleiner", "hinweis": "Empirisch widerlegt"},
        ],
        "loesung_text": "Welcher-Weg-Information kollabiert die Superposition",
        "erklaerung": "<p>Das Elektron interferiert mit sich selbst, weil es beide Wege gleichzeitig nimmt (Superposition). Sobald eine Messung möglich ist, <em>welchen</em> Weg das Elektron nahm — auch wenn man nicht hinschaut — entsteht Dekohärenz. Information reicht aus, die Quantenkohärenz zu zerstören.</p>",
        "kontext": "<p>Feynmans beruehmt gewordener Satz: &ldquo;Niemand versteht die Quantenmechanik.&rdquo; Das Experiment zeigt, dass Messung nicht nur Wissen offenbart, sondern Realitaet veraendert &mdash; ein fundamentaler Unterschied zur klassischen Physik.</p>",
        "erkenntnis": "In der Quantenwelt ist die Möglichkeit einer Messung bereits ausreichend, um das Ergebnis zu beeinflussen. Unwissen ist keine Schwäche — es ist manchmal eine Ressource.",
    },
    "bernoulli-puzzle": {
        "id": "bernoulli-puzzle", "name": "Das Bernoulli-Puzzle", "icon": "✈️",
        "farbe": "sky", "kategorie": "Physik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Wenn du mit einem Strohhalm über ein Stück Papier bläst, hebt sich das Papier — statt gedrückt zu werden. Ein Duschvorhang bläht sich beim Duschen nach innen. Ein Flugzeugflügel ist oben gewölbt, unten flach.",
        "frage": "Was ist das gemeinsame Prinzip hinter all diesen Phänomenen?",
        "optionen": [
            {"text": "Schnellere Strömung → geringerer Druck (Bernoulli)", "hinweis": "Energieerhaltung in Fluiden"},
            {"text": "Heiße Luft steigt auf (Auftrieb)", "hinweis": "Nur bei Temperaturunterschied"},
            {"text": "Luftreibung drückt Flächen zusammen", "hinweis": "Reibung wirkt anders"},
            {"text": "Newton: Luft wird nach unten abgelenkt → Reaktionskraft nach oben", "hinweis": "Auch richtig — aber nicht Bernoulli"},
        ],
        "loesung_text": "Höhere Strömungsgeschwindigkeit → niedrigerer Druck (Bernoulli-Effekt)",
        "erklaerung": "<p>Bernoullis Gleichung: p + ½ρv² + ρgh = const. Wo die Strömung schneller ist, ist der Druck niedriger. Der Flügel oben: mehr Weg → höhere Geschwindigkeit → niedrigerer Druck → Auftrieb. Das Papier: schnelle Luft oben → niedriger Druck → Papier steigt.</p>",
        "kontext": "<p>Hinweis: Der Bernoulli-Effekt allein erklärt nicht vollständig den Flugzeugauftrieb — Newtonscher Impulsübertrag (Ablenken der Luft nach unten) trägt ebenfalls bei. Die Wahrheit in der Strömungslehre ist oft vielschichtiger als Schulbuch-Erklärungen zeigen.</p>",
        "erkenntnis": "Physikalische Prinzipien erscheinen in überraschend vielen Alltagsphänomenen. Wer das Werkzeug kennt, erkennt das Muster — vom Staubsauger bis zum Flugzeugflügel.",
    },
    "foucault-pendel": {
        "id": "foucault-pendel", "name": "Das Foucaultsche Pendel", "icon": "🕰️",
        "farbe": "emerald", "kategorie": "Physik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "1851 hängte Léon Foucault ein 67 m langes Pendel im Pariser Panthéon auf. Im Laufe des Tages drehte sich die Schwingungsebene des Pendels sichtbar. Die Zuschauer erlebten eine Rotation, die sie nicht selbst spürten.",
        "frage": "Was bewies das Pendel — und was dreht sich dabei tatsächlich?",
        "optionen": [
            {"text": "Die Schwingungsebene dreht sich — also dreht sich die Erde darunter", "hinweis": "Trägheitssystem vs. rotierendes System"},
            {"text": "Das Pendel dreht sich durch Luftströmungen", "hinweis": "Dann wäre es nicht reproduzierbar"},
            {"text": "Die Erdanziehung rotiert das Pendel", "hinweis": "Gravitation wirkt nach unten"},
            {"text": "Das Pendel beweist, dass die Sonne um die Erde kreist", "hinweis": "Bezugssystem?"},
        ],
        "loesung_text": "Die Erde dreht sich unter dem Pendel — das Pendel bleibt im Inertialsystem fixiert",
        "erklaerung": "<p>Das Pendel schwingt in einem fixen Inertialsystem (relativ zu den Sternen). Die Erde dreht sich darunter weg. Am Nordpol würde die Ebene in 24 h einmal rotieren; in Paris (48,9°N) dauert es 32 h (Drehrate × sin(Breitengrad)).</p>",
        "kontext": "<p>Das Experiment war das erste direkte, öffentlich sichtbare Beweis der Erdrotation — ohne Astronomieinstrumente. Heute hängen Foucault-Pendel in Museen weltweit als Symbol physikalischen Denkens.</p>",
        "erkenntnis": "Trägheit ist eine mächtige Eigenschaft: Ein schwingendes Pendel 'erinnert' sich an das absolute Bezugssystem, während wir uns mit der Erde mitdrehen.",
    },
    "tensegrity": {
        "id": "tensegrity", "name": "Tensegrity-Strukturen", "icon": "🏗️",
        "farbe": "amber", "kategorie": "Physik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "In einer Tensegrity-Struktur berühren sich keine zwei Stäbe direkt. Jeder Stab schwebt zwischen Seilen. Die Struktur wirkt wie ein Widerspruch: Druckkräfte in schwebenden Elementen, Zugkräfte in den Seilen — und trotzdem stabil.",
        "frage": "Was hält die Struktur zusammen, obwohl keine Stäbe sich berühren?",
        "optionen": [
            {"text": "Magnetismus zwischen den Stäben", "hinweis": "Nicht nötig"},
            {"text": "Gleichgewicht zwischen Zug (Seile) und Druck (Stäbe) — Tensional Integrity", "hinweis": "Der Name ist das Programm"},
            {"text": "Die Seile sind dicker als sie aussehen und tragen Druckkräfte", "hinweis": "Seile können keinen Druck übertragen"},
            {"text": "Klebstoff an unsichtbaren Verbindungspunkten", "hinweis": "Rein mechanisch"},
        ],
        "loesung_text": "Gleichgewicht von Zug und Druck — Tensional Integrity",
        "erklaerung": "<p>Stäbe übertragen Druckkräfte (Kompression), Seile übertragen Zugkräfte (Tension). Die Struktur ist im Gleichgewicht, weil alle Kräfte ausgeglichen sind. Kein Stab braucht einen anderen zu berühren — die Seile halten das System zusammen.</p>",
        "kontext": "<p>Tensegrity (Begriff von Buckminster Fuller) taucht in Biologie auf: Das menschliche Muskel-Skelett-System ist ein biologisches Tensegrity-System. Muskeln (Zugelemente) und Knochen (Druckelemente) arbeiten nach demselben Prinzip.</p>",
        "erkenntnis": "Stabilität entsteht nicht nur durch direkte Verbindungen, sondern durch das globale Kräftegleichgewicht. Das gilt für Strukturen — und für Verhandlungssysteme.",
    },
    "archimedischer-punkt": {
        "id": "archimedischer-punkt", "name": "Der Archimedische Punkt", "icon": "⚖️",
        "farbe": "teal", "kategorie": "Physik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Archimedes sagte: \"Gebt mir einen festen Punkt, und ich hebe die Welt aus den Angeln.\" Mit einem langen Hebel und einem Stützpunkt (Hypomochlion) könnte man theoretisch jede Last heben.",
        "frage": "Wenn die Erde ~6 × 10²⁴ kg wiegt und du mit 60 kg drückst: Wie lang müsste der Hebel (Kraftarm) sein, wenn der Lastarm 1 m beträgt?",
        "optionen": [
            {"text": "Ca. 10²³ m (~10 Milliarden Lichtjahre)", "hinweis": "F_L × l_L = F_K × l_K"},
            {"text": "Ca. 10⁶ m (~1000 km)", "hinweis": "Unterschätzung"},
            {"text": "Ca. 10¹⁰ m (~Sonnenabstand)", "hinweis": "Zu kurz"},
            {"text": "Ca. 10¹⁵ m (~100 Lichtjahre)", "hinweis": "Fast — aber noch zu kurz"},
        ],
        "loesung_text": "Ca. 10²³ m — jenseits des beobachtbaren Universums",
        "erklaerung": "<p>Hebelgesetz: F_K × l_K = F_L × l_L → l_K = (6×10²⁴ × 9,81 × 1) / (60 × 9,81) ≈ 10²³ m. Das Observable Universum hat einen Radius von ~4,4 × 10²⁶ m. Der Hebel wäre zwar kürzer — aber es gibt keinen Stützpunkt im leeren Raum.</p>",
        "kontext": "<p>Der archimedische Punkt ist zur Metapher geworden: ein fixer, unabhängiger Standpunkt außerhalb eines Systems, von dem aus man es bewegt. In Erkenntnistheorie und Verhandlung bedeutet er: eine neutrale Position, die keiner Partei gehört.</p>",
        "erkenntnis": "Das Hebelgesetz ist exakt — aber Ressourcen (Hebellänge, Stützpunkt) begrenzen, was theoretisch Mögliches auch praktisch ist. Prinzip und Praxis sind verschiedene Dinge.",
    },
    "eimer-experiment": {
        "id": "eimer-experiment", "name": "Newtons Eimerversuch", "icon": "🪣",
        "farbe": "pink", "kategorie": "Physik",
        "schwierigkeit": "Fortgeschritten", "dauer": "5 min",
        "setup": "Newton füllt einen Eimer mit Wasser und dreht ihn an einem Seil. Zuerst dreht der Eimer, das Wasser nicht — Oberfläche flach. Dann dreht auch das Wasser mit — Oberfläche wölbt sich. Frage: Wozu dreht sich das Wasser — relativ zum Eimer, relativ zur Erde, relativ zu den Sternen?",
        "frage": "Was sagte Newton über den 'absoluten Raum' — und wie kritisierte Mach das?",
        "optionen": [
            {"text": "Das Wasser dreht sich relativ zum Eimer — das erklärt die Wölbung", "hinweis": "Aber flaches Wasser + drehendem Eimer widerspricht das"},
            {"text": "Das Wasser dreht sich relativ zum absoluten Raum (Newton) — Mach: relativ zur Gesamtmasse des Universums", "hinweis": "Newton vs. Mach"},
            {"text": "Zentrifugalkräfte existieren nicht — es ist eine Illusion", "hinweis": "Sie haben reale Wirkungen"},
            {"text": "Die Wölbung entsteht durch Luftreibung", "hinweis": "Auch im Vakuum?"},
        ],
        "loesung_text": "Newton: absoluter Raum; Mach: Rotation relativ zur kosmischen Massenverteilung",
        "erklaerung": "<p>Newton: Die Wölbung entsteht bei Rotation relativ zum 'absoluten Raum'. Mach (1883) kritisierte: Es gibt keinen absoluten Raum; Trägheit entsteht durch die Wechselwirkung mit der Gesamtmasse des Universums (Machsches Prinzip). Einstein ließ sich davon bei der Allgemeinen Relativitätstheorie inspirieren.</p>",
        "kontext": "<p>Das Machsche Prinzip ist bis heute nicht vollständig in die Allgemeine Relativitätstheorie integriert. Der einfache rotierende Eimer stellt eine der tiefsten Fragen der Physik: Was ist Beschleunigung relativ zu?</p>",
        "erkenntnis": "Einfache Experimente können tiefste Prinzipien aufdecken. Newton und Mach sahen dasselbe Wasser und zogen grundlegend verschiedene Schlüsse — beide hatten ihre Stärken.",
    },
    # ── Spieltheorie ─────────────────────────────────────────────────────
    "matching-pennies": {
        "id": "matching-pennies", "name": "Matching Pennies", "icon": "🪙",
        "farbe": "violet", "kategorie": "Spieltheorie",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Zwei Spieler legen gleichzeitig eine Münze verdeckt auf den Tisch. Spieler A gewinnt 1 €, wenn beide Münzen gleich sind (beide Kopf oder beide Zahl). Spieler B gewinnt 1 €, wenn sie verschieden sind.",
        "frage": "Was ist die optimale Strategie für Spieler A?",
        "optionen": [
            {"text": "Immer Kopf legen — maximaler Erwartungswert", "hinweis": "Was passiert, wenn B das weiß?"},
            {"text": "Gemischt spielen: 50 % Kopf, 50 % Zahl (zufällig)", "hinweis": "Nash-Gleichgewicht in gemischten Strategien"},
            {"text": "Das Muster des Gegners analysieren und ausnutzen", "hinweis": "Nur wenn B eine Strategie hat"},
            {"text": "Zahl legen — weniger vorhersehbar", "hinweis": "Ist Zahl weniger vorhersehbar als Kopf?"},
        ],
        "loesung_text": "50/50 zufällig gemischte Strategie",
        "erklaerung": "<p>Matching Pennies ist ein Nullsummenspiel ohne Nash-Gleichgewicht in reinen Strategien. Das einzige Nash-Gleichgewicht ist die <em>gemischte Strategie</em>: beide spielen jede Option mit 50 %. Jede reine Strategie ist ausnutzbar; nur die gemischte Strategie macht den Gegner indifferent.</p>",
        "kontext": "<p>Gemischte Strategien sind das spieltheoretische Fundament für Fußball-Elfmeter, Tennis-Aufschläge und Poker. Profis mischen tatsächlich ihre Aktionen in der Nash-gleichgewichtigen Häufigkeit.</p>",
        "erkenntnis": "In Nullsummenspielen ohne reine Lösung ist Unvorhersehbarkeit die optimale Strategie. Randomisierung ist kein Zeichen von Schwäche — sie ist Spieltheorie.",
    },
    "cake-cutting": {
        "id": "cake-cutting", "name": "Cake Cutting", "icon": "🎂",
        "farbe": "rose", "kategorie": "Spieltheorie",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Alice und Bob teilen einen Kuchen. Beide haben eigene Vorstellungen, was ein fairer Anteil ist. Es gibt keinen neutralen Schiedsrichter. Wie teilt man den Kuchen so, dass beide zufrieden sind — ohne Kenntnis der Präferenzen des anderen?",
        "frage": "Welches Verfahren garantiert Fairness (beide erhalten mindestens 50 % in ihrer eigenen Bewertung)?",
        "optionen": [
            {"text": "Münzwurf — der Gewinner bekommt alles", "hinweis": "Ex-ante fair, aber nicht für den Verlierer"},
            {"text": "'Du schneidest, ich wähle' — der Schneider teilt, der andere wählt zuerst", "hinweis": "Klassisches Verfahren"},
            {"text": "Beide schätzen den Kuchen und teilen nach Mittelwert", "hinweis": "Wer schätzt zuerst?"},
            {"text": "Ein Algorithmus berechnet die optimale Teilung", "hinweis": "Braucht man Präferenzkenntnis?"},
        ],
        "loesung_text": "'Du schneidest, ich wähle' — envy-free und proportional",
        "erklaerung": "<p>Der Schneider (Alice) wird genau in der Mitte schneiden — denn er weiß, dass Bob das größere Stück nimmt. Beide erhalten mindestens 50 % in ihrer eigenen Bewertung. Das Verfahren ist <em>proportional</em> (jeder ≥ 1/n) und <em>envy-free</em> (keiner beneidet den anderen) — ohne jegliche Kommunikation über Präferenzen.</p>",
        "kontext": "<p>Für n &gt; 2 Personen ist envy-free Teilung algorithmisch komplex. Das Selfridge-Conway-Verfahren (1960/1993) löst es für 3 Personen endlich; für n Personen wurde erst 2016 ein endlicher Algorithmus gefunden (Aziz & Mackenzie).</p>",
        "erkenntnis": "Faire Verfahren brauchen keine Informationen über Präferenzen — sie müssen nur die richtigen Anreize setzen. Das 'Du schneidest, ich wähle'-Prinzip nutzt egoistisches Verhalten als Design-Element.",
    },
    # ── Statistik ─────────────────────────────────────────────────────────
    "berkson": {
        "id": "berkson", "name": "Das Berkson-Paradoxon", "icon": "🏥",
        "farbe": "cyan", "kategorie": "Statistik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "In einer Krankenhausstudie werden Patienten untersucht. Man stellt fest: Raucher scheinen seltener Lungenkrebs zu haben als Nichtraucher. Das widerspricht allem, was wir wissen. Wie ist das möglich?",
        "frage": "Was erklärt diesen scheinbaren Widerspruch?",
        "optionen": [
            {"text": "Rauchen schützt tatsächlich vor Lungenkrebs in bestimmten Populationen", "hinweis": "Unwahrscheinlich"},
            {"text": "Die Stichprobe ist verzerrt: Ins Krankenhaus kommen auch Raucher wegen anderer Krankheiten", "hinweis": "Selection Bias"},
            {"text": "Lungenkrebs wird bei Rauchern seltener diagnostiziert", "hinweis": "Diagnosebias?"},
            {"text": "Der Effekt ist zufällig und verschwindet mit größerer Stichprobe", "hinweis": "Systematisch oder zufällig?"},
        ],
        "loesung_text": "Selection Bias: Die Krankenhausstichprobe ist keine Zufallsstichprobe",
        "erklaerung": "<p>Ins Krankenhaus kommen Menschen, die krank sind — aus verschiedenen Gründen. Raucher sind häufiger wegen Herzkrankheiten, COPD oder anderen Rauchfolgen dort. In dieser selektierten Gruppe erscheinen Raucher seltener mit Lungenkrebs — nicht weil Rauchen schützt, sondern weil sie aus anderen Gründen ins Krankenhaus kamen.</p>",
        "kontext": "<p>Berkson (1946) beschrieb diesen Bias systematisch. Er taucht überall dort auf, wo die Stichprobe durch eine Kombination von Variablen selektiert wird. COVID-Studien zeigten ähnliche Effekte: In Krankenhäusern schienen manche Risikofaktoren schützend, weil sie Patienten aus anderen Gründen einlieferten.</p>",
        "erkenntnis": "Stichproben aus selektierten Populationen liefern verzerrte Korrelationen. Bevor man eine Kausalaussage macht, muss man fragen: Wie entstand die Stichprobe?",
    },
    "p-hacking": {
        "id": "p-hacking", "name": "P-Hacking", "icon": "🎰",
        "farbe": "rose", "kategorie": "Statistik",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Ein Forscher testet, ob Schokolade das Gedächtnis verbessert. Er testet 20 verschiedene kognitive Metriken. Bei einer findet er p = 0,04 (< 0,05). Er veröffentlicht nur diesen Befund: 'Schokolade verbessert Wortmerkung signifikant.'",
        "frage": "Was ist das Problem mit diesem Vorgehen?",
        "optionen": [
            {"text": "0,04 ist nicht klein genug — man braucht p < 0,01", "hinweis": "Nur eine Schwelle verschieben?"},
            {"text": "Bei 20 Tests ist mindestens 1 falscher Treffer (p < 0,05) im Schnitt erwartet", "hinweis": "Multiples Testen"},
            {"text": "Schokolade kann kognitiv nicht wirken — das Ergebnis ist biologisch unmöglich", "hinweis": "Nicht das statistische Problem"},
            {"text": "Die Stichprobe war zu klein", "hinweis": "Vielleicht — aber das ist nicht das Kernproblem hier"},
        ],
        "loesung_text": "Multiples Testen erhöht die Falsch-Positiv-Rate — hier auf ~64 %",
        "erklaerung": "<p>Bei 20 unabhängigen Tests mit α = 0,05 beträgt die Wahrscheinlichkeit, mindestens einen falschen Treffer zu erhalten: 1 − 0,95²⁰ ≈ 64 %. Der Forscher wählt den 'besten' Test aus — ohne Bonferroni-Korrektur oder Prä-Registrierung. Das nennt man P-Hacking oder HARKing (Hypothesizing After Results are Known).</p>",
        "kontext": "<p>Die Replikationskrise (2011–heute) hat gezeigt, dass viele publizierte Ergebnisse in Psychologie, Medizin und Sozialwissenschaften auf P-Hacking zurückzuführen sind. Lösungen: Prä-Registrierung, Bonferroni-Korrektur, größere Stichproben, Open Science.</p>",
        "erkenntnis": "Ein p-Wert unter 0,05 ist kein Beweis — er ist ein statistisches Signal, das in seinem Kontext bewertet werden muss. Wie viele Tests wurden durchgeführt? Was wurde nicht veröffentlicht?",
    },
    "stichproben-raetsel": {
        "id": "stichproben-raetsel", "name": "Die Literary-Digest-Katastrophe", "icon": "📰",
        "farbe": "amber", "kategorie": "Statistik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "1936, USA. Das Magazin Literary Digest befragte 10 Millionen Menschen zur Präsidentschaftswahl. Die riesige Stichprobe prophezeite einen klaren Sieg für den Republikaner Landon. Roosevelt gewann haushoch. Gleichzeitig: George Gallup befragte nur 50.000 Menschen — und lag richtig.",
        "frage": "Warum scheiterte die 10-Millionen-Stichprobe, während 50.000 genügten?",
        "optionen": [
            {"text": "10 Millionen sind zu viele — Oversampling verzerrt", "hinweis": "Mehr ist nie schlechter bei Zufallsstichproben"},
            {"text": "Die Stichprobe war nicht zufällig: Befragte wurden aus Telefonbüchern und Automobilklubs gewählt", "hinweis": "Selection Bias in der Stichprobenkonstruktion"},
            {"text": "Die Wähler haben im letzten Moment ihre Meinung geändert", "hinweis": "Dann hätte Gallup auch falsch gelegen"},
            {"text": "Das Magazin hat die Ergebnisse gefälscht", "hinweis": "Historisch nicht belegt"},
        ],
        "loesung_text": "Selection Bias: Die Stichprobe war systematisch zu wohlhabend",
        "erklaerung": "<p>1936 hatten vor allem Wohlhabende Telefone und Autos — und die stimmten mehrheitlich für Landon. Arme und Mittelstand (Roosevelts Basis) wurden kaum befragt. Gallup verwendete eine repräsentative Zufallsstichprobe — kleiner, aber unverzerrt.</p>",
        "kontext": "<p>Dieser Misserfolg begründete die moderne Meinungsforschung. Das Literary Digest ging danach bankrott. Die Lektion: Stichprobengröße ist sekundär — Repräsentativität ist primär.</p>",
        "erkenntnis": "Größe ersetzt keine Repräsentativität. Eine schlechte Stichprobe wird durch mehr davon nur selbstsicherer in ihrem Irrtum.",
    },
    "benfords-gesetz": {
        "id": "benfords-gesetz", "name": "Benfords Gesetz", "icon": "1️⃣",
        "farbe": "indigo", "kategorie": "Statistik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "In vielen natürlichen Datensätzen (Bevölkerungszahlen, Aktienkurse, Flusslängen, Steuererklärungen) beginnen Zahlen nicht gleichmäßig verteilt mit den Ziffern 1–9. Benford (1938) beobachtete ein klares Muster.",
        "frage": "Wie oft beginnt eine Zahl in solchen Datensätzen mit der Ziffer 1?",
        "optionen": [
            {"text": "Ca. 11 % — gleichmäßige Verteilung über 9 Ziffern", "hinweis": "Wäre die neutrale Erwartung"},
            {"text": "Ca. 30 % — Benford-Verteilung", "hinweis": "log₁₀(1 + 1/1) ≈ 30,1 %"},
            {"text": "Ca. 50 % — die erste Stelle tendiert zur Mitte", "hinweis": "Keine Erklärung"},
            {"text": "Ca. 20 % — doppelt so häufig wie Gleichverteilung", "hinweis": "Zu niedrig"},
        ],
        "loesung_text": "Ca. 30 % — log₁₀(2) ≈ 30,1 %",
        "erklaerung": "<p>P(erste Ziffer = d) = log₁₀(1 + 1/d). Die Erklärung: Zahlen wachsen multiplikativ. Eine Zahl, die sich von 1 auf 2 verdoppelt, durchläuft dieselbe relative Spanne wie von 2 auf 4, 4 auf 8 usw. Auf einer logarithmischen Skala deckt '1x' den größten Bereich ab.</p>",
        "kontext": "<p>Finanzermittler (FBI, IRS) nutzen Benfords Gesetz zur Betrugserkennung: Erfundene Zahlen folgen der Verteilung oft nicht, weil Menschen intuitiv gleichmäßiger verteilen. Der Enron-Skandal und Wahlbetrugsanalysen nutzten Benford-Tests.</p>",
        "erkenntnis": "Zahlen in der Natur sind nicht gleichmäßig verteilt — sie folgen einer Logik der multiplikativen Prozesse. Wer das weiß, kann Anomalien erkennen.",
    },
    "will-rogers": {
        "id": "will-rogers", "name": "Das Will-Rogers-Phänomen", "icon": "📈",
        "farbe": "emerald", "kategorie": "Statistik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Zwei Gruppen: Oklahoma-Einwanderer (IQ-Mittel: 80) und Kalifornier (Mittel: 100). Eine Person mit IQ 90 zieht von Oklahoma nach Kalifornien. Resultat: Oklahomas Mittelwert steigt (80 → 82). Kaliforniens Mittelwert sinkt (100 → 99). Beide Mittelwerte haben sich 'verbessert' — aber niemand hat sich verändert.",
        "frage": "Wie entsteht dieser scheinbare Widerspruch?",
        "optionen": [
            {"text": "Recheneffekt: Der Abgewanderte lag über dem Quell- aber unter dem Zielmittelwert", "hinweis": "Arithmetisches Mittel reagiert auf Grenzwechsel"},
            {"text": "Fehler in der Berechnung — Mittelwerte können nicht gleichzeitig steigen", "hinweis": "Doch — wenn verschiedene Gruppen"},
            {"text": "IQ ist nicht additiv — Mittelwerte sind nicht vergleichbar", "hinweis": "IQ ist skaliert, Mittelwerte sind vergleichbar"},
            {"text": "Die Person verändert sich beim Umzug", "hinweis": "Im Beispiel nicht angenommen"},
        ],
        "loesung_text": "Recheneffekt: Die Person lag über dem Quell- und unter dem Zielmittelwert",
        "erklaerung": "<p>Wenn jemand einen Wert <em>zwischen</em> beiden Mittelwerten hat, hebt er den niedrigeren Mittelwert und senkt den höheren. Beide Mittelwerte 'verbessern' sich rein rechnerisch — ohne dass sich irgendjemand verändert hat. Das Phänomen taucht in Krebsstadien-Statistiken auf: Neue Diagnose-Technologien entdecken frühe Stadien, die dann in eine 'bessere' Kategorie eingestuft werden — und beide Kategorien zeigen höhere Überlebensraten.</p>",
        "kontext": "<p>Benannt nach dem Witz: 'Als die Okies nach Kalifornien auswanderten, stieg der Durchschnitts-IQ in beiden Staaten.' Das Phänomen erklärt zahlreiche medizinische Statistikfehler (Lead-Time Bias).</p>",
        "erkenntnis": "Aggregatstatistiken können irreführen, selbst wenn alle Einzeldaten stimmen. Immer fragen: Welche Gruppe wechselt zwischen den Kategorien?",
    },
    # ── Wahrscheinlichkeit ────────────────────────────────────────────────
    "kelly-kriterium": {
        "id": "kelly-kriterium", "name": "Das Kelly-Kriterium", "icon": "📊",
        "farbe": "violet", "kategorie": "Wahrscheinlichkeit",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Du spielst eine Wette: Du gewinnst mit 60 % Wahrscheinlichkeit. Der Gewinn ist doppelter Einsatz (Kurs 2:1, d.h. netto +100 % auf den Einsatz). Du verlierst mit 40 %. Dein Startkapital: 1000 €. Wie viel Prozent setzt du pro Runde ein, um langfristig maximal zu wachsen?",
        "frage": "Was empfiehlt das Kelly-Kriterium?",
        "optionen": [
            {"text": "100 % — alles einsetzen für maximale Rendite", "hinweis": "Ein Verlust → Bankrott"},
            {"text": "20 % — Kelly-Formel: f* = p − q/b", "hinweis": "f* = 0,6 − 0,4/1 = 0,2"},
            {"text": "50 % — faire Aufteilung", "hinweis": "Zu aggressiv"},
            {"text": "5 % — konservatives Risikomanagement", "hinweis": "Zu viel Potenzial ungenutzt"},
        ],
        "loesung_text": "20 % des Kapitals (Kelly-Formel)",
        "erklaerung": "<p>Kelly-Formel: f* = p − (1−p)/b, wobei p = Gewinnwahrscheinlichkeit, b = Nettogewinn pro Einheit. f* = 0,6 − 0,4/1 = 0,20. Diese Quote maximiert den langfristigen logarithmischen Kapitalzuwachs. Bei höherem Einsatz sinkt das langfristige Wachstum — trotz höherer Einzelrendite.</p>",
        "kontext": "<p>Ed Thorp wandte Kelly auf Blackjack (1960) und Aktienmärkte an. Viele Hedgefonds (Renaissance Technologies) nutzen Kelly-ähnliche Ansätze. Das Halbieren der Kelly-Quote ('Half Kelly') reduziert Volatilität erheblich bei nur geringem Renditeverlust.</p>",
        "erkenntnis": "Gier zerstört langfristiges Wachstum. Das Kelly-Kriterium zeigt: Es gibt einen optimalen Mut-Punkt — wer mehr riskiert, wächst langsamer.",
    },
    "martingale": {
        "id": "martingale", "name": "Das Martingale-System", "icon": "🎲",
        "farbe": "rose", "kategorie": "Wahrscheinlichkeit",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Strategie beim Roulette (Rot/Schwarz, 50/50 angenommen): Setze 1 €. Bei Verlust verdopple. Bei Gewinn setze wieder 1 €. Klingt narrensicher: Du hast immer einen kleinen Gewinn, sobald du gewinnst.",
        "frage": "Warum funktioniert das Martingale-System langfristig nicht?",
        "optionen": [
            {"text": "Bei einer langen Verlustserie übersteigt der benötigte Einsatz das Kapital oder das Tischlimit", "hinweis": "Geometrisches Wachstum"},
            {"text": "Roulette-Räder sind manipuliert", "hinweis": "Irrelevant für das mathematische Argument"},
            {"text": "Der Erwartungswert ist positiv — aber die Varianz ist zu hoch", "hinweis": "Erwartungswert ist tatsächlich leicht negativ beim echten Roulette"},
            {"text": "Das System funktioniert — Casinos verbieten es nur deshalb", "hinweis": "Casinos erlauben Martingale gerne"},
        ],
        "loesung_text": "Endliches Kapital + Tischlimits machen die Strategie bankrott",
        "erklaerung": "<p>Nach n Verlusten in Folge muss man 2ⁿ setzen. Nach 10 Verlusten: 1024 €. Das passiert mit Wahrscheinlichkeit (1/2)¹⁰ ≈ 0,1 % — selten, aber sicher irgendwann. Mit Tischlimit (z.B. 500 €) kann man nach 9 Verlusten nicht mehr verdoppeln und verliert alles. Ohne Tischlimit bräuchte man unendliches Kapital.</p>",
        "kontext": "<p>Das Martingale zeigt das Prinzip der <em>Gambler's Ruin</em>: Bei fairen Spielen mit endlichem Kapital gegen einen unendlichen Gegner (Casino) verliert man immer — nur die Geschwindigkeit variiert.</p>",
        "erkenntnis": "Eine Strategie, die 'immer' gewinnt, solange man unendlich Kapital hat, ist keine Strategie. Die Realität setzt Grenzen — und die Mathematik respektiert sie.",
    },
    "infinite-monkey": {
        "id": "infinite-monkey", "name": "Infinite Monkey Theorem", "icon": "🐒",
        "farbe": "amber", "kategorie": "Wahrscheinlichkeit",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Ein Affe tippt zufällig auf einer Schreibmaschine mit 26 Buchstaben + Leertaste (27 Tasten). Jede Taste wird mit gleicher Wahrscheinlichkeit gedrückt. Hamlet hat ca. 130.000 Zeichen.",
        "frage": "Wie viele Versuche bräuchte man im Erwartungswert, um Hamlet exakt zu tippen?",
        "optionen": [
            {"text": "27¹³⁰·⁰⁰⁰ — eine astronomisch große Zahl", "hinweis": "Größer als Atome im Universum"},
            {"text": "130.000 Versuche — ein Zeichen pro Versuch", "hinweis": "Unabhängige Zeichen, nicht sequentiell"},
            {"text": "Unendlich — es ist prinzipiell unmöglich", "hinweis": "Mit unendlich Zeit ist es sicher (Wahrscheinlichkeit 1)"},
            {"text": "1 Million — Daumenregel für zufällige Texte", "hinweis": "Stark unterschätzt"},
        ],
        "loesung_text": "27¹³⁰·⁰⁰⁰ Versuche — unvorstellbar groß, aber endlich",
        "erklaerung": "<p>Jedes Zeichen hat Wahrscheinlichkeit 1/27. Hamlet zu tippen hat Wahrscheinlichkeit (1/27)¹³⁰⁰⁰⁰. Der Erwartungswert = 27¹³⁰⁰⁰⁰ ≈ 10¹⁸⁶·⁰⁰⁰. Das Universum ist ~4,3 × 10¹⁷ Sekunden alt. Dennoch: Bei unendlich vielen Versuchen ist die Wahrscheinlichkeit 1.</p>",
        "kontext": "<p>Das Theorem gilt für jede endliche Zeichenkette: Gegeben unendliche Zeit, wird sie mit Wahrscheinlichkeit 1 erscheinen. Das ist kein Widerspruch zur Unpraktikabilität — unendliche Zeit ist eben unendlich.</p>",
        "erkenntnis": "Unwahrscheinlich ≠ unmöglich. Aber 'unendlich viel Zeit' ist eine Ressource, die das Universum nicht bietet. Theoretische Möglichkeit und praktische Erreichbarkeit sind sehr verschiedene Dinge.",
    },
    "drunkards-walk": {
        "id": "drunkards-walk", "name": "Der Drunkard's Walk", "icon": "🚶",
        "farbe": "teal", "kategorie": "Wahrscheinlichkeit",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Ein Betrunkener startet bei Position 0. Bei jedem Schritt geht er mit 50 % nach rechts (+1) oder links (−1). Nach 100 Schritten: Was ist der Erwartungswert seiner Position — und wie weit ist er im Durchschnitt vom Start entfernt?",
        "frage": "Wie groß ist die erwartete Entfernung vom Startpunkt nach n Schritten?",
        "optionen": [
            {"text": "0 — er endet im Erwartungswert wo er startete", "hinweis": "Erwartungswert der Position, ja — aber Entfernung?"},
            {"text": "√n — Standardabweichung des Random Walk", "hinweis": "Für n=100: √100 = 10"},
            {"text": "n/2 — er geht im Schnitt halb so weit wie er Schritte macht", "hinweis": "Zu viel"},
            {"text": "n — er geht so weit wie er Schritte macht", "hinweis": "Nur wenn er immer in eine Richtung geht"},
        ],
        "loesung_text": "√n — für n=100 Schritte: ca. 10 Einheiten vom Start",
        "erklaerung": "<p>Der Erwartungswert der <em>Position</em> ist 0 (symmetrisch). Die erwartete <em>Entfernung</em> wächst als √n. Das ist die Standardabweichung eines Binomialmodells: σ = √(n·p·q) = √(100·0,5·0,5) = 5. Genauer: E[|X|] ≈ √(2n/π) ≈ 8 für n=100.</p>",
        "kontext": "<p>Random Walks beschreiben Diffusion, Aktienkurse, Genomevolution und Proteinfaltung. Das √n-Wachstum erklärt, warum Diffusion so langsam ist: verdoppelt man die Zeit, geht man nur √2 ≈ 1,4× weiter.</p>",
        "erkenntnis": "Zufall akkumuliert langsam. Das √n-Gesetz hat fundamentale Konsequenzen für Physik, Biologie und Finanzen: Diversifikation reduziert Risiko proportional zu √n.",
    },
    "littlewoods-law": {
        "id": "littlewoods-law", "name": "Littlewoods Gesetz der Wunder", "icon": "✨",
        "farbe": "sky", "kategorie": "Wahrscheinlichkeit",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Mathematiker John Edensor Littlewood definierte ein 'Wunder' als Ereignis mit Wahrscheinlichkeit 1 zu einer Million. Er schätzte: Ein Mensch ist ~8 Stunden pro Tag 'aktiv bewusst' und erlebt pro Sekunde ein Ereignis.",
        "frage": "Wie oft pro Monat sollte ein 'Wunder' auftreten?",
        "optionen": [
            {"text": "Einmal pro Leben — sehr selten", "hinweis": "Wie viele Ereignisse erlebt man im Monat?"},
            {"text": "Einmal pro Monat — Littlewoods Ergebnis", "hinweis": "8h × 3600s × 30 Tage = 864.000 ≈ 10⁶"},
            {"text": "Einmal pro Jahr", "hinweis": "Zu selten"},
            {"text": "Täglich — Wunder sind normal", "hinweis": "Zu häufig"},
        ],
        "loesung_text": "Einmal pro Monat — Wunder sind statistisch normal",
        "erklaerung": "<p>8 Stunden × 3600 Sekunden × 30 Tage ≈ 864.000 ≈ 10⁶. Bei 10⁶ Ereignissen pro Monat und 'Wunder'-Wahrscheinlichkeit 1/10⁶ erwartet man im Schnitt <em>ein Wunder pro Monat</em>. Das Staunen über Koinzidenzen ist also fehlplatziert — wir sollten mehr überrascht sein, wenn keine auftreten.</p>",
        "kontext": "<p>Littlewood erklärt damit Erscheinungen wie 'Ich habe gerade an jemanden gedacht und er ruft an' oder 'Ich sah dasselbe Auto dreimal heute'. Diese Ereignisse erscheinen bedeutsam — sind aber statistisch erwartbar.</p>",
        "erkenntnis": "Was selten erscheint, passiert sicher — wenn man nur genug Gelegenheiten betrachtet. Wunder sind nicht Beweis für Übernatürliches, sondern für die Stärke großer Zahlen.",
    },
    # ── Kommunikation ─────────────────────────────────────────────────────
    "johari-fenster": {
        "id": "johari-fenster", "name": "Das Johari-Fenster", "icon": "🪟",
        "farbe": "cyan", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Das Johari-Fenster (Luft & Ingham, 1955) teilt Selbstwahrnehmung und Fremdwahrnehmung in 4 Felder: Arena (mir & anderen bekannt), Fassade (mir bekannt, anderen nicht), Blinder Fleck (anderen bekannt, mir nicht), Unbekanntes.",
        "frage": "Welches Feld nennt man den 'Blinden Fleck' — und wie verkleinert man ihn?",
        "optionen": [
            {"text": "Fassade — durch mehr Offenheit verkleinern", "hinweis": "Fassade ist das, was ich verberge"},
            {"text": "Blinder Fleck — durch aktives Einholen von Feedback verkleinern", "hinweis": "Andere sehen, was ich nicht sehe"},
            {"text": "Unbekanntes — durch Selbstreflexion verkleinern", "hinweis": "Das Unbekannte ist weder mir noch anderen bekannt"},
            {"text": "Arena — durch mehr Kommunikation vergrößern", "hinweis": "Die Arena soll wachsen — aber Blinder Fleck ist die Frage"},
        ],
        "loesung_text": "Blinder Fleck — durch aktives Einholen von Feedback verkleinern",
        "erklaerung": "<p>Der Blinde Fleck enthält Eigenschaften, die andere an mir wahrnehmen, ich selbst aber nicht. Nur durch Feedback von außen — ehrliches, spezifisches Feedback — kann ich ihn sehen. Das setzt Vertrauen voraus. Die Fassade verkleinert man durch Selbstöffnung (Disclosure).</p>",
        "kontext": "<p>Das Johari-Fenster wird in Führungstrainings, Therapie und Teamentwicklung eingesetzt. Ziel ist eine große Arena: Das, was alle wissen, schafft produktive Zusammenarbeit. Blinde Flecken in Führungskräften sind eine der häufigsten Quellen für Dysfunktion in Teams.</p>",
        "erkenntnis": "Selbstbild und Fremdbild klaffen oft auseinander. Wer Feedback nicht sucht, lebt in einer selbst konstruierten Version seiner Stärken und Schwächen.",
    },
    "vier-ohren-modell": {
        "id": "vier-ohren-modell", "name": "Das Vier-Ohren-Modell", "icon": "👂",
        "farbe": "violet", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Ein Mann fragt seine Frau beim Kochen: 'Was ist das Grüne in der Suppe?' Schulz von Thun (1981): Jede Nachricht enthält vier Seiten — Sachinhalt, Selbstoffenbarung, Beziehung, Appell.",
        "frage": "Auf welcher Ebene versteht die Frau die Frage möglicherweise — und was antwortet sie darauf?",
        "optionen": [
            {"text": "Sachebene: Sie erklärt, es ist Petersilie", "hinweis": "Sachlich korrekt"},
            {"text": "Beziehungsebene: Sie fühlt sich kritisiert und antwortet gereizt", "hinweis": "Häufige Fehldeutung"},
            {"text": "Appell: Sie versteht es als Aufforderung, weniger Grünes zu nehmen", "hinweis": "Appellebene"},
            {"text": "Alle drei sind mögliche Reaktionen", "hinweis": "Das ist der Kern des Modells"},
        ],
        "loesung_text": "Alle vier Ebenen sind gleichzeitig aktiv — die Deutung liegt beim Empfänger",
        "erklaerung": "<p>Sachinhalt: 'Was ist das Grüne?' Selbstoffenbarung: 'Ich kenne das nicht.' Beziehung: 'Du kochst etwas Fremdes.' Appell: 'Erklär es mir / lass es weg.' Der Sender meinte vielleicht nur die Sachebene — der Empfänger hört auf dem Beziehungsohr und reagiert gereizt. Kommunikationsprobleme entstehen oft durch Mismatch zwischen gesendeter und empfangener Ebene.</p>",
        "kontext": "<p>Schulz von Thuns Modell ist eines der meistzitierten Kommunikationsmodelle im deutschen Sprachraum. Kritik: Es ist deskriptiv, nicht präskriptiv — es erklärt Missverständnisse, löst sie aber nicht automatisch.</p>",
        "erkenntnis": "Jede Nachricht ist mehrdeutig. Wer auf dem falschen Ohr hört, antwortet auf eine Nachricht, die nie gesendet wurde. Klärung der Ebene ist der erste Schritt zur Verständigung.",
    },
    "stille-post": {
        "id": "stille-post", "name": "Stille Post im Business", "icon": "📡",
        "farbe": "rose", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Nachricht des CEO: 'Wir müssen effizienter werden.' Nach 5 Hierarchieebenen kommt an: 'Jeder muss Überstunden machen.' Was erklärt die Verzerrung?",
        "frage": "Welcher Mechanismus erzeugt die größte Verzerrung in Informationsketten?",
        "optionen": [
            {"text": "Absichtliche Manipulation durch einzelne Manager", "hinweis": "Kann passieren — aber was ist strukturell?"},
            {"text": "Jede Person interpretiert und ergänzt durch eigene Vorannahmen und Interessen", "hinweis": "Kognitive und motivationale Filter"},
            {"text": "Technische Übertragungsfehler in E-Mails", "hinweis": "Eher selten in dieser Weise"},
            {"text": "Zu viele Empfänger gleichzeitig — Signal-Rauschen-Problem", "hinweis": "Gilt für Broadcast, nicht Ketten"},
        ],
        "loesung_text": "Interpretation und Interessenfilter verzerren jede Weitergabe",
        "erklaerung": "<p>Jeder Bote deutet die Nachricht aus seiner Perspektive und gibt sie mit seinen Worten weiter. 'Effizienter' ist vage — ein Manager versteht 'Kostensenkung', ein anderer 'mehr Arbeit'. Amygdala-Aktivierung bei Bedrohungen (Jobsicherheit) verstärkt Fehlinterpretation. Hierarchische Kommunikation leidet strukturell unter diesem Filter-Effekt.</p>",
        "kontext": "<p>Lösungen: Direkte Kommunikation (Skip-Level-Meetings), schriftliche Präzisierung, Feedback-Schleifen ('Was hast du verstanden?'). Jeff Bezos' 'no PowerPoint'-Regel zielt darauf ab: Klare Texte zwingen zur Präzision.</p>",
        "erkenntnis": "Je mehr Ebenen, desto mehr Verzerrung. Klarheit an der Quelle reduziert Fehler exponentiell mehr als Korrektur am Ende.",
    },
    "eisbergmodell": {
        "id": "eisbergmodell", "name": "Das Eisbergmodell", "icon": "🧊",
        "farbe": "indigo", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "In einem Konflikt streiten zwei Kollegen darüber, wer das Besprechungszimmer nutzen darf. Sichtbar (20 %): die Positionen. Unsichtbar (80 %): Bedürfnisse, Gefühle, Werte, Vorannahmen.",
        "frage": "Was verbirgt sich typischerweise unter der Oberfläche?",
        "optionen": [
            {"text": "Nur andere Fakten, die noch nicht ausgetauscht wurden", "hinweis": "Fakten sind meist sichtbar"},
            {"text": "Bedürfnisse, Ängste, Werte, Vorannahmen und Beziehungsgeschichte", "hinweis": "Der Eisberg-Anteil"},
            {"text": "Reine Machtspiele — wer setzt sich durch", "hinweis": "Auch möglich, aber nicht vollständig"},
            {"text": "Missverständnisse über den Sachinhalt", "hinweis": "Auch möglich — aber meist tiefer"},
        ],
        "loesung_text": "Bedürfnisse, Ängste, Werte und Beziehungsgeschichte",
        "erklaerung": "<p>Das Eisberg-Modell (nach Freud, popularisiert in Kommunikation): Unter jeder Position stecken Interessen — darunter Bedürfnisse (Anerkennung, Autonomie, Sicherheit), Werte (Fairness, Respekt), Gefühle und alte Verletzungen. Konfliktlösung, die nur Positionen adressiert, löst nie wirklich.</p>",
        "kontext": "<p>Harvard-Konzept (Fisher/Ury): 'Separate people from the problem.' Erst wenn man tiefer gräbt und Bedürfnisse versteht, entstehen kreative Lösungen. Beide Kollegen brauchen vielleicht nur Anerkennung — das Zimmer ist nur das Symbol.</p>",
        "erkenntnis": "Konflikte werden selten durch das gelöst, worüber man streitet. Die eigentlichen Themen liegen unter der Oberfläche.",
    },
    "transaktionsanalyse": {
        "id": "transaktionsanalyse", "name": "Transaktionsanalyse", "icon": "🎭",
        "farbe": "amber", "kategorie": "Kommunikation",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Eric Berne (1964): Jeder Mensch spricht aus einem von drei Ich-Zuständen: Eltern-Ich (Normen, Werte, Regeln), Erwachsenen-Ich (sachlich, rational), Kind-Ich (spontan, emotional, abhängig). Ein Vorgesetzter sagt: 'Wann soll das eigentlich fertig werden?'",
        "frage": "Aus welchem Ich-Zustand spricht das — und welche Reaktion ist am produktivsten?",
        "optionen": [
            {"text": "Eltern-Ich (kritisch) → Erwachsenen-Ich antworten: 'Bis Freitag. Gibt es einen Engpass?'", "hinweis": "Parallele Transaktion bleibt sachlich"},
            {"text": "Kind-Ich (rebellisch) → Kind-Ich antworten: 'Ich weiß auch nicht!'", "hinweis": "Eskalation"},
            {"text": "Erwachsenen-Ich → Eltern-Ich antworten: 'Ich mache was ich kann'", "hinweis": "Gekreuzte Transaktion"},
            {"text": "Das Ich-Zustand-Konzept ist irrelevant — Inhalt zählt", "hinweis": "Aber wie man antwortet, beeinflusst den Verlauf"},
        ],
        "loesung_text": "Aus dem Erwachsenen-Ich antworten — sachlich und lösungsorientiert",
        "erklaerung": "<p>Die Frage kommt aus dem Eltern-Ich (kritisch/kontrollierend). Eine Eltern-Kind-Transaktion (Antwort: defensiv/rechtfertigend) ist am häufigsten — aber destruktiv. Die produktivste Reaktion: Erwachsenen-Ich → Erwachsenen-Ich. 'Bis Freitag — brauche ich noch Ressourcen für X.' Das deeskaliert und bleibt sachlich.</p>",
        "kontext": "<p>Berne unterscheidet komplementäre (parallele) und gekreuzte Transaktionen. Kommunikation läuft reibungslos, wenn beide auf derselben Ebene bleiben. Gekreuzte Transaktionen (z.B. Erwachsenen-Frage bekommt Kind-Antwort) erzeugen Frustration.</p>",
        "erkenntnis": "Wie wir kommunizieren, hängt nicht nur vom Inhalt ab, sondern davon, aus welchem inneren Zustand wir sprechen. Wer sich bewusst für das Erwachsenen-Ich entscheidet, bleibt handlungsfähig.",
    },
    "aktives-zuhoeren": {
        "id": "aktives-zuhoeren", "name": "Aktives Zuhören", "icon": "🎧",
        "farbe": "emerald", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Dein Verhandlungspartner sagt: 'Wir sind wirklich frustriert mit dem bisherigen Prozess. Das zieht sich schon viel zu lange hin.' Du willst aktiv zuhören.",
        "frage": "Welche Reaktion ist typisch für aktives Zuhören?",
        "optionen": [
            {"text": "'Das verstehe ich. Also: Unser Angebot ist…'", "hinweis": "Sofort weiter — kein Zuhören"},
            {"text": "'Ich höre, dass Ihr euch durch die Dauer unter Druck gesetzt fühlt. Was wäre für euch ein gutes Tempo?'", "hinweis": "Paraphrase + offene Frage"},
            {"text": "'Das ist aber nicht unser Problem — ihr habt auch Verzögerungen verursacht.'", "hinweis": "Defensiv — blockiert Vertrauen"},
            {"text": "'Verstanden.' (Kurze Pause, dann weiter.)", "hinweis": "Zu kurz — keine Vertiefung"},
        ],
        "loesung_text": "Paraphrasieren + offene Folgefrage",
        "erklaerung": "<p>Aktives Zuhören hat drei Elemente: 1) Paraphrase (das Gehörte in eigenen Worten wiedergeben), 2) Spiegeln (Gefühle benennen), 3) Vertiefen (offene Frage). Das signalisiert: Ich habe verstanden UND ich will mehr verstehen. Das baut Vertrauen und öffnet Informationen, die bei Gegenwehr verschlossen blieben.</p>",
        "kontext": "<p>FBI-Verhandlungsführer Chris Voss (Never Split the Difference): Die meisten Verhandler planen ihre nächste Aussage, während der andere spricht. Aktives Zuhören ist die mächtigste Technik — und die seltenste.</p>",
        "erkenntnis": "Wer zuhört, gewinnt Informationen. Wer spricht, gibt sie ab. Aktives Zuhören ist keine Nettigkeit — es ist strategisch.",
    },
    "elevator-pitch": {
        "id": "elevator-pitch", "name": "Der Elevator Pitch", "icon": "🛗",
        "farbe": "sky", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Du teilst einen Aufzug mit einem potenziellen Investor. Du hast 60 Sekunden. Deine Idee: Eine App, die Lebensmittelreste mit hungrigen Nachbarn verbindet.",
        "frage": "Was gehört in einen guten Elevator Pitch — und was nicht?",
        "optionen": [
            {"text": "Problem, Lösung, Zielgruppe, Call-to-Action — ohne technische Details", "hinweis": "Kern-Struktur"},
            {"text": "Technologie-Stack, Datenbankarchitektur, API-Spezifikationen", "hinweis": "Zu früh, zu spezifisch"},
            {"text": "Finanzprognosen für 5 Jahre und Break-Even-Analyse", "hinweis": "Zu früh für 60 Sekunden"},
            {"text": "Eine ausführliche Geschichte der Entstehungsidee", "hinweis": "Interessant — aber Investor will Problem/Lösung zuerst"},
        ],
        "loesung_text": "Problem → Lösung → Zielgruppe → Call-to-Action",
        "erklaerung": "<p>Struktur: 'X % der Haushalte werfen wöchentlich Y kg Essen weg [Problem]. Unsere App verbindet sie in 2 Minuten mit hungrigen Nachbarn im Umkreis [Lösung]. Wir richten uns an umweltbewusste Stadtbewohner [Zielgruppe]. Dürfte ich Ihnen in 15 Minuten eine Demo zeigen? [CTA].' Keine Zahlen ohne Kontext, kein Jargon, kein Technologie-Detail.</p>",
        "kontext": "<p>Der Pitch ist nicht das Ziel — er öffnet die Tür. Das Ziel ist ein Follow-up-Gespräch. Deshalb ist der CTA entscheidend: nicht 'Investieren Sie 1 Mio. €', sondern 'Dürfen wir uns treffen?'</p>",
        "erkenntnis": "Radikale Verdichtung erfordert Entscheidung: Was weglassen? Wer sein Kernwertversprechen nicht in 60 Sekunden kommunizieren kann, hat es selbst nicht verstanden.",
    },
    "nonverbale-mimikry": {
        "id": "nonverbale-mimikry", "name": "Nonverbale Mimikry", "icon": "🪞",
        "farbe": "teal", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "In einem Experiment (van Baaren et al., 2003) spiegelten Kellner die Bestellungen der Gäste entweder wörtlich zurück oder paraphrasierten sie. Die Ergebnis: Die spiegelnden Kellner erhielten deutlich höhere Trinkgelder.",
        "frage": "Warum erhöht Mimikry (Spiegeln von Sprache und Gestik) die Sympathie?",
        "optionen": [
            {"text": "Weil Menschen sich durch Nachahmung kontrolliert fühlen", "hinweis": "Gegenteiliger Effekt"},
            {"text": "Weil Mimikry Ähnlichkeit signalisiert — und wir Menschen mögen, die uns ähneln", "hinweis": "Chameleon-Effekt"},
            {"text": "Weil es Kompetenz demonstriert — man merkt sich die Details", "hinweis": "Kompetenz allein erklärt nicht Sympathie"},
            {"text": "Weil es Aufmerksamkeit signalisiert — man hat zugehört", "hinweis": "Teilweise richtig — aber tiefer?"},
        ],
        "loesung_text": "Mimikry signalisiert Zugehörigkeit und Ähnlichkeit (Chameleon-Effekt)",
        "erklaerung": "<p>Chartrand & Bargh (1999): Der Chameleon-Effekt — unbewusstes Spiegeln von Gesten, Körperhaltung, Sprache — fördert Sympathie und Kooperation. Evolutionär: Ähnlichkeit = gleiche Gruppe = Sicherheit. Bewusstes, respektvolles Spiegeln wirkt genauso. Übertriebenes oder offensichtliches Imitieren wirkt manipulativ.</p>",
        "kontext": "<p>FBI-Verhandler und gute Verkäufer setzen das ein. Auch in der Therapie: Therapeuten, die mehr spiegeln, werden als verständnisvoller erlebt. Wichtig: nur subtil und mit echtem Interesse — aufgesetztes Spiegeln wirkt irritierend.</p>",
        "erkenntnis": "Sympathie entsteht durch wahrgenommene Ähnlichkeit. Wer Gemeinsamkeiten signalisiert — sprachlich und körperlich — baut Vertrauen schneller auf.",
    },
    "feedback-sandwich": {
        "id": "feedback-sandwich", "name": "Das Feedback-Sandwich", "icon": "🥪",
        "farbe": "pink", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Führungskraft zu Mitarbeiter: 'Du hast das Projekt toll geleitet! Leider waren die Deadlines nicht eingehalten. Aber dein Engagement war wirklich beeindruckend!' Das ist das klassische Feedback-Sandwich: Positiv–Kritik–Positiv.",
        "frage": "Warum verfehlt das Feedback-Sandwich häufig sein Ziel?",
        "optionen": [
            {"text": "Kritik zwischen Lob geht unter — der Empfänger erinnert sich nur an das Lob", "hinweis": "Sandwich-Effekt"},
            {"text": "Menschen mögen kein Lob von Vorgesetzten", "hinweis": "Unplausibel"},
            {"text": "Das Lob klingt unecht, weil es nur als Vorbereitung wirkt", "hinweis": "Auch ein Problem"},
            {"text": "Sowohl A als auch C — und außerdem wird die Kritik abgeschwächt", "hinweis": "Mehrere Probleme gleichzeitig"},
        ],
        "loesung_text": "Kritik geht unter (Sandwich-Effekt) und Lob wirkt aufgesetzt",
        "erklaerung": "<p>Probleme: 1) Das mittlere Element (Kritik) wird psychologisch abgepuffert — Empfänger fokussiert auf Lob. 2) Das anfängliche Lob wird als manipulative Vorbereitung wahrgenommen. 3) Die eigentliche Botschaft wird unklar. Besser: Direktes, spezifisches Feedback mit klarem Kontext: 'Die Deadlines wurden nicht eingehalten. Das hat X Folgen. Was hat das verhindert, und wie lösen wir das?'</p>",
        "kontext": "<p>Radikale Candor (Kim Scott): Gutes Feedback ist gleichzeitig fürsorglich und direkt. Weder aggressive Konfrontation noch schwammige Verpackung — sondern klare Botschaft mit Respekt.</p>",
        "erkenntnis": "Verpacking von Kritik schwächt sie. Direktheit, kombiniert mit echtem Interesse am Wachstum des Gegenübers, ist effektiver als jede Struktur.",
    },
    "empathie-mapping": {
        "id": "empathie-mapping", "name": "Empathie-Mapping", "icon": "🗺️",
        "farbe": "orange", "kategorie": "Kommunikation",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Vor einer wichtigen Verhandlung erstellst du ein Empathy Map für dein Gegenüber. Das Tool aus dem Design Thinking fragt: Was denkt und fühlt er? Was sieht er? Was hört er? Was sagt und tut er? Was sind seine Pains und Gains?",
        "frage": "Wozu dient ein Empathy Map in einer Verhandlung?",
        "optionen": [
            {"text": "Um die Schwächen des Gegners zu finden und auszunutzen", "hinweis": "Falsch verstandene Empathie"},
            {"text": "Um Interessen, Ängste und Motivationen des Gegenübers zu antizipieren — für kreative Lösungen", "hinweis": "Perspektivwechsel als Vorbereitung"},
            {"text": "Um das eigene Angebot besser zu präsentieren", "hinweis": "Zu selbstbezogen"},
            {"text": "Um zu entscheiden, ob man überhaupt verhandeln soll", "hinweis": "Zu früh — aber auch ein Nutzen"},
        ],
        "loesung_text": "Interessen und Motivationen des Gegenübers antizipieren",
        "erklaerung": "<p>Wer die Perspektive seines Verhandlungspartners einnehmen kann, findet Lösungen, die beide Seiten zufriedenstellen. Das Empathy Map hilft, aus der eigenen Perspektive herauszutreten und gezielt zu fragen: Was will er wirklich? Was fürchtet er? Was erzählt er sich selbst über diese Verhandlung?</p>",
        "kontext": "<p>Harvard-Konzept: Interests, not positions. Das Empathy Map ist ein Werkzeug, um Interessen systematisch zu erforschen — bevor man in die Verhandlung geht. Je besser man den Anderen versteht, desto mehr kreative Optionen sieht man.</p>",
        "erkenntnis": "Empathie ist kein Soft Skill — sie ist strategisch. Wer den Anderen besser versteht als dieser sich selbst, hat strukturellen Vorteil.",
    },
    # ── Rhetorik ──────────────────────────────────────────────────────────
    "sokratische-methode": {
        "id": "sokratische-methode", "name": "Die Sokratische Methode", "icon": "🏛️",
        "farbe": "violet", "kategorie": "Rhetorik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Sokrates behauptete nie, etwas zu wissen. Stattdessen stellte er Fragen, bis sein Gesprächspartner Widersprüche in der eigenen Argumentation erkannte. Das nennt man Elenktik (Widerlegungsgespräch).",
        "frage": "Was ist der Kern der Sokratischen Methode?",
        "optionen": [
            {"text": "Jemanden durch Fragen zu demontieren — bis er kapituliert", "hinweis": "Ergebnis, aber nicht Ziel"},
            {"text": "Durch gezielte Fragen helfen, eigene Widersprüche zu erkennen und zur Wahrheit zu gelangen", "hinweis": "Maieutik — die Hebammen-Kunst"},
            {"text": "Die eigene These durch indirekte Fragen durchzusetzen", "hinweis": "Manipulation, nicht Philosophie"},
            {"text": "Fragen stellen, um Zeit zu gewinnen", "hinweis": "Taktik, aber nicht das Prinzip"},
        ],
        "loesung_text": "Durch Fragen zur Selbsterkenntnis führen (Maieutik)",
        "erklaerung": "<p>Sokrates nannte sich eine 'Hebamme des Geistes' (Maieutik): Er half, bereits vorhandenes Wissen zur Geburt zu verhelfen. Die Methode: Ausgehend von der These des Anderen werden durch Fragen Implikationen aufgezeigt, die zur These im Widerspruch stehen — bis der Andere seine Position überdenkt oder verfeinert.</p>",
        "kontext": "<p>Die Methode wird in Recht, Philosophie und Coaching eingesetzt. Anwälte beim Kreuzverhör, Coaches bei der Reflexion, Lehrer bei der aktiven Wissenskonstruktion — alle nutzen Varianten. Vorteil: Erkenntnisse, zu denen man selbst kommt, wirken stärker als fremde Argumente.</p>",
        "erkenntnis": "Fragen sind oft überzeugender als Aussagen. Wer den Anderen zu seiner eigenen Erkenntnis führt, überzeugt nachhaltiger als wer eine Wahrheit verkündet.",
    },
    "ethos-pathos-logos": {
        "id": "ethos-pathos-logos", "name": "Ethos, Pathos, Logos", "icon": "⚖️",
        "farbe": "rose", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Aristoteles (Rhetorik, 350 v. Chr.) identifizierte drei Überzeugungsmittel: Ethos (Charakter/Glaubwürdigkeit des Sprechers), Pathos (Emotionen des Publikums), Logos (Logik/Beweise).",
        "frage": "Eine Studie zeigt: Bei Finanzentscheidungen überzeugt was am meisten?",
        "optionen": [
            {"text": "Logos — Zahlen und Fakten sind bei Finanzthemen entscheidend", "hinweis": "Rational — aber ist das Menschen?"},
            {"text": "Ethos — Vertrauen in den Sprecher ist der stärkste Hebel", "hinweis": "Cialdini: Autorität und Vertrauen"},
            {"text": "Pathos — Geschichten von Verlust und Gewinn wirken emotional", "hinweis": "Auch stark — aber was dominiert?"},
            {"text": "Alle drei gleich — situationsabhängig", "hinweis": "Richtig in der Tendenz — aber es gibt Präferenzen"},
        ],
        "loesung_text": "Ethos dominiert: Vertrauen in den Sprecher ist der stärkste Faktor",
        "erklaerung": "<p>Studien (Cialdini, Ariely) zeigen: In unsicheren Situationen (wie Finanzentscheidungen) übertragen Menschen ihre Entscheidung auf Autoritäten. Ethos (Wer spricht?) ist dabei stärker als Logos (Was sagt er?). Das erklärt, warum Berater vor allem ihre Credibility aufbauen müssen — und dann erst ihre Argumente.</p>",
        "kontext": "<p>In der Praxis werden alle drei kombiniert: Ethos baut Vertrauen, Pathos erzeugt Motivation, Logos liefert die Rechtfertigung. Die Reihenfolge zählt: Ohne Ethos werden Logos und Pathos als manipulativ erlebt.</p>",
        "erkenntnis": "Zuerst die Person, dann das Argument. Wer nicht glaubwürdig ist, kann das stärkste Argument vortragen — und wird ignoriert.",
    },
    "steel-manning": {
        "id": "steel-manning", "name": "Steel-Manning", "icon": "🛡️",
        "farbe": "indigo", "kategorie": "Rhetorik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Das Gegenteil des Strohmann-Arguments: Statt die schwächste Version der gegnerischen Position anzugreifen, formulierst du die stärkste mögliche Version — und begegnest ihr trotzdem.",
        "frage": "Warum ist Steel-Manning strategisch vorteilhafter als Strohmann-Argumente?",
        "optionen": [
            {"text": "Weil es freundlicher ist und den Gegner nicht verletzt", "hinweis": "Nicht strategisch gedacht"},
            {"text": "Weil ein widergelegtes starkes Argument überzeugender ist als ein widerlegtes schwaches", "hinweis": "Rhetorische Stärke durch Glaubwürdigkeit"},
            {"text": "Weil man dadurch die eigene Argumentation verbessert", "hinweis": "Auch richtig — aber was ist der rhetorische Vorteil?"},
            {"text": "Sowohl B als auch C — doppelter Nutzen", "hinweis": "Beide stimmen"},
        ],
        "loesung_text": "Stärker wirkendes Argument überzeugt mehr, und die eigene Position wird robuster",
        "erklaerung": "<p>Wer den stärksten gegnerischen Einwand adressiert, zeigt Publikum und Gegner: Ich habe alle Aspekte ernst genommen. Das erhöht die Glaubwürdigkeit (Ethos) und macht die eigene Position stabiler. Außerdem: Wenn der Andere sieht, dass man seine beste Argumentation ernst nimmt, entsteht Respekt.</p>",
        "kontext": "<p>In Wissenschaft und Philosophie ist Steel-Manning Standard: Charitably interpret ('principle of charity'). In politischen Debatten ist es selten — was erklärt, warum politische Debatten wenig überzeugen und viel polarisieren.</p>",
        "erkenntnis": "Echte intellektuelle Stärke zeigt sich daran, wie stark die Argumente sind, gegen die man antritt — nicht wie schwach man die gegnerische Position darstellt.",
    },
    "slippery-slope": {
        "id": "slippery-slope", "name": "Slippery Slope", "icon": "🛷",
        "farbe": "amber", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "'Wenn wir Homeoffice erlauben, kommen Mitarbeiter bald gar nicht mehr ins Büro, dann verlieren wir die Unternehmenskultur, dann schrumpft die Firma, dann gehen wir Bankrott.' Das ist ein Slippery-Slope-Argument.",
        "frage": "Wann ist ein Slippery-Slope-Argument legitim — und wann ein Trugschluss?",
        "optionen": [
            {"text": "Immer ein Trugschluss — die Zukunft ist unvorhersehbar", "hinweis": "Zu absolut"},
            {"text": "Legitim, wenn jeder Schritt kausal belegt ist; Trugschluss, wenn Schritte unbegründet sind", "hinweis": "Empirische Frage"},
            {"text": "Immer legitim — man kann nie zu vorsichtig sein", "hinweis": "Präventionsprinzip ≠ logisches Argument"},
            {"text": "Legitim bei gesellschaftlichen Themen, Trugschluss bei persönlichen", "hinweis": "Keine valide Unterscheidung"},
        ],
        "loesung_text": "Legitim wenn kausale Kette belegt; Trugschluss ohne Begründung",
        "erklaerung": "<p>Das Slippery-Slope-Argument ist nicht automatisch falsch — manchmal gibt es empirische Evidenz für eine Kausalkette (z.B. erste Zigarette → erhöhte Suchtwahrscheinlichkeit). Es wird zum Trugschluss, wenn die Verbindung zwischen Schritten nicht begründet wird oder wenn alternative Stoppmechanismen ignoriert werden.</p>",
        "kontext": "<p>Klassische Trugschluss-Version: 'Wenn wir A erlauben, dann irgendwann Z' ohne jeden Schritt zu belegen. Gegenargument: 'Zeig die Kausalkette.' Das ist die Standarderwiderung auf unbegründete Slippery-Slope-Argumente.</p>",
        "erkenntnis": "Ein Argument, das Konsequenzen zeigt, ist wertvoll — wenn die Konsequenzen kausal begründet sind. 'Vielleicht' ist keine Kausalkette.",
    },
    "red-herring": {
        "id": "red-herring", "name": "Red Herring", "icon": "🐟",
        "farbe": "teal", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Im Parlament: Politiker A kritisiert hohe Rüstungsausgaben. Politiker B antwortet: 'Die Opposition hat in ihrer Regierungszeit mehr Schulden gemacht als je zuvor.' Das ist ein Red Herring — ein Ablenkungsmanöver.",
        "frage": "Wie erkennt und widerlegt man ein Red-Herring-Argument?",
        "optionen": [
            {"text": "Auf das neue Thema eingehen — vielleicht ist es wichtiger", "hinweis": "Damit fällt man auf das Manöver herein"},
            {"text": "Das ursprüngliche Thema explizit benennen und zurückführen", "hinweis": "Thema-Tracking"},
            {"text": "Den Sprecher persönlich angreifen", "hinweis": "Ad-Hominem-Gegenzug — auch ein Trugschluss"},
            {"text": "Zustimmen und weitermachen", "hinweis": "Löst das Problem nicht"},
        ],
        "loesung_text": "Benennen + zum Original-Thema zurückführen",
        "erklaerung": "<p>Reaktion: 'Das mag ein separates Thema sein — ich stehe bereit, darüber zu sprechen. Aber zur ursprünglichen Frage: Wie rechtfertigen Sie die aktuellen Rüstungsausgaben?' Drei Schritte: 1) Das Ablenkungsmanöver anerkennen ohne zu verurteilen, 2) zum Kernthema zurückführen, 3) die Frage wiederholen.</p>",
        "kontext": "<p>Red Herrings sind in politischen Debatten, Verhören und Verkaufsgesprächen häufig. Der Begriff stammt angeblich von getrockneten Heringen, die man über Jagdpfade zog, um Hunde abzulenken. Das Erkennen erfordert Thema-Bewusstsein: Was wurde gefragt? Was wurde beantwortet?</p>",
        "erkenntnis": "Wer das Thema kontrolliert, kontrolliert das Gespräch. Red Herrings sind Versuche, diese Kontrolle zu übernehmen. Rückführen ist die Gegenstrategie.",
    },
    "syllogismen-check": {
        "id": "syllogismen-check", "name": "Syllogismen-Check", "icon": "🔗",
        "farbe": "sky", "kategorie": "Rhetorik",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Prämisse 1: Alle Politiker lügen. Prämisse 2: Müller ist Politiker. Schlussfolgerung: Müller lügt. Der Syllogismus ist logisch gültig. Aber ist er wahr?",
        "frage": "Was ist der Unterschied zwischen einem gültigen und einem wahren Syllogismus?",
        "optionen": [
            {"text": "Gültig = logisch korrekte Form; Wahr = Prämissen sind faktisch wahr", "hinweis": "Formal vs. inhaltlich"},
            {"text": "Gültig = kurz; Wahr = ausführlich", "hinweis": "Kein logisches Kriterium"},
            {"text": "Ein gültiger Syllogismus ist immer auch wahr", "hinweis": "'Alle Vögel fliegen. Pinguine sind Vögel. Pinguine fliegen.' — gültig, aber falsch"},
            {"text": "Wahrheit und Gültigkeit sind dasselbe in der Logik", "hinweis": "Wichtige Unterscheidung in der Logik"},
        ],
        "loesung_text": "Gültig = korrekte Form; Wahr = wahre Prämissen + gültige Form (= sound)",
        "erklaerung": "<p>Gültigkeit (validity): Wenn die Prämissen wahr wären, folgt die Konklusion notwendig. Solidheit (soundness): Die Prämissen sind tatsächlich wahr UND die Form ist gültig. 'Alle Politiker lügen' ist eine empirisch falsche Prämisse — der Syllogismus ist gültig, aber nicht solide.</p>",
        "kontext": "<p>In der Praxis: Prüfe immer die Prämissen, nicht nur die Logik. Viele überzeugende Argumente sind formal korrekt, aber auf falschen Annahmen gebaut. Die häufigste Schachstelle: ungeprüfte Allaussagen (alle, immer, nie).</p>",
        "erkenntnis": "Ein logisch korrektes Argument kann trotzdem falsch sein — wenn seine Ausgangspunkte nicht stimmen. Prämissen prüfen ist genauso wichtig wie Logik prüfen.",
    },
    "fallacy-hunting": {
        "id": "fallacy-hunting", "name": "Fallacy Hunting", "icon": "🎯",
        "farbe": "orange", "kategorie": "Rhetorik",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Identifiziere den Trugschluss: 'Professor Koch ist gegen Impfpflicht — aber er ist ja selbst geimpft! Man kann ihm nicht vertrauen.' Das Argument greift die Person an, nicht ihr Argument.",
        "frage": "Welcher Trugschluss wird hier verwendet?",
        "optionen": [
            {"text": "Strohmann — sein Argument wird verzerrt dargestellt", "hinweis": "Sein Argument wird gar nicht erwähnt"},
            {"text": "Ad Hominem — die Person wird angegriffen statt ihr Argument", "hinweis": "'Gegen die Person'"},
            {"text": "False Dilemma — nur zwei Optionen werden präsentiert", "hinweis": "Kein Entweder-Oder hier"},
            {"text": "Appeal to Authority — eine Autorität wird zitiert", "hinweis": "Eher das Gegenteil"},
        ],
        "loesung_text": "Ad Hominem — Angriff auf die Person statt auf das Argument",
        "erklaerung": "<p>Ad Hominem (lat. 'gegen den Menschen'): Man widerlegt nicht das Argument, sondern versucht, den Sprecher zu diskreditieren. Selbst wenn Koch geimpft ist, sagt das nichts darüber aus, ob seine Argumente gegen Impfpflicht stichhaltig sind. Die Glaubwürdigkeit eines Sprechers ist relevant — aber sie ersetzt nicht die Auseinandersetzung mit dem Inhalt.</p>",
        "kontext": "<p>Weitere häufige Trugschlüsse: Strohmann (schwächere Version angreifen), False Dilemma (nur 2 Optionen), Appeal to Nature ('natürlich' = gut), Bandwagon ('alle machen es'), Circular Reasoning (Prämisse = Konklusion).</p>",
        "erkenntnis": "Trugschlüsse identifizieren zu können schützt vor Manipulation — und verhindert, dass man selbst welche begeht. Das Werkzeug ist kritisches Denken, keine Arroganz.",
    },
    "regel-der-drei": {
        "id": "regel-der-drei", "name": "Die Regel der Drei", "icon": "3️⃣",
        "farbe": "pink", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "'Veni, vidi, vici.' (Cäsar) — 'Life, Liberty, and the Pursuit of Happiness.' — 'Blut, Schweiß und Tränen.' Dreiergruppen tauchen in Reden, Slogans und Literatur überproportional häufig auf.",
        "frage": "Warum sind Dreierstrukturen so wirkungsvoll?",
        "optionen": [
            {"text": "Weil drei die minimale Zahl für ein Muster ist — Vollständigkeit ohne Überlastung", "hinweis": "Muster-Erkennung + kognitive Last"},
            {"text": "Weil drei eine heilige Zahl ist — religiöser Ursprung", "hinweis": "Kulturell bedingt — aber nicht die Erklärung"},
            {"text": "Weil Sätze mit drei Elementen grammatikalisch einfacher sind", "hinweis": "Nicht systematisch belegt"},
            {"text": "Weil das Kurzzeitgedächtnis genau 3 Einheiten speichern kann", "hinweis": "Kurzzeitgedächtnis speichert 7±2 Einheiten"},
        ],
        "loesung_text": "Drei etabliert ein Muster mit minimalem kognitivem Aufwand",
        "erklaerung": "<p>Zwei Elemente fühlen sich unvollständig an ('entweder…oder'). Vier sind zu viele für eine einprägsame Einheit. Drei ist das Minimum für ein wahrnehmbares Muster — das Gehirn füllt die Erwartung und findet Abschluss. Außerdem: Der Rhythmus dreier Einheiten erzeugt einen natürlichen Sprechfluss (Kolon-Struktur in der Antike).</p>",
        "kontext": "<p>Storytelling: Setup, Konflikt, Auflösung. Verkauf: Problem, Lösung, Beweis. Präsentation: drei Hauptpunkte. Das Prinzip ist universell — weil es kognitiv und rhythmisch optimal ist.</p>",
        "erkenntnis": "Struktur macht Botschaften einprägsam. Die Drei ist das eleganteste Strukturprinzip der Rhetorik — nicht aus Tradition, sondern aus Kognitionswissenschaft.",
    },
    "euphemismus-jagd": {
        "id": "euphemismus-jagd", "name": "Euphemismus-Jagd", "icon": "🎭",
        "farbe": "emerald", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Unternehmens-Pressemitteilung: 'Im Zuge unserer strategischen Neuausrichtung werden wir strukturelle Anpassungen vornehmen, um unsere Kosteneffizienz zu optimieren und die langfristige Wettbewerbsfähigkeit zu sichern.'",
        "frage": "Was bedeutet diese Aussage im Klartext?",
        "optionen": [
            {"text": "Das Unternehmen eröffnet neue Märkte", "hinweis": "Gegenteil"},
            {"text": "Mitarbeiter werden entlassen", "hinweis": "'Strukturelle Anpassungen' = Stellenabbau"},
            {"text": "Ein Merger wird vorbereitet", "hinweis": "Möglich — aber nicht das Kernbotschaft hier"},
            {"text": "Das Management wird ausgetauscht", "hinweis": "Auch nicht aus dem Text"},
        ],
        "loesung_text": "Mitarbeiter werden entlassen (Stellenabbau)",
        "erklaerung": "<p>Euphemismus-Kette: 'Neuausrichtung' = Kurswechsel wegen Misserfolg. 'Strukturelle Anpassungen' = Entlassungen. 'Kosteneffizienz optimieren' = Kosten senken = Personal abbauen. Euphemismen verringern emotionale Reaktion — auf Kosten der Klarheit und des Respekts gegenüber Betroffenen.</p>",
        "kontext": "<p>George Orwell (1946): 'Politics and the English Language' — Sprache wird absichtlich vage, um Grausamkeiten zu verbergen. Politisches Beispiel: 'Kollateralschäden' = zivile Todesopfer. Das Entlarven von Euphemismen ist eine Bürgerpflicht.</p>",
        "erkenntnis": "Wer Sprache kontrolliert, kontrolliert Wahrnehmung. Klarheit ist eine Form der Integrität — und Euphemismen sind oft eine Form der Feigheit.",
    },
    "anapher-training": {
        "id": "anapher-training", "name": "Anapher-Training", "icon": "🔁",
        "farbe": "cyan", "kategorie": "Rhetorik",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "'We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields…' (Churchill, 1940). 'I have a dream… I have a dream… I have a dream…' (King, 1963). Beide nutzen Wiederholung am Satzbeginn.",
        "frage": "Welches rhetorische Stilmittel ist das — und warum wirkt es so stark?",
        "optionen": [
            {"text": "Epiphora — Wiederholung am Satzende", "hinweis": "Das wäre am Ende, nicht am Anfang"},
            {"text": "Anapher — Wiederholung am Satzbeginn — erzeugt Rhythmus und emotionale Verdichtung", "hinweis": "Griech. anapherein = hinaufbringen"},
            {"text": "Chiasmus — Umkehr der Wortfolge", "hinweis": "z.B. 'Frage nicht was dein Land tut — frage was du tust'"},
            {"text": "Litotes — Untertreibung zur Verstärkung", "hinweis": "z.B. 'nicht schlecht' für 'gut'"},
        ],
        "loesung_text": "Anapher — Wiederholung am Satzbeginn",
        "erklaerung": "<p>Die Anapher (griech. 'hinaufbringen') wiederholt ein Wort oder eine Phrase zu Beginn aufeinanderfolgender Sätze. Wirkung: 1) Rhythmus und Musikalität, 2) emotionale Verdichtung durch Akkumulation, 3) Einprägsamkeit (Gedächtnis). Churchill und King nutzten sie bewusst für maximale emotionale Wirkung in Krisenreden.</p>",
        "kontext": "<p>Andere Anaphern: 'Wir werden uns nicht beugen, wir werden nicht schweigen, wir werden nicht aufgeben.' In der Werbung: 'Because you're worth it. Because you matter. Because you deserve it.' Die Wiederholung erzeugt eine Art Hypnose.</p>",
        "erkenntnis": "Struktur ist Emotion. Wiederholung ist kein Mangel an Variabilität — sie ist ein bewusstes Mittel zur Verdichtung von Bedeutung und Wirkung.",
    },
    # ── Verhandlung ───────────────────────────────────────────────────────
    "zopa": {
        "id": "zopa", "name": "ZOPA – Die Einigungszone", "icon": "🎯",
        "farbe": "violet", "kategorie": "Verhandlung",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Verkäufer will mindestens 85.000 € (Reservationspreis). Käufer ist bereit, maximal 100.000 € zu zahlen. ZOPA = Zone of Possible Agreement.",
        "frage": "Was ist die ZOPA in diesem Beispiel — und was, wenn der Verkäufer 110.000 € will?",
        "optionen": [
            {"text": "ZOPA: 85.000–100.000 €. Bei 110.000 €: keine ZOPA — kein Deal möglich", "hinweis": "ZOPA = Überschneidung der Reservationspreise"},
            {"text": "ZOPA: 92.500 € (Mittelpunkt). Bei 110.000 €: 105.000 €", "hinweis": "ZOPA ist ein Bereich, kein Punkt"},
            {"text": "ZOPA: 100.000 €. Bei 110.000 €: 110.000 € (Käufer muss nachgeben)", "hinweis": "Käufer überschreitet Limit"},
            {"text": "Es gibt keine ZOPA — Verhandlungspreise sind nie vorhersagbar", "hinweis": "ZOPA ist konzeptionell definierbar"},
        ],
        "loesung_text": "ZOPA: 85.000–100.000 €. Bei 110.000 € ist die ZOPA leer",
        "erklaerung": "<p>ZOPA = Bereich zwischen den Reservationspreisen. Hier: jeder Preis zwischen 85.000 und 100.000 € ist für beide akzeptabel — der Verhandlungsspielraum. Bei Verkäufer-Minimum 110.000 € und Käufer-Maximum 100.000 €: Kein Überschneidungsbereich → kein rationaler Deal ohne Werteänderung (z.B. Zahlungsmodalitäten, Zusatzleistungen).</p>",
        "kontext": "<p>Interessant: Beide Parteien kennen selten den Reservationspreis des Anderen. Anker-Taktiken, Informationsasymmetrie und Drohungen versuchen, die wahrgenommene ZOPA zu verschieben. Wer seinen eigenen Reservationspreis kennt (BATNA), verhandelt stabiler.</p>",
        "erkenntnis": "Wer nicht weiß, wo seine ZOPA liegt, kann sie ungewollt verlassen. BATNA und Reservationspreis kennen ist die Grundlage jeder Verhandlung.",
    },
    "logrolling": {
        "id": "logrolling", "name": "Logrolling", "icon": "🔄",
        "farbe": "rose", "kategorie": "Verhandlung",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Du verhandelst ein Arbeitsangebot. Du willst hauptsächlich mehr Gehalt. Dein Chef will Flexibilität (Bereitschaft zu Wochenendarbeit bei Bedarf). Beide Seiten haben unterschiedliche Prioritäten.",
        "frage": "Was ist Logrolling — und warum schafft es Mehrwert?",
        "optionen": [
            {"text": "Gegenseitiges Nachgeben — du gibst auf X, er gibt auf Y", "hinweis": "Korrekt — aber warum Mehrwert?"},
            {"text": "Themen mit unterschiedlichen Prioritäten werden gebündelt und getauscht — so entstehen Trades, die beide besser stellen", "hinweis": "Integrative Verhandlung"},
            {"text": "Du drohst, das Angebot abzulehnen, damit er nachgibt", "hinweis": "Distributiv, nicht integrativ"},
            {"text": "Du verlangst mehr als du willst, damit du scheinbar nachgibst", "hinweis": "Anker-Strategie, nicht Logrolling"},
        ],
        "loesung_text": "Tausch von Themen mit unterschiedlichen Prioritäten — schafft gemeinsamen Mehrwert",
        "erklaerung": "<p>Logrolling: Du gibst nach bei Dingen, die dir weniger wichtig sind (Flexibilität = für dich ok), im Tausch gegen Dinge, die dir viel wichtiger sind (Gehalt). Für den Chef ist es umgekehrt. Beide gewinnen bei Themen, die ihnen wichtig sind. Das ist win-win — kein Nullsummenspiel, sondern Werteexpansion.</p>",
        "kontext": "<p>Voraussetzung: Beide Seiten müssen verschiedene Präferenzen haben — und bereit sein, sie zu teilen. Das Offenbaren von Prioritäten kann riskant erscheinen, schafft aber Mehrwert. Raiffa (1982): 'Compatible issues are often disguised as conflicting ones.'</p>",
        "erkenntnis": "Nicht jede Verhandlung ist ein Nullsummenspiel. Wer Prioritäten aufdeckt und Themen bündelt, vergrößert den Kuchen — bevor er ihn teilt.",
    },
    "good-cop-bad-cop": {
        "id": "good-cop-bad-cop", "name": "Good Cop / Bad Cop", "icon": "👮",
        "farbe": "amber", "kategorie": "Verhandlung",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Verhandlung mit zwei Personen auf der anderen Seite: Person A ist fordernd, aggressiv, setzt Fristen. Person B ist verständnisvoll, signalisiert Entgegenkommen. Am Ende machst du ein Zugeständnis — erleichtert, dass wenigstens Person B verständnisvoll ist.",
        "frage": "Wie erkennst und neutralisierst du die Good-Cop-Bad-Cop-Taktik?",
        "optionen": [
            {"text": "Mit Person B alleine verhandeln — Person A ausschließen", "hinweis": "Schafft neue Probleme"},
            {"text": "Die Taktik benennen: 'Ich bemerke, dass ihr beide sehr unterschiedliche Rollen spielt — lass uns direkt über die Substanz reden'", "hinweis": "Meta-Kommunikation"},
            {"text": "Person A ignorieren und nur auf Person B reagieren", "hinweis": "Person A hat weiter Einfluss auf das Ergebnis"},
            {"text": "Selbst eine eigene Kollegin mitbringen, die ebenfalls aggressiv ist", "hinweis": "Eskalation, keine Neutralisierung"},
        ],
        "loesung_text": "Taktik explizit benennen und auf Sachebene zurückführen",
        "erklaerung": "<p>Die Taktik nutzt psychologischen Kontrast (Bad Cop macht Druck → Good Cop wirkt als Retter) und Erleichterung (du machst Zugeständnisse, um den Bad Cop zu besänftigen). Gegenmaßnahme: Taktik benennen neutralisiert sie sofort. Dann: Klare eigene Interessen und Grenzen kommunizieren, ohne auf die emotionale Inszenierung einzugehen.</p>",
        "kontext": "<p>Die Taktik wird in Verhören, Verkauf und Unternehmensverhandlungen eingesetzt. Wichtig: auch wenn man die Taktik erkennt, respektvoll bleiben — 'Ich glaube, wir werden produktiver, wenn wir direkt kommunizieren.'</p>",
        "erkenntnis": "Psychologische Taktiken verlieren ihre Wirkung, wenn man sie benennt. Transparenz ist die mächtigste Gegenstrategie.",
    },
    "interessen-vs-positionen": {
        "id": "interessen-vs-positionen", "name": "Interessen vs. Positionen", "icon": "🍊",
        "farbe": "teal", "kategorie": "Verhandlung",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Zwei Schwestern streiten um eine Orange. Beide sagen: 'Ich will die Orange!' Der Vater teilt sie hälftig. Ergebnis: Keine ist zufrieden. Was er nicht fragte: Schwester A wollte den Saft, Schwester B die Schale zum Backen.",
        "frage": "Was ist der Unterschied zwischen Positionen und Interessen?",
        "optionen": [
            {"text": "Positionen = was jemand fordert; Interessen = warum er es fordert", "hinweis": "Harvard-Kern"},
            {"text": "Positionen = langfristige Ziele; Interessen = kurzfristige Bedürfnisse", "hinweis": "Falsche Unterscheidung"},
            {"text": "Positionen sind verhandelbar; Interessen nicht", "hinweis": "Eher umgekehrt"},
            {"text": "Interessen sind öffentlich; Positionen privat", "hinweis": "Meistens umgekehrt"},
        ],
        "loesung_text": "Positionen = was man fordert; Interessen = warum (das eigentliche Bedürfnis)",
        "erklaerung": "<p>Harvard-Konzept (Fisher & Ury, Getting to Yes, 1981): Hinter jeder Position steckt ein Interesse. Schwester A: Position = ganze Orange, Interesse = Saft. Schwester B: Position = ganze Orange, Interesse = Schale. Wer Interessen aufdeckt, findet oft Lösungen, die beide besser stellen als jeder Kompromiss der Positionen.</p>",
        "kontext": "<p>Positionen sind oft inkompatibel; Interessen oft nicht. Das Fragen 'Warum?' und 'Was brauchen Sie wirklich?' ist die wichtigste Verhandlungstechnik des Harvard-Konzepts. Es führt von Nullsummenspielen zu Werteexpansion.</p>",
        "erkenntnis": "Wer nur Positionen sieht, kämpft. Wer Interessen versteht, kooperiert. Die Frage 'Warum?' ist die kraftvollste Verhandlungsfrage.",
    },
    "macht-des-schweigens": {
        "id": "macht-des-schweigens", "name": "Die Macht des Schweigens", "icon": "🤫",
        "farbe": "indigo", "kategorie": "Verhandlung",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Du machst ein Angebot: 450 €. Dann schaust du deinen Verhandlungspartner an — und sagst nichts. Er bleibt still. Du wirst unruhig. Nach 15 Sekunden sagst du: 'Oder 420 € wäre auch ok.'",
        "frage": "Was ist psychologisch passiert — und wie nutzt man Schweigen strategisch?",
        "optionen": [
            {"text": "Schweigen signalisiert Ablehnung → du nimmst an, er will weniger", "hinweis": "Interpretation ohne Grundlage"},
            {"text": "Unkomfortables Schweigen erzeugt Druck zur Konzession — du gibst nach, um es zu beenden", "hinweis": "Psychologie der Stille"},
            {"text": "Schweigen ist unhöflich — er hätte sofort reagieren sollen", "hinweis": "Kulturell verschieden, aber nicht die Analyse"},
            {"text": "Du hast ein schlechtes Angebot gemacht — das Schweigen war gerechtfertigt", "hinweis": "Vielleicht — aber der Mechanismus ist anders"},
        ],
        "loesung_text": "Schweigen erzeugt Druckgefühl — wer es bricht, gibt oft Konzessionen",
        "erklaerung": "<p>Menschen sind sozial konditioniert, Stille zu füllen. In Verhandlungen fühlt sich Schweigen nach einem Angebot wie Ablehnung an — der Anbietende interpretiert es als Signal, das Angebot sei zu hoch, und macht spontan Zugeständnisse. Strategisches Schweigen: Nach eigenem Angebot — schweige, bis der Andere reagiert. Das Schweigen gehört dem Anderen.</p>",
        "kontext": "<p>Fahregel: Nach einem Angebot die 'stille Regel' anwenden. Als Käufer: nach Preisnennung stillhalten. Als Verkäufer: nach Angebot stillhalten. Wer als Erster spricht, gibt Information preis oder macht Konzessionen.</p>",
        "erkenntnis": "Stille ist keine leere Zeit — sie ist Druck. Wer Stille aushalten kann, verhandelt stärker. Das Unbehagen liegt auf beiden Seiten — die Frage ist, wer es länger aushält.",
    },
    "nibbling": {
        "id": "nibbling", "name": "Nibbling", "icon": "🐭",
        "farbe": "pink", "kategorie": "Verhandlung",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Der Deal ist fertig verhandelt, beide Seiten sind zufrieden. Kurz vor der Unterschrift sagt die andere Seite: 'Ach ja, könnten Sie noch schnell den Support für das erste Jahr dazugeben? Das wäre doch kein großes Problem, oder?'",
        "frage": "Was ist die beste Reaktion auf diese Last-Minute-Taktik?",
        "optionen": [
            {"text": "Ja sagen — der Deal ist fast durch, man will ihn nicht gefährden", "hinweis": "Genau das, was der Nibbler will"},
            {"text": "Freundlich ablehnen und das Nibbling benennen: 'Das klingt nach einer neuen Verhandlung — lass uns das separat besprechen'", "hinweis": "Benennen und umleiten"},
            {"text": "Den Deal platzen lassen — solche Taktiken duldet man nicht", "hinweis": "Überreaktion"},
            {"text": "Gegennibbling: auch noch etwas extra fordern", "hinweis": "Kann funktionieren — aber Eskalationsrisiko"},
        ],
        "loesung_text": "Freundlich benennen und als neue Verhandlung rahmen",
        "erklaerung": "<p>Nibbling nutzt den 'Foot-in-the-Door'-Effekt und den Sunk-Cost-Druck (man will den Deal nicht für eine 'Kleinigkeit' gefährden). Gegenmaßnahme: 'Diese Frage wurde in unserer Verhandlung nicht besprochen — ich bin gerne bereit, das zu klären, aber dann gehen wir zurück an den Tisch.' Das benennt die Taktik ohne Konfrontation und schützt das Gesamtpaket.</p>",
        "kontext": "<p>Nibbling ist besonders effektiv, wenn die andere Seite emotional in den Deal investiert ist. Prophylaxe: Explizit vereinbaren, was im Deal enthalten ist — und was nicht. 'Dieses Angebot enthält X. Support ist separat.'</p>",
        "erkenntnis": "Last-Minute-Forderungen nutzen Sunk-Cost-Logik. Wer das erkennt, kann ruhig und klar reagieren, ohne den Deal zu gefährden.",
    },
    "salami-taktik": {
        "id": "salami-taktik", "name": "Salami-Taktik", "icon": "🥩",
        "farbe": "orange", "kategorie": "Verhandlung",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "In einer Verhandlung über einen IT-Vertrag: Zuerst wird der Basispreis verhandelt. Dann: 'Ach, und Schulung der Nutzer wäre dabei, oder?' — 'Und natürlich die Migration der Daten?' — 'Und 24/7-Support?' Jede Scheibe wirkt klein.",
        "frage": "Wie erkennt und neutralisiert man die Salami-Taktik?",
        "optionen": [
            {"text": "Jede Einzelforderung separat verhandeln — so bleibt der Überblick", "hinweis": "Das ist genau, was der Salamist will"},
            {"text": "Gesamtumfang zu Beginn definieren und festhalten — Nachforderungen als Neuverhandlung rahmen", "hinweis": "Scope Definition als Schutz"},
            {"text": "Alle Forderungen akzeptieren — dann den Preis erhöhen", "hinweis": "Rückwärtsnibbling — riskant"},
            {"text": "Die Verhandlung abbrechen", "hinweis": "Überreaktion"},
        ],
        "loesung_text": "Scope zu Beginn definieren — Nachforderungen als Neuverhandlung rahmen",
        "erklaerung": "<p>Schutz: Vor Verhandlungsbeginn klären — 'Was genau ist im Scope? Was ist out-of-scope?' Eine detaillierte Leistungsbeschreibung schließt die Tür. Im Verlauf: 'Das klingt nach einer Erweiterung des ursprünglichen Scopes — das würde den Preis entsprechend anpassen.' Sobald der Andere weiß, dass jede Scheibe einen Preis hat, hört das Scheiben-Schneiden auf.</p>",
        "kontext": "<p>Salami-Taktik wird auch politisch eingesetzt: schrittweise Annektierung, schrittweise Untergrabung von Strukturen. Jeder Schritt wirkt tolerierbar — die Summe ist es nicht.</p>",
        "erkenntnis": "Wer den Gesamtumfang nicht kontrolliert, verliert die Kontrolle über den Wert. Scope Management ist Verhandlungsmanagement.",
    },
    "reframing": {
        "id": "reframing", "name": "Reframing in der Verhandlung", "icon": "🖼️",
        "farbe": "sky", "kategorie": "Verhandlung",
        "schwierigkeit": "Mittel", "dauer": "4 min",
        "setup": "Die andere Seite sagt: 'Das können wir uns nicht leisten.' Klassische Reaktion: Argumente warum der Preis gerechtfertigt ist. Reframing-Reaktion: Die Aussage in einen anderen Rahmen setzen.",
        "frage": "Was ist Reframing — und was wäre eine gute Reframing-Reaktion?",
        "optionen": [
            {"text": "Den Preis erklären und rechtfertigen: 'Unsere Kosten sind…'", "hinweis": "Keine Perspektivveränderung"},
            {"text": "Die Aussage umdeuten: 'Was müsste sich ändern, damit es in Ihr Budget passt?'", "hinweis": "Verschiebt von Sackgasse zu Möglichkeit"},
            {"text": "Den Preis sofort senken", "hinweis": "Nachgeben ohne Analyse"},
            {"text": "Fragen: 'Was können Sie sich leisten?' — um den Reservationspreis zu erfragen", "hinweis": "Direkt, aber Reframing ist subtiler"},
        ],
        "loesung_text": "'Was müsste sich ändern, damit es möglich wird?' — Sackgasse → Möglichkeit",
        "erklaerung": "<p>Reframing verändert den Rahmen einer Situation, ohne die Fakten zu ändern. 'Wir können uns das nicht leisten' framt die Situation als closed. 'Was müsste sich ändern, damit es möglich wird?' framt sie als open problem — und lädt beide Seiten ein, kreative Lösungen zu suchen (andere Zahlungsmodalitäten, Leistungsreduktion, Ratenzahlung, Gegenleistungen).</p>",
        "kontext": "<p>Reframing in Mediationen: Aus 'Er ist schuld' wird 'Was brauchen Sie, um vorwärtszukommen?' Aus 'unmöglich' wird 'was wäre nötig?' Das verschiebt die Energie von Konfrontation zu Kooperation.</p>",
        "erkenntnis": "Wer den Rahmen setzt, kontrolliert die Richtung des Gesprächs. Sackgassen sind meist gerahmte Probleme — Reframing öffnet Türen.",
    },
    # ── Psychologie ───────────────────────────────────────────────────────
    "marshmallow-test": {
        "id": "marshmallow-test", "name": "Der Marshmallow-Test", "icon": "🍬",
        "farbe": "violet", "kategorie": "Psychologie",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "Walter Mischel (1972): 4-jährige Kinder bekamen einen Marshmallow. Wer 15 Minuten wartet, bekommt zwei. Jahrzehnte später verglichen Nachfolgestudien: Kinder, die warteten, hatten im Schnitt bessere SAT-Werte, bessere soziale Kompetenz, geringeres BMI.",
        "frage": "Was zeigte eine Replikationsstudie (Watts et al., 2018) über die ursprünglichen Befunde?",
        "optionen": [
            {"text": "Die Ergebnisse wurden vollständig bestätigt — Marshmallow-Geduld ist der stärkste Lebensprediktor", "hinweis": "Repliziert?"},
            {"text": "Nach Kontrolle für sozioökonomischen Status schrumpfte der Effekt erheblich", "hinweis": "Konfundierung durch Einkommen"},
            {"text": "Kinder, die nicht warteten, waren im Schnitt erfolgreicher", "hinweis": "Gegenteil des Originals"},
            {"text": "Der Test misst nur Hunger — kein Willensverhalten", "hinweis": "Zu simplistisch"},
        ],
        "loesung_text": "Nach Kontrolle für sozioökonomischen Status schrumpfte der Effekt stark",
        "erklaerung": "<p>Watts et al. (2018): Der Marshmallow-Test misst nicht nur Selbstkontrolle, sondern auch Vertrauen in die Umgebung. Kinder aus ärmeren Verhältnissen haben gelernt, dass Versprechen nicht immer eingehalten werden. Sozioökonomischer Status und familiäres Klima erklären einen Großteil des Effekts. Selbstkontrolle bleibt wichtig — aber der ursprüngliche Effekt war überschätzt.</p>",
        "kontext": "<p>Der Marshmallow-Test ist ein Beispiel für das Replikationsproblem in der Psychologie. Viele ikonische Studien halten Nachprüfungen mit größeren, diverseren Stichproben nur teilweise stand. Das mindert den Befund — aber ersetzt ihn nicht durch Null.</p>",
        "erkenntnis": "Einfache Tests messen selten eine einzige Eigenschaft. Kontext, Vertrauen und soziale Bedingungen formen Verhalten genauso wie innere Dispositionen.",
    },
    "halo-effekt": {
        "id": "halo-effekt", "name": "Der Halo-Effekt", "icon": "👼",
        "farbe": "rose", "kategorie": "Psychologie",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Edward Thorndike (1920): Soldaten wurden von Offizieren nach Intelligenz, Charakter, Führungsqualität und körperlicher Verfassung bewertet. Die Ratings korrelierten unnatürlich hoch miteinander — ein attraktiver Soldat galt automatisch auch als intelligenter.",
        "frage": "Was ist der Halo-Effekt — und wo schadet er am meisten?",
        "optionen": [
            {"text": "Ein Merkmal überstrahlt alle anderen — Gesamturteil wird verzerrt", "hinweis": "Halo = Heiligenschein"},
            {"text": "Menschen bevorzugen Attraktive — nur oberflächlicher Bias", "hinweis": "Weiter als Attraktivität"},
            {"text": "Wiederholte positive Eindrücke akkumulieren — fair und realistisch", "hinweis": "Kein systematischer Fehler?"},
            {"text": "Ersteindrücke sind immer korrekt — erfahrungsbasiert", "hinweis": "Primacy Effect, aber kein Halo"},
        ],
        "loesung_text": "Ein Merkmal überstrahlt alle anderen — systematische Urteilsverzerrung",
        "erklaerung": "<p>Der Halo-Effekt: Ein positives (oder negatives) Merkmal strahlt auf alle anderen Urteile aus. Attraktive Menschen wirken intelligenter, vertrauenswürdiger und kompetenter — ohne jede Evidenz. Am gefährlichsten: Einstellungsgespräche (erste Minuten bestimmen das Urteil), Leistungsbeurteilungen und Strafurteile (Attraktive bekommen kürzere Strafen).</p>",
        "kontext": "<p>Gegenmittel: Strukturierte Interviews (gleiche Fragen, klare Kriterien), Blind Reviews (anonyme Bewerbungen), getrennte Bewertung verschiedener Merkmale. Daniel Kahneman (Thinking, Fast and Slow): Der Halo-Effekt ist eine Vereinfachungsstrategie des System-1-Denkens.</p>",
        "erkenntnis": "Wir urteilen aus Fragmenten und konstruieren daraus ein vollständiges Bild. Das spart Energie — und erzeugt systematische Fehler. Strukturierte Prozesse schützen vor dem Halo.",
    },
    "bystander-effekt": {
        "id": "bystander-effekt", "name": "Der Bystander-Effekt", "icon": "👥",
        "farbe": "amber", "kategorie": "Psychologie",
        "schwierigkeit": "Einsteiger", "dauer": "4 min",
        "setup": "1964, New York: Kitty Genovese wird über 30 Minuten angegriffen. 38 Nachbarn hörten oder sahen es — niemand rief die Polizei. Darbiey & Latané (1968) untersuchten das Phänomen experimentell.",
        "frage": "Was erklärt den Bystander-Effekt psychologisch?",
        "optionen": [
            {"text": "Gleichgültigkeit und Egoismus der Zuschauer", "hinweis": "Zu einfach — trifft nicht die Mechanismen"},
            {"text": "Pluralistische Ignoranz + Diffusion der Verantwortung: Jeder denkt, die Anderen handeln", "hinweis": "Latané & Darley's Befunde"},
            {"text": "Angst vor dem Angreifer — niemand wollte sich in Gefahr bringen", "hinweis": "Gilt für direkte Eingriffe — aber Telefon?"},
            {"text": "Kollektive Panik — Schockzustand lähmt alle gleichzeitig", "hinweis": "Erklärt nicht warum Einzel-Bystander häufiger handeln"},
        ],
        "loesung_text": "Pluralistische Ignoranz + Diffusion of Responsibility",
        "erklaerung": "<p>Zwei Mechanismen: 1) Pluralistische Ignoranz — jeder schaut auf andere, um die Situation zu deuten. Alle sehen, dass niemand reagiert → 'Scheinbar ist es nicht so schlimm.' 2) Diffusion of Responsibility — je mehr Zuschauer, desto weniger fühlt sich jeder Einzelne verantwortlich. Experimente: Allein sehende Zeugen halfen in 85 % — in Gruppen nur 31 %.</p>",
        "kontext": "<p>Gegenmaßnahme: Direkte Ansprache. 'Sie da, in der roten Jacke — rufen Sie bitte die Polizei!' Direkte Adressierung hebt Diffusion auf. Das wird in Erste-Hilfe-Kursen gelehrt. Die Kitty-Genovese-Story wurde im Nachhinein teils übertrieben dargestellt — die Mechanismen sind aber real.</p>",
        "erkenntnis": "Mehr Zuschauer bedeutet weniger Hilfe. Wer Hilfe braucht, muss konkrete Personen direkt ansprechen — sonst verlässt sich jeder auf andere.",
    },
    "barnum-effekt": {
        "id": "barnum-effekt", "name": "Der Barnum-Effekt", "icon": "🎪",
        "farbe": "emerald", "kategorie": "Psychologie",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Horoskop: 'Sie haben manchmal das Gefühl, nicht ausreichend anerkannt zu werden. Sie haben unausgeschöpfte Potenziale. In manchen Situationen sind Sie extrovertiert, in anderen zurückhaltend.' Fast jeder glaubt, das trifft genau auf ihn zu.",
        "frage": "Warum akzeptieren Menschen vage, allgemeine Aussagen als persönlich zutreffend?",
        "optionen": [
            {"text": "Weil Horoskope tatsächlich wissenschaftlich fundiert sind", "hinweis": "Keine empirische Evidenz"},
            {"text": "Weil Menschen positive Aussagen über sich annehmen und vage Formulierungen auf sich beziehen (Barnum-Effekt)", "hinweis": "Bestätigungsfehler + Vagueness"},
            {"text": "Weil alle Menschen tatsächlich ähnliche Eigenschaften haben", "hinweis": "Dann wäre keine Aussage informativ"},
            {"text": "Weil der Kontext (Horoskop-Lektüre) die Aufmerksamkeit erhöht", "hinweis": "Teilweise — aber nicht vollständig"},
        ],
        "loesung_text": "Vage Aussagen + Bestätigungssuche = Barnum-Effekt",
        "erklaerung": "<p>Forer (1948): Studierenden wurde ein 'persönliches Persönlichkeitsprofil' gegeben — tatsächlich für alle identisch aus einem Astrologiebuch zusammengestellt. Durchschnittliche Treffsicherheitsbewertung: 4,3/5. Mechanismen: 1) Vagheit ('manchmal', 'oft') — alles passt. 2) Confirmation Bias — man sucht bestätigende Beispiele. 3) Positive Formulierungen werden gerne akzeptiert.</p>",
        "kontext": "<p>Der Barnum-Effekt erklärt den Erfolg von Astrologie, Handlesen, Cold Reading und manchen Persönlichkeitstests. Gegenmaßnahme: Prüfen, ob die Aussage auch für andere zutrifft — Spezifizität ist das Kriterium für Aussagekraft.</p>",
        "erkenntnis": "Wir sind anfälliger für Schmeichelei und Allgemeinaussagen als wir denken. Kritisches Denken heißt: Wie spezifisch ist diese Aussage — und könnte sie für jeden gelten?",
    },
    "flow-analyse": {
        "id": "flow-analyse", "name": "Flow – der optimale Zustand", "icon": "🌊",
        "farbe": "sky", "kategorie": "Psychologie",
        "schwierigkeit": "Einsteiger", "dauer": "3 min",
        "setup": "Mihaly Csikszentmihalyi (1990) beschreibt Flow als Zustand vollständiger Aufgabe-Absorption: Zeit vergeht unmerklich, man ist völlig fokussiert, keine Selbstwahrnehmung. Er entsteht an einem bestimmten Punkt zwischen Fähigkeit und Herausforderung.",
        "frage": "Unter welchen Bedingungen entsteht Flow?",
        "optionen": [
            {"text": "Wenn die Aufgabe leicht ist — kein Stress, keine Hindernisse", "hinweis": "Leichte Aufgaben erzeugen Langeweile"},
            {"text": "Wenn Herausforderung und Fähigkeit im Gleichgewicht sind — weder zu schwer noch zu leicht", "hinweis": "Flow-Kanal nach Csikszentmihalyi"},
            {"text": "Wenn man unter extremem Zeitdruck steht", "hinweis": "Druck → Angst, wenn Fähigkeit fehlt"},
            {"text": "Wenn die Aufgabe völlig neuartig ist — maximale Stimulation", "hinweis": "Neuheit ohne Kompetenz → Frustration"},
        ],
        "loesung_text": "Gleichgewicht zwischen Herausforderung und Fähigkeit",
        "erklaerung": "<p>Flow-Kanal: Zu leicht → Langeweile. Zu schwer → Angst. Im Gleichgewicht → Flow. Zusätzliche Bedingungen: klare Ziele, sofortiges Feedback, Kontrolle über die Handlung. Flow ist nicht passiv — er erfordert aktive Auseinandersetzung mit einer Aufgabe auf dem Niveau der eigenen Kapazität.</p>",
        "kontext": "<p>Anwendungen: Game Design (Spiele halten Spieler im Flow durch adaptive Schwierigkeit), Lernen (optimale Zone im Sinne von Vygotskys 'Zone of Proximal Development'), Arbeit (Jobs mit passender Anforderung erzeugen Engagement). Flow ist messbar und steuerbar.</p>",
        "erkenntnis": "Optimale Leistung und tiefe Zufriedenheit entstehen nicht bei Ruhe oder Überforderung — sondern an der Grenze der eigenen Fähigkeit. Den eigenen Flow-Kanal zu kennen ist eine Lebenskompetenz.",
    },
    "milgram-gehorsam": {
        "id": "milgram-gehorsam", "name": "Das Milgram-Experiment", "icon": "⚡",
        "farbe": "rose", "kategorie": "Psychologie",
        "schwierigkeit": "Mittel", "dauer": "5 min",
        "setup": "Stanley Milgram (1961): Versuchspersonen wurden angewiesen, einem 'Schüler' (Schauspieler) bei Falschantworten Elektroschocks zu verabreichen — ansteigend bis zu 450 Volt (tödlich). Jemand im weißen Kittel sagte: 'Das Experiment muss weitergehen.'",
        "frage": "Wie viele der Versuchspersonen verabreichten den maximalen Schock (450 V)?",
        "optionen": [
            {"text": "Ca. 5 % — die meisten verweigerten nach ersten Schmerzsignalen", "hinweis": "Milgrams Erwartung vor dem Experiment"},
            {"text": "Ca. 65 % — fast zwei Drittel gingen bis zum Maximum", "hinweis": "Erschreckendes Ergebnis"},
            {"text": "Ca. 30 % — knapp ein Drittel gehorchte vollständig", "hinweis": "Tatsächlich höher"},
            {"text": "100 % — alle gehorchten der Autorität", "hinweis": "Nicht ganz — aber erschreckend viele"},
        ],
        "loesung_text": "Ca. 65 % — fast zwei Drittel verabreichten den maximalen Schock",
        "erklaerung": "<p>65 % der Teilnehmer verabreichten 450-Volt-Schocks — obwohl der 'Schüler' schrie und aufhörte zu reagieren. Die Erklärung: Gehorsam gegenüber legitimen Autoritäten, graduelles Commitment (jeder Schritt war nur klein größer), Verantwortungsdiffusion ('Ich folge nur Anweisungen'), physische Distanz zum Opfer.</p>",
        "kontext": "<p>Das Experiment wurde im Kontext des Eichmann-Prozesses (1960) geplant. Milgrams Frage: Ist Gehorsam im Nationalsozialismus ein deutsches Phänomen? Antwort: Nein — es ist ein menschliches. Ethisch hoch umstritten: Viele Teilnehmer litten unter den Erkenntnissen über sich selbst. Heute nicht mehr genehmigungsfähig.</p>",
        "erkenntnis": "Böses entsteht oft nicht aus Bösartigkeit, sondern aus Gehorsam. Die Absicht, das Richtige zu tun, schützt nicht vor dem Falschen, wenn Autoritäten Kontext definieren. Das ist die erschütternde Lektion.",
    },
}


@router.get("/{puzzle_id}", response_class=HTMLResponse)
def generic_raetsel_page(request: Request, puzzle_id: str):
    p = GENERIC_PUZZLES.get(puzzle_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Rätsel nicht gefunden")
    return templates.TemplateResponse(
        request, "raetsel/generic.html", {"p": p, "active_page": "raetsel"}
    )

