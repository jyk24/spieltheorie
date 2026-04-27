import datetime as _dt

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .raetsel import RAETSEL_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_SCHWIERIGKEIT_ORDER = {"Einsteiger": 0, "Mittel": 1, "Fortgeschritten": 2}


@router.get("/tagesraetsel", response_class=HTMLResponse)
def tagesraetsel(request: Request):
    today = _dt.date.today()
    day_num = today.timetuple().tm_yday
    puzzle = RAETSEL_META[day_num % len(RAETSEL_META)]

    # Next puzzle preview (tomorrow)
    next_puzzle = RAETSEL_META[(day_num + 1) % len(RAETSEL_META)]

    weekday_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    month_de = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                "Juli", "August", "September", "Oktober", "November", "Dezember"]
    date_str = f"{weekday_de[today.weekday()]}, {today.day}. {month_de[today.month - 1]} {today.year}"

    # Last 7 days for streak display (dates as ISO strings, JS will check localStorage)
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
