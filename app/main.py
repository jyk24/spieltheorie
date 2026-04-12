from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, SessionLocal
from .seed import seed_lessons, seed_progress
from .routers import dashboard, lektionen, spiele, fortschritt


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
