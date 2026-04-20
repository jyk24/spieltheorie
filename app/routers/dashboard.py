from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..achievements import ACHIEVEMENTS
from ..database import get_db
from ..game_registry import GAME_ICONS, GAME_LABELS
from ..models import Lesson, UserAchievement
from ..services import get_all_progress

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_LEVELS = [
    {"level": 1, "title": "Einsteiger",       "icon": "🌱", "min": 0,   "max": 5},
    {"level": 2, "title": "Lernender",        "icon": "📖", "min": 5,   "max": 15},
    {"level": 3, "title": "Fortgeschrittener","icon": "🧠", "min": 15,  "max": 30},
    {"level": 4, "title": "Stratege",         "icon": "♟️", "min": 30,  "max": 50},
    {"level": 5, "title": "Experte",          "icon": "🎯", "min": 50,  "max": 80},
    {"level": 6, "title": "Meister",          "icon": "🏆", "min": 80,  "max": 120},
    {"level": 7, "title": "Grandmaster",      "icon": "🎓", "min": 120, "max": 200},
]


def _player_level(total_games: int) -> dict:
    current = _LEVELS[0]
    for lvl in _LEVELS:
        if total_games >= lvl["min"]:
            current = lvl
    span = current["max"] - current["min"]
    progress = min(100, int((total_games - current["min"]) / span * 100)) if span else 100
    games_to_next = max(0, current["max"] - total_games)
    return {**current, "progress": progress, "games_to_next": games_to_next}


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = get_all_progress(db)

    # Achievements
    unlocked = db.query(UserAchievement).order_by(UserAchievement.unlocked_at.desc()).all()
    unlocked_slugs = {a.slug for a in unlocked}
    ach_by_slug = {a["slug"]: a for a in ACHIEVEMENTS}
    recent_badges = [
        {**ach_by_slug[row.slug], "unlocked_at": row.unlocked_at}
        for row in unlocked[:3]
        if row.slug in ach_by_slug
    ]
    next_badge = next((a for a in ACHIEVEMENTS if a["slug"] not in unlocked_slugs), None)

    next_lesson = db.query(Lesson).order_by(Lesson.order_index).first()
    player_level = _player_level(stats["total_games"])

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "active_page": "dashboard",
            "stats": stats,
            "next_lesson": next_lesson,
            "player_level": player_level,
            "recent_badges": recent_badges,
            "next_badge": next_badge,
            "unlocked_count": len(unlocked_slugs),
            "total_achievements": len(ACHIEVEMENTS),
            "game_icons": GAME_ICONS,
            "game_labels": GAME_LABELS,
            "is_new_user": stats["total_games"] == 0,
        },
    )
