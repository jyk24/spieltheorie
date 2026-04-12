import json

import markdown
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Lesson
from ..services import mark_lesson_viewed

router = APIRouter(prefix="/lektionen")
templates = Jinja2Templates(directory="app/templates")

CATEGORY_ORDER = ["Grundlagen", "Kooperation", "Verhandlung", "Psychologie", "Fortgeschritten"]


@router.get("", response_class=HTMLResponse)
def lektionen_list(request: Request, db: Session = Depends(get_db)):
    all_lessons = db.query(Lesson).order_by(Lesson.order_index).all()

    grouped: dict[str, list] = {cat: [] for cat in CATEGORY_ORDER}
    for lesson in all_lessons:
        grouped.setdefault(lesson.category, []).append(lesson)

    return templates.TemplateResponse(
        "lektionen.html",
        {
            "request": request,
            "active_page": "lektionen",
            "grouped": grouped,
            "category_order": CATEGORY_ORDER,
        },
    )


@router.get("/{slug}", response_class=HTMLResponse)
def lektion_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter_by(slug=slug).first()
    if not lesson:
        return HTMLResponse("Lektion nicht gefunden", status_code=404)

    mark_lesson_viewed(db, slug)

    content_html = markdown.markdown(
        lesson.content_md,
        extensions=["tables", "fenced_code"],
    )
    sources = json.loads(lesson.sources_json or "[]")

    # Nächste / vorherige Lektion
    all_slugs = [l.slug for l in db.query(Lesson).order_by(Lesson.order_index).all()]
    idx = all_slugs.index(slug)
    prev_slug = all_slugs[idx - 1] if idx > 0 else None
    next_slug = all_slugs[idx + 1] if idx < len(all_slugs) - 1 else None

    return templates.TemplateResponse(
        "lektion_detail.html",
        {
            "request": request,
            "active_page": "lektionen",
            "lesson": lesson,
            "content_html": content_html,
            "sources": sources,
            "prev_slug": prev_slug,
            "next_slug": next_slug,
        },
    )
