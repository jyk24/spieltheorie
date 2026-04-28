import datetime as _dt
import uuid

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import TagesraetselStreak
from .raetsel import RAETSEL_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_SCHWIERIGKEIT_ORDER = {"Einsteiger": 0, "Mittel": 1, "Fortgeschritten": 2}

SESSION_COOKIE = "sid"
SESSION_MAX_AGE = 60 * 60 * 24 * 365  # 1 Jahr


def _get_session_id(request: Request) -> str:
    sid = request.cookies.get(SESSION_COOKIE)
    return sid if sid else str(uuid.uuid4())


def _calc_streak(session_id: str, db: Session) -> int:
    today = _dt.date.today()
    streak = 0
    check = today
    while True:
        exists = db.query(TagesraetselStreak).filter_by(
            session_id=session_id, date=check.isoformat()
        ).first()
        if not exists:
            break
        streak += 1
        check -= _dt.timedelta(days=1)
    return streak


def _get_done_dates(session_id: str, db: Session) -> set[str]:
    rows = db.query(TagesraetselStreak.date).filter_by(session_id=session_id).all()
    return {r.date for r in rows}


@router.get("/tagesraetsel", response_class=HTMLResponse)
def tagesraetsel(request: Request):
    today = _dt.date.today()
    day_num = today.timetuple().tm_yday
    puzzle = RAETSEL_META[day_num % len(RAETSEL_META)]

    next_puzzle = RAETSEL_META[(day_num + 1) % len(RAETSEL_META)]

    weekday_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    month_de = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                "Juli", "August", "September", "Oktober", "November", "Dezember"]
    date_str = f"{weekday_de[today.weekday()]}, {today.day}. {month_de[today.month - 1]} {today.year}"

    week_days = []
    for i in range(6, -1, -1):
        d = today - _dt.timedelta(days=i)
        week_days.append({
            "iso": d.isoformat(),
            "label": weekday_de[d.weekday()][:2],
            "is_today": d == today,
        })

    return templates.TemplateResponse(
        request,
        "tagesraetsel.html",
        {
            "active_page": "tagesraetsel",
            "puzzle": puzzle,
            "next_puzzle": next_puzzle,
            "date_str": date_str,
            "today_iso": today.isoformat(),
            "week_days": week_days,
        },
    )


@router.get("/tagesraetsel/streak")
def get_streak(request: Request, db: Session = Depends(get_db)):
    sid = _get_session_id(request)
    streak = _calc_streak(sid, db)
    done_dates = _get_done_dates(sid, db)
    today_iso = _dt.date.today().isoformat()

    response = JSONResponse({
        "streak": streak,
        "done_today": today_iso in done_dates,
        "done_dates": list(done_dates),
    })
    if not request.cookies.get(SESSION_COOKIE):
        response.set_cookie(
            SESSION_COOKIE, sid,
            max_age=SESSION_MAX_AGE,
            httponly=True,
            samesite="lax",
        )
    return response


@router.post("/tagesraetsel/complete")
def complete_puzzle(request: Request, db: Session = Depends(get_db)):
    sid = _get_session_id(request)
    today = _dt.date.today()
    today_iso = today.isoformat()

    today_num = today.timetuple().tm_yday
    puzzle = RAETSEL_META[today_num % len(RAETSEL_META)]
    puzzle_id = puzzle.get("id", puzzle.get("name", "unknown"))

    existing = db.query(TagesraetselStreak).filter_by(
        session_id=sid, date=today_iso
    ).first()
    if not existing:
        entry = TagesraetselStreak(
            session_id=sid,
            user_id=None,
            date=today_iso,
            puzzle_id=str(puzzle_id),
        )
        db.add(entry)
        db.commit()

    streak = _calc_streak(sid, db)
    done_dates = _get_done_dates(sid, db)

    response = JSONResponse({
        "streak": streak,
        "done_today": True,
        "done_dates": list(done_dates),
    })
    response.set_cookie(
        SESSION_COOKIE, sid,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
    )
    return response
