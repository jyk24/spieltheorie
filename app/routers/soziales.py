"""Soziales – Soziale Intelligenz Hub (Kommunikation, Psychologie, Rhetorik, Verhandlung)."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .raetsel import RAETSEL_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_KATEGORIEN = {"Kommunikation", "Psychologie", "Rhetorik", "Verhandlung"}

FRAMEWORKS = [
    {
        "titel": "Schulz von Thun – 4 Ohren",
        "icon": "👂",
        "beschreibung": "Jede Nachricht hat 4 Seiten: Sachinhalt, Selbstoffenbarung, Beziehungshinweis, Appell.",
        "url": "/skills",
    },
    {
        "titel": "Cialdini – 7 Prinzipien",
        "icon": "🎯",
        "beschreibung": "Gegenseitigkeit, Knappheit, Autorität, Konsistenz, Sympathie, Soziale Bewährtheit, Einheit.",
        "url": "/skills",
    },
    {
        "titel": "Aristoteles – Rhetorik",
        "icon": "🗣️",
        "beschreibung": "Ethos (Glaubwürdigkeit), Pathos (Emotion), Logos (Logik) – das Fundament jeder Überzeugung.",
        "url": "/skills",
    },
    {
        "titel": "BATNA & Verhandlung",
        "icon": "🤝",
        "beschreibung": "Beste Alternative bestimmt deine Verhandlungsmacht – wer BATNA kennt, verhandelt sicher.",
        "url": "/skills",
    },
    {
        "titel": "Kognitive Verzerrungen",
        "icon": "🧠",
        "beschreibung": "Ankereffekt, Framing, Bestätigungsfehler – erkenne die blinden Flecken deines Denkens.",
        "url": "/skills",
    },
    {
        "titel": "Gewaltfreie Kommunikation",
        "icon": "🕊️",
        "beschreibung": "Beobachtung, Gefühl, Bedürfnis, Bitte – die 4 Schritte nach Marshall Rosenberg.",
        "url": "/skills",
    },
]


@router.get("/soziales", response_class=HTMLResponse)
def soziales_hub(request: Request):
    raetsel = [r for r in RAETSEL_META if r.get("kategorie") in _KATEGORIEN]
    return templates.TemplateResponse(
        request,
        "soziales.html",
        {"active_page": "soziales", "raetsel": raetsel, "frameworks": FRAMEWORKS},
    )
