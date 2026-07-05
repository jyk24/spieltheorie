"""Fermi-Schätzungen – Größenordnungen abschätzen wie Enrico Fermi.

Fermi-Probleme trainieren quantitatives Denken: Man zerlegt eine schwer
schätzbare Größe in besser schätzbare Faktoren, multipliziert – und liegt
oft überraschend nah an der Wahrheit. Ziel ist nicht Genauigkeit, sondern
die richtige *Größenordnung* (Faktor 10 zur Wahrheit gilt als Erfolg).
"""
import datetime as _dt
import math

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/fermi")
templates = Jinja2Templates(directory="app/templates")


# ---------------------------------------------------------------------------
# Fragenkatalog – kuratiert, mit Quellen und Fermi-Zerlegung
# ---------------------------------------------------------------------------

FERMI_QUESTIONS = [
    {
        "id": "klavierstimmer-chicago",
        "icon": "🎹",
        "name": "Klavierstimmer in Chicago",
        "kategorie": "Klassiker",
        "schwierigkeit": "Einsteiger",
        "frage": "Wie viele professionelle Klavierstimmer arbeiten in Chicago?",
        "einheit": "Klavierstimmer",
        "antwort": 200,
        "band_niedrig": 100,
        "band_hoch": 400,
        "quelle": "Klassisches Fermi-Problem aus der Physiker-Ausbildung; empirische Schätzungen 1990er-Jahre",
        "kontext": "Enrico Fermi (Nobelpreis 1938) stellte seinen Studenten in Chicago genau diese Frage. Kein Nachschlagen erlaubt – nur Denken. Die Berufsschätzung des US-Arbeitsministeriums lag bei etwa 200 tätigen Klavierstimmern im Großraum Chicago.",
        "zerlegung": [
            {"faktor": "Einwohner Chicago (Metropolregion)", "wert": "≈ 9.000.000"},
            {"faktor": "Menschen pro Haushalt", "wert": "≈ 2"},
            {"faktor": "→ Haushalte", "wert": "≈ 4.500.000"},
            {"faktor": "Anteil mit Klavier", "wert": "≈ 1 / 30 ≈ 3 %"},
            {"faktor": "→ Klaviere im Privatbesitz", "wert": "≈ 150.000"},
            {"faktor": "Stimmungen pro Klavier & Jahr", "wert": "≈ 1"},
            {"faktor": "→ Stimmungen pro Jahr", "wert": "≈ 150.000"},
            {"faktor": "Stimmungen ein Stimmer / Jahr (4 pro Tag × 200 Arbeitstage)", "wert": "≈ 800"},
            {"faktor": "→ Klavierstimmer", "wert": "≈ 150.000 / 800 ≈ 190"},
        ],
    },
    {
        "id": "worte-pro-tag",
        "icon": "💬",
        "name": "Wörter pro Tag",
        "kategorie": "Alltag",
        "schwierigkeit": "Einsteiger",
        "frage": "Wie viele Wörter spricht ein Mensch an einem durchschnittlichen Tag?",
        "einheit": "Wörter",
        "antwort": 16000,
        "band_niedrig": 8000,
        "band_hoch": 22000,
        "quelle": "Mehl et al., Science 317:82 (2007) – EAR-Studie mit 396 Probanden",
        "kontext": "Die vielzitierte Behauptung, Frauen sprächen 20.000 Wörter pro Tag und Männer nur 7.000, entpuppte sich 2007 als Mythos: Beide Geschlechter kamen auf etwa 16.000 Wörter, mit sehr großer Streuung (500 bis 47.000).",
        "zerlegung": [
            {"faktor": "Wache Stunden pro Tag", "wert": "≈ 16"},
            {"faktor": "Anteil mit Sprechen (Job, Familie, Telefon)", "wert": "≈ 40 % ≈ 6,5 h"},
            {"faktor": "Sprechminuten daraus", "wert": "≈ 400 min"},
            {"faktor": "Wörter pro Minute (Konversation)", "wert": "≈ 100 – 150"},
            {"faktor": "→ Wörter", "wert": "≈ 16.000"},
        ],
    },
    {
        "id": "herzschlaege-leben",
        "icon": "❤️",
        "name": "Herzschläge im Leben",
        "kategorie": "Biologie",
        "schwierigkeit": "Einsteiger",
        "frage": "Wie oft schlägt das Herz eines Menschen in einem 80-jährigen Leben?",
        "einheit": "Schläge",
        "antwort": 2_800_000_000,
        "band_niedrig": 2_000_000_000,
        "band_hoch": 3_500_000_000,
        "quelle": "Levine, Cardiology 90:207 (1997) – Herz-Ratenberechnung über Lebenszeit",
        "kontext": "Faszinierend: Fast alle Säugetiere haben in ihrem Leben etwa 1 Milliarde Herzschläge – nur der Mensch schafft dank moderner Medizin das Zwei- bis Dreifache. Die Maus schlägt 500-mal pro Minute und lebt zwei Jahre, der Elefant 30-mal und lebt 70 Jahre.",
        "zerlegung": [
            {"faktor": "Ruhepuls (Schläge pro Minute)", "wert": "≈ 70"},
            {"faktor": "Minuten pro Stunde", "wert": "60"},
            {"faktor": "Stunden pro Tag", "wert": "24"},
            {"faktor": "Tage pro Jahr", "wert": "365"},
            {"faktor": "Lebensjahre", "wert": "80"},
            {"faktor": "→ Schläge", "wert": "70 × 60 × 24 × 365 × 80 ≈ 2,9 Mrd."},
        ],
    },
    {
        "id": "golfbaelle-schulbus",
        "icon": "⛳",
        "name": "Golfbälle in einem Schulbus",
        "kategorie": "Volumen",
        "schwierigkeit": "Mittel",
        "frage": "Wie viele Golfbälle passen in einen US-Schulbus (Yellow Bus)?",
        "einheit": "Golfbälle",
        "antwort": 500_000,
        "band_niedrig": 250_000,
        "band_hoch": 900_000,
        "quelle": "Klassische Google-Bewerbungsfrage, William Poundstone: How Would You Move Mount Fuji? (2003)",
        "kontext": "Diese Frage wurde von Google in Bewerbungsgesprächen gestellt – nicht wegen der Antwort, sondern wegen des Vorgehens. Google hat solche Fragen 2013 abgeschafft: sie prädizieren keine Job-Performance (Laszlo Bock, SVP People Ops).",
        "zerlegung": [
            {"faktor": "Bus-Innenraum (L × B × H)", "wert": "≈ 12 m × 2,3 m × 2 m"},
            {"faktor": "→ Volumen", "wert": "≈ 55 m³"},
            {"faktor": "Abzug Sitze, Motor, Freiraum", "wert": "≈ 30 %"},
            {"faktor": "→ Nutzvolumen", "wert": "≈ 38 m³ ≈ 38.000 Liter"},
            {"faktor": "Volumen eines Golfballs (⌀ 4,3 cm)", "wert": "≈ 41 cm³"},
            {"faktor": "Packungseffizienz Kugeln", "wert": "≈ 65 %"},
            {"faktor": "→ Golfbälle", "wert": "(38.000.000 × 0,65) / 41 ≈ 600.000"},
        ],
    },
    {
        "id": "blaetter-eiche",
        "icon": "🍂",
        "name": "Blätter einer Eiche",
        "kategorie": "Biologie",
        "schwierigkeit": "Mittel",
        "frage": "Wie viele Blätter hat eine ausgewachsene Eiche (~25 m hoch)?",
        "einheit": "Blätter",
        "antwort": 250_000,
        "band_niedrig": 100_000,
        "band_hoch": 500_000,
        "quelle": "Bundeswaldinventur; Studien zur Laubbaum-Photosynthese (z.B. Röhle 1997)",
        "kontext": "Eine ausgewachsene Eiche produziert pro Jahr circa 200 kg Blattmasse und 25 kg Sauerstoff – genug für 10 Menschen. Die Zahl der Blätter variiert je nach Alter, Standort und Jahr stark, aber die Größenordnung liegt sicher bei einigen Hunderttausend.",
        "zerlegung": [
            {"faktor": "Kronen-Durchmesser", "wert": "≈ 15 m"},
            {"faktor": "Kronen-Höhe (nur belaubt)", "wert": "≈ 12 m"},
            {"faktor": "→ Kronen-Volumen (Ellipsoid)", "wert": "≈ 1.400 m³"},
            {"faktor": "Blattdichte (Blätter pro m³ Krone)", "wert": "≈ 200"},
            {"faktor": "→ Blätter", "wert": "≈ 280.000"},
        ],
    },
    {
        "id": "pizzen-deutschland",
        "icon": "🍕",
        "name": "Pizzen pro Tag in Deutschland",
        "kategorie": "Alltag",
        "schwierigkeit": "Mittel",
        "frage": "Wie viele Pizzen werden in Deutschland an einem durchschnittlichen Tag gegessen (Restaurant + TK + Selbstgemacht)?",
        "einheit": "Pizzen",
        "antwort": 1_700_000,
        "band_niedrig": 800_000,
        "band_hoch": 3_000_000,
        "quelle": "GfK Consumer Scan 2022 (TK-Pizza); DEHOGA Umsatzstatistik Gastronomie",
        "kontext": "Deutsche essen im Durchschnitt 7,5 kg Tiefkühlpizza pro Kopf und Jahr – Weltrekord. Zusätzlich kommen Restaurant-Pizzen (~1,5 Mrd. jährlich) und selbstgemachte hinzu. Die Pizza ist Deutschlands beliebteste Speise nach Umfragen.",
        "zerlegung": [
            {"faktor": "Einwohner Deutschland", "wert": "≈ 84 Mio."},
            {"faktor": "Pizzen pro Kopf und Jahr", "wert": "≈ 7 – 8"},
            {"faktor": "→ Pizzen pro Jahr", "wert": "≈ 620 Mio."},
            {"faktor": "→ Pizzen pro Tag", "wert": "620 Mio. / 365 ≈ 1,7 Mio."},
        ],
    },
    {
        "id": "haare-kopf",
        "icon": "💇",
        "name": "Haare auf einem Kopf",
        "kategorie": "Biologie",
        "schwierigkeit": "Einsteiger",
        "frage": "Wie viele Haare hat ein durchschnittlicher menschlicher Kopf?",
        "einheit": "Haare",
        "antwort": 100_000,
        "band_niedrig": 80_000,
        "band_hoch": 150_000,
        "quelle": "Loussouarn et al., British Journal of Dermatology 156:117 (2007)",
        "kontext": "Blonde haben mit ~150.000 die meisten Haare, Rothaarige mit ~90.000 die wenigsten. Wir verlieren normal 50–100 Haare pro Tag. Ein einzelnes Haar wächst 2–7 Jahre lang, ~1 cm pro Monat, und trägt bis zu 100 g Zugkraft.",
        "zerlegung": [
            {"faktor": "Kopfhautfläche (Schädel)", "wert": "≈ 700 cm²"},
            {"faktor": "Haardichte (Follikel pro cm²)", "wert": "≈ 150"},
            {"faktor": "→ Haare", "wert": "≈ 105.000"},
        ],
    },
    {
        "id": "buecher-nationalbibliothek",
        "icon": "📚",
        "name": "Bücher der Deutschen Nationalbibliothek",
        "kategorie": "Wissenswert",
        "schwierigkeit": "Fortgeschritten",
        "frage": "Wie viele Bücher (Monografien, keine Zeitschriften/Medien) besitzt die Deutsche Nationalbibliothek?",
        "einheit": "Bücher",
        "antwort": 20_000_000,
        "band_niedrig": 10_000_000,
        "band_hoch": 40_000_000,
        "quelle": "Deutsche Nationalbibliothek – Jahresbericht 2023",
        "kontext": "Die DNB (Frankfurt + Leipzig) sammelt seit 1913 pflichtgemäß jede in Deutschland veröffentlichte Publikation. Insgesamt umfasst der Bestand über 45 Mio. Medieneinheiten, davon etwa die Hälfte Bücher. Pro Jahr kommen ~600.000 neue Medien dazu.",
        "zerlegung": [
            {"faktor": "Neue Bücher pro Jahr in Deutschland", "wert": "≈ 70.000 – 90.000"},
            {"faktor": "Pflichtabgabe seit ca. 1913", "wert": "≈ 110 Jahre"},
            {"faktor": "→ Titel im DNB-Bestand (nur Bücher, ohne Reprints)", "wert": "≈ 20 Mio."},
        ],
    },
    {
        "id": "wasser-mensch-leben",
        "icon": "💧",
        "name": "Wasserverbrauch im Leben",
        "kategorie": "Alltag",
        "schwierigkeit": "Mittel",
        "frage": "Wie viele Liter Trinkwasser verbraucht ein Deutscher (Haushalt) in einem 80-jährigen Leben?",
        "einheit": "Liter",
        "antwort": 3_800_000,
        "band_niedrig": 2_000_000,
        "band_hoch": 6_000_000,
        "quelle": "Bundesverband der Energie- und Wasserwirtschaft (BDEW) 2023: 128 L/Tag pro Person",
        "kontext": "Deutschland ist beim Wasserverbrauch sehr sparsam: 128 Liter täglich pro Kopf im Haushalt – 1990 waren es noch 147 Liter. Nicht mitgerechnet: der 'virtuelle' Wasserverbrauch durch importierte Lebensmittel und Konsumgüter, der etwa 4.000 L/Tag beträgt.",
        "zerlegung": [
            {"faktor": "Wasserverbrauch pro Person und Tag (Haushalt)", "wert": "≈ 128 L"},
            {"faktor": "Tage pro Jahr", "wert": "365"},
            {"faktor": "Lebensjahre", "wert": "80"},
            {"faktor": "→ Liter", "wert": "128 × 365 × 80 ≈ 3.740.000"},
        ],
    },
    {
        "id": "gedanken-pro-tag",
        "icon": "🧠",
        "name": "Gedanken pro Tag",
        "kategorie": "Kognition",
        "schwierigkeit": "Fortgeschritten",
        "frage": "Wie viele bewusste Gedanken hat ein Mensch an einem Tag (grobe Neuro-Schätzung)?",
        "einheit": "Gedanken",
        "antwort": 6_000,
        "band_niedrig": 2_000,
        "band_hoch": 15_000,
        "quelle": "Tseng & Poppenk, Nature Communications 11:3480 (2020) – fMRT-basierte Gedanken-Übergänge",
        "kontext": "Die oft zitierte Zahl '60.000 Gedanken pro Tag' hat keine wissenschaftliche Grundlage. Eine 2020 in Nature Communications veröffentlichte Studie mit fMRT identifizierte etwa 6.200 diskrete Gedanken-Übergänge pro Tag – ein Zehntel der Alltagsweisheit.",
        "zerlegung": [
            {"faktor": "Wache Stunden pro Tag", "wert": "≈ 16"},
            {"faktor": "Minuten daraus", "wert": "≈ 960"},
            {"faktor": "Gedanken pro Minute (fMRT-Studie)", "wert": "≈ 6,5"},
            {"faktor": "→ Gedanken", "wert": "≈ 6.200"},
        ],
    },
    {
        "id": "ameisen-erde",
        "icon": "🐜",
        "name": "Ameisen auf der Erde",
        "kategorie": "Biologie",
        "schwierigkeit": "Fortgeschritten",
        "frage": "Wie viele einzelne Ameisen leben insgesamt auf der Erde?",
        "einheit": "Ameisen",
        "antwort": 20_000_000_000_000_000,
        "band_niedrig": 5_000_000_000_000_000,
        "band_hoch": 50_000_000_000_000_000,
        "quelle": "Schultheiss et al., PNAS 119:e2201550119 (2022) – Meta-Analyse von 465 Studien",
        "kontext": "Die weltweit umfassendste Meta-Analyse (2022) schätzt: 20 Billiarden (2×10¹⁶) Ameisen leben auf der Erde. Ihre gesamte Biomasse beträgt ~12 Mio. Tonnen Trockengewicht – mehr als die Biomasse aller wilden Vögel und Säugetiere zusammen. Pro Mensch existieren rund 2,5 Millionen Ameisen.",
        "zerlegung": [
            {"faktor": "Landfläche Erde", "wert": "≈ 149 Mio. km² = 1,49 × 10¹⁴ m²"},
            {"faktor": "Ameisendichte (weltweit gemittelt)", "wert": "≈ 130 pro m²"},
            {"faktor": "→ Ameisen", "wert": "≈ 2 × 10¹⁶"},
        ],
    },
    {
        "id": "wolken-tropfen",
        "icon": "☁️",
        "name": "Tropfen in einer Wolke",
        "kategorie": "Physik",
        "schwierigkeit": "Fortgeschritten",
        "frage": "Wie viele Wassertröpfchen enthält eine typische kleine Cumulus-Wolke (1 km³)?",
        "einheit": "Tropfen",
        "antwort": 1_000_000_000_000_000,
        "band_niedrig": 100_000_000_000_000,
        "band_hoch": 10_000_000_000_000_000,
        "quelle": "Rogers & Yau: A Short Course in Cloud Physics (1996)",
        "kontext": "Eine Cumulus-Wolke enthält bis zu 500.000 Liter Wasser – aber verteilt auf so winzige Tröpfchen (10-20 μm), dass ihre kombinierte Zahl kaum vorstellbar ist. Deshalb 'schwebt' die Wolke: Der Luftwiderstand pro Tropfen überwiegt die Gravitation.",
        "zerlegung": [
            {"faktor": "Wolken-Volumen", "wert": "≈ 1 km³ = 10⁹ m³ = 10¹² Liter"},
            {"faktor": "Wassergehalt Cumulus", "wert": "≈ 0,5 g/m³"},
            {"faktor": "→ Wassermasse", "wert": "≈ 500 Tonnen = 5 × 10⁸ g"},
            {"faktor": "Tropfengröße (Radius 10 μm)", "wert": "≈ 4 × 10⁻⁹ g je Tropfen"},
            {"faktor": "→ Tropfen", "wert": "≈ 1,3 × 10¹⁷"},
        ],
    },
]


FERMI_BY_ID = {q["id"]: q for q in FERMI_QUESTIONS}


# ---------------------------------------------------------------------------
# Log-Skala-Scoring
# ---------------------------------------------------------------------------

def _score(user_estimate: float, truth: float) -> dict:
    """Log-Skala Score. Faktor 10 = Bronze, Faktor 3 = Silber, Faktor 2 = Gold."""
    if user_estimate <= 0 or truth <= 0:
        return {
            "faktor": None,
            "log_off": None,
            "stufe": "invalid",
            "text": "Schätzung muss positiv sein.",
            "farbe": "slate",
        }
    ratio = user_estimate / truth
    log_off = abs(math.log10(ratio))
    faktor = max(ratio, 1 / ratio)

    if log_off < math.log10(2):
        stufe, text, farbe = "gold", "⭐⭐⭐ Meisterhaft – innerhalb Faktor 2!", "amber"
    elif log_off < math.log10(3):
        stufe, text, farbe = "silber", "⭐⭐ Sehr gut – innerhalb Faktor 3.", "emerald"
    elif log_off < 1:  # < Faktor 10
        stufe, text, farbe = "bronze", "⭐ Fermi-Ziel erreicht: Größenordnung stimmt (Faktor 10).", "sky"
    elif log_off < 2:  # < Faktor 100
        stufe, text, farbe = "nah", "🔎 Knapp verfehlt: 1–2 Größenordnungen daneben.", "indigo"
    else:
        stufe, text, farbe = "weit", "😅 Weit daneben: mehr als 100-fach abweichend.", "rose"
    return {
        "faktor": faktor,
        "log_off": log_off,
        "stufe": stufe,
        "text": text,
        "farbe": farbe,
    }


def _format_zahl(n: float) -> str:
    """Deutsche Formatierung, mit sinnvollen Einheiten."""
    if n == 0:
        return "0"
    abs_n = abs(n)
    if abs_n >= 1e15:
        return f"{n/1e15:.2f} Billiarden".replace(".", ",")
    if abs_n >= 1e12:
        return f"{n/1e12:.2f} Billionen".replace(".", ",")
    if abs_n >= 1e9:
        return f"{n/1e9:.2f} Mrd.".replace(".", ",")
    if abs_n >= 1e6:
        return f"{n/1e6:.2f} Mio.".replace(".", ",")
    if abs_n >= 1000:
        return f"{n:,.0f}".replace(",", ".")
    return f"{n:.0f}"


# ---------------------------------------------------------------------------
# Routen
# ---------------------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
def fermi_overview(request: Request):
    day_num = _dt.date.today().timetuple().tm_yday
    featured = FERMI_QUESTIONS[day_num % len(FERMI_QUESTIONS)]
    return templates.TemplateResponse(
        request,
        "fermi.html",
        {
            "active_page": "fermi",
            "fragen": FERMI_QUESTIONS,
            "featured": featured,
            "gesamt": len(FERMI_QUESTIONS),
        },
    )


@router.get("/{qid}", response_class=HTMLResponse)
def fermi_frage(request: Request, qid: str):
    q = FERMI_BY_ID.get(qid)
    if q is None:
        raise HTTPException(status_code=404, detail="Fermi-Frage nicht gefunden")
    idx = next(i for i, x in enumerate(FERMI_QUESTIONS) if x["id"] == qid)
    next_q = FERMI_QUESTIONS[(idx + 1) % len(FERMI_QUESTIONS)]
    return templates.TemplateResponse(
        request,
        "fermi_frage.html",
        {"active_page": "fermi", "q": q, "next_q": next_q},
    )


@router.post("/{qid}/schaetzung", response_class=HTMLResponse)
def fermi_schaetzung(request: Request, qid: str, schaetzung: str = Form(...)):
    q = FERMI_BY_ID.get(qid)
    if q is None:
        raise HTTPException(status_code=404, detail="Fermi-Frage nicht gefunden")

    raw = schaetzung.strip().replace(".", "").replace(",", ".").replace(" ", "")
    try:
        user = float(raw)
    except ValueError:
        user = 0.0

    result = _score(user, q["antwort"])
    return templates.TemplateResponse(
        request,
        "partials/fermi_result.html",
        {
            "q": q,
            "user": user,
            "user_str": _format_zahl(user),
            "antwort_str": _format_zahl(q["antwort"]),
            "band_n_str": _format_zahl(q["band_niedrig"]),
            "band_h_str": _format_zahl(q["band_hoch"]),
            "result": result,
        },
    )
