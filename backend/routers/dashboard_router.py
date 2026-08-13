from fastapi import APIRouter, Depends

import database
import schemas
from auth import trenutni_korisnik

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=schemas.DashboardStatistika)
def statistika():
    return {
        "brojIgraca": len(database.igraci),
        "brojEkipa": len(database.ekipe),
        "brojTrenera": len(database.treneri),
        "brojUtakmica": len(database.utakmice),
        "brojTreninga": len(database.treninzi),
        "ukupnoClanarina": sum(c["Iznos"] for c in database.clanarine.values()),
    }
