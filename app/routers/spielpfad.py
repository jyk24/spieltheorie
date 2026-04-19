"""Spielpfad – geführter Lernweg durch alle Spiele."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import UserProgress

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

LERNPFAD = [
    {
        "level": 1,
        "title": "Einstieg",
        "subtitle": "Die drei Grundbausteine der Spieltheorie",
        "color": "emerald",
        "games": [
            {"id": "gefangenendilemma", "name": "Gefangenendilemma", "icon": "🔒",
             "subtitle": "Kooperation oder Eigennutz?", "runden": 10},
            {"id": "ultimatum", "name": "Ultimatumspiel", "icon": "⚖️",
             "subtitle": "Fairness hat ihren Preis", "runden": 10},
            {"id": "vertrauen", "name": "Vertrauensspiel", "icon": "🤝",
             "subtitle": "Lohnt sich Vertrauen?", "runden": 8},
        ],
    },
    {
        "level": 2,
        "title": "Konflikt & Koordination",
        "subtitle": "Wenn Interessen kollidieren – oder sich ergänzen",
        "color": "blue",
        "games": [
            {"id": "chicken", "name": "Feiglingsspiel", "icon": "🚗",
             "subtitle": "Wer weicht zuerst zurück?", "runden": 8},
            {"id": "stag-hunt", "name": "Hirschjagd", "icon": "🦌",
             "subtitle": "Riskiert man mehr, gewinnt man mehr", "runden": 8},
            {"id": "koordination", "name": "Koordinationsspiel", "icon": "🎯",
             "subtitle": "Einen gemeinsamen Weg finden", "runden": 8},
            {"id": "rps", "name": "Schere-Stein-Papier", "icon": "✂️",
             "subtitle": "Zufall als optimale Strategie", "runden": 7},
        ],
    },
    {
        "level": 3,
        "title": "Gruppen & Märkte",
        "subtitle": "Entscheidungen mit mehr als zwei Spielern",
        "color": "amber",
        "games": [
            {"id": "public-goods", "name": "Öffentliche Güter", "icon": "🏛️",
             "subtitle": "Das Trittbrettfahrerproblem", "runden": 8},
            {"id": "diktator", "name": "Diktatorspiel", "icon": "👑",
             "subtitle": "Macht ohne Konsequenz", "runden": 8},
            {"id": "auktion", "name": "Vickrey-Auktion", "icon": "🔨",
             "subtitle": "Die überraschend einfache Lösung", "runden": 5},
        ],
    },
    {
        "level": 4,
        "title": "Fortgeschritten",
        "subtitle": "Komplexe Entscheidungsstrukturen",
        "color": "orange",
        "games": [
            {"id": "beauty-contest", "name": "Schönheitswettbewerb", "icon": "🎯",
             "subtitle": "Was denken die anderen?", "runden": 6},
            {"id": "centipede", "name": "Centipede-Spiel", "icon": "🐛",
             "subtitle": "Wenn Logik sich selbst untergräbt", "runden": 4},
            {"id": "dollarauktion", "name": "Dollarauktion", "icon": "💸",
             "subtitle": "Die Eskalationsfalle", "runden": "var."},
            {"id": "verhandlung", "name": "Verhandlung", "icon": "💼",
             "subtitle": "Alles auf einmal", "runden": 6},
        ],
    },
    {
        "level": 5,
        "title": "Meister",
        "subtitle": "Emergenz und Marktdynamiken",
        "color": "violet",
        "games": [
            {"id": "minderheit", "name": "Minderheitsspiel", "icon": "🔢",
             "subtitle": "Gegen den Strom schwimmen", "runden": 8},
        ],
    },
]

# Flache Liste der Reihenfolge aller Spiele im Pfad
PFAD_ORDER = [g["id"] for level in LERNPFAD for g in level["games"]]


@router.get("/spielpfad", response_class=HTMLResponse)
def spielpfad_page(request: Request, db: Session = Depends(get_db)):
    # Fortschritt aus DB laden
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
