from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..achievements import ACHIEVEMENTS
from ..database import get_db
from ..game_registry import GAME_ICONS, GAME_LABELS
from ..models import GameSession, UserAchievement
from ..services import get_all_progress

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/redesign", response_class=HTMLResponse)
async def redesign(request: Request):
    """Editorial-Skin (Beta) — neue Designoption, parallel zum klassischen Layout."""
    return templates.TemplateResponse(request, "redesign.html", {})


@router.get("/api/redesign/stats")
def redesign_stats(db: Session = Depends(get_db)):
    """JSON-API für das Editorial-Design: Echtdaten für Dashboard und Fortschritt."""
    stats = get_all_progress(db)

    unlocked_count = db.query(UserAchievement).count()

    recent_sessions = (
        db.query(GameSession)
        .order_by(GameSession.created_at.desc())
        .limit(5)
        .all()
    )

    sessions_data = [
        {
            "game_type": s.game_type,
            "game_name": GAME_LABELS.get(s.game_type, s.game_type),
            "game_icon": GAME_ICONS.get(s.game_type, "🎮"),
            "result": s.result,
            "score": s.score,
            "date": s.created_at.strftime("%d.%m.%Y") if s.created_at else "",
        }
        for s in recent_sessions
    ]

    return {
        "total_games": stats["total_games"],
        "total_score": stats["total_score"],
        "lessons_viewed": stats["lessons_viewed"],
        "total_lessons": stats["total_lessons"],
        "unlocked_achievements": unlocked_count,
        "total_achievements": len(ACHIEVEMENTS),
        "recent_sessions": sessions_data,
    }
