"""Spielpfad – geführter Lernweg durch alle Spiele."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..game_registry import GAME_BY_SLUG
from ..models import UserProgress

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Only path-specific fields here (subtitle, runden).
# name and icon are pulled from game_registry at startup.
_LERNPFAD_RAW = [
    {
        "level": 1,
        "title": "Einstieg",
        "subtitle": "Die drei Grundbausteine der Spieltheorie",
        "color": "emerald",
        "games": [
            {"id": "gefangenendilemma", "subtitle": "Kooperation oder Eigennutz?", "runden": 10},
            {"id": "ultimatum",         "subtitle": "Fairness hat ihren Preis",     "runden": 10},
            {"id": "vertrauen",         "subtitle": "Lohnt sich Vertrauen?",         "runden": 8},
        ],
    },
    {
        "level": 2,
        "title": "Konflikt & Koordination",
        "subtitle": "Wenn Interessen kollidieren – oder sich ergänzen",
        "color": "blue",
        "games": [
            {"id": "chicken",    "subtitle": "Wer weicht zuerst zurück?",         "runden": 8},
            {"id": "stag-hunt",  "subtitle": "Riskiert man mehr, gewinnt man mehr", "runden": 8},
            {"id": "koordination","subtitle": "Einen gemeinsamen Weg finden",     "runden": 8},
            {"id": "rps",        "subtitle": "Zufall als optimale Strategie",      "runden": 7},
        ],
    },
    {
        "level": 3,
        "title": "Gruppen & Märkte",
        "subtitle": "Entscheidungen mit mehr als zwei Spielern",
        "color": "amber",
        "games": [
            {"id": "public-goods", "subtitle": "Das Trittbrettfahrerproblem",         "runden": 8},
            {"id": "diktator",     "subtitle": "Macht ohne Konsequenz",               "runden": 8},
            {"id": "auktion",      "subtitle": "Die überraschend einfache Lösung",    "runden": 5},
        ],
    },
    {
        "level": 4,
        "title": "Fortgeschritten",
        "subtitle": "Komplexe Entscheidungsstrukturen",
        "color": "orange",
        "games": [
            {"id": "beauty-contest", "subtitle": "Was denken die anderen?",          "runden": 6},
            {"id": "centipede",      "subtitle": "Wenn Logik sich selbst untergräbt", "runden": 4},
            {"id": "dollarauktion",  "subtitle": "Die Eskalationsfalle",              "runden": "var."},
            {"id": "verhandlung",    "subtitle": "Alles auf einmal",                  "runden": 6},
        ],
    },
    {
        "level": 5,
        "title": "Meister",
        "subtitle": "Emergenz und Marktdynamiken",
        "color": "violet",
        "games": [
            {"id": "minderheit",      "subtitle": "Gegen den Strom schwimmen",       "runden": 8},
            {"id": "gewinner-fluch",  "subtitle": "Wer gewinnt, zahlt zu viel",      "runden": 5},
            {"id": "cournot",         "subtitle": "Mengenführerschaft im Duopol",    "runden": 8},
        ],
    },
    {
        "level": 6,
        "title": "Experte",
        "subtitle": "Evolution, Nullsumme und Information",
        "color": "rose",
        "games": [
            {"id": "habicht-taube",       "subtitle": "Aggression vs. Kooperation – ESS",       "runden": 10},
            {"id": "geschlechter-kampf",  "subtitle": "Wer gibt nach – Battle of the Sexes",    "runden": 8},
            {"id": "freiwilligen-dilemma","subtitle": "Trittbrettfahren oder helfen?",           "runden": 8},
            {"id": "gleiche-muenzen",     "subtitle": "Matching Pennies – reines Nullsummenspiel", "runden": 10},
        ],
    },
]


def _enrich_game(g: dict) -> dict:
    """Merge path-specific fields with name/icon from the central registry."""
    meta = GAME_BY_SLUG.get(g["id"], {})
    return {
        **g,
        "name": meta.get("name", g["id"]),
        "icon": meta.get("icon", "🎮"),
        "mechanic": meta.get("mechanic", ""),
        "literature": meta.get("literature", ""),
    }


LERNPFAD = [
    {**level, "games": [_enrich_game(g) for g in level["games"]]}
    for level in _LERNPFAD_RAW
]

# Flat ordered list of slugs (used for progress tracking)
PFAD_ORDER = [g["id"] for level in LERNPFAD for g in level["games"]]


@router.get("/spielpfad", response_class=HTMLResponse)
def spielpfad_page(request: Request, db: Session = Depends(get_db)):
    progress_rows = db.query(UserProgress).all()
    played = {
        row.game_type.replace("_", "-"): row.games_played
        for row in progress_rows
    }

    return templates.TemplateResponse(
        request,
        "spielpfad.html",
        {
            "active_page": "spielpfad",
            "lernpfad": LERNPFAD,
            "played": played,
        },
    )
