from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import GedaechtnisScore

router = APIRouter(prefix="/gedaechtnis")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def gedaechtnis_uebersicht(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis.html", {"active_page": "gedaechtnis"})


@router.get("/corsi", response_class=HTMLResponse)
def corsi(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_corsi.html", {"active_page": "gedaechtnis"})


@router.get("/zahlen", response_class=HTMLResponse)
def zahlen(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_zahlen.html", {"active_page": "gedaechtnis"})


@router.get("/memory", response_class=HTMLResponse)
def memory(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_memory.html", {"active_page": "gedaechtnis"})


@router.get("/namen", response_class=HTMLResponse)
def namen(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_namen.html", {"active_page": "gedaechtnis"})


@router.get("/karten", response_class=HTMLResponse)
def karten(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_karten.html", {"active_page": "gedaechtnis"})


@router.get("/wortfolge", response_class=HTMLResponse)
def wortfolge(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_wortfolge.html", {"active_page": "gedaechtnis"})


@router.get("/theorie", response_class=HTMLResponse)
def theorie(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_theorie.html", {"active_page": "gedaechtnis"})


@router.get("/reaktionszeit", response_class=HTMLResponse)
def reaktionszeit(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_reaktionszeit.html", {"active_page": "gedaechtnis"})


@router.get("/chimp", response_class=HTMLResponse)
def chimp(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_chimp.html", {"active_page": "gedaechtnis"})


@router.get("/verbal", response_class=HTMLResponse)
def verbal(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_verbal.html", {"active_page": "gedaechtnis"})


@router.get("/bestenliste", response_class=HTMLResponse)
def bestenliste(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_bestenliste.html", {"active_page": "gedaechtnis"})


# ── Score-API ────────────────────────────────────────────────────────────────

# Games where lower score = better (reaction time in ms)
_LOWER_IS_BETTER = {"reaktionszeit"}

# Human-readable labels per game
GAME_META_GEDAECHTNIS = {
    "corsi":        {"name": "Blockspanne",           "unit": "Span",    "icon": "🔵"},
    "zahlen":       {"name": "Ziffernfolge",           "unit": "Ziffern", "icon": "🔢"},
    "memory":       {"name": "Memory",                 "unit": "Punkte",  "icon": "🃏"},
    "wortfolge":    {"name": "Wortfolge",              "unit": "Woerter", "icon": "📝"},
    "namen":        {"name": "Namen & Gesichter",      "unit": "Punkte",  "icon": "👤"},
    "karten":       {"name": "Kartendeck",             "unit": "Karten",  "icon": "🂡"},
    "reaktionszeit":{"name": "Reaktionszeit",          "unit": "ms",      "icon": "⚡"},
    "chimp":        {"name": "Schimpansen-Test",       "unit": "Level",   "icon": "🐒"},
    "verbal":       {"name": "Verbales Gedaechtnis",   "unit": "Punkte",  "icon": "💬"},
}


class ScoreIn(BaseModel):
    game_type: str
    score: int
    player_name: str = "Anonym"


@router.post("/score")
def submit_score(payload: ScoreIn, db: Session = Depends(get_db)):
    if payload.game_type not in GAME_META_GEDAECHTNIS:
        raise HTTPException(status_code=400, detail="Unbekannter Spieltyp")
    if len(payload.player_name.strip()) == 0:
        payload.player_name = "Anonym"
    entry = GedaechtnisScore(
        game_type=payload.game_type,
        score=payload.score,
        player_name=payload.player_name[:30],
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    # Compute rank
    lower_better = payload.game_type in _LOWER_IS_BETTER
    if lower_better:
        rank = db.query(GedaechtnisScore).filter(
            GedaechtnisScore.game_type == payload.game_type,
            GedaechtnisScore.score < payload.score,
        ).count() + 1
    else:
        rank = db.query(GedaechtnisScore).filter(
            GedaechtnisScore.game_type == payload.game_type,
            GedaechtnisScore.score > payload.score,
        ).count() + 1
    total = db.query(GedaechtnisScore).filter(GedaechtnisScore.game_type == payload.game_type).count()
    return {"ok": True, "rank": rank, "total": total}


@router.get("/scores/{game_type}")
def get_scores(game_type: str, db: Session = Depends(get_db)):
    if game_type not in GAME_META_GEDAECHTNIS:
        raise HTTPException(status_code=400, detail="Unbekannter Spieltyp")
    lower_better = game_type in _LOWER_IS_BETTER
    order_col = asc(GedaechtnisScore.score) if lower_better else desc(GedaechtnisScore.score)
    rows = (
        db.query(GedaechtnisScore)
        .filter(GedaechtnisScore.game_type == game_type)
        .order_by(order_col)
        .limit(10)
        .all()
    )
    meta = GAME_META_GEDAECHTNIS[game_type]
    return {
        "game_type": game_type,
        "name": meta["name"],
        "unit": meta["unit"],
        "lower_is_better": lower_better,
        "scores": [{"rank": i + 1, "player": r.player_name, "score": r.score} for i, r in enumerate(rows)],
    }


# ── Technik-Detailseiten ─────────────────────────────────────────────────────

TECHNIKEN: dict = {
    "gedaechtnispalast": {
        "slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast",
        "farbe": "indigo", "typ": "Raumgedächtnis", "schwierigkeit": "Mittel",
        "lernzeit": "2–4 Wochen bis zur Routine",
        "best_fuer": "Listen, Vorträge, Fremdwörter, beliebige Sequenzen",
        "spiel": None, "spiel_label": None,
        "meta_desc": "Gedächtnispalast (Method of Loci) – detaillierte Anleitung, Neurowissenschaft, Beispiele. Die älteste und mächtigste Merktechnik, Schritt für Schritt erklärt.",
        "kurz": "Du platzierst Informationen als lebhafte Bilder an Stationen einer dir bekannten Route. Beim mentalen Durchgehen erscheinen die Bilder — und damit die Inhalte — automatisch. Genutzt von Cicero, Sherlock Holmes und modernen Gedächtnisweltmeistern.",
        "gehirn": [
            "Der Hippocampus verarbeitet sowohl räumliche Navigation als auch episodisches Gedächtnis. Sogenannte Ortszellen (Place Cells, John O'Keefe, Nobelpreis 2014) feuern spezifisch an bestimmten Orten. Wenn du eine bekannte Route entlanggehst, erstellt dein Gehirn automatisch eine mentale Karte — und an jedem Punkt ist eine eigene Gedächtnisspur verankert.",
            "Der Gedächtnispalast nutzt dieses evolutionär alte System: indem du abstrakte Information mit einem konkreten Ort verknüpfst, lädst du Inhalte auf ein bereits existierendes, robustes Speichernetz auf. Das räumliche Gedächtnis ist nahezu unlimitiert und außerordentlich langlebig.",
            "Dresler et al. (2017, Neuron) zeigten: nach 6 Wochen Training mit dem Gedächtnispalast verändert sich die Konnektivität im Hippocampus messbar. Durchschnittliche Erwachsene steigern ihre Merkspanne für Zufallszahlen von ~7 auf 80+.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Route festlegen",
             "text": "Wähle einen Ort, den du blind kennst: deine Wohnung, dein Schulweg, dein Büro. Definiere 10–20 Stationen in fester räumlicher Reihenfolge (Haustür → Flur → Garderobe → Wohnzimmer → Sofa…). Die Stationen müssen klar voneinander trennbar sein.",
             "tipp": "Beginne mit 10 Stationen. Sobald du diese blind abrufen kannst, erweitere auf 20. Du kannst beliebig viele Routen anlegen — jede ist ein eigener Palast."},
            {"nr": 2, "titel": "Inhalte in konkrete Bilder übersetzen",
             "text": "Abstraktes muss bildlich werden. Nicht 'Inflation' merken — sondern: ein riesiger, platzender Ballon. Nicht 'BATNA' — sondern: Batman der mit einem Fischernetz kämpft. Je lebhafter, übertriebener und emotionaler das Bild, desto besser haftet es.",
             "tipp": "Nutze Bewegung, Geräusche, Gerüche. Ein Bild, das explodiert, stinkt oder lacht, ist immer einprägsamer als ein statisches."},
            {"nr": 3, "titel": "Bild an Station platzieren",
             "text": "Stelle dir vor, wie das Bild mit der Station interagiert — nicht nur davor steht. Der Ballon verstopft die Haustür. Batman kämpft auf dem Sofa. Je enger die Interaktion zwischen Bild und Ort, desto stärker der Anker.",
             "tipp": "Lass Bilder mit dem Ort verschmelzen: kleben an der Wand, hängen von der Lampe, explodieren aus dem Regal."},
            {"nr": 4, "titel": "Route einüben",
             "text": "Gehe die Route nach dem Einprägen sofort mental durch (innerhalb von 10 Minuten). Dann nach 1 Stunde, am nächsten Morgen. Bei jedem Durchgang werden die Bilder klarer und die Verbindungen stärker.",
             "tipp": None},
            {"nr": 5, "titel": "Abruf im Ernstfall",
             "text": "Schließe kurz die Augen und betrete mental deinen Palast. Gehe zur ersten Station — das Bild erscheint. Übersetze es zurück in den Begriff. Weiter zur zweiten Station, usw.",
             "tipp": "Viele berichten, dass der Palast beim Abruf 'von selbst läuft' — die Bilder tauchen auf, bevor man bewusst daran denkt."},
        ],
        "beispiele": [
            {"titel": "5 Harvard-Verhandlungsprinzipien",
             "inhalt": "Route: Haustür → Flur → Wohnzimmer → Küche → Balkon\n\n1. Haustür: Batman schlägt gegen die Tür (BATNA)\n2. Flur: Ein Seilgarten aus Kletterseilen (ZOPA – Zone Of Possible Agreement)\n3. Wohnzimmer: Riesiges pulsierendes Herz auf dem Sofa (Interessen)\n4. Küche: 100 Briefumschläge quellen aus dem Herd (Optionen)\n5. Balkon: Richter in Robe trinkt Kaffee (Legitimität)"},
            {"titel": "8-Punkte-Vortrag ohne Notizen",
             "inhalt": "Vortrag über Entscheidungspsychologie, 8 Kernpunkte. Route: Haustür, Garderobe, Spiegel, Sofa, Regal, Kühlschrank, Herd, Fenster.\n\nJeder Punkt wird als kurze dramatische Szene an einer Station platziert. Beim Vortrag gehst du mental durch deine Wohnung — die Punkte erscheinen in der richtigen Reihenfolge."},
        ],
        "fehler": [
            "Bilder zu abstrakt: 'Fairness' ist kein Bild. 'Eine Waage, die jemanden zerquetscht' ist eines.",
            "Route zu unbekannt: starte mit dem vertrautesten Ort. Ein nie besuchter Ort funktioniert nicht.",
            "Zu wenige Stationen: mit 3 Stationen ist der Palast instabil. Ziel: 15–20 für einen nützlichen Palast.",
            "Einmal visualisiert und fertig: ohne Wiederholung (spätestens nach 24 h) verblasst auch der Palast.",
            "Mehrere Paläste beginnen gleich: wenn alle Routen an 'Haustür' starten, entstehen Interferenzen. Lösung: sehr unterschiedliche Orte wählen.",
        ],
        "tipps": [
            "Lege mehrere Paläste an: Wohnung, Schulweg, Supermarkt — jede Route ist ein eigener Palast, der nie kollidiert.",
            "Kombiniere mit Major-System: Zahlen in Bilder umwandeln → im Palast platzieren.",
            "Für langen Stoff: eine Route pro Kapitel. Das Gehirn unterscheidet Paläste zuverlässig.",
            "Übe vorwärts und rückwärts: rückwärts abrufen stärkt die Gedächtnisspur dramatisch.",
            "Emotionale Orte (Kindheitszimmer) sind nahezu unzerstörbare Paläste.",
        ],
        "kombination": [
            {"slug": "major-system", "icon": "🔢", "titel": "Major-System", "grund": "Zahlen in Bilder konvertieren → im Palast platzieren. Standardkombination für Zahlengedächtnis-Weltrekorde."},
            {"slug": "pao-system", "icon": "🎭", "titel": "PAO-System", "grund": "Drei Elemente zu einer Szene verdichten → im Palast platzieren. Ideal für Kartendecks."},
            {"slug": "geschichten", "icon": "📖", "titel": "Geschichten-Methode", "grund": "Wenn Reihenfolge egal: Geschichte. Wenn Reihenfolge zählt: Palast. Kombiniert: Geschichte entlang der Palastroute."},
        ],
    },

    "major-system": {
        "slug": "major-system", "icon": "🔢", "titel": "Major-System",
        "farbe": "violet", "typ": "Zahlenkodierung", "schwierigkeit": "Mittel",
        "lernzeit": "1–2 Wochen für den Code, Monate bis zur Routine",
        "best_fuer": "Zahlen, PINs, Jahreszahlen, Statistiken, Daten",
        "spiel": "karten", "spiel_label": "🎴 Kartendeck trainieren",
        "meta_desc": "Major-System erklärt: Ziffern zu Konsonanten zu Wörtern zu Bildern. Vollständige Tabelle, Lernhilfen, Beispiele für Jahreszahlen und PINs.",
        "kurz": "Jede Ziffer wird einem Konsonanten-Klang zugeordnet. Aus den Konsonanten einer Zahl formt man ein Wort — und das Wort wird zum Bild. Zahlen, die sich 'nicht merken lassen', werden zu lebhaften, abrufbaren Szenen.",
        "gehirn": [
            "Unser Gehirn ist schlecht darin, abstrakte Symbole wie '7384' zu speichern — sie aktivieren kaum emotionale oder assoziative Netzwerke. Das Major-System überbrückt diesen Nachteil, indem es Ziffern in Lautmuster und dann in konkrete Wörter konvertiert.",
            "Wörter aktivieren das phonologische und semantische Gedächtnis. Visualisierte Wörter aktivieren zusätzlich visuell-kortikale Netzwerke. Durch 'Dual Coding' (Paivio, 1971) entstehen zwei unabhängige Gedächtnisspuren gleichzeitig — fällt eine aus, greift die andere.",
            "Das System wurde im 17. Jahrhundert entwickelt und von Mnemotechnikern wie Aimé Paris verfeinert. In seiner heutigen Form ermöglicht es Gedächtnisathleten, Tausende von Zufallszahlen in Minuten zu memorieren.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Zahlentabelle auswendig lernen",
             "text": "0 → S / Z  (Null: S-Laut)\n1 → T / D / Th  (Tonne: 1 Strich nach unten)\n2 → N  (N hat 2 Striche nach unten)\n3 → M  (M hat 3 Striche nach unten)\n4 → R  (letzter Konsonant von 'vier')\n5 → L  (Hand mit 5 Fingern: L-Form)\n6 → Sch / Ch / J  (6 dreht sich in ein Sch)\n7 → K / G / Ng / Qu  (zwei 7en ergeben ein K)\n8 → F / V / Ph / W  (Schreibschrift-8 wie f-Schlinge)\n9 → P / B  (9 ist gespiegeltes p oder b)\n\nNur Konsonanten zählen. Vokale (a, e, i, o, u) und h, w, y sind Füller ohne Zahlenwert.",
             "tipp": "Lerne erst 0–4 auswendig, dann 5–9. Teste dich sofort mit 2-stelligen Zahlen: 73 = K+M = 'Kamm', 18 = T+F = 'Topf'."},
            {"nr": 2, "titel": "Zahl in Konsonanten übersetzen",
             "text": "Segmentiere die Zahl: 1789 → 1=T, 7=K, 8=F, 9=B → Konsonantenfolge T-K-F-B. Oder aufteilen: 17=TK und 89=FB und Wörter suchen: 'Dackel' (D=1, CK=7, L=5 – nein) → 'Tage' + 'Pfau' → Ein Tageblatt fliegt auf einen Pfau.",
             "tipp": None},
            {"nr": 3, "titel": "Wort auswählen und visualisieren",
             "text": "Für jede Konsonanten-Kombination gibt es viele mögliche Wörter. Wähle immer das bildlichste: konkrete Nomen (Tisch, Adler, Pfanne) sind besser als abstrakte Begriffe.",
             "tipp": "Erstelle eine persönliche 100-Wörter-Liste (00–99), die du immer wieder benutzt. Dann wird jede 2-stellige Zahl sofort zu einem festen Bild."},
            {"nr": 4, "titel": "Bild im Gedächtnispalast platzieren",
             "text": "Das kodierte Wort wird als Bild im Palast platziert. Für längere Zahlen: Sequenz von Bildern an den Stationen. Die Bilder müssen mit dem Ort interagieren.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "Jahreszahl 1848 (Märzrevolution)",
             "inhalt": "1=T, 8=F, 4=R, 8=F → T-F-R-F\nAufteilen: 18=TF und 48=RF\n18 → 'Topf' (T=1, P=9... nein) → 'Diva' (D=1, V=8) → eine Diva\n48 → 'Riff' (R=4, F=8) → ein Meeresriff\n\nSzene: Eine Diva steht auf einem Riff und singt. → 1848.\n\nBeim Abruf: Diva → D=1, V=8 → 18; Riff → R=4, F=8 → 48 → 1848."},
            {"titel": "PIN 7391",
             "inhalt": "7=K, 3=M, 9=B/P, 1=T/D → K-M-B-T\n→ 'Kombucha' (K=7, M=3, B=9, T=1 – Vokale frei!)\n\nBild: Eine riesige Kombucha-Flasche am Geldautomat.\n→ PIN 7391."},
            {"titel": "Statistik: 68-95-99,7 (Normalverteilung)",
             "inhalt": "68 → 6=Sch, 8=F → 'Schafe' → eine Herde Schafe\n95 → 9=B, 5=L → 'Beil' → ein Beil\n99,7 → 9=P, 9=B, 7=K → 'Papagei' → ein Papagei\n\nGeschichte: Eine Herde Schafe (68%) flieht vor einem Beil (95%), das ein Papagei (99,7%) wirft."},
        ],
        "fehler": [
            "Konsonanten-Klang mit Buchstaben verwechseln: 'sch' ist EINE Einheit (=6), nicht S+C+H.",
            "W, H, Y als Konsonanten zählen — sie sind wertlose Füller.",
            "Keine persönliche 100-Wörter-Liste anlegen: ohne feste Liste bleibt das System langsam.",
            "Zu abstrakte Wörter: 'Konzept' statt 'Knochen'. Konkrete Nomen immer bevorzugen.",
            "Major allein nutzen: kombiniert mit dem Gedächtnispalast wird es erst mächtig.",
        ],
        "tipps": [
            "Investiere 1–2 Stunden in eine feste 100-Wörter-Liste (00–99). Diese Investition zahlt sich ein Leben lang aus.",
            "Übe täglich 10 Minuten mit zufälligen 2-stelligen Zahlen, bis die Übersetzung automatisch läuft.",
            "Für häufig genutzte Jahreszahlen: mehrere Wort-Optionen parat haben.",
            "Kombiniere mit Gedächtnispalast: Zahlenbilder im Palast → nahezu unbegrenzte Kapazität.",
        ],
        "kombination": [
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "Zahlenbilder im Palast platzieren — die Standardkombination für Zahlengedächtnis-Weltrekorde."},
            {"slug": "pao-system", "icon": "🎭", "titel": "PAO-System", "grund": "PAO erweitert Major um Person und Aktion — drei Zahlen verdichten zu einer einzigen Szene."},
        ],
    },

    "chunking": {
        "slug": "chunking", "icon": "📦", "titel": "Chunking",
        "farbe": "emerald", "typ": "Strukturierung", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar",
        "best_fuer": "Zahlenfolgen, Passwörter, IBANs, Vokabellisten, Lernstoff",
        "spiel": "zahlen", "spiel_label": "🔢 Ziffernfolge trainieren",
        "meta_desc": "Chunking erklärt: Informationen in bedeutungsvolle Blöcke aufteilen. Millers Law, Arbeitsgedächtnis, sofort anwendbar auf Zahlen, Listen und Lernstoff.",
        "kurz": "Große Informationsmengen werden in kleinere, bedeutungsvolle Einheiten (Chunks) aufgeteilt. Das Arbeitsgedächtnis verarbeitet jeden Chunk als eine Einheit — so passen mehr Informationen hinein, als die rohe Kapazitätsgrenze vermuten lässt.",
        "gehirn": [
            "George Miller beschrieb 1956 in 'The Magical Number Seven, Plus or Minus Two': das menschliche Kurzzeitgedächtnis fasst 7 ± 2 Chunks. Ein Chunk ist dabei eine bedeutungsvolle Einheit — sie kann aus einem einzelnen Zeichen oder aus Hunderten von Zeichen bestehen, je nachdem wie vertraut der Inhalt ist.",
            "Ein Schachgroßmeister 'sieht' nicht 32 Figuren an 64 Feldern, sondern 5–8 taktische Muster. Sein Arbeitsgedächtnis ist nicht größer als das eines Amateurs — aber seine Chunks sind riesig. Diesen Effekt kann man trainieren.",
            "Neuere Forschung (Cowan, 2001) schätzt die echte Kapazitätsgrenze sogar auf nur 4 ± 1 Chunks. Umso wichtiger: Informationen in möglichst große, bedeutungsvolle Einheiten packen.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Muster erkennen",
             "text": "Schau dir das Material an und frage: Gibt es natürliche Grenzen? Gibt es Rhythmus, Bedeutung, Kategorie oder räumliche Gruppen? 071145678901 hat auf den ersten Blick keine Struktur — als Telefonnummer gelesen: 0711 / 456 / 789 / 01 plötzlich schon.",
             "tipp": "Bei Zahlen: suche nach bekannten Mustern (Jahreszahlen, bekannte Nummern). 1989 ist ein Chunk (Mauerfall), keine vier Ziffern."},
            {"nr": 2, "titel": "Bedeutungsvolle Gruppen bilden",
             "text": "Ideal sind Gruppen von 3–4 Elementen. Die Gruppen sollten nach konsistenter Logik gebildet werden: alphabetisch, thematisch, rhythmisch, nach Bedeutung.",
             "tipp": None},
            {"nr": 3, "titel": "Meta-Label vergeben",
             "text": "Jeder Chunk bekommt einen Namen oder ein Bild — das Label. Das Label ist das, was du dir merkst; der Inhalt des Chunks entfaltet sich beim Abruf automatisch.",
             "tipp": "Wenn du für einen Chunk kein Label findest, ist er zu abstrakt oder zu groß. Teile ihn weiter auf."},
            {"nr": 4, "titel": "Chunk-Sequenz separat lernen",
             "text": "Erst die Reihenfolge der Chunks lernen (Struktur), dann den Inhalt jedes Chunks. Diese Trennung verhindert Überladung des Arbeitsgedächtnisses.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "IBAN merken",
             "inhalt": "DE12 3456 7890 1234 5678\n\nChunks: [DE12] [3456] [7890] [1234] [5678]\nLabels: [Länderkürzel + Prüfziffer] [Jahreszahl?] [Uhrzeit rückwärts] [...]  [Geburtsjahr?]\n\nNur 5 Chunks statt 22 Zeichen."},
            {"titel": "20 Vokabeln strukturieren",
             "inhalt": "20 neue Englischvokabeln als thematische Chunks:\n\nChunk 1 – Wetterphänomene: drizzle, hail, sleet, blizzard\nChunk 2 – Stimmungsverben: grumble, whine, sigh, rejoice\nChunk 3 – Küche: simmer, sauté, blanch, julienne\nChunk 4 – Reisen: embark, itinerary, layover, customs\nChunk 5 – Technik: bandwidth, latency, buffer, encrypt\n\nStatt 20 einzelne Wörter: 5 Chunks mit je 4 Elementen."},
        ],
        "fehler": [
            "Chunks zu groß: 12 Elemente in einem Chunk sind kein Chunk — das ist eine Liste.",
            "Keine Labels vergeben: ohne Meta-Label muss der Inhalt direkt erinnert werden, der Effizienzvorteil fällt weg.",
            "Zufällig chunken: 'die ersten 5 Elemente, dann die nächsten 5' ist kein Chunking. Bedeutung schlägt Bequemlichkeit.",
            "Nicht zwischen Chunk-Struktur und Chunk-Inhalt trennen: beides gleichzeitig lernen überlädt das Arbeitsgedächtnis.",
        ],
        "tipps": [
            "Nutze bestehende Chunks: Jahreszeiten, Monate, Wochentage sind bereits fertige Chunks, die du als Labels nutzen kannst.",
            "Nach dem Lesen einer Seite: welche 3–4 Kernaussagen (Chunks) gibt es? Das ist Chunk-Destillation.",
            "Chunking ist die Basis fast aller anderen Merktechniken. Jede Palast-Station ist ein Chunk.",
            "Für Prüfungen: lerne zuerst die Kapitelstruktur als Chunk-Baum, dann den Inhalt.",
        ],
        "kombination": [
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "Jede Palast-Station ist ein Chunk. Chunking und Palast sind natürliche Partner."},
            {"slug": "spaced-repetition", "icon": "📅", "titel": "Spaced Repetition", "grund": "Gut gechunkte Information wird effizienter durch Spaced Repetition konsolidiert."},
            {"slug": "elaborative-enkodierung", "icon": "🔍", "titel": "Elaborative Enkodierung", "grund": "Chunks, die du dir erklären kannst, sind stabiler als Chunks die nur auswendig gelernt sind."},
        ],
    },

    "pao-system": {
        "slug": "pao-system", "icon": "🎭", "titel": "PAO-System",
        "farbe": "amber", "typ": "Kompressionssystem", "schwierigkeit": "Fortgeschritten",
        "lernzeit": "Mehrere Monate für eine vollständige PAO-Liste",
        "best_fuer": "Kartendeck, 2-stellige Zahlen, lange Sequenzen",
        "spiel": "karten", "spiel_label": "🎴 Kartendeck trainieren",
        "meta_desc": "PAO-System (Person-Aktion-Objekt): 52 Karten als 18 Szenen – wie Gedächtnissportler ein Kartendeck in 2 Minuten merken. Schritt-für-Schritt-Anleitung.",
        "kurz": "Jedem Element (Karte, Zahl) wird eine feste Person, eine Aktion und ein Objekt zugeordnet. Je drei aufeinanderfolgende Elemente werden dann zu einer einzigen dramatischen Szene kombiniert — drei Karten werden zu einem Bild statt zu dreien.",
        "gehirn": [
            "PAO nutzt 'Superchunking': drei Informationseinheiten werden zu einer einzigen episodischen Szene komprimiert. Eine Szene ('Einstein wirft einen Apfel') belegt nur einen Slot im Arbeitsgedächtnis, obwohl sie drei Informationen trägt.",
            "Die Kraft liegt im episodischen Gedächtnis: Ereignisse erinnern wir viel besser als abstrakte Listen. Durch PAO werden abstrakte Sequenzen in lebhafte Erinnerungen verwandelt — das Gehirn ist für Szenen, nicht für Symbole gebaut.",
            "Gedächtnissportler, die ein 52-Karten-Deck in unter 2 Minuten merken, nutzen fast ausnahmslos PAO kombiniert mit dem Gedächtnispalast. Das Deck wird zu 17–18 Szenen, die an Palast-Stationen platziert werden.",
        ],
        "schritte": [
            {"nr": 1, "titel": "PAO-Liste erstellen",
             "text": "Für jedes Element (Karte, 2-stellige Zahl) eine feste Person, Aktion und Objekt festlegen. Für Karten: 52 Einträge. Für 2-stellige Zahlen: 100 Einträge (00–99). Die Zuordnungen müssen persönlich und emotional sein — berühmte Personen, markante Aktionen.",
             "tipp": "Beginne mit 10 Karten und trainiere sie in echten Übungen. Eine vollständige Liste in einer Woche zu lernen ist unrealistisch — schrittweise ausbauen."},
            {"nr": 2, "titel": "Dreiergruppen zu Szenen zusammenführen",
             "text": "Bei einer Kartensequenz: Karten 1, 2, 3 bilden eine Szene. Person aus Karte 1, Aktion aus Karte 2, Objekt aus Karte 3. Karten 4, 5, 6 → nächste Szene. Aus 52 Karten entstehen ~17 Szenen.",
             "tipp": None},
            {"nr": 3, "titel": "Szenen im Palast platzieren",
             "text": "Jede der ~17 Szenen wird an einer Station im Gedächtnispalast platziert. Beim Abruf: Palast durchgehen → Szene ablesen → Person (Karte 1), Aktion (Karte 2), Objekt (Karte 3).",
             "tipp": "Die Szene muss dynamisch sein: 'Einstein hält einen Apfel' ist schwach. 'Einstein katapultiert einen Apfel durch ein Fenster' ist stark."},
            {"nr": 4, "titel": "Rückwärts-Dekodierung üben",
             "text": "Beim Abruf: Bild → 'Wessen Aktion? Welches Objekt?' → drei Karten. Übe die Rückübersetzung separat, bis sie automatisch funktioniert.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "Drei Karten als eine Szene",
             "inhalt": "PAO-Zuordnung (Beispiel):\nAs♠  → Albert Einstein | katapultiert | Apfel\n2♥   → Marie Curie | reitet auf | Glühbirne\n3♦   → Sherlock Holmes | raucht mit | Lupe\n\nSequenz: As♠, 2♥, 3♦\n→ Szene: Einstein (Person As♠) reitet auf (Aktion 2♥) einer Lupe (Objekt 3♦).\n\nEin Bild statt drei Karten."},
            {"titel": "Zahlen-PAO (00–99)",
             "inhalt": "42 → 4=R, 2=N → 'Rana' / 'Rune' → Gandalf | weist mit Stab | Feuerball\n17 → 1=T, 7=K → 'Tück' → Joker | stolpert über | Spielkarte\n89 → 8=F, 9=B → 'Fobe' → Buchhalter | zählt | Geldscheine\n\nDreistellige Sequenz 421789:\n[42][17][89] → Gandalf (42) stolpert über (17) Geldscheine (89).\nEine Szene für 6 Ziffern."},
        ],
        "fehler": [
            "PAO-Liste zu schnell erstellen: schlechte Zuordnungen (zu abstrakt, ohne emotionale Verbindung) verlangsamen den Abruf dauerhaft.",
            "Szene nicht dynamisch: 'Person hält Objekt' ist kein Film. 'Person schleudert Objekt durch explodierendes Fenster' schon.",
            "PAO ohne Gedächtnispalast: ohne räumlichen Anker verliert die Sequenz ihre Ordnung.",
            "Zu früh mit zu vielen Elementen beginnen: 10 Karten trainieren, dann schrittweise erweitern.",
        ],
        "tipps": [
            "Nutze Personen, die du gut kennst und emotional verbindest: Filmcharaktere, Sportler, Familienmitglieder.",
            "Aktionen immer dynamisch und extrem: nicht 'gehen', sondern 'explodieren', 'katapultieren', 'verschlingen'.",
            "Übe die PAO-Liste mit Karteikarten (Karte → Bild → Karte), bis die Übersetzung unter 0,5 Sekunden läuft.",
            "PAO funktioniert auch für Vokabeln: Fremdwort → Person (die so klingt) + Aktion (die Bedeutung symbolisiert).",
        ],
        "kombination": [
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "PAO-Szenen im Palast platzieren — die Kombination aller Weltmeister."},
            {"slug": "major-system", "icon": "🔢", "titel": "Major-System", "grund": "Zahlen-PAO baut auf Major auf: Konsonanten der Zahl ergeben die Person/Aktion/Objekt-Grundlage."},
        ],
    },

    "spaced-repetition": {
        "slug": "spaced-repetition", "icon": "📅", "titel": "Spaced Repetition",
        "farbe": "sky", "typ": "Wiederholungssystem", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar; Disziplin ist der limitierende Faktor",
        "best_fuer": "Vokabeln, Fakten, Definitionen, alles mit langer Haltbarkeit",
        "spiel": "memory", "spiel_label": "🃏 Memory (Paar-Training)",
        "meta_desc": "Spaced Repetition: Ebbinghaus Vergessenskurve, optimale Wiederholungsabstände, Leitner-System, Anki. Wissenschaftlich die effektivste Methode für Langzeitgedächtnis.",
        "kurz": "Inhalte werden genau dann wiederholt, wenn du sie gerade zu vergessen drohst — kurz nach dem Lernen, dann nach 1 Tag, 3 Tagen, 1 Woche. Das Gehirn stärkt Gedächtnisspuren am meisten, wenn sie gerade zu verblassen beginnen.",
        "gehirn": [
            "Hermann Ebbinghaus dokumentierte 1885, dass Gedächtnisspuren nach dem Lernen exponentiell verblassen — die Vergessenskurve. Er entdeckte aber auch: wird Stoff genau vor dem Vergessen wiederholt, wird die Kurve bei jedem Zyklus flacher. Nach 5–6 optimalen Wiederholungen ist der Stoff langfristig verankert.",
            "Der Mechanismus: Abrufen eines Gedächtnisinhalts stärkt die beteiligten Synapsen. Entscheidend: aktives Abrufen aus dem Gedächtnis (Recall) ist dabei viel wirksamer als passives Wiederlesen. Tests stärken mehr als Lesen — der Testing Effect (Roediger & Karpicke, 2006).",
            "Moderne Algorithmen wie SuperMemo SM-2 (Basis für Anki) berechnen den optimalen Wiederholungszeitpunkt individuell pro Karte. Wer eine Karte schnell beantwortet, bekommt ein längeres Intervall. So entsteht ein personalisiertes System das Zeit maximiert.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Material in atomare Karteikarten aufteilen",
             "text": "Eine Karte = ein Fakt, eine Vokabel, eine Definition. Nicht mehrere Informationen pro Karte — das verhindert präzises Spacing. Vorder- und Rückseite: Frage → Antwort.",
             "tipp": "Atome statt Moleküle: lieber 5 einfache Karten als 1 komplexe. Komplexe Karten können nicht effizient gespaced werden."},
            {"nr": 2, "titel": "Wiederholungsintervalle einhalten",
             "text": "Manuell (Leitner-Box): 5 Fächer. Neue Karte → Fach 1. Richtig beantwortet → nächstes Fach. Falsch → zurück zu Fach 1.\n\nIntervalle: Fach 1 = täglich, Fach 2 = alle 2 Tage, Fach 3 = wöchentlich, Fach 4 = zweiwöchentlich, Fach 5 = monatlich.\n\nDigital: Anki oder RemNote berechnen den optimalen Zeitpunkt automatisch.",
             "tipp": None},
            {"nr": 3, "titel": "Aktiven Recall üben — nicht Wiederlesen",
             "text": "Schau auf die Frage, bedecke die Antwort und versuche sie aus dem Gedächtnis abzurufen. Das Abrufen selbst ist der Lernprozess. Passives Wiederlesen gibt eine falsche Sicherheit — Fluency Illusion.",
             "tipp": "Das Ringen mit der Antwort (Desirable Difficulty) stärkt die Gedächtnisspur mehr als sofortiges Nachschauen. Warte, bevor du schaust."},
            {"nr": 4, "titel": "Konsequent täglich wiederholen",
             "text": "Das System funktioniert nur, wenn fällige Karten tatsächlich wiederholt werden. Täglich 15–20 Minuten Anki ist effektiver als 2 Stunden einmal pro Woche. Kontinuität ist alles.",
             "tipp": "Streak-Mechaniken in Apps nutzen — die psychologische Wirkung ist real."},
        ],
        "beispiele": [
            {"titel": "Spanische Vokabeln mit Anki",
             "inhalt": "Karte: 'mariposa' → 'Schmetterling'\n\nTag 1: Gelernt.\nTag 2: Recall richtig → Intervall 4 Tage.\nTag 6: Recall richtig → Intervall 10 Tage.\nTag 16: Fast vergessen, knapp richtig → Intervall auf 7 Tage (reduziert).\nTag 23: Richtig → 14 Tage.\n\nNach 5 Wiederholungen: sitzt langfristig."},
            {"titel": "Prüfungsvorbereitung (4 Wochen)",
             "inhalt": "Woche 1–2: Alle Definitionen als Karten anlegen. Täglich 20 min Anki.\nWoche 3: Karten mit kurzem Intervall häufen sich — mehr Aufwand, aber Stoff konsolidiert.\nWoche 4 (Prüfungswoche): 90% des Stoffs bereits gefestigt. Kein Pauken in der Nacht davor nötig.\n\nKlassisches Pauken (alles in der letzten Nacht): hohe Kurzzeit-Leistung, rapides Vergessen danach.\nSpaced Repetition: moderate Mühe verteilt, aber dauerhaftes Behalten."},
        ],
        "fehler": [
            "Passiv wiederlesen statt aktiv abrufen: 'ich kenn das schon' ist Selbsttäuschung — Fluency Illusion.",
            "Karten zu komplex: 'Erkläre die Französische Revolution' ist keine SR-Karte. 'Welches Ereignis startete 1789 die Revolution?' schon.",
            "Fällige Karten aufschieben: wenn Karten 3 Tage übergangen werden, kollabiert das Spacing-System.",
            "Zu schnell zu viele neue Karten einführen: max. 20 neue Karten täglich, sonst bricht die Disziplin ein.",
            "Spaced Repetition als einzige Methode: SR speichert Fakten, aber kein Verständnis. Immer mit elaborativen Techniken kombinieren.",
        ],
        "tipps": [
            "Anki ist kostenlos, funktioniert offline und synchronisiert zwischen Geräten. 1 h Setup-Investition lohnt sich.",
            "Bester Zeitpunkt: morgens nach dem Aufwachen — Schlaf konsolidiert Gedächtnis, Wiederholung direkt danach ist besonders effektiv.",
            "Für komplexe Zusammenhänge: Cloze-Cards (Lückentext) statt einfacher Frage-Antwort.",
            "Community-Decks in Anki für häufige Themen (Medizin, Sprachen) existieren — nicht jede Karte selbst erstellen.",
        ],
        "kombination": [
            {"slug": "elaborative-enkodierung", "icon": "🔍", "titel": "Elaborative Enkodierung", "grund": "Erst elaborativ verstehen, dann mit Spaced Repetition festigen. Tiefes Verstehen macht SR 10× effektiver."},
            {"slug": "schluesselwort", "icon": "🗝️", "titel": "Schlüsselwort-Methode", "grund": "Schlüsselwort-Bild in Anki-Karte einbetten → optimales Langzeit-Vokabellernen."},
            {"slug": "chunking", "icon": "📦", "titel": "Chunking", "grund": "Gut gechunktes Material ist leichter in Karteikarten zu destillieren."},
        ],
    },

    "akrostichon": {
        "slug": "akrostichon", "icon": "🔤", "titel": "Akrostichon & Akronym",
        "farbe": "rose", "typ": "Anfangsbuchstaben-Technik", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar",
        "best_fuer": "Geordnete Listen, Fachbegriffe, Reihenfolgen bis ~10 Elemente",
        "spiel": "namen", "spiel_label": "👤 Namen & Gesichter",
        "meta_desc": "Akrostichon und Akronym: Anfangsbuchstaben als Merkhilfe. Unterschied erklärt, Schritt-für-Schritt, Beispiele für Planeten, Farben, OSI-Modell, Verhandlung.",
        "kurz": "Die Anfangsbuchstaben einer Liste werden zu einem Wort (Akronym) oder einem Satz (Akrostichon) zusammengefügt. Einfach, schnell und überraschend wirkungsvoll — besonders wenn die Liste eine feste Reihenfolge hat.",
        "gehirn": [
            "Akronyme nutzen das phonologische Gedächtnis und den Serial-Position-Effekt: Anfangselemente werden bevorzugt erinnert. Indem nur die Anfangsbuchstaben gespeichert werden und diese zu einem Wort oder Satz verbunden sind, reduziert sich die Informationslast drastisch.",
            "Ein Satz wie 'Mein Vater erklärt mir jeden Samstag unseren Nachthimmel' wird als rhythmische Einheit im Gedächtnis gespeichert, nicht als 8 separate Wörter. Der Rhythmus und die Bedeutungsstruktur des Satzes werden zum Abruf-Anker für die dahinterstehende Liste.",
            "Doppelter Enkodierungseffekt: wenn das Akrostichon eine lebhafte Szene erzeugt, wird es durch Dual Coding (sprachlich + visuell) nochmals stabiler.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Liste aufschreiben und Anfangsbuchstaben extrahieren",
             "text": "Schreibe die gesamte Liste auf. Notiere dann nur die Anfangsbuchstaben jedes Elements:\nMerkur, Venus, Erde, Mars, Jupiter, Saturn, Uranus, Neptun → M-V-E-M-J-S-U-N",
             "tipp": "Wenn die Reihenfolge egal ist: Buchstaben neu sortieren, um ein besseres Wort zu bilden."},
            {"nr": 2, "titel": "Akronym versuchen",
             "text": "Versuche aus den Anfangsbuchstaben ein reales oder erfundenes Wort zu bilden. Wenn das klappt: fertig. Wenn nicht: weiter zu Schritt 3.",
             "tipp": "Vokale können zwischen Konsonanten eingefügt werden — aber das verwässert die Zuverlässigkeit. Besser ein Akrostichon-Satz."},
            {"nr": 3, "titel": "Akrostichon: Buchstaben zu einem Satz",
             "text": "Bilde einen Satz, bei dem jedes Wort mit einem Anfangsbuchstaben beginnt. M-V-E-M-J-S-U-N → 'Mein Vater erklärt mir jeden Samstag unseren Nachthimmel'. Je absurder und dramatischer der Satz, desto besser.",
             "tipp": None},
            {"nr": 4, "titel": "Bild hinzufügen",
             "text": "Stelle dir die Szene des Akrostichons bildlich vor: Vater zeigt auf Sternenhimmel, jeder Planet als übergroßes Spielzeug. Das Bild fungiert als zusätzlicher Anker.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "Planeten in Reihenfolge",
             "inhalt": "Merkur, Venus, Erde, Mars, Jupiter, Saturn, Uranus, Neptun\n→ M-V-E-M-J-S-U-N\n\nAkrostichon (DE): 'Mein Vater erklärt mir jeden Samstag unseren Nachthimmel'\nAkrostichon (absurder): 'Mein Vater erschoss mit Jagdgewehr seine ungeliebten Nachbarn'\n\nBild: Vater steht im Garten, zeigt auf Planeten, jeder leuchtet in anderer Farbe."},
            {"titel": "OSI-Modell (7 Schichten)",
             "inhalt": "Physical, Data Link, Network, Transport, Session, Presentation, Application\n→ P-D-N-T-S-P-A\n\nEN: 'Please Do Not Throw Sausage Pizza Away'\nDE: 'Papa Der Nette Trug Seiner Putzfrau Auberginen'\n\nBild: Papa trägt einen Teller Auberginen-Pizza an einem Seil herunter."},
            {"titel": "Harvard-Prinzipien (BATNA & Co.)",
             "inhalt": "BATNA ist selbst bereits ein Akronym: Best Alternative To a Negotiated Agreement.\n→ B-A-T-N-A\n\nMerkhilfe für den Inhalt: 'Batman Atmet Tief Neben Abgrund'\nBild: Batman steht am Abgrund, denkt über seine beste Alternative nach."},
        ],
        "fehler": [
            "Akronym erzwingen: wenn kein natürliches Wort entsteht, ist das Akrostichon besser. Ein aufgezwungenes Pseudo-Wort ist schwerer zu merken als die Liste selbst.",
            "Kein Bild hinzufügen: der Satz allein ist gut, aber das dazugehörige Bild macht ihn dauerhaft.",
            "Für zu lange Listen: ab ~12 Elementen wird der Satz zu lang und verliert die mnemonische Kraft. Lieber zwei kürzere Sätze.",
            "Reihenfolge ignorieren: wenn die Reihenfolge der Liste wichtig ist, muss der Satz diese exakt widerspiegeln.",
        ],
        "tipps": [
            "Englische Akrostichons sind oft eleganter als deutsche — Englisch hat mehr kurze Wörter.",
            "Wenn du eine gute Version gefunden hast: teile sie — sie wird durch Wiedererzählen stabiler.",
            "Kombiniere Akronym mit einem Bild des Akronyms: NATO → ein Soldat namens Nato der in einem Tor steht.",
            "Für lange Fachbegriffe, die selbst Akronyme sind: lerne das Akronym zuerst, dann entfalte es im Akrostichon-Satz.",
        ],
        "kombination": [
            {"slug": "geschichten", "icon": "📖", "titel": "Geschichten-Methode", "grund": "Der Akrostichon-Satz wird zu einer kleinen Geschichte ausgebaut — das stärkt Bild und Sequenz."},
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "Das Akronym/Akrostichon als ein einziges Bild im Palast platzieren — mehrere Listen gleichzeitig merken."},
        ],
    },

    "geschichten": {
        "slug": "geschichten", "icon": "📖", "titel": "Geschichten-Methode",
        "farbe": "teal", "typ": "Verkettung / Linking", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar",
        "best_fuer": "Einkaufslisten, Aufgabenlisten, Vokabeln, lose Wortlisten bis ~12 Elemente",
        "spiel": "wortfolge", "spiel_label": "📝 Wortfolge trainieren",
        "meta_desc": "Geschichten-Methode (Linking): Lose Begriffe mit einer absurden Geschichte verknüpfen. Von-Restorff-Effekt, Anleitung, Beispiele für Einkaufslisten und Vokabeln.",
        "kurz": "Lose Elemente werden in einer lebhaften, absurden Geschichte miteinander verkettet. Jedes Bild triggert das nächste automatisch — die Assoziationskette führt durch die gesamte Liste. Je ungewöhnlicher und emotionaler, desto besser.",
        "gehirn": [
            "Der Von-Restorff-Effekt (Isolation Effect, 1933): ungewöhnliche, überraschende Elemente werden bevorzugt erinnert. Eine Banane in einer Obstschüssel fällt nicht auf — eine Banane, die durch die Wand fliegt, schon. Die Geschichten-Methode nutzt diesen Effekt systematisch.",
            "Narrative Strukturen sind evolutionär tief verankert. Menschen sind 'story animals' — Geschichten erinnern wir schneller und länger als Faktenlisten. Durch das Einbetten in eine Geschichte wird das episodische statt des semantischen Gedächtnisses aktiviert. Episodisches Gedächtnis ist deutlich robuster.",
            "Bidirektionale Assoziation: Bild B ruft Bild A ab (da B aus A entstand), und C ruft B ab. Diese Verkettung schafft ein redundantes Netz — fällt ein Link aus, ist der nächste oft trotzdem erreichbar.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Erstes Element konkretisieren",
             "text": "Übersetze das erste Element in ein spezifisches, konkretes Bild. Nicht 'Buch' allgemein — sondern 'ein riesiges, leuchtendes Buch mit rollenden Augen'. Je spezifischer und grotesker, desto besser der Anker.",
             "tipp": "Starte immer an einem festen Ankerpunkt — z. B. deiner Eingangstür. Das gibt der Geschichte räumlichen Kontext."},
            {"nr": 2, "titel": "Zweites Element absurd verknüpfen",
             "text": "Das zweite Element wächst aus dem ersten heraus: es explodiert, fliegt, singt, verwandelt sich. Die Verbindung muss sich bewegen und emotional sein. 'Das Buch öffnet sich und ein Drachen springt heraus' — Buch → Drachen.",
             "tipp": "Benutze immer ein starkes Verb: explodiert, verschluckt, katapultiert, verwandelt sich, stürzt, trifft. Schwache Verbindungen ('neben dem Buch liegt ein Drachen') werden schnell vergessen."},
            {"nr": 3, "titel": "Kette fortsetzen",
             "text": "Jedes neue Bild entsteht aus dem Ende der vorherigen Szene. Der Drachen landet im Regen — der Regen füllt einen Schuh — der Schuh wird von einer Schnecke getragen. Die Geschichte ist zusammenhängend, jedes Element kausiert das nächste.",
             "tipp": "Übertriebene Emotionen helfen: Ekel, Lachen, Erschrecken, Staunen. Die emotionale Reaktion ist selbst ein Anker."},
            {"nr": 4, "titel": "Geschichte einmal komplett durchgehen",
             "text": "Gehe die Geschichte direkt nach dem Erstellen einmal vollständig wie einen Film durch. Dann nach 10 Minuten nochmal. Das erste Abrufen festigt die Verknüpfungen am meisten.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "Einkaufsliste (8 Punkte)",
             "inhalt": "Milch, Brot, Eier, Tomaten, Nudeln, Käse, Wein, Bananen\n\nGeschichte:\nEine Milchflasche läuft die Straße entlang → trifft ein tanzendes Brot → das Brot stolpert, lässt Eier fallen → Eier platzen und enthüllen Tomaten → Tomaten rollen in eine Nudelpfanne → Pfanne explodiert mit Käse → Käse klebt an einer Weinflasche → die Flasche weint und hält eine Banane hoch.\n\nAbruf: Milchflasche → Brot → Eier → Tomaten → Nudeln → Käse → Wein → Bananen ✓"},
            {"titel": "5 Vokabeln Spanisch",
             "inhalt": "mariposa (Schmetterling), cielo (Himmel), lluvia (Regen), tierra (Erde), sol (Sonne)\n\nGeschichte:\nEin Schmetterling fliegt in den Himmel → dort beginnt es zu regnen → der Regen füllt die Erde → aus der Erde bricht die Sonne hervor → die Sonne lässt einen neuen Schmetterling entstehen.\n\nZusatz: Klanggeber (Schlüsselwort-Methode) für jedes Wort ins Bild einbauen."},
        ],
        "fehler": [
            "Schwache Verbindungen: 'Apfel liegt neben Buch' ist kein Link. 'Apfel explodiert in das Buch' ist einer.",
            "Geschichte zu lang: ab ~15 Elementen verliert die Geschichte Kohärenz. Für längere Listen besser den Gedächtnispalast nutzen.",
            "Zu realistische Szenen: das Gehirn filtert Erwartbares. Die Szene muss ungewöhnlich sein — physikalische Gesetze gelten in der Geschichte nicht.",
            "Kein erster Abruf: ohne Durchgang innerhalb von 30 Minuten verblassen die Links sehr schnell.",
        ],
        "tipps": [
            "Für Einkaufslisten, To-Dos, kurze Listen ist die Geschichten-Methode die schnellste Technik überhaupt — keine Vorbereitung nötig.",
            "Kombiniere mit dem Gedächtnispalast für lange Listen: die Geschichte spielt sich entlang der Palastroute ab.",
            "Die Geschichte muss nicht schön sein — je absurder und persönlicher, desto besser.",
            "Übe täglich mit der Wortfolge-App: sie trainiert genau diese Technik mit zufälligen Wortlisten.",
        ],
        "kombination": [
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "Für kurze Listen: Geschichte. Für lange geordnete Sequenzen: Palast. Kombiniert: Geschichte spielt sich entlang der Palastroute ab."},
            {"slug": "schluesselwort", "icon": "🗝️", "titel": "Schlüsselwort-Methode", "grund": "Für Fremdwörter: Schlüsselwort-Bild als Element in die Geschichte einbauen."},
        ],
    },

    "schluesselwort": {
        "slug": "schluesselwort", "icon": "🗝️", "titel": "Schlüsselwort-Methode",
        "farbe": "orange", "typ": "Assoziationstechnik", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar; mit Übung wird es automatisch",
        "best_fuer": "Fremdsprachen-Vokabeln, Fachbegriffe, Namen",
        "spiel": "wortfolge", "spiel_label": "📝 Wortfolge trainieren",
        "meta_desc": "Schlüsselwort-Methode für Vokabeln: Klanggeber + Bedeutungsbild. Atkinson & Raugh, Schritt-für-Schritt, Beispiele für Spanisch, Italienisch, Fachbegriffe.",
        "kurz": "Ein fremdes Wort wird durch ein klanglich ähnliches deutsches Schlüsselwort ersetzt — das Schlüsselwort wird dann mit der Bedeutung des Fremdworts zu einem Bild verknüpft. Zwei Schritte: klingt wie → bedeutet.",
        "gehirn": [
            "Atkinson und Raugh zeigten 1975: die Schlüsselwort-Methode verdoppelt den Lernerfolg für Fremdvokabeln verglichen mit reiner Wiederholung. Der Effekt ist robust und über viele Sprachen und Altersgruppen hinweg repliziert worden.",
            "Der Mechanismus nutzt zwei Systeme gleichzeitig: das phonologische Gedächtnis (Klanggeber: 'carta' klingt wie 'Karte') und das visuelle Gedächtnis (Bild: Postkarte klebt auf einem Brief). Diese bidirektionale Verknüpfung erzeugt eine stabile Gedächtnisspur.",
            "Entscheidend ist der zweite Schritt — das Bild. Ohne das Bild ist die phonetische Assoziation zu fragil. Das Bild muss die Bedeutung eindeutig enkodieren und gleichzeitig das Schlüsselwort enthalten.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Klanggeber finden (akustische Phase)",
             "text": "Höre das Fremdwort oder sprich es aus. Suche ein deutsches Wort, das klanglich ähnlich ist. Es muss nicht perfekt passen — grobe phonetische Ähnlichkeit reicht. 'carta' (Brief, Span.) → 'Karte'.",
             "tipp": "Wenn kein deutsches Wort klingt ähnlich: zerlege das Fremdwort in Silben. Ital. 'farfalla' → far + falla → 'Farbe' + 'Fall'."},
            {"nr": 2, "titel": "Bild erstellen (Bildphase)",
             "text": "Bilde ein mentales Bild, das sowohl das Schlüsselwort als auch die Bedeutung zeigt. 'carta' → 'Karte' → eine Postkarte, auf der ein Brief liegt. 'farfalla' → 'Farbe' + 'Fall' → ein bunter Schmetterling fällt in Farbe.",
             "tipp": "Das Bild muss die Bedeutung eindeutig enkodieren. Nicht 'Karte und Brief zusammen', sondern 'Postkarte klebt auf einem verschlossenen Brief'."},
            {"nr": 3, "titel": "Bidirektionale Verbindung üben",
             "text": "Übe beide Richtungen: Fremdwort → Bedeutung UND Bedeutung → Fremdwort. Beim aktiven Sprechen braucht man beide Richtungen. Spaced-Repetition-Karten in beide Richtungen anlegen.",
             "tipp": None},
        ],
        "beispiele": [
            {"titel": "Spanische Vokabeln",
             "inhalt": "carta (Brief) → 'Karte' → Postkarte klebt auf Brief\nmariposa (Schmetterling) → 'Mary-Po-Sa' → Mary hält Posaune, Schmetterling setzt sich drauf\ncielo (Himmel) → 'Kiel' → ein Kielschiff segelt durch den Himmel\nperro (Hund) → 'Pero' → ein Hund namens Pero schreibt Pirouetten\ncabeza (Kopf) → 'Käfig' → ein Käfig sitzt auf einem Kopf"},
            {"titel": "Lateinische Fachbegriffe (Biologie)",
             "inhalt": "Hippocampus (Gedächtnisregion) → 'Hippo + Campus' → ein Nilpferd auf einem Uni-Campus sortiert Erinnerungen\nAmygdala (Mandelkern, Emotion) → 'Mandel' → eine Mandel die Wut und Angst ausstrahlt\nSynapse (Nervenverbindung) → 'Syn-Apse' → zwei Affen (Syn/Apse) reichen sich über eine Lücke die Hände"},
            {"titel": "Englische Fachbegriffe",
             "inhalt": "BATNA → 'Batman' → Batman hält ein Verhandlungs-Netz\nKPI → 'Kippy' → Hund namens Kippy misst Leistungskennzahlen\nSWOT → 'Swat-Team' → ein Swat-Team analysiert Stärken und Schwächen"},
        ],
        "fehler": [
            "Nur die akustische Phase ohne das Bild: 'carta → Karte' allein ist zu schwach für langfristiges Erinnern.",
            "Das Bild zu abstrakt: 'Karte und Brief zusammen' ist kein Bild. 'Postkarte klebt auf verschlossenem Brief' schon.",
            "Schlüsselwort zu weit vom Fremdwort entfernt: wenn Klanggeber und Original zu unterschiedlich klingen, bricht die akustische Phase.",
            "Nur eine Richtung üben: wer nur 'carta → Brief' übt, kann spontan nicht sagen was 'Brief' auf Spanisch heißt.",
        ],
        "tipps": [
            "Schlüsselwort-Methode + Spaced Repetition in Anki: Bild auf Vorderseite, Fremdwort + Bedeutung auf Rückseite.",
            "Persönliche Schlüsselwörter sind immer effektiver als generische: 'mariposa klingt wie meine Tante Marisol' ist stärker als jede Standardassoziation.",
            "Langzeitziel: Fremdwort triggert direkt die Bedeutung ohne Umweg über das Schlüsselwort. Das dauert, stellt sich aber automatisch ein.",
            "Für Ortsnamen: Klanggeber + geografisches Detail. 'Bogotá' → Bogen + Stadt → ein Bogen der in die Stadt schießt.",
        ],
        "kombination": [
            {"slug": "geschichten", "icon": "📖", "titel": "Geschichten-Methode", "grund": "Schlüsselwort-Bilder in einer Geschichte verketten — ganze Vokabellisten als Geschichte merken."},
            {"slug": "spaced-repetition", "icon": "📅", "titel": "Spaced Repetition", "grund": "Schlüsselwort-Bild in Anki-Karte einbetten → optimales Langzeit-Vokabellernen."},
            {"slug": "gedaechtnispalast", "icon": "🏛️", "titel": "Gedächtnispalast", "grund": "Schlüsselwort-Bilder im Palast platzieren → viele Vokabeln geordnet abrufbar."},
        ],
    },

    "elaborative-enkodierung": {
        "slug": "elaborative-enkodierung", "icon": "🔍", "titel": "Elaborative Enkodierung",
        "farbe": "pink", "typ": "Verarbeitungstiefe", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar; wird mit Übung intuitiv",
        "best_fuer": "Konzepte, Zusammenhänge, Theorie, komplexes Wissen",
        "spiel": None, "spiel_label": None,
        "meta_desc": "Elaborative Enkodierung: Tiefe Verarbeitung statt Wiederholung. Craik & Lockhart Levels of Processing, Feynman-Technik, Self-Explanation. Für Konzepte und Zusammenhänge.",
        "kurz": "Statt Inhalte zu wiederholen, fragt man sich: Warum ist das so? Was folgt daraus? Wie hängt das mit Bekanntem zusammen? Tiefe semantische Verarbeitung erzeugt dauerhaftere Gedächtnisspuren als Wiederholung — das zeigt die Forschung eindeutig.",
        "gehirn": [
            "Craik und Lockhart entwickelten 1972 die 'Levels of Processing'-Theorie: je tiefer ein Inhalt verarbeitet wird, desto dauerhafter die Gedächtnisspur. Oberflächliche Verarbeitung (Wie viele Buchstaben hat das Wort?) erzeugt schwache Spuren. Semantische Verarbeitung (Was bedeutet es? Wozu dient es?) erzeugt starke, langlebige Spuren.",
            "Der Generation Effect (Slamecka & Graf, 1978): selbst generiertes Wissen wird besser erinnert als gelesenes. Wenn du dir selbst erklärst, warum etwas so ist, wird es tiefer verarbeitet und langfristiger gespeichert als bloßes Lesen.",
            "Elaborative Enkodierung aktiviert präfrontale Cortexregionen zusätzlich zum Hippocampus. Je mehr Hirnregionen an der Verarbeitung beteiligt sind, desto mehr Abrufwege existieren — das macht Wissen stabiler und flexibler anwendbar.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Zuerst lesen ohne Unterbrechung",
             "text": "Lies den Abschnitt vollständig durch, ohne sofort Notizen zu machen. Das gibt dem Inhalt Zeit, im Arbeitsgedächtnis zu 'landen'.",
             "tipp": None},
            {"nr": 2, "titel": "In eigenen Worten erklären (Feynman-Technik)",
             "text": "Klappe das Buch zu. Erkläre den Inhalt laut oder schriftlich, als würdest du ihn einem Fachfremden erklären. Wo du ins Stocken gerätst, fehlt echtes Verständnis.",
             "tipp": "Das Stocken ist wertvoll — es zeigt exakt, wo die Wissenslücke ist. Dort zurück zum Material, nicht übergehen."},
            {"nr": 3, "titel": "Fragen stellen",
             "text": "Warum ist das so? Unter welchen Bedingungen gilt es nicht? Was würde sich ändern, wenn...? Was folgt logisch daraus? Diese Fragen zwingen das Gehirn zu tiefer semantischer Verarbeitung.",
             "tipp": "Curious Child-Technik: stelle so lange 'Warum?' bis du an die fundamentalsten Grundlagen des Themas stößt."},
            {"nr": 4, "titel": "Mit Vorwissen verknüpfen",
             "text": "Wo habe ich etwas Ähnliches schon gesehen? Gibt es eine Analogie aus meinem Alltag? Querverbindungen sind die stärksten Gedächtnisanker.",
             "tipp": None},
            {"nr": 5, "titel": "Anwendungsfall generieren",
             "text": "In welcher konkreten Situation würde ich dieses Wissen nutzen? Stelle dir 2–3 spezifische Szenarien vor. Das verankert Wissen im episodischen Gedächtnis statt nur im semantischen.",
             "tipp": "Wenn du keinen Anwendungsfall findest: frage dich, ob du den Inhalt wirklich verstanden hast oder nur auswendig lernst."},
        ],
        "beispiele": [
            {"titel": "Nash-Gleichgewicht elaborativ lernen",
             "inhalt": "Oberflächlich: 'Kein Spieler kann durch einseitige Abweichung profitieren.'\n\nElaborativ:\n• Warum weicht keiner ab? → Weil der andere dann auch reagieren würde, was schlechter wäre.\n• Wann gilt es nicht? → Bei unvollständiger Information, bei irrationalem Verhalten.\n• Analogie: Links- vs. Rechtsverkehr — beide Systeme sind Nash-Gleichgewichte. Keiner weicht allein ab.\n• Anwendungsfall: Preisverhandlung mit Monopolist — gibt es ein Nash-Gleichgewicht, und wie breche ich es auf?"},
            {"titel": "Chemische Formel H₂O",
             "inhalt": "Oberflächlich: 'Zwei Wasserstoff, ein Sauerstoff.'\n\nElaborativ:\n• Warum ist Wasser bei Raumtemperatur flüssig? → Wasserstoffbrückenbindungen halten Moleküle zusammen.\n• Was folgt aus der Polarität? → Wasser ist ein ausgezeichnetes Lösungsmittel.\n• Analogie: H₂O-Polarität ist wie ein Magnet — ein Ende leicht positiv, das andere leicht negativ.\n• Warum ist Eis leichter als Wasser? → Im Eis bilden Wasserstoffbrücken ein Gitter mit mehr Raum."},
        ],
        "fehler": [
            "Stocken beim Feynman-Test ignorieren und weitermachen: der Punkt, wo man stockt, ist der wichtigste Lernmoment.",
            "Elaboration mit Auswendiglernen verwechseln: 'ich kann die Definition sagen' ist keine Elaboration.",
            "Keine Analogien finden: 'das hat keine Analogie zu meinem Alltag' — fast immer falsch. Aktiver suchen.",
            "Für reine Faktenlisten nutzen: für Vokabeln und isolierte Daten ist Spaced Repetition effizienter. Elaboration ist für Konzepte.",
        ],
        "tipps": [
            "Rubber-Duck-Debugging: erkläre den Stoff einer Gummiente. Der Prozess des Erklärens löst Verständnislücken auf.",
            "Schreibe nach dem Lesen einen Absatz aus dem Kopf — nicht abschauen. Was du nicht aus dem Kopf schreiben kannst, hast du nicht elaboriert.",
            "Nutze die Technik beim ersten Lesen, nicht als Nachbereitung: lese langsam und stoppe nach jedem Abschnitt.",
            "Elaboration + Spaced Repetition: erst elaborativ verstehen, dann Kernaussagen in Anki-Karten destillieren und festigen.",
        ],
        "kombination": [
            {"slug": "spaced-repetition", "icon": "📅", "titel": "Spaced Repetition", "grund": "Erst elaborativ verstehen, dann mit Spaced Repetition festigen. Tiefes Verstehen macht SR 10× effektiver."},
            {"slug": "chunking", "icon": "📦", "titel": "Chunking", "grund": "Elaboration hilft, die richtigen Chunks zu identifizieren — was ist Kernaussage, was ist Detail?"},
        ],
    },

    "zeigarnik": {
        "slug": "zeigarnik", "icon": "⏸️", "titel": "Zeigarnik-Effekt",
        "farbe": "lime", "typ": "Aufmerksamkeitslenkung", "schwierigkeit": "Einsteiger",
        "lernzeit": "Sofort anwendbar",
        "best_fuer": "Lernen, Präsentationen, Problemlösung, kreativer Output",
        "spiel": "corsi", "spiel_label": "🟦 Blockspanne (Konzentration)",
        "meta_desc": "Zeigarnik-Effekt: Unvollendetes bleibt im Gedächtnis. Bluma Zeigarnik, Ovsiankina-Effekt, Anwendung beim Lernen und in Präsentationen.",
        "kurz": "Unvollendete Aufgaben bleiben länger im aktiven Gedächtnis als abgeschlossene. Das Gehirn hält offene 'Loops' aktiv — was sich in erhöhter Erinnerungsleistung zeigt. Richtig eingesetzt ist das ein mächtiges Lernwerkzeug.",
        "gehirn": [
            "Bluma Zeigarnik beobachtete 1927, dass Kellner sich unbezahlte Bestellungen viel genauer erinnerten als bereits bezahlte. Sie testete dies systematisch: unabgeschlossene Aufgaben werden signifikant besser erinnert als abgeschlossene. Der Mechanismus: 'Aufgaben-Spannungen' im Arbeitsgedächtnis bleiben aktiv, bis die Aufgabe beendet ist.",
            "Der verwandte Ovsiankina-Effekt (1928): unterbrochene Aufgaben werden spontan wieder aufgenommen — auch ohne äußeren Anreiz. Das Gehirn 'will' Unvollendetes beenden. Diese Tendenz kann man nutzen, um sich automatisch wieder mit einem Thema zu beschäftigen.",
            "Cliffhanger in TV-Serien, angebrochene Aufgaben, offene Fragen — all das nutzt den Zeigarnik-Effekt, um Aufmerksamkeit zu binden. Für das Lernen bedeutet das: strategische Unterbrechungen steigern die Verarbeitungstiefe.",
        ],
        "schritte": [
            {"nr": 1, "titel": "Thema ankratzen, nicht abschließen",
             "text": "Beim Lernen: lies einen Abschnitt nicht vollständig durch, sondern stoppe an der interessantesten Stelle. Stelle eine Frage ans Material, ohne sofort die Antwort nachzuschlagen. Das Gehirn wird die Frage im Hintergrund weiterbearbeiten.",
             "tipp": "Funktioniert besonders gut vor dem Einschlafen: Frage ans Thema stellen, Buch schließen. Viele berichten, am nächsten Morgen Antworten zu haben."},
            {"nr": 2, "titel": "Pausen aktiv nutzen",
             "text": "Nach 25–45 Minuten Lernen: kurze Pause (5–10 Min), in der das Gelernte nicht aktiv bearbeitet wird. Der Hippocampus konsolidiert während Pausen — sogenanntes 'memory replay'.",
             "tipp": "Kein Handy in der Pause — neue Reize unterbrechen die Konsolidierung."},
            {"nr": 3, "titel": "Cliffhanger erzeugen",
             "text": "Fange eine schwierige Aufgabe an, ohne sie abzuschließen. 10 Minuten arbeiten, dann Pause, dann weitermachen. Die Aktivierung des offenen Loops erhöht Konzentration und Interesse beim Weitermachen.",
             "tipp": None},
            {"nr": 4, "titel": "In Präsentationen: offene Fragen stellen",
             "text": "Stelle zu Beginn einer Präsentation eine Frage oder ein Rätsel, das du erst am Ende auflöst. Das Publikum trägt den offenen Loop durch die gesamte Präsentation — erhöhte Aufmerksamkeit und bessere Retention.",
             "tipp": "Gute Einstiegsfrage: überraschend, spezifisch, relevant. 'Warum gewinnt der bessere Verhandler nicht immer?' — offen lassen bis zum Schluss."},
        ],
        "beispiele": [
            {"titel": "Zeigarnik-optimiertes Lernen",
             "inhalt": "Standard: Kapitel lesen → verstehen → Pause → nächstes Kapitel.\n\nZeigarnik-optimiert:\n1. Überschrift lesen → Frage formulieren: 'Was ist das Nash-Gleichgewicht und warum wichtig?'\n2. Erstes Drittel lesen → Pause (Frage noch offen)\n3. Im Hintergrund: Gehirn arbeitet an der Frage weiter\n4. Weiterlesen → Antwort erscheint befriedigender und bleibt haften\n5. Kapitel bewusst mit offener Folgefrage abschließen"},
            {"titel": "Präsentation mit Zeigarnik",
             "inhalt": "Classic Opening: 'Heute spreche ich über Verhandlungsstrategien nach dem Harvard-Modell.'\n\nZeigarnik Opening: 'In einem Experiment verloren 80% der Teilnehmer mehrere Hundert Euro — obwohl die Lösung trivial war. Woran lag das? Die Antwort gibt es am Ende.'\n\nErgebnis: Publikum trägt die offene Frage durch die Präsentation → höhere Aufmerksamkeit + bessere Retention der Kernaussagen."},
        ],
        "fehler": [
            "Zu viele offene Loops gleichzeitig: wenn alles unvollendet ist, wird das Arbeitsgedächtnis überlastet. 1–2 strategische Cliffhanger, nicht 10.",
            "Open Loop ohne Closure: wenn die Frage nie beantwortet wird, entsteht Frustration statt Retention.",
            "Zeigarnik mit Prokrastination verwechseln: unvollendete Aufgaben aus Vermeidung sind kein Lernwerkzeug — der Effekt wirkt nur bei aktiv begonnenen Aufgaben.",
            "In Prüfungssituationen: schwierige Fragen nicht mit dem Zeigarnik-Effekt offen lassen — das bindet Konzentration für andere Fragen.",
        ],
        "tipps": [
            "Der Zeigarnik-Effekt erklärt, warum Serienjunkies nicht aufhören können. Du kannst das fürs Lernen nachbauen.",
            "Bevor du von einem Thema abschaltest: formuliere explizit eine offene Frage ans Material. Dein Gehirn wird weiterarbeiten.",
            "Pomodoro-Technik (25/5 Min) ist eine strukturierte Form des Zeigarnik-Lernens: kurze Unterbrechungen erzeugen controlled open loops.",
            "Für kreative Arbeit: halte immer einen angefangenen Satz oder einen Entwurf 'offen' wenn du aufhörst. Die nächste Sitzung beginnt mit sofortigem Wiedereintauchen.",
        ],
        "kombination": [
            {"slug": "elaborative-enkodierung", "icon": "🔍", "titel": "Elaborative Enkodierung", "grund": "Zeigarnik öffnet den Loop (Frage stellen), Elaboration schließt ihn (Antwort erarbeiten). Maximale Verarbeitungstiefe."},
            {"slug": "spaced-repetition", "icon": "📅", "titel": "Spaced Repetition", "grund": "Fast Forgetting kurz nach dem Lernen ist der Zeigarnik-Zustand — Spaced Repetition schließt diesen Loop zum richtigen Zeitpunkt."},
        ],
    },
}


@router.get("/technik/{slug}", response_class=HTMLResponse)
def technik_detail(request: Request, slug: str):
    t = TECHNIKEN.get(slug)
    if not t:
        raise HTTPException(status_code=404, detail="Technik nicht gefunden")
    return templates.TemplateResponse(
        request, "gedaechtnis_technik.html", {"t": t, "active_page": "gedaechtnis"}
    )
