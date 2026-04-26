"""Spieltheorie & Entscheidung – thematischer Hub."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .raetsel import RAETSEL_META
from .spiele import GAME_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_KATEGORIEN = {"Spieltheorie", "Wahrscheinlichkeit", "Statistik", "Kognition"}

GRUNDLAGEN_SEKTIONEN = [
    {"slug": "einfuehrung",        "titel": "Einführung in die Spieltheorie",    "icon": "🎯", "dauer": "8 min"},
    {"slug": "nash",               "titel": "Nash-Gleichgewicht",                "icon": "♟️", "dauer": "10 min"},
    {"slug": "dominante-strategie","titel": "Dominante Strategien",              "icon": "⚡", "dauer": "6 min"},
    {"slug": "sequentiell",        "titel": "Sequentielle Spiele & Backward Induction", "icon": "🔢", "dauer": "8 min"},
    {"slug": "gemischte",          "titel": "Gemischte Strategien",              "icon": "🎲", "dauer": "7 min"},
    {"slug": "kooperation",        "titel": "Kooperation & Wiederholung",        "icon": "🤝", "dauer": "9 min"},
    {"slug": "verhandlung",        "titel": "Verhandlung & Bargaining",          "icon": "💼", "dauer": "10 min"},
    {"slug": "information",        "titel": "Information & Signaling",           "icon": "📡", "dauer": "10 min"},
    {"slug": "evolution",          "titel": "Evolutionäre Spieltheorie",         "icon": "🧬", "dauer": "8 min"},
]

SKILLS_CARDS = [
    {"titel": "BATNA & ZOPA",         "icon": "🤝", "beschreibung": "Beste Alternative bestimmt deine Verhandlungsmacht", "url": "/skills"},
    {"titel": "Prospect Theory",       "icon": "📉", "beschreibung": "Verluste wiegen doppelt so schwer wie Gewinne",     "url": "/skills"},
    {"titel": "Signaling & Screening", "icon": "📡", "beschreibung": "Glaubwürdige Signale in asymmetrischer Information","url": "/skills"},
    {"titel": "Ankern & Framing",      "icon": "⚓", "beschreibung": "Der erste Wert prägt das gesamte Ergebnis",         "url": "/skills"},
]


@router.get("/spieltheorie", response_class=HTMLResponse)
def spieltheorie_hub(request: Request):
    raetsel = [r for r in RAETSEL_META if r.get("kategorie") in _KATEGORIEN]
    return templates.TemplateResponse(
        request,
        "spieltheorie.html",
        {
            "active_page": "spieltheorie",
            "games": GAME_META,
            "raetsel": raetsel,
            "grundlagen": GRUNDLAGEN_SEKTIONEN,
            "skills": SKILLS_CARDS,
        },
    )
