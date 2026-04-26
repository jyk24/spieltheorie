"""Glossar - Fachbegriffe aus Spieltheorie, Psychologie, Mathematik und mehr."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

GLOSSAR = [
    {
        "id": "ad-hominem",
        "titel": "Ad Hominem",
        "definition": (
            "Lateinisch: 'gegen die Person'. Trugschluss, bei dem nicht das Argument angegriffen wird, "
            "sondern die Person, die es vertritt. Beispiel: 'Du kannst ueber Ernaehrung nichts wissen "
            "- du bist selbst uebergewichtig.' Das Argument kann trotzdem stichhaltig sein."
        ),
        "kategorie": "Rhetorik",
        "link": "/raetsel/trugschluesse",
    },
    {
        "id": "adverse-selection",
        "titel": "Adverse Selektion",
        "definition": (
            "Wenn eine Seite mehr Informationen hat als die andere (Informationsasymmetrie), "
            "waehlt die uninformierte Seite tendenziell schlechtere Partner. "
            "Beispiel: Krankenversicherungen ziehen Kranke an, was Praemien erhoeht und Gesunde vertreibt. "
            "Beschrieben von George Akerlof im 'Markt fuer Zitronen' (1970)."
        ),
        "kategorie": "Spieltheorie",
        "link": "/raetsel/marktverlust",
    },
    {
        "id": "allais-paradoxon",
        "titel": "Allais-Paradoxon",
        "definition": (
            "Klassische Verletzung der Erwartungsnutzentheorie (Maurice Allais, 1953). "
            "Menschen waehlen Option A gegenueber B, aber bei einer modifizierten Version B' gegenueber A', "
            "obwohl die Logik beides ausschliesst. Zeigt, dass Menschen keine reinen Erwartungswert-Maximierer sind."
        ),
        "kategorie": "Entscheidung",
        "link": "/raetsel/allais",
    },
    {
        "id": "ambiguitaetsaversion",
        "titel": "Ambiguitaetsaversion",
        "definition": (
            "Menschen bevorzugen bekannte Risiken (kalkulierbare Wahrscheinlichkeiten) gegenueber unbekannten "
            "(Knightsche Unsicherheit), auch wenn der Erwartungswert derselbe ist. "
            "Demonstriert durch das Ellsberg-Paradoxon: Lieber aus Urne mit bekanntem 50/50-Verhaeltnis ziehen "
            "als aus einer mit unbekanntem Verhaeltnis."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/ellsberg",
    },
    {
        "id": "ankereffekt",
        "titel": "Ankereffekt",
        "definition": (
            "Kognitive Verzerrung: Der erste genannte Wert (der 'Anker') beeinflusst alle folgenden Schaetzungen, "
            "auch wenn er voellig willkuerlich ist. Amos Tversky & Daniel Kahneman zeigten, dass Versuchspersonen "
            "nach Drehen eines praeparierten Gluecksrads hoehere oder niedrigere Zahlen schaetzten. "
            "In Verhandlungen: Der erste Preis praegt das gesamte Ergebnis."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/anker-experiment",
    },
    {
        "id": "auszahlungsmatrix",
        "titel": "Auszahlungsmatrix",
        "definition": (
            "Tabellarische Darstellung eines strategischen Spiels: Zeilen = Strategien von Spieler 1, "
            "Spalten = Strategien von Spieler 2, Zellen = Auszahlungen beider. "
            "Kernwerkzeug der Spieltheorie, um Nash-Gleichgewichte und dominante Strategien zu identifizieren."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "backward-induction",
        "titel": "Backward Induction (Rueckwaertsinduktion)",
        "definition": (
            "Loesungsmethode fuer sequentielle Spiele: Man beginnt beim letzten moeglichen Zug und "
            "schlussfolgert rueckwaerts bis zum Anfang, was ein rationaler Spieler tun wuerde. "
            "Beispiel: Im Piratenproblem berechnet man zuerst, was bei 2 Piraten optimal ist, dann bei 3 usw. "
            "Fuehrt manchmal zu kontraintuitiven Ergebnissen (Centipede-Paradox)."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "batna",
        "titel": "BATNA",
        "definition": (
            "Best Alternative to a Negotiated Agreement - die beste Alternative, falls kein Verhandlungsdeal "
            "zustande kommt. Das BATNA bestimmt deine Verhandlungsmacht: je staerker deine Alternative, "
            "desto mehr kannst du fordern. Konzept aus dem Harvard-Verhandlungsmodell (Fisher & Ury, 'Getting to Yes')."
        ),
        "kategorie": "Verhandlung",
        "link": "/raetsel/batna",
    },
    {
        "id": "bayes-theorem",
        "titel": "Bayes-Theorem",
        "definition": (
            "Formel zur rationalen Aktualisierung von Ueberzeugungen aufgrund neuer Evidenz: "
            "P(H|E) = P(E|H) x P(H) / P(E). Sprich: 'Wie wahrscheinlich ist die Hypothese, "
            "gegeben die Evidenz?' Kern des Bayesianischen Denkens. "
            "Praktisches Beispiel: Ein positiver HIV-Test bedeutet nicht automatisch 99% Wahrscheinlichkeit - "
            "bei seltenen Krankheiten koennen falsch-positive Ergebnisse dominieren."
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/bayes-theorem",
    },
    {
        "id": "bedingte-wahrscheinlichkeit",
        "titel": "Bedingte Wahrscheinlichkeit",
        "definition": (
            "Die Wahrscheinlichkeit eines Ereignisses A, gegeben dass Ereignis B bereits eingetreten ist: "
            "P(A|B) = P(A und B) / P(B). Grundbaustein des Bayes-Theorems. "
            "Beispiel: Wie wahrscheinlich ist es, dass jemand eine Krankheit hat, "
            "wenn sein Test positiv ausgefallen ist?"
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/falsch-positiv",
    },
    {
        "id": "beobachtereffekt",
        "titel": "Beobachtereffekt (Quantenmechanik)",
        "definition": (
            "In der Quantenmechanik veraendert der Akt der Messung den Zustand eines Systems. "
            "Vor der Messung befindet sich ein Quantenobjekt in einer Superposition mehrerer Zustaende. "
            "Beim Messen 'kollabiert' die Wellenfunktion auf einen einzigen Wert. "
            "Das ist keine Frage der Technologie - es ist ein fundamentales Prinzip der Quantenwelt."
        ),
        "kategorie": "Physik",
        "link": "/raetsel/schroedinger",
    },
    {
        "id": "bounded-rationality",
        "titel": "Bounded Rationality",
        "definition": (
            "Begrenzte Rationalitaet (Herbert Simon, 1955): Menschen haben endliche kognitive Ressourcen, "
            "Zeit und Information. Statt das Optimum zu suchen, waehlen sie die erste 'hinreichend gute' Option "
            "(Satisficing statt Optimizing). Erklaert, warum echtes Verhalten oft von spieltheoretischen "
            "Prognosen abweicht."
        ),
        "kategorie": "Entscheidung",
        "link": "/grundlagen",
    },
    {
        "id": "braess-paradoxon",
        "titel": "Braess-Paradoxon",
        "definition": (
            "Wenn man einem Netzwerk (z. B. Strassennetz) eine neue, schnelle Verbindung hinzufuegt, "
            "kann sich die durchschnittliche Reisezeit fuer alle erhoehen. "
            "Jeder Fahrer waehlt rational die schnellste Route, aber die kollektive Folge ist ein schlechteres Ergebnis. "
            "Nash-Gleichgewicht ungleich gesellschaftliches Optimum."
        ),
        "kategorie": "Spieltheorie",
        "link": "/raetsel/braess",
    },
    {
        "id": "brinkmanship",
        "titel": "Brinkmanship",
        "definition": (
            "Strategie, den Gegner an den Rand einer Katastrophe zu fuehren, um ein Zugestaendnis zu erzwingen. "
            "Wer durchhaelt (oder wer glaubwuerdig macht, er werde durchhalten), gewinnt. "
            "Bekanntes Beispiel: Kubakrise 1962. Kernproblem: Die Drohung muss glaubwuerdig sein, "
            "auch wenn das Nachgeben fuer beide besser waere."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/chicken",
    },
    {
        "id": "commitment",
        "titel": "Commitment (Selbstbindung)",
        "definition": (
            "Eine glaubwuerdige, vorab angekuendigte und schwer rueckgaengig zu machende Handlung, "
            "die die eigene Strategie festlegt. Scheinbar irrationale Selbstbindung kann rational sein, "
            "wenn sie den Gegner ueberzeugt. Beispiel: Schiff verbrennen - Rueckzug unmoeglich - Gegner weicht. "
            "Thomas Schelling erhielt den Wirtschaftsnobelpreis 2005 u. a. fuer diese Einsicht."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "condorcet-paradoxon",
        "titel": "Condorcet-Paradoxon",
        "definition": (
            "Bei Mehrheitswahlen mit 3 oder mehr Optionen kann es zyklische Praeferenzen geben: "
            "A gewinnt gegen B, B gegen C, C gegen A. Es gibt keine klare Mehrheitspraeferenz. "
            "Zeigt, dass demokratische Abstimmungen zu willkuerlichen Ergebnissen fuehren koennen, "
            "je nachdem welche Optionen wie abgestimmt werden (Agenda-Setting-Problem)."
        ),
        "kategorie": "Spieltheorie",
        "link": "/raetsel/condorcet",
    },
    {
        "id": "dominante-strategie",
        "titel": "Dominante Strategie",
        "definition": (
            "Eine Strategie, die unabhaengig davon, was andere Spieler tun, mindestens genauso gut ist "
            "wie jede Alternative. Wenn ein Spieler eine dominante Strategie hat, sollte er sie immer spielen. "
            "Beispiel: Im Gefangenendilemma ist 'Gestehen' die dominante Strategie fuer beide, "
            "obwohl 'Schweigen' fuer beide besser waere."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "dunning-kruger",
        "titel": "Dunning-Kruger-Effekt",
        "definition": (
            "Kognitive Verzerrung (Dunning & Kruger, 1999): Inkompetente Menschen ueberschaetzen ihre Faehigkeiten "
            "erheblich, da sie nicht erkennen, was sie nicht wissen. Experten hingegen unterschaetzen sich oft, "
            "weil sie wissen, wie viel sie noch nicht wissen. "
            "Das Paradox: Kompetenz, das eigene Unwissen einzuschaetzen, ist selbst eine Faehigkeit."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/dunning-kruger",
    },
    {
        "id": "ellsberg-paradoxon",
        "titel": "Ellsberg-Paradoxon",
        "definition": (
            "Zeigt Ambiguitaetsaversion: Wenn Urne A 50 rote und 50 schwarze Kugeln hat und Urne B ein "
            "unbekanntes Verhaeltnis, ziehen Menschen lieber aus Urne A, obwohl beide rein statistisch "
            "gleichwertig sein koennten. Menschen scheuen Unsicherheit ueber Wahrscheinlichkeiten, "
            "nicht nur ueber Ergebnisse."
        ),
        "kategorie": "Entscheidung",
        "link": "/raetsel/ellsberg",
    },
    {
        "id": "erwartungswert",
        "titel": "Erwartungswert",
        "definition": (
            "Der durchschnittliche Wert eines Zufallsereignisses bei unendlich vielen Wiederholungen: "
            "E(X) = Summe(p_i x x_i). Beispiel: Muenzwurf mit 10 EUR Gewinn bei Kopf, 0 EUR bei Zahl: E = 5 EUR. "
            "Grenzen: Erwartungswert ignoriert Risikoaversion (St. Petersburger Paradoxon) "
            "und ist bei einzelnen Entscheidungen wenig aussagekraeftig."
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/st-petersburg",
    },
    {
        "id": "ess",
        "titel": "Evolutionaer Stabile Strategie (ESS)",
        "definition": (
            "Eine Strategie in einer Population, die nicht durch eine alternative Strategie (Mutante) "
            "verdraengt werden kann. Konzept der evolutionaeren Spieltheorie (Maynard Smith & Price, 1973). "
            "Beispiel: Im Habicht-Taube-Spiel ist eine gemischte Population evolutionaer stabil, "
            "weder reine Aggressivitaet noch reine Passivitaet."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/habicht-taube",
    },
    {
        "id": "focal-point",
        "titel": "Focal Point (Schelling-Punkt)",
        "definition": (
            "Eine Loesung, auf die sich Menschen ohne Kommunikation natuerlichweise einigen, "
            "weil sie auffaellig oder 'offensichtlich' erscheint. Thomas Schelling zeigte: "
            "Wenn zwei Fremde sich in New York treffen sollen ohne Absprache, waehlen die meisten "
            "'Mittag unter dem Empire State Building'. Focal Points erklaeren Koordination ohne Sprache."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "framing-effekt",
        "titel": "Framing-Effekt",
        "definition": (
            "Dieselbe Information, unterschiedlich formuliert, fuehrt zu verschiedenen Entscheidungen. "
            "Kahneman & Tversky: '90% Ueberlebenschance' klingt besser als '10% Sterberisiko', "
            "obwohl mathematisch identisch. "
            "In Verhandlungen: Gewinne betonen statt Verluste vermeiden."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/framing",
    },
    {
        "id": "gefangenendilemma",
        "titel": "Gefangenendilemma",
        "definition": (
            "Das bekannteste Spiel der Spieltheorie: Zwei Verdaechtige werden getrennt verhoert. "
            "Gestehen bringt geringere Strafe als wenn nur der andere schweigt. "
            "Schweigen ist die beste kollektive Loesung, aber riskant. "
            "Ergebnis: Beide gestehen (Nash-Gleichgewicht), obwohl beide schweigen fuer beide besser waere. "
            "Zeigt die Spannung zwischen individuellem und kollektivem Optimum."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/gefangenendilemma",
    },
    {
        "id": "gemischte-strategie",
        "titel": "Gemischte Strategie",
        "definition": (
            "Eine Strategie, bei der ein Spieler randomisiert - mit bestimmten Wahrscheinlichkeiten "
            "zwischen reinen Strategien waehlt. Notwendig, wenn kein reines Nash-Gleichgewicht existiert. "
            "Beispiel: Schere-Stein-Papier - optimale Strategie ist gleichmaessige Zufallswahl (je 1/3). "
            "Jede erkennbare Muster-Strategie kann ausgenutzt werden."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "gesetz-grosse-zahlen",
        "titel": "Gesetz der grossen Zahlen",
        "definition": (
            "Je oefter ein Zufallsexperiment wiederholt wird, desto naeher liegt der beobachtete Durchschnitt "
            "am theoretischen Erwartungswert. Bei 10 Muenzwuerfen kann leicht 8x Kopf vorkommen; "
            "bei 10.000 Wuerfen liegt man sehr nah an 50%. "
            "Wichtig: Gilt fuer den Durchschnitt, nicht fuer Absolutwerte."
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/gesetz-grosse-zahlen",
    },
    {
        "id": "heuristik",
        "titel": "Heuristik",
        "definition": (
            "Mentale Faustregeln, die schnelle Entscheidungen ohne vollstaendige Analyse ermoeglichen. "
            "Kahneman: 'System 1'-Denken. Heuristiken sind effizient, erzeugen aber systematische Fehler "
            "(z. B. Verfuegbarkeitsheuristik: Was leicht erinnert wird, gilt als haeufig). "
            "Kern von Kahnemans 'Thinking, Fast and Slow'."
        ),
        "kategorie": "Psychologie",
        "link": "/grundlagen",
    },
    {
        "id": "informationsasymmetrie",
        "titel": "Informationsasymmetrie",
        "definition": (
            "Eine Seite in einer Transaktion oder einem Spiel hat mehr relevante Informationen als die andere. "
            "Fuehrt zu Marktversagen (Adverse Selektion, Moral Hazard) und ist Grundlage fuer "
            "Signaling und Screening. Nobelpreistraeger Akerlof, Spence, Stiglitz (2001) fuer diese Einsichten."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "informationskaskade",
        "titel": "Informationskaskade",
        "definition": (
            "Phaenomen, bei dem rationale Individuen die Entscheidungen anderer kopieren und dabei "
            "ihre eigene private Information ignorieren. Ursache: Die aggregierte Herde-Info scheint "
            "die eigene zu ueberwiegen. Fuehrt zu Herdenverhalten, sodass Gruppen manchmal "
            "kollektiv irren, obwohl jeder individuell rational handelt."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/informationskaskade",
    },
    {
        "id": "k-level-thinking",
        "titel": "K-Level Thinking",
        "definition": (
            "Modell der strategischen Tiefe: Level-0-Spieler handeln zufaellig. "
            "Level-1 optimiert gegen Level-0. Level-2 optimiert gegen Level-1 usw. "
            "Echte Menschen spielen meist Level-1 bis Level-3, selten hoeher. "
            "Experiment: Schoenheitswettbewerb (rate 2/3 des Durchschnitts) - optimale Antwort variiert "
            "je nach Level."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/beauty-contest",
    },
    {
        "id": "kognitive-dissonanz",
        "titel": "Kognitive Dissonanz",
        "definition": (
            "Unbehagen, das entsteht, wenn Ueberzeugungen, Handlungen oder Einstellungen im Widerspruch stehen. "
            "Leon Festinger (1957): Menschen verringern die Dissonanz oft durch Anpassen von Ueberzeugungen, "
            "nicht Verhalten. Klassisches Experiment: Probanden, die Boeden schrubbten, berichteten "
            "danach, die Aufgabe sei interessant gewesen."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/kognitive-dissonanz",
    },
    {
        "id": "konfirmationsfehler",
        "titel": "Konfirmationsfehler",
        "definition": (
            "Tendenz, Informationen zu suchen, zu interpretieren und zu erinnern, die die eigenen "
            "Ueberzeugungen bestaetigen. Gegenteilige Evidenz wird ignoriert oder abgewertet. "
            "Francis Bacon beschrieb es 1620; Wason-Auswahlaufgabe demonstriert es experimentell. "
            "Praktische Gefahr: fuehrt zu Festhalten an falschen Theorien."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/konfirmationsfehler",
    },
    {
        "id": "konvergenz",
        "titel": "Konvergenz (Mathematik)",
        "definition": (
            "Eine unendliche Reihe oder Folge konvergiert, wenn sie einem endlichen Grenzwert immer "
            "naeher kommt. Beispiel: 1 + 1/2 + 1/4 + 1/8 + ... = 2 (konvergiert). "
            "Gegenteil: Divergenz - die Reihe waechst ins Unendliche oder schwankt ohne Grenzwert. "
            "Wichtig: Auch wenn die einzelnen Summanden immer kleiner werden, kann die Reihe divergieren "
            "(Harmonische Reihe: 1 + 1/2 + 1/3 + 1/4 + ... = unendlich)."
        ),
        "kategorie": "Mathematik",
        "link": "/raetsel/harmonische-reihe",
    },
    {
        "id": "logos-pathos-ethos",
        "titel": "Logos, Pathos, Ethos",
        "definition": (
            "Aristoteles' drei Ueberzeugungsmittel: Logos = logische Argumentation mit Fakten und Belegen. "
            "Pathos = emotionale Ansprache, die Gefuehle des Publikums aktiviert. "
            "Ethos = Glaubwuerdigkeit und Charakter des Sprechers. "
            "Wirkungsvolle Kommunikation nutzt alle drei, je nach Situation unterschiedlich gewichtet."
        ),
        "kategorie": "Rhetorik",
        "link": "/soziales",
    },
    {
        "id": "markt-fuer-zitronen",
        "titel": "Markt fuer Zitronen",
        "definition": (
            "George Akerlofs Modell (1970, Nobelpreis 2001): Beim Gebrauchtwagenmarkt wissen Verkaeufer, "
            "ob ihr Auto gut (Pfirsich) oder schlecht (Zitrone) ist - Kaeufer nicht. "
            "Kaeufer bieten daher nur den Durchschnittspreis. Gute Autos werden zurueckgezogen. "
            "Am Ende bleiben nur Zitronen - der Markt kollabiert durch Informationsasymmetrie."
        ),
        "kategorie": "Spieltheorie",
        "link": "/raetsel/marktverlust",
    },
    {
        "id": "minimax",
        "titel": "Minimax-Theorem",
        "definition": (
            "John von Neumann (1928): In jedem endlichen Zwei-Spieler-Nullsummenspiel gibt es eine "
            "optimale gemischte Strategie, die den maximalen Verlust minimiert. "
            "Der Minimax-Wert entspricht dem Maximin-Wert: der Punkt, an dem kein Spieler durch Abweichen gewinnen kann. "
            "Grundstein der mathematischen Spieltheorie."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "moral-hazard",
        "titel": "Moral Hazard",
        "definition": (
            "Wenn jemand nach Vertragsabschluss weniger Sorgfalt zeigt, weil er die Risiken nicht selbst traegt. "
            "Beispiel: Vollkaskoversicherung kann dazu verleiten, risikoreudiger zu fahren. "
            "Kernproblem: Eine Seite kann das Verhalten der anderen nicht vollstaendig beobachten. "
            "Zusammen mit Adverser Selektion ein zentrales Problem bei Informationsasymmetrie."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "nash-gleichgewicht",
        "titel": "Nash-Gleichgewicht",
        "definition": (
            "Ein Zustand, in dem kein Spieler durch einseitiges Abweichen seinen Nutzen verbessern kann. "
            "John Nash (1950): Jedes endliche Spiel hat mindestens ein Nash-Gleichgewicht in gemischten Strategien. "
            "Wichtig: Nash-Gleichgewicht ist nicht zwingend optimal fuer alle (Gefangenendilemma). "
            "Es beschreibt Stabilitaet, nicht Effizienz."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "newcomb-paradoxon",
        "titel": "Newcomb-Paradoxon",
        "definition": (
            "Box A enthaelt immer 1.000 EUR. Box B enthaelt 1.000.000 EUR, aber nur wenn ein Prognostiker "
            "vorhergesagt hat, dass du nur Box B nimmst. Der Prognostiker liegt immer richtig. "
            "Zwei-Boxer: Nehme beide (dominante Strategie). Ein-Boxer: Nehme nur B (hoeherer Erwartungswert). "
            "Zeigt den Konflikt zwischen Kausalitaet und Evidenzbasiertem Denken."
        ),
        "kategorie": "Entscheidung",
        "link": "/raetsel/newcomb",
    },
    {
        "id": "nullsummenspiel",
        "titel": "Nullsummenspiel",
        "definition": (
            "Spiel, in dem die Summe aller Gewinne und Verluste gleich null ist: "
            "Was einer gewinnt, verliert ein anderer exakt. Beispiele: Schere-Stein-Papier, Poker, "
            "Matching Pennies. Gegenteil: Positivsummenspiel (alle koennen gewinnen). "
            "Verhandlungen werden oft faelschlicherweise als Nullsumme betrachtet, "
            "aber tatsaechlich gibt es meistens Pareto-Verbesserungen."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "pareto-optimal",
        "titel": "Pareto-Optimalitaet",
        "definition": (
            "Ein Zustand ist Pareto-optimal, wenn niemand besser gestellt werden kann, "
            "ohne jemand anderen schlechter zu stellen. Benannt nach Vilfredo Pareto (1906). "
            "Wichtig: Pareto-Optimalitaet sagt nichts ueber Gleichheit oder Fairness - "
            "ein Zustand, bei dem einer alles hat, kann Pareto-optimal sein."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "priming",
        "titel": "Priming",
        "definition": (
            "Unbewusste Aktivierung von Konzepten oder Erinnerungen durch vorherige Reize, "
            "die nachfolgende Gedanken und Verhaltensweisen beeinflusst. "
            "Bargh et al. (1996): Versuchspersonen, die mit Woertern ueber Alter geprimt wurden, "
            "liefen danach langsamer. Praktisch: Reihenfolge von Fragen in Befragungen beeinflusst Antworten."
        ),
        "kategorie": "Psychologie",
        "link": "/raetsel/priming",
    },
    {
        "id": "prospect-theory",
        "titel": "Prospect Theory",
        "definition": (
            "Daniel Kahneman & Amos Tversky (1979, Nobelpreis 2002): Menschen bewerten Gewinne und Verluste "
            "relativ zu einem Referenzpunkt, nicht absolut. Kerneinsichten: (1) Verluste wiegen etwa doppelt "
            "so schwer wie gleich grosse Gewinne (Verlustaversion). (2) Grenznutzen nimmt ab. "
            "(3) Kleine Wahrscheinlichkeiten werden ueberschaetzt, mittlere unterschaetzt."
        ),
        "kategorie": "Entscheidung",
        "link": "/grundlagen",
    },
    {
        "id": "quantenmechanik",
        "titel": "Quantenmechanik",
        "definition": (
            "Physikalische Theorie, die das Verhalten sehr kleiner Teilchen (Elektronen, Photonen, Atome) "
            "beschreibt. Unterscheidet sich fundamental von klassischer Physik: Teilchen haben keine "
            "exakten Positionen und Impulse gleichzeitig (Heisenbergsche Unschaerferelation), "
            "existieren in Superpositionen und zeigen Tunneleffekte. "
            "Grundlage fuer Laser, Transistoren, MRT und Quantencomputer."
        ),
        "kategorie": "Physik",
        "link": "/raetsel/schroedinger",
    },
    {
        "id": "regression-zur-mitte",
        "titel": "Regression zur Mitte",
        "definition": (
            "Extreme Messwerte neigen bei wiederholter Messung dazu, naeher am Durchschnitt zu liegen, "
            "auch ohne externe Ursache. Francis Galton (1886) bei Koerpergroesse. "
            "Praktische Falle: Wenn ein Schueler nach schlechter Leistung besser wird, "
            "ist das oft Regression zur Mitte, nicht der Effekt von Lob oder Strafe."
        ),
        "kategorie": "Statistik",
        "link": "/raetsel/regression-zur-mitte",
    },
    {
        "id": "rubinstein-bargaining",
        "titel": "Rubinstein-Bargaining",
        "definition": (
            "Sequentielles Verhandlungsmodell (Ariel Rubinstein, 1982): Zwei Spieler wechseln sich mit "
            "Angeboten ab. Warten kostet durch Diskontrate. "
            "Gleichgewicht: Spieler 1 erhaelt den groesseren Anteil. "
            "Kerneinsicht: Geduld ist Macht. Wer weniger dringend auf das Ergebnis wartet, erhaelt mehr."
        ),
        "kategorie": "Verhandlung",
        "link": "/grundlagen",
    },
    {
        "id": "reine-strategie",
        "titel": "Reine Strategie",
        "definition": (
            "Eine Strategie, bei der ein Spieler immer dieselbe Aktion waehlt, ohne Zufall. "
            "Gegenteil: Gemischte Strategie (randomisiert). In vielen Spielen gibt es kein reines "
            "Nash-Gleichgewicht, weshalb gemischte Strategien notwendig werden."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "satisficing",
        "titel": "Satisficing",
        "definition": (
            "Herbert Simons Begriff (1956): Die erste 'hinreichend gute' Option waehlen, "
            "statt alle Moeglichkeiten zu analysieren. Kombination von 'satisfy' und 'suffice'. "
            "Rational bei begrenzter Zeit und Information, erklaert viele reale Entscheidungen, "
            "die von Erwartungswert-Maximierung abweichen."
        ),
        "kategorie": "Entscheidung",
        "link": "/grundlagen",
    },
    {
        "id": "screening",
        "titel": "Screening",
        "definition": (
            "Die uninformierte Seite bietet verschiedene Vertragsoptionen an, sodass "
            "verschiedene Typen die fuer sie passende Option waehlen und sich dadurch selbst offenbaren. "
            "Beispiel: Fluggesellschaften bieten guenstige Tickets mit Einschraenkungen an, "
            "nur Freizeitreisende waehlen sie; Geschaeftsreisende zahlen mehr fuer Flexibilitaet."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "signaling",
        "titel": "Signaling",
        "definition": (
            "Informationsuebermittlung durch glaubwuerdige, oft kostspielige Handlungen. "
            "Michael Spence (Nobelpreis 2001): Universitaetsabschluss als Signal fuer Arbeitgeber, "
            "nicht weil er zwingend Produktivitaet steigert, sondern weil er fuer weniger faehige "
            "Kandidaten zu teuer waere. Glaubwuerdiges Signal muss fuer den sendenden Typ billiger sein."
        ),
        "kategorie": "Spieltheorie",
        "link": "/grundlagen",
    },
    {
        "id": "simpson-paradoxon",
        "titel": "Simpson-Paradoxon",
        "definition": (
            "Statistisches Phaenomen: Zusammenhang in Subgruppen kann verschwinden oder sich umkehren, "
            "wenn die Gruppen zusammengefasst werden. "
            "Historisches Beispiel: UCB 1973 - Maenner wurden haeufiger aufgenommen als Frauen, "
            "aber in jedem Fachbereich einzeln betrachtet stimmte das Gegenteil. "
            "Ursache: Confounding Variable (Frauen bewarben sich auf andere Faecher)."
        ),
        "kategorie": "Statistik",
        "link": "/raetsel/simpson",
    },
    {
        "id": "spielerfehlschluss",
        "titel": "Spielerfehlschluss",
        "definition": (
            "Irrtum: Wenn ein Zufallsereignis oft hintereinander eingetreten ist, "
            "glaube ich, das Gegenteil sei nun faellig. 1913, Monte Carlo: Roulette zeigte 26x Schwarz. "
            "Spieler setzten Millionen auf Rot - und verloren. "
            "Fakten: Unabhaengige Ereignisse haben kein Gedaechtnis. Die Muenze weiss nicht, was vorhin war."
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/spielerfehlschluss",
    },
    {
        "id": "strohmann",
        "titel": "Strohmann-Argument",
        "definition": (
            "Rhetorischer Trugschluss: Die Position des Gegners wird falsch oder uebertrieben dargestellt, "
            "dann wird die verfaelschte Version widerlegt. "
            "Gegenstrategie: Statt den 'Strohmann' zu bekaempfen, auf das echte Argument hinweisen. "
            "Gegenteil: Steel-Manning - die staerkste moegliche Version des Gegenarguments angreifen."
        ),
        "kategorie": "Rhetorik",
        "link": "/raetsel/trugschluesse",
    },
    {
        "id": "sunk-cost",
        "titel": "Sunk Cost Fallacy",
        "definition": (
            "Fehler: Bereits ausgegebene Kosten (die nicht mehr rueckgaengig zu machen sind) "
            "beeinflussen zukuenftige Entscheidungen. Rational: Nur zukuenftige Kosten und Ertraege zaehlen. "
            "Real: 'Ich habe schon so viel investiert, jetzt kann ich nicht aufhoeren.' "
            "Klassisch in der Dollar-Auktion oder beim Weiterfuehren schlechter Projekte."
        ),
        "kategorie": "Entscheidung",
        "link": "/spiele/dollarauktion",
    },
    {
        "id": "superposition",
        "titel": "Superposition",
        "definition": (
            "In der Quantenmechanik kann ein Teilchen oder System in mehreren Zustaenden gleichzeitig existieren. "
            "Ein Elektron ist nicht an Ort A oder Ort B, es ist an beiden Orten gleichzeitig "
            "(mit bestimmten Wahrscheinlichkeiten), bis es gemessen wird. "
            "Schroedinger wollte mit seiner Katze zeigen, wie seltsam es waere, "
            "wenn dieses Prinzip auf makroskopische Objekte zutreffen wuerde."
        ),
        "kategorie": "Physik",
        "link": "/raetsel/schroedinger",
    },
    {
        "id": "survivorship-bias",
        "titel": "Survivorship Bias",
        "definition": (
            "Fehler durch Betrachtung nur der erfolgreichen Faelle - die gescheiterten werden uebersehen. "
            "Klassisches Beispiel: Abraham Wald im 2. Weltkrieg - Panzerstellen an zurueckgekehrten Flugzeugen "
            "waren falsch; die Flugzeuge mit Treffern an anderen Stellen waren nie zurueckgekehrt. "
            "Anwendung: Ueberlebende Hedgefonds scheinen brillant; die Dutzenden die scheiterten, "
            "sind aus dem Datensatz verschwunden."
        ),
        "kategorie": "Statistik",
        "link": "/raetsel/survivorship-bias",
    },
    {
        "id": "tit-for-tat",
        "titel": "Tit-for-Tat",
        "definition": (
            "Strategie im wiederholten Gefangenendilemma (Robert Axelrod, 1984): "
            "Kooperiere beim ersten Zug, dann tue in jedem weiteren Zug genau das, was der Gegner "
            "im vorherigen Zug getan hat. Einfach, fair (kein erster Verrat), vergebend (vergisst nach einem Zug). "
            "Gewann Axelrods Computer-Turnier gegen komplexere Strategien."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/gefangenendilemma",
    },
    {
        "id": "trittbrettfahrer",
        "titel": "Trittbrettfahrer-Problem",
        "definition": (
            "Wer profitiert von einem oeffentlichen Gut (Strasse, Verteidigung, saubere Luft), "
            "ohne dazu beizutragen. Wenn alle so denken, wird das Gut nicht bereitgestellt. "
            "Kernproblem der Oeffentliche-Gueter-Spiele und vieler realer Kooperationsdilemmata."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/public-goods",
    },
    {
        "id": "ultimatumspiel",
        "titel": "Ultimatumspiel",
        "definition": (
            "Proposer teilt einen Betrag auf. Responder kann annehmen oder ablehnen, "
            "bei Ablehnung bekommen beide nichts. Rein rationale Theorie: Proposer bietet minimalen Betrag, "
            "Responder nimmt an (besser als nichts). Experiment: Angebote unter 20-30% werden oft abgelehnt. "
            "Zeigt, dass Fairness fuer Menschen einen echten Nutzenwert hat."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/ultimatum",
    },
    {
        "id": "unabhaengige-ereignisse",
        "titel": "Unabhaengige Ereignisse",
        "definition": (
            "Zwei Ereignisse sind unabhaengig, wenn das Eintreten des einen die Wahrscheinlichkeit "
            "des anderen nicht beeinflusst: P(A und B) = P(A) x P(B). "
            "Wichtig: Muenzwuerfe sind unabhaengig, das letzte Ergebnis hat keine Auswirkung auf das naechste. "
            "Kern des Spielerfehlschlusses."
        ),
        "kategorie": "Wahrscheinlichkeit",
        "link": "/raetsel/spielerfehlschluss",
    },
    {
        "id": "verlustaversion",
        "titel": "Verlustaversion",
        "definition": (
            "Aus der Prospect Theory: Verluste schmerzen psychologisch etwa doppelt so stark, "
            "wie gleich grosse Gewinne befriedigen. 100 EUR verlieren fuehlt sich schlimmer an "
            "als 100 EUR gewinnen sich gut anfuehlt. "
            "Folge: Menschen meiden Risiken, auch wenn der Erwartungswert positiv ist."
        ),
        "kategorie": "Psychologie",
        "link": "/grundlagen",
    },
    {
        "id": "vickrey-auktion",
        "titel": "Vickrey-Auktion (Zweitpreisauktion)",
        "definition": (
            "Jeder bietet verdeckt seinen Wert. Der Hoechstbietende gewinnt, zahlt aber den zweit-hoechsten Preis. "
            "Spieltheoretisches Ergebnis: Wahrheitsaussage des eigenen Werts ist dominante Strategie. "
            "Kein Anreiz zu ueber- oder unterbieten. William Vickrey (Nobelpreis 1996). "
            "Wird u. a. bei Google-Anzeigenauktionen eingesetzt."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/auktion",
    },
    {
        "id": "wellenfunktion",
        "titel": "Wellenfunktion",
        "definition": (
            "Mathematische Funktion, die den Quantenzustand eines Systems vollstaendig beschreibt. "
            "Das Betragsquadrat gibt die Wahrscheinlichkeit an, das Teilchen an einem bestimmten Ort "
            "oder mit einem bestimmten Impuls zu messen. "
            "Bei einer Messung 'kollabiert' die Wellenfunktion auf einen einzigen Wert."
        ),
        "kategorie": "Physik",
        "link": "/raetsel/schroedinger",
    },
    {
        "id": "winner-fluch",
        "titel": "Fluch des Gewinners",
        "definition": (
            "Bei Common-Value-Auktionen (alle bieten fuer denselben unbekannten Wert) neigt der Gewinner "
            "dazu, zu viel bezahlt zu haben, denn er hatte den optimistischsten Schaetzwert. "
            "Rational: Wenn du weisst, dass du nur gewinnst wenn du am hoechsten geboten hast, "
            "solltest du dein Gebot unter deiner Schaetzung ansetzen."
        ),
        "kategorie": "Spieltheorie",
        "link": "/spiele/gewinner-fluch",
    },
    {
        "id": "zeitdiskontierung",
        "titel": "Zeitdiskontierung",
        "definition": (
            "Menschen und Akteure bewerten zukuenftige Gewinne weniger als gegenwaertige. "
            "Ein Euro heute ist mehr wert als ein Euro morgen. Diskontrate delta: "
            "je naeher delta an 1, desto geduldiger der Akteur; je naeher 0, desto ungeduldiger. "
            "Zentral in Rubinstein-Bargaining: Wer weniger diskontiert, verhandelt staerker."
        ),
        "kategorie": "Entscheidung",
        "link": "/grundlagen",
    },
    {
        "id": "zopa",
        "titel": "ZOPA",
        "definition": (
            "Zone of Possible Agreement - der Bereich zwischen den BATNAs beider Verhandlungsseiten, "
            "in dem eine fuer beide akzeptable Einigung moeglich ist. "
            "Wenn mein BATNA-Wert hoeher ist als deiner, gibt es keine ZOPA und kein Deal ist moeglich. "
            "Ziel in Verhandlungen: ZOPA maximieren durch Erweiterung der Verhandlungsdimensionen."
        ),
        "kategorie": "Verhandlung",
        "link": "/raetsel/batna",
    },
]

GLOSSAR.sort(key=lambda x: x["titel"].lower())
KATEGORIEN = sorted({e["kategorie"] for e in GLOSSAR})
BUCHSTABEN = sorted({e["titel"][0].upper() for e in GLOSSAR})


@router.get("/glossar", response_class=HTMLResponse)
def glossar_view(request: Request):
    return templates.TemplateResponse(
        request,
        "glossar.html",
        {
            "active_page": "glossar",
            "eintraege": GLOSSAR,
            "kategorien": KATEGORIEN,
            "buchstaben": BUCHSTABEN,
        },
    )
