import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import GameSession, Lesson, UserProgress
from ..services import get_all_progress

router = APIRouter(prefix="/fortschritt")
templates = Jinja2Templates(directory="app/templates")

GAME_LABELS = {
    "gefangenendilemma": "Gefangenendilemma",
    "ultimatum": "Ultimatumspiel",
    "vertrauen": "Vertrauensspiel",
    "verhandlung": "Verhandlungssimulation",
}


@router.get("", response_class=HTMLResponse)
def fortschritt(request: Request, db: Session = Depends(get_db)):
    stats = get_all_progress(db)

    # Score-Verlauf für Chart.js (letzte 20 Sessions)
    sessions = (
        db.query(GameSession)
        .order_by(GameSession.created_at.asc())
        .limit(20)
        .all()
    )
    chart_labels = [f"#{s.id}" for s in sessions]
    chart_scores = [s.score for s in sessions]
    chart_games = [GAME_LABELS.get(s.game_type, s.game_type) for s in sessions]

    # Lektionsfortschritt
    all_lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    viewed_slugs: set[str] = set()
    for p in db.query(UserProgress).all():
        viewed_slugs.update(json.loads(p.lessons_viewed_json or "[]"))

    lessons_with_status = [
        {"lesson": l, "viewed": l.slug in viewed_slugs}
        for l in all_lessons
    ]

    return templates.TemplateResponse(
        "fortschritt.html",
        {
            "request": request,
            "active_page": "fortschritt",
            "stats": stats,
            "chart_labels": json.dumps(chart_labels),
            "chart_scores": json.dumps(chart_scores),
            "chart_games": json.dumps(chart_games),
            "lessons_with_status": lessons_with_status,
            "game_labels": GAME_LABELS,
        },
    )
