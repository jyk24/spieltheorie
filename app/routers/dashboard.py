from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Lesson
from ..services import get_all_progress

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = get_all_progress(db)
    next_lesson = (
        db.query(Lesson)
        .order_by(Lesson.order_index)
        .first()
    )
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "active_page": "dashboard",
            "stats": stats,
            "next_lesson": next_lesson,
        },
    )
