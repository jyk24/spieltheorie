"""Spieltheorie Grundlagen – Einführung in rationales Denken und Spieltheorie."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/grundlagen", response_class=HTMLResponse)
def grundlagen_page(request: Request):
    return templates.TemplateResponse(
        request, "grundlagen.html", {"active_page": "grundlagen"}
    )
