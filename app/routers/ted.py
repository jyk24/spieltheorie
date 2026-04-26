"""TED Insights - Kernkonzepte aus den einflussreichsten TED Talks."""
import random as _random
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/ted")
templates = Jinja2Templates(directory="app/templates")

TED_TALKS = [
    {
        "id": "dan-ariely",
        "sprecher": "Dan Ariely",
        "titel_de": "Sind wir Herr unserer Entscheidungen?",
        "titel_original": "Are We in Control of Our Own Decisions?",
        "jahr": 2008,
        "icon": "🧠",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Dan Ariely zeigt anhand faszinierender Experimente, dass menschliche Entscheidungen "
            "systematisch irrational sind - aber vorhersehbar. Kontext, Vergleiche und die Art der "
            "Praesentation beeinflussen uns staerker als wir denken. Wer diese Muster kennt, kann sie "
            "sowohl erkennen als auch gezielt nutzen."
        ),
        "kernkonzept": "Vorhersehbare Irrationalitaet",
        "schluessel_erkenntnis": "Irrationales Verhalten folgt erkennbaren Mustern - wer sie kennt, kann Entscheidungen gezielt gestalten.",
        "anwendung": "In Verhandlungen praegt der erste genannte Preis (Anker) alle weiteren Einschaetzungen - nutze diesen Effekt bewusst.",
        "ted_url": "https://www.ted.com/talks/dan_ariely_are_we_in_control_of_our_own_decisions",
        "verwandte_raetsel": ["anker-experiment", "framing", "allais"],
        "quiz": [
            {
                "frage": "Was versteht Ariely unter 'Predictable Irrationality'?",
                "optionen": [
                    {"text": "Menschen sind manchmal zufaellig irrational", "korrekt": False},
                    {"text": "Irrationales Verhalten folgt systematischen, vorhersehbaren Mustern", "korrekt": True},
                    {"text": "Nur gestresste Menschen entscheiden irrational", "korrekt": False},
                    {"text": "Experten sind immun gegen Irrationalitaet", "korrekt": False},
                ],
                "erklaerung": "Arielys Kernthese: Irrationale Entscheidungen sind kein Zufall. Sie folgen konsistenten Mustern, die man kennen und voraussagen kann.",
            },
            {
                "frage": "Was zeigt Arielys Experiment mit den Organspende-Raten in Europa?",
                "optionen": [
                    {"text": "Laender mit mehr Aufklaerung haben hoehere Spendenraten", "korrekt": False},
                    {"text": "Opt-out-Formulare erzeugen deutlich hoehere Spendenraten als Opt-in", "korrekt": True},
                    {"text": "Finanzielle Anreize steigern die Bereitschaft am staerksten", "korrekt": False},
                    {"text": "Junge Menschen spenden haeufiger als aeltere", "korrekt": False},
                ],
                "erklaerung": "Laender mit Opt-out-System (z.B. Oesterreich: 99%) haben dramatisch hoehere Raten als Opt-in-Laender (z.B. Deutschland: 12%). Die Default-Option entscheidet.",
            },
            {
                "frage": "Welchen Effekt demonstriert Ariely mit dem Economist-Abonnement-Experiment?",
                "optionen": [
                    {"text": "Guenstigere Optionen werden fast immer bevorzugt", "korrekt": False},
                    {"text": "Eine unattraktive Koederoption laesst eine andere Option besser aussehen", "korrekt": True},
                    {"text": "Menschen lesen lieber gedruckte als digitale Medien", "korrekt": False},
                    {"text": "Buendelung von Produkten verwirrt Kunden", "korrekt": False},
                ],
                "erklaerung": "Der 'Decoy Effect': Eine schlechte Option (Print allein, teuer) laesst eine andere Option (Print+Digital, gleicher Preis) viel attraktiver wirken.",
            },
            {
                "frage": "Was ist der 'Zero Price Effect' nach Ariely?",
                "optionen": [
                    {"text": "Kostenlose Produkte haben keinen wahrgenommenen Nutzen", "korrekt": False},
                    {"text": "Kostenlose Optionen werden ueberproportional stark bevorzugt", "korrekt": True},
                    {"text": "Menschen misstrauen Gratis-Angeboten grundsaetzlich", "korrekt": False},
                    {"text": "Preise nahe null werden genauso wahrgenommen wie Preise bei null", "korrekt": False},
                ],
                "erklaerung": "Sobald etwas gratis ist, steigt die Nachfrage sprunghaft - weit mehr als durch einen minimalen Preisunterschied erklaerbar waere. 'Kostenlos' loest eine emotionale Reaktion aus.",
            },
            {
                "frage": "Was folgt laut Ariely fuer Verhandlungen und Preisgestaltung?",
                "optionen": [
                    {"text": "Wer zuerst ein Angebot macht, ist immer im Nachteil", "korrekt": False},
                    {"text": "Der erste genannte Preis (Anker) praegt alle weiteren Einschaetzungen stark", "korrekt": True},
                    {"text": "Emotionen sollten aus Verhandlungen herausgehalten werden", "korrekt": False},
                    {"text": "Rationale Argumente sind stets ausschlaggebend", "korrekt": False},
                ],
                "erklaerung": "Arielys Forschung bestaetigt den Ankereffekt: Wer den ersten Preis nennt, setzt den Rahmen fuer die gesamte Verhandlung.",
            },
        ],
    },
    {
        "id": "daniel-kahneman",
        "sprecher": "Daniel Kahneman",
        "titel_de": "Das Raetsel von Erleben und Erinnern",
        "titel_original": "The Riddle of Experience vs. Memory",
        "jahr": 2010,
        "icon": "🔬",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Nobelpreistraeger Daniel Kahneman unterscheidet das 'erlebende Selbst' (wie wir uns im Moment fuehlen) "
            "vom 'erinnernden Selbst' (wie wir Erlebnisse im Nachhinein bewerten). Die Peak-End-Regel zeigt: "
            "Wir erinnern uns vor allem an den Hoehepunkt und das Ende - nicht an den Durchschnitt."
        ),
        "kernkonzept": "Erlebendes vs. Erinnerndes Selbst / Peak-End-Regel",
        "schluessel_erkenntnis": "Was wir erinnern, ist nicht was wir erlebt haben - der Peak und das Ende praegenunser Urteil.",
        "anwendung": "Verhandlungen sollten mit einem starken positiven Abschluss enden - das ist es, was die andere Seite im Gedaechtnis behalten wird.",
        "ted_url": "https://www.ted.com/talks/daniel_kahneman_the_riddle_of_experience_vs_memory",
        "verwandte_raetsel": ["kognitive-dissonanz", "dunning-kruger", "framing"],
        "quiz": [
            {
                "frage": "Was unterscheidet das 'erlebende Selbst' vom 'erinnernden Selbst'?",
                "optionen": [
                    {"text": "Das erlebende Selbst ist rationaler", "korrekt": False},
                    {"text": "Das erlebende Selbst bewertet den Moment; das erinnernde Selbst bewertet die Geschichte davon", "korrekt": True},
                    {"text": "Das erinnernde Selbst ist praeziser und realistischer", "korrekt": False},
                    {"text": "Beide Selbste kommen zum gleichen Ergebnis", "korrekt": False},
                ],
                "erklaerung": "Kahneman zeigt, dass wir zwei 'Ichs' haben: eines das Moment fuer Moment erlebt, und eines das Geschichten erzaehlt und Entscheidungen trifft.",
            },
            {
                "frage": "Was besagt die Peak-End-Regel?",
                "optionen": [
                    {"text": "Wir erinnern uns am besten an den Anfang eines Erlebnisses", "korrekt": False},
                    {"text": "Wir erinnern uns vor allem an den emotionalen Hoehepunkt und das Ende", "korrekt": True},
                    {"text": "Laengere Erlebnisse werden besser erinnert als kuerzere", "korrekt": False},
                    {"text": "Wir mitteln unbewusst alle Momente eines Erlebnisses", "korrekt": False},
                ],
                "erklaerung": "Kahnemans Kolonoskopie-Experiment zeigte: Patienten bewerten einenlaengeren Eingriff als angenehmer, wenn er mit weniger Schmerz endet - obwohl der Gesamtschmerz groesser war.",
            },
            {
                "frage": "Was zeigt Kahnemans Darm-Experiment (Kolonoskopie) ueber Erinnerungen?",
                "optionen": [
                    {"text": "Schmerz wird immer praezise erinnert", "korrekt": False},
                    {"text": "Ein laengerer Eingriff mit besserem Ende wird als weniger schlimm erinnert", "korrekt": True},
                    {"text": "Kurze intensive Erfahrungen bleiben laenger im Gedaechtnis", "korrekt": False},
                    {"text": "Patienten erinnern den Anfang am deutlichsten", "korrekt": False},
                ],
                "erklaerung": "Das erinnernde Selbst ignoriert die Dauer fast vollstaendig ('Duration Neglect') und gewichtet nur Peak und Ende.",
            },
            {
                "frage": "Wie nennt Kahneman die zwei Denksysteme des Gehirns?",
                "optionen": [
                    {"text": "Rational und Emotional", "korrekt": False},
                    {"text": "System 1 (schnell, intuitiv) und System 2 (langsam, analytisch)", "korrekt": True},
                    {"text": "Bewusst und Unbewusst", "korrekt": False},
                    {"text": "Links und Rechts", "korrekt": False},
                ],
                "erklaerung": "System 1 laeuft automatisch und schnell - ideal fuer Routineentscheidungen. System 2 ist langsam und anstrengend - notwendig fuer komplexe Analyse.",
            },
            {
                "frage": "Welche praktische Konsequenz hat die Peak-End-Regel fuer Praesentationen?",
                "optionen": [
                    {"text": "Der Anfang ist am wichtigsten fuer den ersten Eindruck", "korrekt": False},
                    {"text": "Ein starker Abschluss praegt die gesamte Bewertung nachhaltig", "korrekt": True},
                    {"text": "Gleichmaessige Qualitaet ist wichtiger als ein guter Abschluss", "korrekt": False},
                    {"text": "Die Laenge der Praesentation bestimmt die Erinnerung", "korrekt": False},
                ],
                "erklaerung": "Da das erinnernde Selbst das Ende uebergewichtet, sollte jede Praesentation, Verhandlung oder Begegnung mit einem positiven Hoehepunkt enden.",
            },
        ],
    },
    {
        "id": "barry-schwartz",
        "sprecher": "Barry Schwartz",
        "titel_de": "Das Paradox der Wahl",
        "titel_original": "The Paradox of Choice",
        "jahr": 2005,
        "icon": "🛒",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Mehr Auswahl bedeutet nicht mehr Freiheit und Glueck - sondern haeufig Laehmung und Unzufriedenheit. "
            "Barry Schwartz zeigt, warum uns 200 Jeans-Sorten ungluecklicher machen als 3. "
            "Maximierer (die beste Option suchen) leiden staerker als Satisficer (die erste gute Option nehmen)."
        ),
        "kernkonzept": "Paradox der Wahl / Maximizer vs. Satisficer",
        "schluessel_erkenntnis": "Zu viele Optionen erhoehen Entscheidungslahmung, Bedauern und Unglueck - weniger Auswahl kann gluecklicher machen.",
        "anwendung": "In Verhandlungen: Zu viele Optionen verwirren. Wenige, klar strukturierte Angebote erleichtern Einigung und reduzieren Nachbedauern.",
        "ted_url": "https://www.ted.com/talks/barry_schwartz_the_paradox_of_choice",
        "verwandte_raetsel": ["allais", "ellsberg"],
        "quiz": [
            {
                "frage": "Was ist der Kern von Schwartz' 'Paradox der Wahl'?",
                "optionen": [
                    {"text": "Mehr Auswahl fuehrt immer zu besseren Entscheidungen", "korrekt": False},
                    {"text": "Zu viele Optionen fuehren zu Entscheidungslahmung und geringerer Zufriedenheit", "korrekt": True},
                    {"text": "Menschen bevorzugen grundsaetzlich weniger Optionen", "korrekt": False},
                    {"text": "Auswahl ist nur fuer Experten problematisch", "korrekt": False},
                ],
                "erklaerung": "Schwartz' These: Waehrend ein Minimum an Auswahl Freiheit ermoeglicht, macht ueberwaltigendeAuswahl uns ungluecklicher, nicht gluecklicher.",
            },
            {
                "frage": "Was unterscheidet einen 'Maximizer' von einem 'Satisficer'?",
                "optionen": [
                    {"text": "Maximizer sind rationaler und zufriedener", "korrekt": False},
                    {"text": "Maximizer suchen die beste Option und sind oft ungluecklicher; Satisficer akzeptieren 'gut genug'", "korrekt": True},
                    {"text": "Satisficer geben schneller auf und sind weniger erfolgreich", "korrekt": False},
                    {"text": "Beide kommen zum gleichen Ergebnis, nur schneller oder langsamer", "korrekt": False},
                ],
                "erklaerung": "Herbert Simons 'Satisficing' (satisfy + suffice): Die erste hinreichend gute Option nehmen macht gluecklicher als endlos nach dem Optimum zu suchen.",
            },
            {
                "frage": "Was ist 'Opportunity Cost' im Kontext der Wahl?",
                "optionen": [
                    {"text": "Die Kosten fuer eine falsche Entscheidung", "korrekt": False},
                    {"text": "Der Wert der nicht gewaehlten Alternativen, der die Zufriedenheit mit der Wahl mindert", "korrekt": True},
                    {"text": "Die Zeit, die fuer eine Entscheidung benoetigt wird", "korrekt": False},
                    {"text": "Die finanziellen Kosten einer Entscheidung", "korrekt": False},
                ],
                "erklaerung": "Je mehr Optionen, desto staerker denken wir an die aufgegebenen Alternativen - und desto weniger geniessen wir die getroffene Wahl.",
            },
            {
                "frage": "Was zeigt Schwartz mit dem Marmeladen-Experiment (Iyengar & Lepper)?",
                "optionen": [
                    {"text": "Kunden kaufen mehr, wenn es mehr Sorten gibt", "korrekt": False},
                    {"text": "Mehr Optionen (24 Sorten) fuehren zu weniger Kaeufen als weniger Optionen (6 Sorten)", "korrekt": True},
                    {"text": "Preis ist entscheidender als Auswahl", "korrekt": False},
                    {"text": "Menschen kaufen immer die teuerste Option", "korrekt": False},
                ],
                "erklaerung": "Bei 6 Sorten kauften 30% der interessierten Kunden; bei 24 Sorten nur 3%. Choice Overload laehmte die Kaufentscheidung.",
            },
            {
                "frage": "Welche Loesung schlaegt Schwartz fuer das Paradox der Wahl vor?",
                "optionen": [
                    {"text": "Immer mehr Informationen sammeln vor einer Entscheidung", "korrekt": False},
                    {"text": "Aktiv Optionen einschraenken und Satisficing statt Maximizing betreiben", "korrekt": True},
                    {"text": "Entscheidungen delegieren, wann immer moeglich", "korrekt": False},
                    {"text": "Nur bei kleinen Entscheidungen waehlen, bei grossen keine Wahl treffen", "korrekt": False},
                ],
                "erklaerung": "Schwartz empfiehlt: Regeln setzen (z.B. immer die erste gute Option nehmen), Optionen aktiv begrenzen und auf Bedauern verzichten - das macht gluecklicher.",
            },
        ],
    },
    {
        "id": "dan-gilbert",
        "sprecher": "Dan Gilbert",
        "titel_de": "Die erstaunliche Wissenschaft des Gluecks",
        "titel_original": "The Surprising Science of Happiness",
        "jahr": 2004,
        "icon": "😊",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Harvard-Psychologe Dan Gilbert zeigt, dass Menschen ein 'psychologisches Immunsystem' besitzen, "
            "das sie gluecklich macht - egal was passiert. Synthetisches Glueck (das wir erzeugen) ist genauso "
            "real wie natuerliches Glueck (das wir finden). Wir ueberschaetzen systematisch, wie ungluecklich uns "
            "negative Ereignisse machen werden."
        ),
        "kernkonzept": "Synthetisches Glueck / Affektive Prognose",
        "schluessel_erkenntnis": "Menschen koennen Glueck synthetisieren - und unterschaetzen diese Faehigkeit systematisch.",
        "anwendung": "Entscheide schnell und finalisiere Entscheidungen: Reversible Entscheidungen machen ungluecklicher als irreversible, weil wir nicht aufhoeren zu vergleichen.",
        "ted_url": "https://www.ted.com/talks/dan_gilbert_the_surprising_science_of_happiness",
        "verwandte_raetsel": ["framing", "regression-zur-mitte"],
        "quiz": [
            {
                "frage": "Was ist 'synthetisches Glueck' nach Gilbert?",
                "optionen": [
                    {"text": "Kuenstliches Glueck durch Drogen oder Ablenkung", "korrekt": False},
                    {"text": "Glueck, das wir selbst erzeugen, indem wir unsere Sichtweise auf ein Ergebnis anpassen", "korrekt": True},
                    {"text": "Oberflachliches Glueck ohne echte Grundlage", "korrekt": False},
                    {"text": "Glueck durch Simulation und Vorstellung", "korrekt": False},
                ],
                "erklaerung": "Synthetisches Glueck entsteht, wenn wir das Beste aus dem machen, was wir haben. Gilbert zeigt: Es ist genauso real und dauerhaft wie 'natuerliches' Glueck.",
            },
            {
                "frage": "Was zeigt Gilberts Forschung ueber 'Affective Forecasting'?",
                "optionen": [
                    {"text": "Menschen prognostizieren ihre Gefuehle akkurat", "korrekt": False},
                    {"text": "Menschen ueberschaetzen systematisch, wie stark und lange negative Ereignisse sie ungluecklich machen", "korrekt": True},
                    {"text": "Positive Ereignisse werden genauer prognostiziert als negative", "korrekt": False},
                    {"text": "Nur Optimisten liegen bei emotionalen Prognosen falsch", "korrekt": False},
                ],
                "erklaerung": "'Impact Bias': Wir glauben, dass schlechte Nachrichten (Krankheit, Jobverlust, Trennungen) uns weit laenger ungluecklich machen werden - aber unser psychologisches Immunsystem reguliert uns schnell zurueck.",
            },
            {
                "frage": "Was zeigt das Experiment mit Lotteriegewinnern und Querschnittsgelaehmten?",
                "optionen": [
                    {"text": "Lotteriegewinner sind dauerhaft gluecklicher", "korrekt": False},
                    {"text": "Beide Gruppen kommen nach einem Jahr auf aehnliche Gluecksniveaus zurueck", "korrekt": True},
                    {"text": "Querschnittsgelaehmte sind langfristig ungluecklicher", "korrekt": False},
                    {"text": "Glueck haengt vor allem von aeusseren Umstaenden ab", "korrekt": False},
                ],
                "erklaerung": "Brickman et al. (1978): Ein Jahr nach dem Ereignis waren Lotteriegewinner und Querschnittsgelaehmte in ihrer Lebenszufriedenheit nicht mehr weit auseinander.",
            },
            {
                "frage": "Warum macht laut Gilbert eine irreversible Entscheidung gluecklicher als eine reversible?",
                "optionen": [
                    {"text": "Weil irreversible Entscheidungen groessere Konsequenzen haben", "korrekt": False},
                    {"text": "Weil bei irreversiblen Entscheidungen das Vergleichen endet und das Annehmen beginnt", "korrekt": True},
                    {"text": "Weil man bei reversiblen Entscheidungen mehr Optionen hat", "korrekt": False},
                    {"text": "Weil irreversible Entscheidungen rationaler sind", "korrekt": False},
                ],
                "erklaerung": "Reversibilitaet haelt uns im Vergleichsmodus - wir fragen uns staendig 'waere die andere Option besser gewesen?' und synthetisieren daher weniger Glueck.",
            },
            {
                "frage": "Was ist der Kern von Gilberts These fuer persoenliche Entscheidungen?",
                "optionen": [
                    {"text": "Man soll immer die beste messbare Option waehlen", "korrekt": False},
                    {"text": "Wir werden gluecklicher sein als wir erwarten, egal wie die Entscheidung ausgeht", "korrekt": True},
                    {"text": "Glueck haengt primaer von materiellen Faktoren ab", "korrekt": False},
                    {"text": "Schnelle Entscheidungen fuehren immer zu Bedauern", "korrekt": False},
                ],
                "erklaerung": "Das psychologische Immunsystem arbeitet zuverlassig: Wir sind resilient und anpassungsfaehig - und unterschaetzen das systematisch.",
            },
        ],
    },
    {
        "id": "daniel-pink",
        "sprecher": "Daniel Pink",
        "titel_de": "Das Raetsel der Motivation",
        "titel_original": "The Puzzle of Motivation",
        "jahr": 2009,
        "icon": "🎯",
        "kategorie": "Fuehrung",
        "kurzfassung": (
            "Daniel Pink zeigt, dass extrinsische Belohnungen (Geld, Boni) fuer kreative Aufgaben kontraproduktiv sind. "
            "Die Wissenschaft der Motivation zeigt: Autonomie (selbst entscheiden), Mastery (besser werden) "
            "und Purpose (sinnvoller Beitrag) sind die wahren Triebkraefte intrinsischer Motivation."
        ),
        "kernkonzept": "Autonomy-Mastery-Purpose",
        "schluessel_erkenntnis": "Fuer kreative Arbeit schaden extrinsische Belohnungen oft - Autonomie, Mastery und Purpose sind die wirksameren Motivatoren.",
        "anwendung": "In Verhandlungen ueber Arbeitsbedingungen und Kooperationen: Mehr Eigenverantwortung und Sinnhaftigkeit motivieren staerker als Gehaltsbonus.",
        "ted_url": "https://www.ted.com/talks/dan_pink_the_puzzle_of_motivation",
        "verwandte_raetsel": ["kognitive-dissonanz"],
        "quiz": [
            {
                "frage": "Was zeigt das 'Kerzen-Problem' (Duncker) in Bezug auf Motivation?",
                "optionen": [
                    {"text": "Finanzielle Anreize verbessern die Loesungsfindung", "korrekt": False},
                    {"text": "Hoehe Belohnungen verschlechtern die Leistung bei Aufgaben, die kreatives Denken erfordern", "korrekt": True},
                    {"text": "Zeitdruck foerdert kreative Loesungen", "korrekt": False},
                    {"text": "Gruppen loesen kreative Probleme besser als Einzelpersonen", "korrekt": False},
                ],
                "erklaerung": "Wenn 'funktionales Fixieren' ueberwunden werden muss (die Schachtel als Ablage nutzen, nicht nur als Behaelter), verschlechtern Geldbelohnungen die Leistung - weil Fokus auf Belohnung kreatives Denken einengt.",
            },
            {
                "frage": "Welche drei Elemente bilden Pinks Modell intrinsischer Motivation?",
                "optionen": [
                    {"text": "Gehalt, Sicherheit, Anerkennung", "korrekt": False},
                    {"text": "Autonomie, Mastery, Purpose", "korrekt": True},
                    {"text": "Ziele, Feedback, Belohnung", "korrekt": False},
                    {"text": "Freiheit, Wettbewerb, Erfolg", "korrekt": False},
                ],
                "erklaerung": "Autonomie = selbst entscheiden wie/wann/was. Mastery = Meisterschaft in etwas Wichtigem anstreben. Purpose = das eigene Tun als Teil von etwas Groesserem erleben.",
            },
            {
                "frage": "Was ist die 'Karotte-und-Stock'-These, die Pink kritisiert?",
                "optionen": [
                    {"text": "Strafe und Belohnung sind gleichwertig wirksam", "korrekt": False},
                    {"text": "Die Annahme, dass extrinsische Belohnungen (Geld, Boni) immer die beste Motivation liefern", "korrekt": True},
                    {"text": "Mitarbeiter benoetigen klare Hierarchien", "korrekt": False},
                    {"text": "Intrinsische Motivation existiert nur bei Kuenstlern", "korrekt": False},
                ],
                "erklaerung": "Pink zeigt anhand von 40 Jahren Forschung: Das Management-Modell des 20. Jahrhunderts (belohnen und bestrafen) funktioniert fuer kreative Wissensarbeit nicht.",
            },
            {
                "frage": "Was ist 'Mastery' in Pinks Modell?",
                "optionen": [
                    {"text": "Das Erreichen einer Fuehrungsposition", "korrekt": False},
                    {"text": "Das Streben, in etwas Bedeutungsvollem immer besser zu werden", "korrekt": True},
                    {"text": "Das Beherrschen vieler verschiedener Faehigkeiten", "korrekt": False},
                    {"text": "Die Anerkennung durch andere fuer Leistung", "korrekt": False},
                ],
                "erklaerung": "Mastery ist asymptotisch - man naehert sich dem Ideal immer mehr an, erreicht es aber nie ganz. Dieser Prozess des Wachsens ist intrinsisch motivierend.",
            },
            {
                "frage": "Was zeigt das Beispiel von Wikipedia und Encarta fuer Pinks These?",
                "optionen": [
                    {"text": "Grosse Unternehmen produzieren immer bessere Produkte", "korrekt": False},
                    {"text": "Intrinsisch motivierte Freiwillige koennen professionell Bezahlte in Qualitaet und Umfang uebertreffen", "korrekt": True},
                    {"text": "Internet-Projekte haben strukturelle Vorteile gegenueber Software", "korrekt": False},
                    {"text": "Microsoft hat seinen Fokus falsch gesetzt", "korrekt": False},
                ],
                "erklaerung": "Wikipedia (Millionen Freiwilliger, kein Gehalt) hat die von Microsoft bezahlte Encarta-Enzyklopaedie verdraengt - ein Paradebeispiel fuer die Kraft von Autonomy, Mastery und Purpose.",
            },
        ],
    },
    {
        "id": "carol-dweck",
        "sprecher": "Carol Dweck",
        "titel_de": "Die Kraft zu glauben, dass man sich verbessern kann",
        "titel_original": "The Power of Believing That You Can Improve",
        "jahr": 2014,
        "icon": "🌱",
        "kategorie": "Kognition",
        "kurzfassung": (
            "Stanford-Psychologin Carol Dweck beschreibt zwei grundlegende Denkweisen: das 'Fixed Mindset' "
            "(Faehigkeiten sind angeboren und unveraenderlich) und das 'Growth Mindset' (Faehigkeiten koennen "
            "durch Einsatz entwickelt werden). Ein einfaches Wort - 'noch nicht' statt 'nicht bestanden' - "
            "kann diesen Unterschied auslosen."
        ),
        "kernkonzept": "Growth Mindset vs. Fixed Mindset",
        "schluessel_erkenntnis": "Wer glaubt, dass Faehigkeiten wachsen koennen, lernt schneller, haelt laenger durch und erreicht mehr.",
        "anwendung": "In Feedbackgespraechen: Lobe den Prozess (Einsatz, Strategie, Ausdauer), nicht die Person oder angeborene Faehigkeiten.",
        "ted_url": "https://www.ted.com/talks/carol_dweck_the_power_of_believing_that_you_can_improve",
        "verwandte_raetsel": ["dunning-kruger", "konfirmationsfehler"],
        "quiz": [
            {
                "frage": "Was kennzeichnet ein 'Fixed Mindset'?",
                "optionen": [
                    {"text": "Die Ueberzeugung, dass Faehigkeiten durch Ueben wachsen", "korrekt": False},
                    {"text": "Die Ueberzeugung, dass Intelligenz und Talent angeboren und unveraenderlich sind", "korrekt": True},
                    {"text": "Eine pessimistische Grundhaltung gegenueber dem Leben", "korrekt": False},
                    {"text": "Mangelnde Bereitschaft, neue Dinge auszuprobieren", "korrekt": False},
                ],
                "erklaerung": "Im Fixed Mindset wird jede Aufgabe zum Test der eigenen Faehigkeiten - Fehler bedrohen das Selbstbild. Deshalb vermeidet man Herausforderungen.",
            },
            {
                "frage": "Was ist die Bedeutung des Wortes 'noch nicht' ('not yet') in Dwecks Forschung?",
                "optionen": [
                    {"text": "Es ist eine hoeflichere Art, Fehler zu beschreiben", "korrekt": False},
                    {"text": "Es signalisiert, dass eine Faehigkeit noch im Wachstum ist - kein Versagen, sondern ein Lernweg", "korrekt": True},
                    {"text": "Es verzoegert notwendiges Feedback", "korrekt": False},
                    {"text": "Es ist nur fuer junge Kinder geeignet", "korrekt": False},
                ],
                "erklaerung": "'Nicht bestanden' gibt ein Urteil. 'Noch nicht' gibt einen Weg. Diese sprachliche Verschiebung foerdert das Growth Mindset und die Ausdauer.",
            },
            {
                "frage": "Welche Art von Lob foerdert ein Growth Mindset?",
                "optionen": [
                    {"text": "Lob fuer Intelligenz ('Du bist so klug!')", "korrekt": False},
                    {"text": "Lob fuer den Prozess (Einsatz, Strategie, Durchhaltevermoegen)", "korrekt": True},
                    {"text": "Kein Lob, um Verwoehnheit zu vermeiden", "korrekt": False},
                    {"text": "Lob fuer das Ergebnis, unabhaengig vom Prozess", "korrekt": False},
                ],
                "erklaerung": "Dwecks Experimente: Kinder, die fuer Intelligenz gelobt wurden, vermieden danach schwierigere Aufgaben. Kinder, die fuer Anstrengung gelobt wurden, suchten groessere Herausforderungen.",
            },
            {
                "frage": "Was zeigen Studien ueber Gehirn-Aktivitaet bei Fixed vs. Growth Mindset-Studenten?",
                "optionen": [
                    {"text": "Fixed-Mindset-Studenten haben generell weniger Gehirnaktivitaet", "korrekt": False},
                    {"text": "Growth-Mindset-Studenten zeigen groessere neuronale Aktivitaet beim Verarbeiten von Fehlern", "korrekt": True},
                    {"text": "Beide Gruppen zeigen identische Gehirnmuster", "korrekt": False},
                    {"text": "Fehler verursachen bei Fixed-Mindset-Studenten mehr Lernaktivitaet", "korrekt": False},
                ],
                "erklaerung": "EEG-Studien zeigen: Growth-Mindset-Studenten verarbeiten Fehler intensiver neurologisch - sie 'nutzen' Fehler als Lernmomente staerker.",
            },
            {
                "frage": "In welchen Kontexten ist das Growth Mindset besonders wirkungsvoll?",
                "optionen": [
                    {"text": "Nur im schulischen Kontext bei Kindern", "korrekt": False},
                    {"text": "In allen Bereichen - von Bildung bis Sport, Fuehrung und persoenlichem Wachstum", "korrekt": True},
                    {"text": "Vor allem bei einfachen, wiederholbaren Aufgaben", "korrekt": False},
                    {"text": "Nur wenn man bereits grundlegende Faehigkeiten besitzt", "korrekt": False},
                ],
                "erklaerung": "Dwecks Forschung erstreckt sich auf Schulen, Unternehmen, Sport und Beziehungen. Das Growth Mindset foerdert ueberall Resilienz, Lernen und Leistung.",
            },
        ],
    },
    {
        "id": "simon-sinek",
        "sprecher": "Simon Sinek",
        "titel_de": "Wie grosse Fuehrungspersoenlichkeiten zur Handlung inspirieren",
        "titel_original": "How Great Leaders Inspire Action",
        "jahr": 2009,
        "icon": "⭕",
        "kategorie": "Fuehrung",
        "kurzfassung": (
            "Simon Sinek praesentiert das 'Golden Circle'-Modell: Inspirierende Unternehmen und Fuehrungskraefte "
            "kommunizieren von innen nach aussen - beginnend mit dem Warum (Purpose), dann dem Wie (Prozess), "
            "dann dem Was (Produkt). Apple verkauft keine Computer, sondern den Glauben daran, den Status quo herauszufordern."
        ),
        "kernkonzept": "Golden Circle: Why - How - What",
        "schluessel_erkenntnis": "Menschen kaufen nicht was du machst, sondern warum du es machst - das Warum spricht das limbische Gehirn an.",
        "anwendung": "In Verhandlungen und Praesentationen: Beginne mit dem Warum (dem Zweck, dem Glauben) - nicht mit Features oder Daten.",
        "ted_url": "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",
        "verwandte_raetsel": [],
        "quiz": [
            {
                "frage": "Was ist der Kern des 'Golden Circle'-Modells von Sinek?",
                "optionen": [
                    {"text": "Erst das Was erklaeren, dann das Wie, dann das Warum", "korrekt": False},
                    {"text": "Inspirierende Kommunikation beginnt mit dem Warum und arbeitet sich nach aussen vor", "korrekt": True},
                    {"text": "Das Wie ist das wichtigste Kommunikationselement", "korrekt": False},
                    {"text": "Alle drei Ebenen sind gleichwertig und koennen beliebig geordnet werden", "korrekt": False},
                ],
                "erklaerung": "Inside-out: Warum (Purpose) -> Wie (Prozess) -> Was (Produkt). Die meisten Unternehmen kommunizieren umgekehrt - und sind damit weniger inspirierend.",
            },
            {
                "frage": "Welchen neurologischen Grund nennt Sinek fuer die Wirkung des 'Warum'?",
                "optionen": [
                    {"text": "Das Warum aktiviert den praefrontalen Kortex fuer rationale Entscheidungen", "korrekt": False},
                    {"text": "Das Warum spricht das limbische Gehirn an, das fuer Gefuehle und Verhalten zustaendig ist", "korrekt": True},
                    {"text": "Das Warum ist leichter zu verarbeiten, weil es kuerzer ist", "korrekt": False},
                    {"text": "Das Warum aktiviert das Belohnungssystem", "korrekt": False},
                ],
                "erklaerung": "Das limbische Gehirn kontrolliert Gefuehle, Vertrauen und Entscheidungen - aber keine Sprache. Deshalb 'fuehlen' wir Entscheidungen oft, bevor wir sie begruenden koennen.",
            },
            {
                "frage": "Wie erklaert Sinek Apples Erfolg mit dem Golden Circle?",
                "optionen": [
                    {"text": "Apple hat ueberlegene Technologie, die andere nicht kopieren koennen", "korrekt": False},
                    {"text": "Apple kommuniziert zuerst seinen Purpose ('den Status quo herausfordern'), dann seine Produkte", "korrekt": True},
                    {"text": "Apples Marketingbudget ist groesser als das der Konkurrenz", "korrekt": False},
                    {"text": "Apple bietet die guenstigsten Produkte im Markt an", "korrekt": False},
                ],
                "erklaerung": "Sinek: 'Everything we do, we believe in challenging the status quo. The way we challenge the status quo is by making products that are beautifully designed and simple to use.' - erst Warum, dann Was.",
            },
            {
                "frage": "Was lehrt das Beispiel der Gebruedern Wright im Vergleich zu Samuel Langley?",
                "optionen": [
                    {"text": "Ressourcen und Finanzierung sind entscheidend fuer Innovationen", "korrekt": False},
                    {"text": "Wer von einem klaren Warum angetrieben wird, erreicht sein Ziel - auch ohne mehr Ressourcen", "korrekt": True},
                    {"text": "Technisches Wissen ist wichtiger als Motivation", "korrekt": False},
                    {"text": "Teamgroesse korreliert mit Innovationserfolg", "korrekt": False},
                ],
                "erklaerung": "Langley hatte Geld, Ruhm, ein Team - aber kein klares Warum. Die Gebruedern Wright hatten keines davon, aber sie glaubten, dass das Fliegen die Welt veraendern wuerde.",
            },
            {
                "frage": "Was ist der 'Tipping Point' in Sineks Modell der Verbreitung von Ideen?",
                "optionen": [
                    {"text": "Der Moment, wenn 50% der Bevoelkerung eine Idee kennen", "korrekt": False},
                    {"text": "Wenn genug Early Adopters (10-15%) eine Idee annehmen, verbreitet sie sich automatisch", "korrekt": True},
                    {"text": "Der Punkt, an dem Massenwerbung einsetzt", "korrekt": False},
                    {"text": "Der Moment, wenn ein Produkt profitabel wird", "korrekt": False},
                ],
                "erklaerung": "Basierend auf Rogers' Diffusion of Innovations: Early Adopters kaufen aus Ueberzeugung (Warum-Resonanz), nicht aus rationalen Gruenden - und bringen andere mit.",
            },
        ],
    },
    {
        "id": "julian-treasure",
        "sprecher": "Julian Treasure",
        "titel_de": "Wie du so sprichst, dass Menschen zuhoeren wollen",
        "titel_original": "How to Speak So That People Want to Listen",
        "jahr": 2013,
        "icon": "🎤",
        "kategorie": "Kommunikation",
        "kurzfassung": (
            "Sound-Experte Julian Treasure benennt die 7 Todsunden der Kommunikation (Klatsch, Urteilen, Negativitaet, "
            "Klagen, Ausreden, Uebertreiben, Dogmatismus) und die 4 Grundlagen kraftvoller Sprache: "
            "HAIL - Honesty, Authenticity, Integrity, Love. Dazu praktische Werkzeuge fuer Stimme und Sprache."
        ),
        "kernkonzept": "HAIL-Prinzipien fuer kraftvolle Kommunikation",
        "schluessel_erkenntnis": "Wer nach HAIL (Ehrlichkeit, Authentizitaet, Integritaet, Zuneigung) spricht, wird gehoert - wer die 7 Todsunden begeht, verliert sein Publikum.",
        "anwendung": "In Verhandlungen: Stimme bewusst einsetzen (Tempo, Tonhoehe, Lautstaerke, Schweigen) und mit Authentizitaet und Direktheit sprechen.",
        "ted_url": "https://www.ted.com/talks/julian_treasure_how_to_speak_so_that_people_want_to_listen",
        "verwandte_raetsel": ["aktives-zuhoeren"],
        "quiz": [
            {
                "frage": "Wofuer steht das Akronym HAIL nach Julian Treasure?",
                "optionen": [
                    {"text": "Help, Ask, Inform, Listen", "korrekt": False},
                    {"text": "Honesty, Authenticity, Integrity, Love", "korrekt": True},
                    {"text": "Harmony, Attention, Impact, Logic", "korrekt": False},
                    {"text": "Height, Articulation, Intonation, Length", "korrekt": False},
                ],
                "erklaerung": "HAIL: Honesty (klar und direkt sprechen), Authenticity (man selbst sein), Integrity (tun was man sagt), Love (das Beste fuer andere wollen).",
            },
            {
                "frage": "Welche der folgenden Verhaltensweisen gehoert zu Treasures '7 Todsunden' der Kommunikation?",
                "optionen": [
                    {"text": "Direktes Feedback geben", "korrekt": False},
                    {"text": "Klagen (Negativitaet ueber die Welt verbreiten)", "korrekt": True},
                    {"text": "Aktiv zuhoeren", "korrekt": False},
                    {"text": "Pausen in der Rede einsetzen", "korrekt": False},
                ],
                "erklaerung": "Die 7 Todsunden: Gossip, Judging, Negativity, Complaining, Excuses, Embroidery (Uebertreiben), Dogmatism. Sie sabotieren jede Kommunikation.",
            },
            {
                "frage": "Was empfiehlt Treasure als taegliche Uebung fuer die Stimme?",
                "optionen": [
                    {"text": "Singen unter der Dusche als Aufwaermung", "korrekt": True},
                    {"text": "Stundenlange Stille vor wichtigen Gespraechen", "korrekt": False},
                    {"text": "Schreien in einem leeren Raum", "korrekt": False},
                    {"text": "Zehn Minuten lautes Vorlesen", "korrekt": False},
                ],
                "erklaerung": "Singen aktiviert und 'oeffnet' die Stimme. Treasure empfiehlt taegliche Stimmubungen, u.a. Aufwaermuebungen wie 'Ba-Be-Bi-Bo-Bu' oder Stimmlippen-Massage.",
            },
            {
                "frage": "Welche vier stimmlichen Werkzeuge nennt Treasure als besonders wirkungsvoll?",
                "optionen": [
                    {"text": "Lautstaerke, Geschwindigkeit, Tonhoehe und Schweigen", "korrekt": True},
                    {"text": "Wortschatz, Grammatik, Aussprache und Gestik", "korrekt": False},
                    {"text": "Augenkontakt, Mimik, Koerpersprache und Abstand", "korrekt": False},
                    {"text": "Humor, Metaphern, Zahlen und Geschichten", "korrekt": False},
                ],
                "erklaerung": "Treasure: Register (tief = Autoritaet), Timbre (warm vs. kalt), Tempo (Pausen fuer Wirkung), Lautstaerke (leise zieht an). Bewusster Einsatz macht den Unterschied.",
            },
            {
                "frage": "Warum empfiehlt Treasure, Konversationen mit 'Hara hachi bu' zu beginnen?",
                "optionen": [
                    {"text": "Es ist ein Aufwaermritual aus Japan", "korrekt": False},
                    {"text": "Er empfiehlt dies nicht - er nennt es als Beispiel fuer kulturelles Wissen", "korrekt": False},
                    {"text": "Er nennt das Prinzip des 80%-Essens als Analogie: Nicht alles aussprechen, Raum lassen", "korrekt": True},
                    {"text": "Es ist eine Atemtechnik fuer Redner", "korrekt": False},
                ],
                "erklaerung": "Treasure nutzt das japanische Konzept (Iss bis du zu 80% satt bist) als Metapher: Auch in Gespraechen gilt - nicht alles sagen, Raum fuer den anderen lassen.",
            },
        ],
    },
    {
        "id": "amy-cuddy",
        "sprecher": "Amy Cuddy",
        "titel_de": "Koerpersprache praegte wer du bist",
        "titel_original": "Your Body Language May Shape Who You Are",
        "jahr": 2012,
        "icon": "💪",
        "kategorie": "Kommunikation",
        "kurzfassung": (
            "Harvard-Psychologin Amy Cuddy zeigt, dass Koerpersprache nicht nur anderen signalisiert wie wir uns fuehlen, "
            "sondern auch uns selbst beeinflusst. Power Poses (offene, ausgedehnte Koerperposition) erhoehen "
            "Testosteron, senken Cortisol und steigern Selbstvertrauen - selbst wenn man sich nicht sicher fuehlt."
        ),
        "kernkonzept": "Power Poses und Embodied Cognition",
        "schluessel_erkenntnis": "Koerper beeinflussen Geist: Zwei Minuten Power Pose veraendern Hormonspiegel und Selbstwahrnehmung.",
        "anwendung": "Vor Verhandlungen und Praesentationen: Power Pose im Badezimmer - der Koerper kann dem Geist helfen, Sicherheit aufzubauen.",
        "ted_url": "https://www.ted.com/talks/amy_cuddy_your_body_language_may_shape_who_you_are",
        "verwandte_raetsel": ["priming"],
        "quiz": [
            {
                "frage": "Was versteht Cuddy unter einer 'Power Pose'?",
                "optionen": [
                    {"text": "Eine aggressive, einschuechternde Koerperposition", "korrekt": False},
                    {"text": "Eine offene, ausgedehnte Koerperposition, die Raum einnimmt und Zuversicht signalisiert", "korrekt": True},
                    {"text": "Eine entspannte Sitzposition fuer Entspannung", "korrekt": False},
                    {"text": "Jede aufrechte Koerperposition", "korrekt": False},
                ],
                "erklaerung": "Power Poses wie der 'Wonder Woman'-Stand oder Arme ausgestreckt auf einem Tisch sind gross, offen und raumeinnehmend - das Gegenteil von 'klein machen'.",
            },
            {
                "frage": "Welche hormonellen Veraenderungen beobachtete Cuddys Forschung nach zwei Minuten Power Pose?",
                "optionen": [
                    {"text": "Erhoehtes Cortisol und gesenktes Testosteron", "korrekt": False},
                    {"text": "Erhoehtes Testosteron und gesenktes Cortisol", "korrekt": True},
                    {"text": "Keine messbaren Veraenderungen", "korrekt": False},
                    {"text": "Erhoehtes Adrenalin und Noradrenalin", "korrekt": False},
                ],
                "erklaerung": "Cuddys Studie: 2 Minuten High-Power-Pose -> Testosteron +20%, Cortisol -25%. Low-Power-Pose -> umgekehrte Effekte. Die Koerperhaltung signalisiert dem eigenen Gehirn Macht.",
            },
            {
                "frage": "Was ist das Prinzip der 'Embodied Cognition' nach Cuddy?",
                "optionen": [
                    {"text": "Gedanken beeinflussen den Koerper", "korrekt": False},
                    {"text": "Koerperliche Zustaende und Haltungen beeinflussen Gedanken, Gefuehle und Verhalten", "korrekt": True},
                    {"text": "Koerper und Geist sind vollstaendig getrennt", "korrekt": False},
                    {"text": "Nur extreme Koerperhaltungen haben psychologische Wirkung", "korrekt": False},
                ],
                "erklaerung": "Embodied Cognition: Der Koerper 'denkt' mit. Laecheln macht gluecklich (nicht nur umgekehrt), aufrechte Haltung macht zuversichtlicher - Geist und Koerper sind bidirektional.",
            },
            {
                "frage": "Was empfiehlt Cuddy vor nervoeser Situation (z.B. Vorstellungsgespraech)?",
                "optionen": [
                    {"text": "Tief durchatmen und sich positiv einreden", "korrekt": False},
                    {"text": "2 Minuten alleine Power Pose einnehmen, um Vertrauen zu aufzubauen", "korrekt": True},
                    {"text": "Die Nervositaet durch Leistungsdruck ueberdecken", "korrekt": False},
                    {"text": "Sich auf das schlechteste Ergebnis vorbereiten", "korrekt": False},
                ],
                "erklaerung": "Vor dem Eintreten ins Meeting: kurz auf die Toilette, Power Pose einnehmen. Die hormonellen Effekte helfen dem Gehirn, in einen zuversichtigeren Zustand zu wechseln.",
            },
            {
                "frage": "Was ist Cuddys persoenliche Geschichte, die den Talk so wirkungsvoll macht?",
                "optionen": [
                    {"text": "Sie hat eine schwere Krankheit ueberstanden", "korrekt": False},
                    {"text": "Nach einem Unfall wurde ihr gesagt, sie sei nicht intelligent genug fuer die Uni - sie wurde trotzdem Harvard-Professorin", "korrekt": True},
                    {"text": "Sie hat ihren Karrieredurchbruch mit einer einzigen Praesentation gemacht", "korrekt": False},
                    {"text": "Sie war schon als Kind besonders selbstbewusst", "korrekt": False},
                ],
                "erklaerung": "Cuddy erlitt einen schweren Autounfall, der ihren IQ um Punkte senkte. Sie wurde als 'nicht gut genug' eingestuft - durch 'Fake it till you become it' wurde sie trotzdem Harvard-Professorin.",
            },
        ],
    },
    {
        "id": "brene-brown",
        "sprecher": "Brene Brown",
        "titel_de": "Die Macht der Verletzlichkeit",
        "titel_original": "The Power of Vulnerability",
        "jahr": 2010,
        "icon": "❤️",
        "kategorie": "Kommunikation",
        "kurzfassung": (
            "Forscherin Brene Brown hat 12 Jahre lang untersucht, was Menschen, die ein tiefes Gefuehl von "
            "Verbundenheit erleben, von anderen unterscheidet. Ihr Ergebnis: Sie haben den Mut, verletzlich zu sein. "
            "Verletzlichkeit ist keine Schwaeche, sondern der Geburtsort von Innovation, Kreativitaet und Veraenderung."
        ),
        "kernkonzept": "Verletzlichkeit als Staerke / Wholehearted Living",
        "schluessel_erkenntnis": "Wer Verletzlichkeit vermeidet, blockiert auch Verbundenheit, Freude, Kreativitaet und Glueck.",
        "anwendung": "In Verhandlungen und Fuehrung: Echte Verbundenheit entsteht durch Authentizitaet - nicht durch perfekte Praesentation.",
        "ted_url": "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "verwandte_raetsel": [],
        "quiz": [
            {
                "frage": "Was unterscheidet 'Wholehearted People' laut Brown von anderen?",
                "optionen": [
                    {"text": "Sie haben keine Angst und sind immer selbstbewusst", "korrekt": False},
                    {"text": "Sie haben den Mut, imperfekt zu sein und Verletzlichkeit zuzulassen", "korrekt": True},
                    {"text": "Sie sind introvertierter und weniger auf Anerkennung angewiesen", "korrekt": False},
                    {"text": "Sie haben mehr positive Lebenserfahrungen gemacht", "korrekt": False},
                ],
                "erklaerung": "Brown: Wholehearted living bedeutet, von einem Ort der Wuerdigkeit heraus zu leben - nicht von einem Ort der Scham oder des 'Ich bin nicht gut genug'.",
            },
            {
                "frage": "Was ist nach Brown der Unterschied zwischen Scham (shame) und Schuld (guilt)?",
                "optionen": [
                    {"text": "Scham ist konstruktiv, Schuld ist destruktiv", "korrekt": False},
                    {"text": "Scham = 'Ich bin schlecht', Schuld = 'Ich habe etwas Schlechtes getan'", "korrekt": True},
                    {"text": "Beide sind gleichermassen schaedlich", "korrekt": False},
                    {"text": "Schuld motiviert, Scham ist neutral", "korrekt": False},
                ],
                "erklaerung": "Scham betrifft die Identitaet ('Ich bin ein schlechter Mensch'), Schuld betrifft das Verhalten ('Ich habe eine Fehler gemacht'). Schuld kann motivieren - Scham laehmtund zerstoert.",
            },
            {
                "frage": "Was bedeutet 'Numbing' in Browns Kontext?",
                "optionen": [
                    {"text": "Das Betaeuben negativer Emotionen durch Alkohol, Arbeit oder Ablenkung", "korrekt": True},
                    {"text": "Das Glueck anderer faelscht wahrzunehmen", "korrekt": False},
                    {"text": "Empathie absichtlich abschalten", "korrekt": False},
                    {"text": "Sich gegen Kritik unempfindlich machen", "korrekt": False},
                ],
                "erklaerung": "Browns wichtige Einsicht: Man kann Emotionen nicht selektiv betaeuben. Wer Schmerz und Verletzlichkeit betaeubt, betaeubt auch Freude, Dankbarkeit und Glueck.",
            },
            {
                "frage": "Was sagt Brown ueber den Zusammenhang von Verletzlichkeit und Kreativitaet?",
                "optionen": [
                    {"text": "Kreativitaet braucht keine Verletzlichkeit", "korrekt": False},
                    {"text": "Verletzlichkeit ist der Geburtsort von Innovation, Kreativitaet und Veraenderung", "korrekt": True},
                    {"text": "Kreative Menschen sind weniger verletzlich", "korrekt": False},
                    {"text": "Verletzlichkeit und Kreativitaet sind unabhaengig voneinander", "korrekt": False},
                ],
                "erklaerung": "Um etwas zu kreieren, muss man zeigen, was man gemacht hat - bevor man weiss ob es gut ist. Das erfordert Verletzlichkeit. Wer diese vermeidet, kann nichts Echtes erschaffen.",
            },
            {
                "frage": "Was empfiehlt Brown als praktischen Umgang mit Verletzlichkeit?",
                "optionen": [
                    {"text": "Verletzlichkeit ueben, indem man staendig alles offenbart", "korrekt": False},
                    {"text": "Verletzlichkeit als Notwendigkeit annehmen und Verbundenheit aktiv suchen", "korrekt": True},
                    {"text": "Verletzlichkeit durch Selbststaerkung minimieren", "korrekt": False},
                    {"text": "Verletzlichkeit nur im privaten Umfeld zeigen", "korrekt": False},
                ],
                "erklaerung": "Brown: Verbundenheit ist, warum wir hier sind. Sie ist das Warum und Wozu unseres Lebens. Sich erlauben, gesehen zu werden - das ist der Weg zu echter Verbundenheit.",
            },
        ],
    },
    {
        "id": "susan-cain",
        "sprecher": "Susan Cain",
        "titel_de": "Die Kraft der Introvertierten",
        "titel_original": "The Power of Introverts",
        "jahr": 2012,
        "icon": "📚",
        "kategorie": "Kommunikation",
        "kurzfassung": (
            "Susan Cain zeigt, dass unsere Gesellschaft und Bildungssysteme extrovertierte Eigenschaften systematisch "
            "bevorzugen - auf Kosten der Staerken von Introvertierten. Introvertion ist keine Krankheit, sondern "
            "eine andere Art, die Welt zu verarbeiten. Die besten Ideen entstehen oft in der Stille - nicht im Brainstorming."
        ),
        "kernkonzept": "Introversion vs. Gruppendenken / Stille als Kraftquelle",
        "schluessel_erkenntnis": "Moderne Buerogestaltung und Gruppenarbeit erzwingen Extraversion - und verpassen damit das Potenzial der Haelfte aller Menschen.",
        "anwendung": "In Teams: Introvertierte brauchen Zeit fuer Einzelarbeit vor Gruppendiskussionen, um ihr volles Potenzial einzubringen.",
        "ted_url": "https://www.ted.com/talks/susan_cain_the_power_of_introverts",
        "verwandte_raetsel": ["informationskaskade"],
        "quiz": [
            {
                "frage": "Wie definiert Cain Introversion?",
                "optionen": [
                    {"text": "Scheu und soziale Angst", "korrekt": False},
                    {"text": "Eine Praeferenz fuer ruhige, wenig stimulierende Umgebungen - nicht Scheu", "korrekt": True},
                    {"text": "Mangel an sozialen Faehigkeiten", "korrekt": False},
                    {"text": "Egozentrismus und Zurueckgezogenheit", "korrekt": False},
                ],
                "erklaerung": "Introversion ist nicht dasselbe wie Scheu (Angst vor sozialer Verurteilung). Introvertierte koennen sehr sozial sein - sie erhalten ihre Energie aus Stille statt aus Gesellschaft.",
            },
            {
                "frage": "Was kritisiert Cain an modernen Schulen und Bueros?",
                "optionen": [
                    {"text": "Zu viel Fokus auf individuelle Leistung statt Teamarbeit", "korrekt": False},
                    {"text": "Sie sind auf Extroversion ausgelegt und marginalisieren introvertierte Arbeitsweisen", "korrekt": True},
                    {"text": "Zu wenig Technologieeinsatz fuer introvertierte Zusammenarbeit", "korrekt": False},
                    {"text": "Sie bewerten theoretisches Wissen hoeher als praktische Faehigkeiten", "korrekt": False},
                ],
                "erklaerung": "Cain: Offene Grossraumbueoros, permanente Gruppenarbeit und die Pflicht zur Extraversion verschwenden das Potenzial der 30-50% Introvertierten.",
            },
            {
                "frage": "Was zeigt Forschung ueber Brainstorming in Gruppen?",
                "optionen": [
                    {"text": "Gruppenbrainstorming erzeugt mehr und bessere Ideen als Einzelarbeit", "korrekt": False},
                    {"text": "Einzelarbeit vor der Diskussion erzeugt haeufig mehr und bessere Ideen", "korrekt": True},
                    {"text": "Diverse Gruppen sind immer kreativer als homogene", "korrekt": False},
                    {"text": "Die Raumgestaltung hat keinen Einfluss auf Kreativitaet", "korrekt": False},
                ],
                "erklaerung": "Studien zeigen: In Gruppen-Brainstorming dominiert der Konformitaetsdruck, Lautere setzen sich durch - individuelle Ideenfindung vor der Gruppensitzung ist produktiver.",
            },
            {
                "frage": "Welche historischen Beispiele nennt Cain fuer erfolgreiche Introvertierte?",
                "optionen": [
                    {"text": "Steve Jobs, Napoleon, Alexander der Grosse", "korrekt": False},
                    {"text": "Eleanor Roosevelt, Rosa Parks, Gandhi", "korrekt": True},
                    {"text": "Winston Churchill, Barack Obama, Bill Clinton", "korrekt": False},
                    {"text": "Thomas Edison, Henry Ford, Walt Disney", "korrekt": False},
                ],
                "erklaerung": "Cain zeigt, dass viele der einflussreichsten Fuehrungspersoenlichkeiten introvertiert waren - und gerade deshalb tief nachdachten, bevor sie handelten.",
            },
            {
                "frage": "Was ist Cains praktische Empfehlung fuer den Umgang mit Introvertierten?",
                "optionen": [
                    {"text": "Introvertierte sollten lernen, extravertierter zu sein", "korrekt": False},
                    {"text": "Zeit fuer Einzelarbeit vor Gruppenentscheidungen einplanen und Stille als Ressource sehen", "korrekt": True},
                    {"text": "Introvertierte in separaten Teams ohne Gruppeninteraktion arbeiten lassen", "korrekt": False},
                    {"text": "Introvertierte in Fuehrungsrollen vermeiden", "korrekt": False},
                ],
                "erklaerung": "Cain: Stoppt, alle in Gruppenarbeit zu zwingen. Gebt Menschen Zeit fuer Einzelarbeit. Nutzt Technologie fuer asynchrone Beitraege. Valorisiert Stille als Denkraum.",
            },
        ],
    },
    {
        "id": "robert-waldinger",
        "sprecher": "Robert Waldinger",
        "titel_de": "Was macht ein gutes Leben? Lektionen aus der laengsten Studie ueber Glueck",
        "titel_original": "What Makes a Good Life? Lessons from the Longest Study on Happiness",
        "jahr": 2015,
        "icon": "💞",
        "kategorie": "Kognition",
        "kurzfassung": (
            "Psychiater Robert Waldinger leitet die Harvard-Studie ueber Glueck - die laengste wissenschaftliche "
            "Untersuchung dieser Art (75+ Jahre, begonnen 1938). Das klare Ergebnis: Gute Beziehungen machen uns "
            "gluecklicher und gesunder. Einsamkeit ist so schaedlich wie Rauchen. Beziehungsqualitaet ist wichtiger als -quantitaet."
        ),
        "kernkonzept": "Beziehungen als Schluessel zu Glueck und Gesundheit",
        "schluessel_erkenntnis": "Gute Beziehungen schuetzen uns - nicht Reichtum, Ruhm oder harte Arbeit. Einsamkeit toetet.",
        "anwendung": "Langfristige Kooperationen und Verhandlungsbeziehungen pflegen: Der Beziehungsaspekt ist oft wichtiger als das einzelne Geschaeftsergebnis.",
        "ted_url": "https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness",
        "verwandte_raetsel": [],
        "quiz": [
            {
                "frage": "Was ist die Haupterkenntnis der Harvard-Gluecksstudie nach 75 Jahren?",
                "optionen": [
                    {"text": "Gesundheit und Finanzen sind die wichtigsten Faktoren fuer Glueck", "korrekt": False},
                    {"text": "Gute Beziehungen halten uns gluecklicher und gesunder", "korrekt": True},
                    {"text": "Berufserfolg und Selbstverwirklichung sind entscheidend", "korrekt": False},
                    {"text": "Glueck haengt primaer von genetischen Faktoren ab", "korrekt": False},
                ],
                "erklaerung": "75 Jahre Daten, zwei Kohortengruppen (Harvard-Studenten und Bostoner Arme): Der staerkste Praediktor fuer Gesundheit und Glueck im Alter sind enge, vertrauensvolle Beziehungen.",
            },
            {
                "frage": "Wie wirkt sich Einsamkeit laut Waldinger auf die Gesundheit aus?",
                "optionen": [
                    {"text": "Einsamkeit hat minimale Auswirkungen auf die koerperliche Gesundheit", "korrekt": False},
                    {"text": "Einsamkeit ist so schaedlich wie Rauchen und verkuerzt das Leben messbar", "korrekt": True},
                    {"text": "Einsamkeit schadet nur psychisch, nicht koerperlich", "korrekt": False},
                    {"text": "Einsamkeit schadet nur aelteren Menschen", "korrekt": False},
                ],
                "erklaerung": "Waldinger: Einsamkeit ist giftig. Einsame Menschen klagen haeufiger ueber Schmerzen, ihr Gehirn baute frueher ab, ihr Leben war kuerzer.",
            },
            {
                "frage": "Was ist der Unterschied zwischen Beziehungsquantitaet und -qualitaet in der Studie?",
                "optionen": [
                    {"text": "Quantitaet (viele Kontakte) ist entscheidender als Qualitaet", "korrekt": False},
                    {"text": "Qualitaet (Tiefe, Vertrauen) ist entscheidend - auch Konflikte in guten Beziehungen schuetzen", "korrekt": True},
                    {"text": "Beide sind gleich wichtig", "korrekt": False},
                    {"text": "Online-Kontakte sind genauso wertvoll wie Praesenz-Kontakte", "korrekt": False},
                ],
                "erklaerung": "Nicht die Anzahl der Freunde, sondern die Qualitaet der engen Beziehungen zaehlt. Selbst konfliktreiche Ehen, in denen man dem Partner vertrauen kann, schuetzen die Gesundheit.",
            },
            {
                "frage": "Was glaubten die meisten 25-jaehrigen Teilnehmer, was sie gluecklich machen wuerde?",
                "optionen": [
                    {"text": "Gesundheit und Sport", "korrekt": False},
                    {"text": "Reichtum und Ruhm", "korrekt": True},
                    {"text": "Familie und Beziehungen", "korrekt": False},
                    {"text": "Frieden und Natur", "korrekt": False},
                ],
                "erklaerung": "Zu Beginn der Studie glaubten fast alle jungen Maenner, dass Reichtum, Ruhm und harte Arbeit sie gluecklich machen wuerden. Die Daten zeigten das Gegenteil.",
            },
            {
                "frage": "Was empfiehlt Waldinger praktisch fuer ein gutes Leben?",
                "optionen": [
                    {"text": "In Immobilien und Aktien investieren", "korrekt": False},
                    {"text": "In Beziehungen investieren - alte Kontakte auffrischen, Verbindungen vertiefen", "korrekt": True},
                    {"text": "Gesundheit und Sport als erste Prioritaet setzen", "korrekt": False},
                    {"text": "Beruf und Selbstverwirklichung balancieren", "korrekt": False},
                ],
                "erklaerung": "Waldingers Botschaft: Beziehungen sind die wichtigste Investition. Rufe den alten Freund an, geh zum Familientreffen, ersetze Bildschirmzeit durch Menschen-Zeit.",
            },
        ],
    },
    {
        "id": "mihaly-csikszentmihalyi",
        "sprecher": "Mihaly Csikszentmihalyi",
        "titel_de": "Flow - das Geheimnis des Gluecks",
        "titel_original": "Flow, the Secret to Happiness",
        "jahr": 2004,
        "icon": "🌊",
        "kategorie": "Kognition",
        "kurzfassung": (
            "Psychologe Mihaly Csikszentmihalyi beschreibt den Flow-Zustand: vollstaendiges Aufgehen in einer Taetigkeit, "
            "die gerade herausfordernd genug ist. Zeit fliegt, Selbstbewusstsein verschwindet, Freude entsteht. "
            "Flow ist der Zustand hoechster intrinsischer Motivation - und lernbar."
        ),
        "kernkonzept": "Flow - optimales Erleben durch Challenge-Skill-Balance",
        "schluessel_erkenntnis": "Flow entsteht, wenn Herausforderung und Koennen im Gleichgewicht sind - zu einfach langweilt, zu schwer macht Angst.",
        "anwendung": "Aufgaben so gestalten, dass sie knapp ueber dem aktuellen Koennen liegen - das ist die Zone maximaler Motivation und Leistung.",
        "ted_url": "https://www.ted.com/talks/mihaly_csikszentmihalyi_flow_the_secret_to_happiness",
        "verwandte_raetsel": [],
        "quiz": [
            {
                "frage": "Was sind die Kernbedingungen fuer den Flow-Zustand?",
                "optionen": [
                    {"text": "Entspannung, Stille und Ruhe", "korrekt": False},
                    {"text": "Klare Ziele, sofortiges Feedback, und eine Balance zwischen Herausforderung und Koennen", "korrekt": True},
                    {"text": "Hohe Motivation und externe Belohnungen", "korrekt": False},
                    {"text": "Multitasking und hohe Produktivitaet", "korrekt": False},
                ],
                "erklaerung": "Csikszentmihalyi identifizierte drei Kernbedingungen: Klare Ziele (weiss, was zu tun ist), sofortiges Feedback (weiss, wie gut man vorrankommt), Herausforderung ~ Koennen.",
            },
            {
                "frage": "Was passiert, wenn die Herausforderung viel groesser ist als das eigene Koennen?",
                "optionen": [
                    {"text": "Man erlebt Flow durch den Adrenalinkick", "korrekt": False},
                    {"text": "Man erlebt Angst und Ueberforderung statt Flow", "korrekt": True},
                    {"text": "Man lernt schneller und gelangt so in Flow", "korrekt": False},
                    {"text": "Man erlebt Gleichgueltigkeit", "korrekt": False},
                ],
                "erklaerung": "Das Flow-Kanal-Modell: Zu schwierig -> Angst. Zu einfach -> Langeweile. Nur im schmalen Kanal 'Challenge ~ Skill' entsteht Flow.",
            },
            {
                "frage": "Was ist ein 'autotelic experience' nach Csikszentmihalyi?",
                "optionen": [
                    {"text": "Eine Erfahrung, die durch externe Belohnungen motiviert wird", "korrekt": False},
                    {"text": "Eine Erfahrung, die um ihrer selbst willen gemacht wird - der Prozess ist die Belohnung", "korrekt": True},
                    {"text": "Eine intensive Erinnerung, die praegende Wirkung hat", "korrekt": False},
                    {"text": "Eine spirituelle Erfahrung jenseits des Alltags", "korrekt": False},
                ],
                "erklaerung": "Autotelic (griech.: auto = selbst, telos = Ziel): Die Taetigkeit traegt ihr Ziel in sich. Man braucht keine externe Belohnung - der Prozess selbst ist erfuellend.",
            },
            {
                "frage": "Wie kann man laut Csikszentmihalyi mehr Flow im Alltag erleben?",
                "optionen": [
                    {"text": "Einfachere Aufgaben waehlen, um Erfolge zu erzielen", "korrekt": False},
                    {"text": "Aufgaben suchen, die knapp ueber dem eigenen Koennen liegen, und klare Ziele setzen", "korrekt": True},
                    {"text": "Viele Pausen einplanen und Ablenkungen reduzieren", "korrekt": False},
                    {"text": "Mehr Urlaub und Erholungszeiten einplanen", "korrekt": False},
                ],
                "erklaerung": "Flow ist nicht nur Glueck - es ist Wachstum. Man muss Aufgaben aktiv so gestalten, dass sie knapp herausfordernd genug sind. Das erfordert Selbstkenntnis und Planung.",
            },
            {
                "frage": "In welchen Berufsgruppen beobachtete Csikszentmihalyi am haeufigsten Flow?",
                "optionen": [
                    {"text": "Nur in kreativen Berufen wie Kunst und Musik", "korrekt": False},
                    {"text": "In allen Berufen, von Chirurgen bis Schachspielern, wenn die Bedingungen stimmen", "korrekt": True},
                    {"text": "Vor allem bei gut bezahlten Managern", "korrekt": False},
                    {"text": "Nur bei Menschen mit bestimmten Persoenlichkeitstypen", "korrekt": False},
                ],
                "erklaerung": "Csikszentmihalyi interviewte Tausende: Bergsteiger, Chirurgen, Schachspieler, Komponisten, Schweisser. Flow ist universal - es geht um die Qualitaet der Erfahrung, nicht den Beruf.",
            },
        ],
    },
    {
        "id": "ken-robinson",
        "sprecher": "Ken Robinson",
        "titel_de": "Toeten Schulen die Kreativitaet?",
        "titel_original": "Do Schools Kill Creativity?",
        "jahr": 2006,
        "icon": "🎨",
        "kategorie": "Kognition",
        "kurzfassung": (
            "Sir Ken Robinson argumentiert, dass Bildungssysteme weltweit Kreativitaet systematisch unterdruecken - "
            "indem sie Fehler bestrafen und akademische Faehigkeiten ueber kuenstlerische stellen. "
            "Kinder sind von Natur aus kreativ; Schulen trainieren dieses Potenzial heraus. "
            "Robinson fordert eine Revolution in der Bildung, die Kreativitaet gleichwertig behandelt."
        ),
        "kernkonzept": "Kreativitaet und Bildungsrevolution",
        "schluessel_erkenntnis": "Alle Kinder sind kreativ - Bildungssysteme erziehen Kreativitaet heraus, weil Fehler als schlimmste Moeglichkeit gilt.",
        "anwendung": "In Fuehrung und Teams: Fehler als Lernmoment begreifen und eine Kultur des Ausprobierens foerdern, nicht nur des perfekten Ergebnisses.",
        "ted_url": "https://www.ted.com/talks/sir_ken_robinson_do_schools_kill_creativity",
        "verwandte_raetsel": ["dunning-kruger"],
        "quiz": [
            {
                "frage": "Was zeigt Robinsons Beispiel des Gilchrist-Tests ueber divergentes Denken?",
                "optionen": [
                    {"text": "Kinder koennen Erwachsene in analytischem Denken uebertreffen", "korrekt": False},
                    {"text": "98% der Kinder mit 3-5 Jahren sind Genies im divergenten Denken - mit 25 Jahren nur noch 2%", "korrekt": True},
                    {"text": "Intelligenz nimmt mit dem Alter linear zu", "korrekt": False},
                    {"text": "Divergentes Denken kann nicht gemessen werden", "korrekt": False},
                ],
                "erklaerung": "Der Test fragte, wie viele Verwendungsmoeglichkeiten eine Bueroklamme hat. Vorschulkinder nannten hunderte Ideen; Erwachsene blockierten sich selbst durch erlernte Selbstzensur.",
            },
            {
                "frage": "Was ist Robinsons Argument gegen die Hierarchie der Schulfaecher?",
                "optionen": [
                    {"text": "Mathematik sollte mehr Gewicht erhalten", "korrekt": False},
                    {"text": "Kreative Faecher werden systematisch abgewertet, obwohl Kreativitaet genauso wichtig ist", "korrekt": True},
                    {"text": "Alle Faecher sollten gleich bewertet werden", "korrekt": False},
                    {"text": "Sport sollte an die Spitze der Hierarchie", "korrekt": False},
                ],
                "erklaerung": "Weltweit gilt die gleiche Hierarchie: Mathematik und Sprachen oben, Kuenste unten. Robinson: Das bereitet Kinder auf Berufe des 19. Jahrhunderts vor - nicht des 21.",
            },
            {
                "frage": "Was sagt Robinson ueber den Umgang mit Fehlern in Bildungssystemen?",
                "optionen": [
                    {"text": "Fehler sollen bestraft werden, um Praezision zu foerdern", "korrekt": False},
                    {"text": "Fehler als schlimmste Moeglichkeit zu behandeln, toetet Kreativitaet und Risikobereitschaft", "korrekt": True},
                    {"text": "Fehler sollen ignoriert werden", "korrekt": False},
                    {"text": "Fehler sind nur in kreativen Berufen akzeptabel", "korrekt": False},
                ],
                "erklaerung": "Robinson: 'If you're not prepared to be wrong, you'll never come up with anything original.' Die Angst vor Fehlern ist das groesste Kreativitaets-Hemmnis.",
            },
            {
                "frage": "Was ist das zentrale Argument von Robinsons Gillian-Lynne-Geschichte?",
                "optionen": [
                    {"text": "Talentierte Menschen werden immer erkannt", "korrekt": False},
                    {"text": "Was heute als ADHS pathologisiert wuerde, war bei ihr Tanz-Talent - Kontext entscheidet", "korrekt": True},
                    {"text": "Tanzen ist wichtiger als akademische Bildung", "korrekt": False},
                    {"text": "Eltern sollten die Bildung selbst in die Hand nehmen", "korrekt": False},
                ],
                "erklaerung": "Gillian Lynne (Choreografin von 'Cats') wurde als Kind als 'lerngestoert' eingestuft. Ein kluger Arzt sah: Sie muss tanzen. Sie wurde weltberuehmt. Die falsche Diagnose waere verheerend gewesen.",
            },
            {
                "frage": "Welche Art von Bildungsrevolution fordert Robinson?",
                "optionen": [
                    {"text": "Mehr Technologie und digitale Tools im Unterricht", "korrekt": False},
                    {"text": "Kreativitaet gleichwertig mit Alphabetisierung behandeln und Individualitaet foerdern", "korrekt": True},
                    {"text": "Rueckkehr zu klassischen Bildungsidealen", "korrekt": False},
                    {"text": "Abschaffung von Tests und Pruefungen", "korrekt": False},
                ],
                "erklaerung": "Robinson fordert ein fundamentales Umdenken: weg von der Bildung als Fabrik, hin zur Bildung als Oekosystem, das individuelle Talente entdeckt und entwickelt.",
            },
        ],
    },
    {
        "id": "hans-rosling",
        "sprecher": "Hans Rosling",
        "titel_de": "Die besten Statistiken, die du je gesehen hast",
        "titel_original": "The Best Stats You've Never Seen",
        "jahr": 2006,
        "icon": "📊",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Statistiker Hans Rosling zerstoert mit lebendigen Daten-Visualisierungen die Mythen ueber "
            "'Entwicklungslaender' und 'Erste Welt'. Die Welt ist komplexer und fortschrittlicher als die meisten denken. "
            "Sein Gapminder-Tool macht abstrakte Statistiken sichtbar und zeigt: Fakten bekaempfen Vorurteile."
        ),
        "kernkonzept": "Daten-Mythen und faktenbasiertes Denken",
        "schluessel_erkenntnis": "Unsere Weltbilder sind oft Jahrzehnte veraltet - Fakten und Datenvisualisierung sind das Gegenmittel.",
        "anwendung": "In Verhandlungen und Entscheidungen: Annahmen ueber Maerkte, Laender oder Gruppen regelmaessig mit aktuellen Daten ueberpruefen.",
        "ted_url": "https://www.ted.com/talks/hans_rosling_the_best_stats_you_ve_never_seen",
        "verwandte_raetsel": ["survivorship-bias", "simpson"],
        "quiz": [
            {
                "frage": "Was zeigt Rosling mit seinem beruehmten 'Bubble Chart'?",
                "optionen": [
                    {"text": "Dass Industrielaender immer reicher werden", "korrekt": False},
                    {"text": "Wie Laender ueber Jahrzehnte in Lebenserwartung und Einkommen konvergieren", "korrekt": True},
                    {"text": "Dass Bevoelkerungswachstum Armut verursacht", "korrekt": False},
                    {"text": "Dass Bildungsinvestitionen keinen Effekt haben", "korrekt": False},
                ],
                "erklaerung": "Rosling animiert Jahrzehnte von Gapminder-Daten: Man sieht live, wie sich die Welt veraendert hat - Asien holt auf, Afrika macht Fortschritte. Die 'Entwicklungsland vs. Erste Welt'-Dichotomie ist ueberholt.",
            },
            {
                "frage": "Was zeigt Roslings Test mit Universitaetsprofessoren?",
                "optionen": [
                    {"text": "Professoren haben exzellentes Weltwissen", "korrekt": False},
                    {"text": "Professoren schnitten schlechter ab als Schimpansen, die zufaellig raten", "korrekt": True},
                    {"text": "Professoren unterschaetzen Fortschritt in Laendern des globalen Suedens", "korrekt": False},
                    {"text": "Nur Roslings Fragen waren zu schwer", "korrekt": False},
                ],
                "erklaerung": "Bei Fragen zum globalen Zustand (Kindersterblichkeit, Schulbesuche etc.) lagen Professoren systematisch schlechter als Zufallsrate. Schimpansen, die zwischen zwei Antworten waehlen, haetten 50% richtig - die Professoren weniger.",
            },
            {
                "frage": "Was ist Gapminder und wozu dient es?",
                "optionen": [
                    {"text": "Ein Statistikprogramm fuer Akademiker", "korrekt": False},
                    {"text": "Ein freies Tool fuer interaktive Datenvisualisierung, das globale Entwicklungsdaten zeigt", "korrekt": True},
                    {"text": "Eine Nichtregierungsorganisation fuer Entwicklungshilfe", "korrekt": False},
                    {"text": "Ein Test fuer geographisches Weltwissen", "korrekt": False},
                ],
                "erklaerung": "Gapminder.org macht Weltentwicklungsdaten (UN, WHO, Weltbank) fuer jeden frei zugaenglich und interaktiv visualisierbar - mit dem Ziel, Mythen durch Fakten zu ersetzen.",
            },
            {
                "frage": "Was ist Roslings wichtigste Botschaft ueber Daten und Entscheidungen?",
                "optionen": [
                    {"text": "Statistiken luegen immer", "korrekt": False},
                    {"text": "Wir arbeiten mit veralteten Weltbildern und muessen Annahmen regelmaessig mit Daten pruefen", "korrekt": True},
                    {"text": "Nur Experten koennen Statistiken korrekt interpretieren", "korrekt": False},
                    {"text": "Emotionen sind wichtiger als Daten fuer Entscheidungen", "korrekt": False},
                ],
                "erklaerung": "Roslings Kernbotschaft: 'The world cannot be understood without numbers. But the world cannot be understood with numbers alone.' Fakten brauchen Kontext - und Kontexte muessen aktuell sein.",
            },
            {
                "frage": "Wie teilt Rosling die Welt statt in 'Erste' und 'Dritte Welt'?",
                "optionen": [
                    {"text": "In reich, mittel und arm", "korrekt": False},
                    {"text": "In vier Einkommensstufen (Level 1-4) nach Kaufkraft und Lebensstandard", "korrekt": True},
                    {"text": "Nach Kontinenten mit je eigenen Entwicklungspfaden", "korrekt": False},
                    {"text": "In industrialisiert und nicht-industrialisiert", "korrekt": False},
                ],
                "erklaerung": "Roslings Nachfolger-Buch 'Factfulness': 4 Level nach Kaufkraft ($1-2, $4-8, $8-32, $32+/Tag) ersetzen die veraltete Zweitelung - sie beschreibt Realitaet praeziser.",
            },
        ],
    },
    {
        "id": "sherry-turkle",
        "sprecher": "Sherry Turkle",
        "titel_de": "Verbunden, aber allein",
        "titel_original": "Connected, but Alone?",
        "jahr": 2012,
        "icon": "📱",
        "kategorie": "Kommunikation",
        "kurzfassung": (
            "MIT-Psychologin Sherry Turkle untersucht, wie digitale Kommunikation und Smartphones unsere "
            "Faehigkeit zu echter Verbundenheit veraendern. Wir bevorzugen Textnachrichten weil wir kontrollieren "
            "koennen, was wir sagen - aber verlieren dabei Empathie, Tiefe und echtes Zuhoeren."
        ),
        "kernkonzept": "Digital-Kommunikation und Empathie-Erosion",
        "schluessel_erkenntnis": "Smartphones geben uns Kontrolle ueber Gespraeche - aber auf Kosten von echtem Verbundensein und Empathie.",
        "anwendung": "In Verhandlungen: Smartphone weglegen. Echte Gespraeche mit Pausen, Blickkontakt und Zoegren sind tiefer und effektiver als optimierte Nachrichten.",
        "ted_url": "https://www.ted.com/talks/sherry_turkle_connected_but_alone",
        "verwandte_raetsel": ["aktives-zuhoeren"],
        "quiz": [
            {
                "frage": "Was meint Turkle mit 'alone together'?",
                "optionen": [
                    {"text": "Menschen koennen gleichzeitig arbeiten und sozial sein", "korrekt": False},
                    {"text": "Wir sind staendig verbunden, aber tatsaechlich allein - ohne echte Praesenz bei anderen", "korrekt": True},
                    {"text": "Introvertierte sind gluecklich in Gesellschaft ohne zu interagieren", "korrekt": False},
                    {"text": "Online-Communities schaffen echte Gemeinschaft", "korrekt": False},
                ],
                "erklaerung": "Turkle: Wir sitzen im Familienessen - jeder auf seinem Handy. Wir sind verbunden mit hunderten, aber wirklich praesent bei niemandem. 'Alone Together'.",
            },
            {
                "frage": "Warum bevorzugen laut Turkle viele Menschen Textnachrichten gegenueber Telefonaten?",
                "optionen": [
                    {"text": "Texte sind effizienter und zeitsparender", "korrekt": False},
                    {"text": "Texte erlauben es, zu editieren, zu loeschen und die perfekte Version von sich zu praesentieren", "korrekt": True},
                    {"text": "Texte werden besser verstanden als gesprochene Sprache", "korrekt": False},
                    {"text": "Texte reduzieren Missverstaendnisse", "korrekt": False},
                ],
                "erklaerung": "Turkle: Texte geben Kontrolle. Aber Gespraeche mit all ihren Unvollkommenheiten, Pausen und Korrekturen sind das, was echte Empathie und Verbundenheit schafft.",
            },
            {
                "frage": "Was beobachtet Turkle bei Kindern und der Nutzung von Smartphones durch Eltern?",
                "optionen": [
                    {"text": "Kinder werden durch Smartphone-Nutzung der Eltern unabhaengiger", "korrekt": False},
                    {"text": "Kinder fragen weniger, warum die Eltern nicht zuhoeren - sie lernen, dass sie nicht wichtig sind", "korrekt": True},
                    {"text": "Kinder entwickeln durch fruehe Technologieexposition bessere digitale Faehigkeiten", "korrekt": False},
                    {"text": "Kinder kompensieren die digitale Ablenkung durch mehr Phantasiespiele", "korrekt": False},
                ],
                "erklaerung": "Turkle berichtet von Kindern, die aufgehoert haben, auf Eltern-Aufmerksamkeit zu bestehen, wenn das Handy in der Hand ist. Die Botschaft, die ankommt: Das Handy ist wichtiger als du.",
            },
            {
                "frage": "Was schlaegt Turkle als erstem Schritt vor?",
"optionen": [
                    {"text": "Smartphones komplett verbannen", "korrekt": False},
                    {"text": "Handyfreie Zonen schaffen - Tisch, Schlafzimmer - und wieder sprechen lernen", "korrekt": True},
                    {"text": "Social Media auf ein Minimum reduzieren", "korrekt": False},
                    {"text": "Kindern Smartphones erst ab 18 erlauben", "korrekt": False},
                ],
                "erklaerung": "Turkle fordert keine digitale Abstinenz, sondern bewusstes Design: Zeiten und Orte ohne Devices, um echte Gespraeche - mit all ihren Unvollkommenheiten - wieder moeglich zu machen.",
            },
            {
                "frage": "Was ist Turkles Hauptthese ueber das Selbst und Technologie?",
                "optionen": [
                    {"text": "Technologie erweitert das menschliche Selbst positiv", "korrekt": False},
                    {"text": "Wir nutzen Technologie, um uns einem Selbst zu entfliehen, das wir fuehlen muessen - aber nicht ertragen koennen", "korrekt": True},
                    {"text": "Das digitale Selbst ist authentischer als das physische", "korrekt": False},
                    {"text": "Technologie macht uns zu besseren Kommunikatoren", "korrekt": False},
                ],
                "erklaerung": "Turkles tiefste Beobachtung: Smartphones werden als Puffer gegen Einsamkeit genutzt - aber sie verhindern gerade die Faehigkeit, bei sich selbst zu sein, die echte Verbindung mit anderen erst ermoeglicht.",
            },
        ],
    },
    {
        "id": "william-ury",
        "sprecher": "William Ury",
        "titel_de": "Der Weg vom Nein zum Ja",
        "titel_original": "The Walk from 'No' to 'Yes'",
        "jahr": 2010,
        "icon": "🤝",
        "kategorie": "Verhandlung",
        "kurzfassung": (
            "Verhandlungsexperte William Ury (Harvard, BATNA-Mitbegruender) beschreibt den 'Weg zum Balkon': "
            "Innehalten und sich mental distanzieren, bevor man reagiert. Echte Verhandlungsmacht entsteht nicht "
            "durch Haerte, sondern durch das innere Ja - die Klarheit ueber das, was man wirklich will."
        ),
        "kernkonzept": "Inneres BATNA / 'Going to the Balcony'",
        "schluessel_erkenntnis": "Die schwierigste Verhandlung ist die mit dir selbst - wer sein inneres Ja kennt, verhandelt staerker.",
        "anwendung": "Vor jeder Verhandlung: Zum Balkon gehen (innehalten, Distanz gewinnen) und das eigene Warum klaeren - nicht nur das Was.",
        "ted_url": "https://www.ted.com/talks/william_ury_the_walk_from_no_to_yes",
        "verwandte_raetsel": ["batna"],
        "quiz": [
            {
                "frage": "Was bedeutet es laut Ury, 'auf den Balkon zu gehen'?",
                "optionen": [
                    {"text": "Die Verhandlung unterbrechen und den Raum verlassen", "korrekt": False},
                    {"text": "Mental einen Schritt zuruecktreten, um aus der Distanz klarer zu sehen und zu reagieren", "korrekt": True},
                    {"text": "Eine neutrale dritte Partei hinzuzuziehen", "korrekt": False},
                    {"text": "Die eigene Position oeffentlich machen", "korrekt": False},
                ],
                "erklaerung": "Der Balkon ist eine Metapher: ein mentaler Ort der Klarheit und Distanz vom Gefechtslarm der Verhandlung. Von dort sieht man das Stueck - und spielt nicht nur eine reaktive Rolle darin.",
            },
            {
                "frage": "Was ist Urys Konzept des 'inneren BATNA'?",
                "optionen": [
                    {"text": "Die beste externe Alternative zur Einigung", "korrekt": False},
                    {"text": "Die innere Klarheit ueber das, was man wirklich will, jenseits des Ergebnisses", "korrekt": True},
                    {"text": "Eine Reservestrategie fuer den Verhandlungsausfall", "korrekt": False},
                    {"text": "Das Wissen ueber die BATNA der Gegenseite", "korrekt": False},
                ],
                "erklaerung": "Ury: Das staerkste BATNA ist nicht eine externe Alternative, sondern das innere Ja - die Verbindung mit den eigenen tiefsten Interessen und Werten. Das macht einen unerschuetterlich.",
            },
            {
                "frage": "Welche drei Arten des 'Neins' unterscheidet Ury?",
                "optionen": [
                    {"text": "Hartes, weiches und verhandelbares Nein", "korrekt": False},
                    {"text": "Nein aus Macht, Nein aus Schutz, Nein aus Ablehnung", "korrekt": True},
                    {"text": "Strategisches, emotionales und defensives Nein", "korrekt": False},
                    {"text": "Sofortiges, verzoegertes und indirektes Nein", "korrekt": False},
                ],
                "erklaerung": "Ury: Hinter jedem Nein steckt eine positive Intention - Selbstschutz, Identitaet, Werte. Wer das Nein versteht, kann es in ein Ja verwandeln.",
            },
            {
                "frage": "Was ist die Grundlage von Urys 'Getting to Yes'-Ansatz?",
                "optionen": [
                    {"text": "Immer das erste Angebot ablehnen und hoeherfeilschen", "korrekt": False},
                    {"text": "Auf Interessen fokussieren, nicht auf Positionen", "korrekt": True},
                    {"text": "Freundlichkeit als taktisches Mittel einsetzen", "korrekt": False},
                    {"text": "So lange verhandeln, bis der Gegner aufgibt", "korrekt": False},
                ],
                "erklaerung": "Harvard-Verhandlungsmodell (Ury & Fisher): Hinter Positionen ('Ich will X') liegen Interessen ('Ich brauche Sicherheit/Anerkennung'). Einigung auf Interessen-Ebene ist haeufig leichter als auf Positions-Ebene.",
            },
            {
                "frage": "Was nennt Ury als den wichtigsten Schritt in jeder Verhandlung?",
                "optionen": [
                    {"text": "Den richtigen ersten Anker setzen", "korrekt": False},
                    {"text": "Zuerst mit sich selbst verhandeln und das eigene Ja finden", "korrekt": True},
                    {"text": "Moeglichst viele Informationen ueber die Gegenseite sammeln", "korrekt": False},
                    {"text": "Eine klare Drohung als Verhandlungseinstieg nutzen", "korrekt": False},
                ],
                "erklaerung": "Ury: 'The most important negotiation in your life is with yourself.' Wer weiss, was er wirklich will und bereit ist, dafuer einzustehen, verhandelt mit einer inneren Sicherheit, die keine Taktik ersetzen kann.",
            },
        ],
    },
    {
        "id": "malcolm-gladwell",
        "sprecher": "Malcolm Gladwell",
        "titel_de": "Wahl, Glueck und Spaghettisauce",
        "titel_original": "Choice, Happiness and Spaghetti Sauce",
        "jahr": 2004,
        "icon": "🍝",
        "kategorie": "Entscheidung",
        "kurzfassung": (
            "Malcolm Gladwell erzaehlt die Geschichte des Psychophysikers Howard Moskowitz, der herausfand: "
            "Es gibt nicht die eine perfekte Spaghettisauce - es gibt Cluster von Praeferenzen. "
            "Die Lektion: Wer nach dem Optimum sucht, uebersieht, dass Vielfalt und Segmentierung maechtiger sind als Einheitsloesungen."
        ),
        "kernkonzept": "Vielfalt der Praeferenzen / Horizontal Segmentation",
        "schluessel_erkenntnis": "Es gibt kein universelles Optimum - Vielfalt und individuelle Praeferenzen sind die Regel, nicht die Ausnahme.",
        "anwendung": "In Verhandlungen: Biete Optionen an, die verschiedene Praeferenz-Cluster ansprechen - eine Einheitslosung verfehlt oft alle.",
        "ted_url": "https://www.ted.com/talks/malcolm_gladwell_choice_happiness_and_spaghetti_sauce",
        "verwandte_raetsel": [],
        "quiz": [
            {
                "frage": "Was war Howard Moskowitz' Durchbruch bei seiner Spaghettisaucen-Studie?",
                "optionen": [
                    {"text": "Er fand die eine perfekte Spaghettisauce", "korrekt": False},
                    {"text": "Er entdeckte, dass es Cluster von Praeferenzen gibt - keine universelle 'beste' Sauce", "korrekt": True},
                    {"text": "Er bewies, dass der Preis entscheidend fuer die wahrgenommene Qualitaet ist", "korrekt": False},
                    {"text": "Er zeigte, dass chemische Zusaetze Praeferenzen bestimmen", "korrekt": False},
                ],
                "erklaerung": "Moskowitz' Erkenntnis: Clustere die Daten richtig, und du findest nicht einen Idealtyp, sondern Gruppen. Fuer Spaghettisauce: Plainsauce-Menschen, Spicy-Menschen, Extra-Chunky-Menschen.",
            },
            {
                "frage": "Welchen Fehler machten Kaffee- und Lebensmittelunternehmen laut Gladwell vor Moskowitz?",
                "optionen": [
                    {"text": "Sie investierten zu wenig in Marktforschung", "korrekt": False},
                    {"text": "Sie suchten nach dem einen perfekten Produkt statt nach Segmenten", "korrekt": True},
                    {"text": "Sie ignorierten demographische Faktoren", "korrekt": False},
                    {"text": "Sie produ zierten zu teure Produkte", "korrekt": False},
                ],
                "erklaerung": "Nescafe fragte Konsumenten, wie sie Kaffee moegen - und bekam 'mittelstark' als Antwort. Moskowitz erkannte: Menschen koennen ihre Praeferenzen nicht verbalisieren. Man muss sie testen.",
            },
            {
                "frage": "Was ist das Prinzip der 'horizontalen Segmentierung' nach Gladwell?",
                "optionen": [
                    {"text": "Produkte nach Preis in Segmente einteilen", "korrekt": False},
                    {"text": "Statt ein Optimum zu suchen, verschiedene gleichwertige Varianten fuer verschiedene Praeferenz-Gruppen anbieten", "korrekt": True},
                    {"text": "Maerkte nach geographischer Lage aufteilen", "korrekt": False},
                    {"text": "Kundensegmente nach Alter und Einkommen trennen", "korrekt": False},
                ],
                "erklaerung": "Horizontal (statt vertikal nach Qualitaet): Es gibt nicht gut vs. schlecht, sondern verschieden - fuer verschiedene Menschen. Das ist das Gegenteil von 'eine Groesse passt allen'.",
            },
            {
                "frage": "Was ist Gladwells philosophische Schlussfolgerung?",
                "optionen": [
                    {"text": "Mehr Auswahl macht immer gluecklicher", "korrekt": False},
                    {"text": "Der Weg zu Glueck liegt darin, anzuerkennen, dass Menschen unterschiedliche Beduerfnisse haben", "korrekt": True},
                    {"text": "Wissenschaft kann menschliche Praeferenzen vollstaendig vorhersagen", "korrekt": False},
                    {"text": "Unternehmen sollen nur das Beste produzieren", "korrekt": False},
                ],
                "erklaerung": "Gladwell: 'Howard understood that when it comes to tomato sauce, there is no perfect pasta sauce - only perfect pasta sauces.' Das gilt fuer alles - Arbeit, Beziehungen, Entscheidungen.",
            },
            {
                "frage": "Was lernt man aus Moskowitz' frueherer Arbeit fuer die US-Armee ueber Praeferenz-Forschung?",
                "optionen": [
                    {"text": "Soldaten haben homogene Geschmackspraeferenzen", "korrekt": False},
                    {"text": "Was Menschen sagen, was sie wollen, und was sie wirklich wollen, weicht systematisch ab", "korrekt": True},
                    {"text": "Hunger eliminiert individuelle Geschmackspraeferenzen", "korrekt": False},
                    {"text": "Feldverpflegung muss alle Naehrstoffe optimal abdecken", "korrekt": False},
                ],
                "erklaerung": "Moskowitz arbeitete an der Frage, wie man Feldverpflegung so gestaltet, dass Soldaten sie wirklich essen. Er lernte: Was Menschen sagen vs. was sie tun, sind zwei verschiedene Dinge.",
            },
        ],
    },
]

TALKS_BY_ID = {t["id"]: t for t in TED_TALKS}
KATEGORIEN = ["Entscheidung", "Kommunikation", "Verhandlung", "Kognition", "Fuehrung"]


@router.get("/quiz", response_class=HTMLResponse)
def ted_quiz_page(request: Request, kategorie: str = ""):
    pool = TED_TALKS if not kategorie else [t for t in TED_TALKS if t["kategorie"] == kategorie]
    all_questions = []
    for talk in pool:
        for q in talk.get("quiz", []):
            all_questions.append({
                **q,
                "sprecher": talk["sprecher"],
                "talk_id": talk["id"],
                "talk_icon": talk["icon"],
                "kernkonzept": talk["kernkonzept"],
            })
    selected = _random.sample(all_questions, min(10, len(all_questions)))
    return templates.TemplateResponse(request, "ted_quiz.html", {
        "active_page": "ted",
        "fragen": selected,
        "kategorie": kategorie,
        "kategorien": KATEGORIEN,
    })


@router.get("", response_class=HTMLResponse)
def ted_overview(request: Request):
    return templates.TemplateResponse(request, "ted.html", {
        "active_page": "ted",
        "talks": TED_TALKS,
        "kategorien": KATEGORIEN,
    })


@router.get("/{talk_id}", response_class=HTMLResponse)
def ted_detail(talk_id: str, request: Request):
    from .raetsel import RAETSEL_META
    talk = TALKS_BY_ID.get(talk_id)
    if not talk:
        return HTMLResponse("Talk nicht gefunden", status_code=404)
    raetsel_by_id = {r["id"]: r for r in RAETSEL_META}
    verwandte = [raetsel_by_id[rid] for rid in talk["verwandte_raetsel"] if rid in raetsel_by_id]
    idx = next((i for i, t in enumerate(TED_TALKS) if t["id"] == talk_id), 0)
    prev_talk = TED_TALKS[idx - 1] if idx > 0 else None
    next_talk = TED_TALKS[idx + 1] if idx < len(TED_TALKS) - 1 else None
    return templates.TemplateResponse(request, "ted_detail.html", {
        "active_page": "ted",
        "talk": talk,
        "verwandte_raetsel": verwandte,
        "prev_talk": prev_talk,
        "next_talk": next_talk,
    })
