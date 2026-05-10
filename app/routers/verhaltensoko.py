"""Verhaltensökonomie Hub – Kognition, Wahrscheinlichkeit, Statistik & Psychologie."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .raetsel import RAETSEL_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_KATEGORIEN = {"Kognition", "Statistik", "Wahrscheinlichkeit", "Psychologie"}

THEMEN = [
    {
        "titel": "Prospect Theory & Verlustaversion",
        "icon": "⚖️",
        "beschreibung": "Verluste wiegen doppelt so schwer wie gleich große Gewinne – Kahneman & Tversky (1979, Nobelpreis 2002).",
        "url": "/raetsel/verlustaversion",
        "farbe": "amber",
    },
    {
        "titel": "Kognitive Verzerrungen",
        "icon": "🧠",
        "beschreibung": "Ankereffekt, Sunk Cost, Status-quo-Bias, Dunning-Kruger – das Repertoire systematischer Denkfehler.",
        "url": "/raetsel/sunk-cost",
        "farbe": "rose",
    },
    {
        "titel": "Bayesianisches Denken",
        "icon": "📐",
        "beschreibung": "Überzeugungen rational aktualisieren – Bayes-Theorem, falsch-positive Tests, Basisraten.",
        "url": "/raetsel/bayes-theorem",
        "farbe": "indigo",
    },
    {
        "titel": "Nudging & Entscheidungsarchitektur",
        "icon": "👉",
        "beschreibung": "Status-quo-Bias, Default-Effekte, Libertärer Paternalismus – Thaler & Sunstein (Nobelpreis 2017).",
        "url": "/raetsel/nudging",
        "farbe": "teal",
    },
    {
        "titel": "Wahrscheinlichkeitsfehler",
        "icon": "🎰",
        "beschreibung": "Spielerfehlschluss, Monty Hall, Geburtstagsparadoxon – Intuitionen, die systematisch scheitern.",
        "url": "/raetsel/monty-hall",
        "farbe": "violet",
    },
    {
        "titel": "Statistische Fallen",
        "icon": "📊",
        "beschreibung": "Simpson-Paradox, Survivorship Bias, Goodharts Gesetz – wenn Daten und Metriken täuschen.",
        "url": "/raetsel/goodharts-gesetz",
        "farbe": "sky",
    },
]


@router.get("/verhaltensoko", response_class=HTMLResponse)
def verhaltensoko_hub(request: Request):
    raetsel = [r for r in RAETSEL_META if r.get("kategorie") in _KATEGORIEN]
    return templates.TemplateResponse(
        request,
        "verhaltensoko.html",
        {"active_page": "verhaltensoko", "raetsel": raetsel, "themen": THEMEN},
    )
