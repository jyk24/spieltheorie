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
    {
        "titel": "Endowment-Effekt",
        "icon": "☕",
        "beschreibung": "Wer eine Tasse besitzt, verlangt beim Verkauf das Doppelte des Kaufpreises. Besitz verändert Bewertung – die klassische Cornell-Studie von Kahneman, Knetsch & Thaler (1990).",
        "url": "/raetsel/endowment-effekt",
        "farbe": "amber",
    },
    {
        "titel": "IKEA-Effekt",
        "icon": "🪑",
        "beschreibung": "Selbst gebastelte Origami-Kraniche kosten das Fünffache. Investierte Anstrengung wird zum Teil des empfundenen Werts – Norton, Mochon & Ariely (2012).",
        "url": "/raetsel/ikea-effekt",
        "farbe": "orange",
    },
    {
        "titel": "Peak-End-Regel",
        "icon": "🌡️",
        "beschreibung": "Nicht die Summe des Erlebnisses zählt, sondern der Höhepunkt und das Ende. Warum Menschen die längere Prozedur wählen – Kahneman & Kollegen (1993).",
        "url": "/raetsel/peak-end-regel",
        "farbe": "teal",
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
