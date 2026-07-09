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
    {"slug": "section-1", "titel": "Was ist Spieltheorie?",                 "icon": "🎯", "dauer": "5 min"},
    {"slug": "section-2", "titel": "Was bedeutet „rational“?",              "icon": "🧠", "dauer": "4 min"},
    {"slug": "section-3", "titel": "Die drei Kernkonzepte",                 "icon": "♟️", "dauer": "8 min"},
    {"slug": "section-4", "titel": "Wichtige Spieltypen",                   "icon": "🗂️", "dauer": "6 min"},
    {"slug": "section-5", "titel": "Gemischte Strategien",                  "icon": "🎲", "dauer": "7 min"},
    {"slug": "section-6", "titel": "Grenzen der Rationalität",              "icon": "⚠️", "dauer": "6 min"},
    {"slug": "section-7", "titel": "Signaling, Screening & Information",    "icon": "📡", "dauer": "8 min"},
    {"slug": "section-8", "titel": "Verhandlung & Spieltheorie",            "icon": "💼", "dauer": "8 min"},
    {"slug": "section-9", "titel": "Evolutionäre Spieltheorie",             "icon": "🧬", "dauer": "8 min"},
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
