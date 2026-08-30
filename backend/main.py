from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import engine
from routers import (
    auth_router,
    clanarina_router,
    dashboard_router,
    ekipa_router,
    igrac_router,
    pozicija_router,
    stadion_router,
    trener_router,
    trening_router,
    utakmica_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI): #provjerava dali je mysql dostupan
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    yield


app = FastAPI(title="Nogometni klub API", lifespan=lifespan)

# frontend (Angular dev server) radi na drugom portu, pa treba CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(pozicija_router.router)
app.include_router(stadion_router.router)
app.include_router(trener_router.router)
app.include_router(ekipa_router.router)
app.include_router(igrac_router.router)
app.include_router(clanarina_router.router)
app.include_router(utakmica_router.router)
app.include_router(trening_router.router)
app.include_router(dashboard_router.router)


@app.get("/")
def root():
    return {"message": "Nogometni klub API je pokrenut"}


@app.get("/health")
def health():
    return {"status": "ok"}
