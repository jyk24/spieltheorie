from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/redesign", response_class=HTMLResponse)
async def redesign(request: Request):
    """Editorial-Skin (Beta) — neue Designoption, parallel zum klassischen Layout."""
    return templates.TemplateResponse(request, "redesign.html", {})
