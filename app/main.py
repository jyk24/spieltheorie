from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, SessionLocal
from .seed import seed_lessons, seed_progress
from .routers import dashboard, lektionen, spiele, fortschritt, raetsel, grundlagen, spielpfad, konzepte, lernpfade, skills, redesign, gedaechtnis, spieltheorie_hub, denkraetsel, soziales


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


BASE_URL = "https://imaginative-fulfillment-production.up.railway.app"

_SITEMAP_URLS = [
    "/", "/lernpfade", "/spieltheorie", "/denkraetsel", "/soziales",
    "/grundlagen", "/konzepte", "/spiele", "/raetsel",
    "/skills", "/gedaechtnis", "/fortschritt",
    "/gedaechtnis/theorie", "/gedaechtnis/wortfolge", "/gedaechtnis/zahlen",
    "/gedaechtnis/corsi", "/gedaechtnis/memory", "/gedaechtnis/namen", "/gedaechtnis/karten",
    "/gedaechtnis/technik/gedaechtnispalast", "/gedaechtnis/technik/major-system",
    "/gedaechtnis/technik/chunking", "/gedaechtnis/technik/pao-system",
    "/gedaechtnis/technik/spaced-repetition", "/gedaechtnis/technik/akrostichon",
    "/gedaechtnis/technik/geschichten", "/gedaechtnis/technik/schluesselwort",
    "/gedaechtnis/technik/elaborative-enkodierung", "/gedaechtnis/technik/zeigarnik",
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
