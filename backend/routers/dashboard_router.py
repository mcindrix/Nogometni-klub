from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from auth import trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=schemas.DashboardStatistika)
def statistika(db: Session = Depends(get_db)):
    return {
        "brojIgraca": db.query(func.count(models.Igrac.IgracID)).scalar() or 0,
        "brojEkipa": db.query(func.count(models.Ekipa.EkipaID)).scalar() or 0,
        "brojTrenera": db.query(func.count(models.Trener.TrenerID)).scalar() or 0,
        "brojUtakmica": db.query(func.count(models.Utakmica.UtakmicaID)).scalar() or 0,
        "brojTreninga": db.query(func.count(models.Trening.TreningID)).scalar() or 0,
        "ukupnoClanarina": db.query(func.sum(models.Clanarina.Iznos)).scalar() or 0.0,
    }
