import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..achievements import ACHIEVEMENTS
from ..database import get_db
from ..game_registry import GAME_ICONS, GAME_LABELS
from ..models import GameSession, Lesson, UserAchievement, UserProgress
from .raetsel import RAETSEL_META
from ..services import get_all_progress

router = APIRouter(prefix="/fortschritt")
templates = Jinja2Templates(directory="app/templates")

RESULT_LABELS = {"win": "Gewonnen", "loss": "Verloren", "draw": "Unentschieden"}
RESULT_COLORS = {"win": "emerald", "loss": "red", "draw": "amber"}


@router.get("", response_class=HTMLResponse)
def fortschritt(request: Request, db: Session = Depends(get_db)):
    stats = get_all_progress(db)

    # Score-Verlauf für Chart.js (letzte 20 Sessions)
    chart_sessions = (
        db.query(GameSession)
        .order_by(GameSession.created_at.asc())
        .limit(20)
        .all()
    )
    chart_labels = [f"#{s.id}" for s in chart_sessions]
    chart_scores = [s.score for s in chart_sessions]
    chart_games = [GAME_LABELS.get(s.game_type, s.game_type) for s in chart_sessions]

    # Lektionsfortschritt
    all_lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    viewed_slugs: set[str] = set()
    for p in db.query(UserProgress).all():
        viewed_slugs.update(json.loads(p.lessons_viewed_json or "[]"))

    lessons_with_status = [
        {"lesson": l, "viewed": l.slug in viewed_slugs}
        for l in all_lessons
    ]

    # Letzte 10 Sessionen (klickbar)
    recent_sessions = (
        db.query(GameSession)
        .order_by(GameSession.created_at.desc())
        .limit(10)
        .all()
    )

    # Errungenschaften
    unlocked = db.query(UserAchievement).all()
    unlocked_slugs = {a.slug for a in unlocked}
    achievement_dates = {
        a.slug: a.unlocked_at.strftime("%d.%m.%Y") if a.unlocked_at else ""
        for a in unlocked
    }

    return templates.TemplateResponse(
        request,
        "fortschritt.html",
        {
            "active_page": "fortschritt",
            "stats": stats,
            "chart_labels": json.dumps(chart_labels),
            "chart_scores": json.dumps(chart_scores),
            "chart_games": json.dumps(chart_games),
            "lessons_with_status": lessons_with_status,
            "game_labels": GAME_LABELS,
            "game_icons": GAME_ICONS,
            "recent_sessions": recent_sessions,
            "result_labels": RESULT_LABELS,
            "result_colors": RESULT_COLORS,
            "all_achievements": ACHIEVEMENTS,
            "unlocked_slugs": unlocked_slugs,
            "achievement_dates": achievement_dates,
            "raetsel_meta": RAETSEL_META,
        },
    )


@router.get("/session/{session_id}", response_class=HTMLResponse)
def session_detail(session_id: int, request: Request, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session nicht gefunden")
    moves = json.loads(session.moves_json or "[]")
    return templates.TemplateResponse(
        request,
        "session_detail.html",
        {
            "active_page": "fortschritt",
            "session": session,
            "moves": moves,
            "game_label": GAME_LABELS.get(session.game_type, session.game_type),
            "result_labels": RESULT_LABELS,
            "result_colors": RESULT_COLORS,
        },
    )
