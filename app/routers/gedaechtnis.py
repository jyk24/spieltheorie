from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/gedaechtnis")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def gedaechtnis_uebersicht(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis.html", {"active_page": "gedaechtnis"})


@router.get("/corsi", response_class=HTMLResponse)
def corsi(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_corsi.html", {"active_page": "gedaechtnis"})


@router.get("/zahlen", response_class=HTMLResponse)
def zahlen(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_zahlen.html", {"active_page": "gedaechtnis"})


@router.get("/memory", response_class=HTMLResponse)
def memory(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_memory.html", {"active_page": "gedaechtnis"})


@router.get("/namen", response_class=HTMLResponse)
def namen(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_namen.html", {"active_page": "gedaechtnis"})


@router.get("/karten", response_class=HTMLResponse)
def karten(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_karten.html", {"active_page": "gedaechtnis"})


@router.get("/wortfolge", response_class=HTMLResponse)
def wortfolge(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_wortfolge.html", {"active_page": "gedaechtnis"})


@router.get("/theorie", response_class=HTMLResponse)
def theorie(request: Request):
    return templates.TemplateResponse(request, "gedaechtnis_theorie.html", {"active_page": "gedaechtnis"})
