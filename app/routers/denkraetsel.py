"""Denkrätsel – Analytisches Denken Hub (Mathematik, Physik, Logik)."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .raetsel import RAETSEL_META

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_KATEGORIEN = {"Mathematik", "Physik", "Logik"}


@router.get("/denkraetsel", response_class=HTMLResponse)
def denkraetsel_hub(request: Request):
    raetsel = [r for r in RAETSEL_META if r.get("kategorie") in _KATEGORIEN]
    return templates.TemplateResponse(
        request,
        "denkraetsel.html",
        {"active_page": "denkraetsel", "raetsel": raetsel},
    )
