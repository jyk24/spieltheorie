from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

# ── AUTH-AKTIVIERUNG: diesen Block einkommentieren ────────────────────────────
# from .auth import decode_token
# from .models import User
# ─────────────────────────────────────────────────────────────────────────────

from .database import Base, SessionLocal, engine
from .seed import seed_lessons, seed_progress
from .routers import (
    dashboard, lektionen, spiele, fortschritt, raetsel, grundlagen,
    spielpfad, konzepte, lernpfade, skills, redesign, gedaechtnis,
    spieltheorie_hub, denkraetsel, soziales, glossar, ted, tagesraetsel,
)

# ── AUTH-AKTIVIERUNG: diese Zeile einkommentieren ─────────────────────────────
# from .routers import auth_router
# ─────────────────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_lessons(db)
        seed_progress(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Spieltheorie & Verhandlungstrainer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ── AUTH-AKTIVIERUNG: diesen Middleware-Block einkommentieren ─────────────────
# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     request.state.current_user = None
#     token = request.cookies.get("access_token")
#     if token:
#         user_id = decode_token(token)
#         if user_id:
#             db = SessionLocal()
#             try:
#                 user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
#                 request.state.current_user = user
#             finally:
#                 db.close()
#     return await call_next(request)
# ─────────────────────────────────────────────────────────────────────────────

@app.middleware("http")
async def set_current_user(request: Request, call_next):
    request.state.current_user = None
    return await call_next(request)


# ── AUTH-AKTIVIERUNG: diese Zeile einkommentieren ─────────────────────────────
# app.include_router(auth_router.router)
# ─────────────────────────────────────────────────────────────────────────────

app.include_router(dashboard.router)
app.include_router(lektionen.router)
app.include_router(spiele.router)
app.include_router(fortschritt.router)
app.include_router(raetsel.router)
app.include_router(grundlagen.router)
app.include_router(spielpfad.router)
app.include_router(konzepte.router)
app.include_router(lernpfade.router)
app.include_router(skills.router)
app.include_router(redesign.router)
app.include_router(gedaechtnis.router)
app.include_router(spieltheorie_hub.router)
app.include_router(denkraetsel.router)
app.include_router(soziales.router)
app.include_router(glossar.router)
app.include_router(ted.router)
app.include_router(tagesraetsel.router)


BASE_URL = "https://imaginative-fulfillment-production.up.railway.app"

_SITEMAP_URLS = [
    "/", "/lernpfade", "/spieltheorie", "/denkraetsel", "/soziales", "/ted", "/ted/quiz", "/tagesraetsel",
    "/grundlagen", "/konzepte", "/spiele", "/raetsel",
    "/raetsel/parrondo",
    "/skills", "/gedaechtnis", "/fortschritt", "/glossar",
    "/gedaechtnis/theorie", "/gedaechtnis/wortfolge", "/gedaechtnis/zahlen",
    "/gedaechtnis/corsi", "/gedaechtnis/memory", "/gedaechtnis/namen", "/gedaechtnis/karten",
    "/gedaechtnis/technik/gedaechtnispalast", "/gedaechtnis/technik/major-system",
    "/gedaechtnis/technik/chunking", "/gedaechtnis/technik/pao-system",
    "/gedaechtnis/technik/spaced-repetition", "/gedaechtnis/technik/akrostichon",
    "/gedaechtnis/technik/geschichten", "/gedaechtnis/technik/schluesselwort",
    "/gedaechtnis/technik/elaborative-enkodierung", "/gedaechtnis/technik/zeigarnik",
    "/gedaechtnis/reaktionszeit", "/gedaechtnis/chimp", "/gedaechtnis/verbal",
    "/gedaechtnis/bestenliste",
]


@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
def robots_txt():
    return f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in _SITEMAP_URLS:
        lines.append(f"  <url><loc>{BASE_URL}{path}</loc></url>")
    lines.append("</urlset>")
    return Response(content="\n".join(lines), media_type="application/xml")
