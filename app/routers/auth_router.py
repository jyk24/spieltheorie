"""Auth-Routen: Registrieren, Anmelden, Abmelden, Profil."""
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import COOKIE_NAME, create_access_token, get_user_from_request, hash_password, verify_password
from ..database import get_db
from ..models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/registrieren", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db)):
    current_user = get_user_from_request(request, db)
    if current_user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "registrieren.html", {"active_page": ""})


@router.post("/registrieren", response_class=HTMLResponse)
def register_submit(
    request: Request,
    display_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    errors = []
    if len(display_name.strip()) < 2:
        errors.append("Name muss mindestens 2 Zeichen lang sein.")
    if "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Bitte eine gültige E-Mail-Adresse eingeben.")
    if len(password) < 8:
        errors.append("Passwort muss mindestens 8 Zeichen lang sein.")
    if password != password2:
        errors.append("Passwörter stimmen nicht überein.")
    if not errors:
        existing = db.query(User).filter(User.email == email.lower().strip()).first()
        if existing:
            errors.append("Diese E-Mail ist bereits registriert.")

    if errors:
        return templates.TemplateResponse(
            request,
            "registrieren.html",
            {"active_page": "", "errors": errors, "form_email": email, "form_name": display_name},
            status_code=422,
        )

    user = User(
        email=email.lower().strip(),
        display_name=display_name.strip(),
        hashed_password=hash_password(password),
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=7 * 24 * 3600,
        samesite="lax",
    )
    return response


@router.get("/anmelden", response_class=HTMLResponse)
def login_form(request: Request, db: Session = Depends(get_db)):
    current_user = get_user_from_request(request, db)
    if current_user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "anmelden.html", {"active_page": ""})


@router.post("/anmelden", response_class=HTMLResponse)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email.lower().strip(), User.is_active == True).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request,
            "anmelden.html",
            {"active_page": "", "error": "E-Mail oder Passwort falsch.", "form_email": email},
            status_code=401,
        )

    user.last_login = datetime.utcnow()
    db.commit()

    token = create_access_token(user.id)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=7 * 24 * 3600,
        samesite="lax",
    )
    return response


@router.post("/abmelden")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response


@router.get("/profil", response_class=HTMLResponse)
def profil(request: Request, db: Session = Depends(get_db)):
    current_user = get_user_from_request(request, db)
    if not current_user:
        return RedirectResponse("/anmelden", status_code=303)
    return templates.TemplateResponse(
        request,
        "profil.html",
        {"active_page": "", "current_user": current_user},
    )


@router.post("/profil", response_class=HTMLResponse)
def profil_update(
    request: Request,
    display_name: str = Form(...),
    db: Session = Depends(get_db),
):
    current_user = get_user_from_request(request, db)
    if not current_user:
        return RedirectResponse("/anmelden", status_code=303)

    errors = []
    if len(display_name.strip()) < 2:
        errors.append("Name muss mindestens 2 Zeichen lang sein.")

    if errors:
        return templates.TemplateResponse(
            request,
            "profil.html",
            {"active_page": "", "current_user": current_user, "errors": errors},
            status_code=422,
        )

    current_user.display_name = display_name.strip()
    db.commit()
    return templates.TemplateResponse(
        request,
        "profil.html",
        {"active_page": "", "current_user": current_user, "success": "Profil gespeichert."},
    )
