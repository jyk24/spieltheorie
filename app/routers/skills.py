"""Skills & Kompetenzen – Rhetorik, Führung, Präsentation, Psychologie."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/skills")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def skills_overview(request: Request):
    return templates.TemplateResponse(
        request, "skills.html", {"active_page": "skills"}
    )
