from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import admin_ili_trener, samo_admin
from database import get_db

router = APIRouter(prefix="/api/clanarina", tags=["Clanarina"], dependencies=[Depends(admin_ili_trener)])


@router.get("", response_model=list[schemas.ClanarinaRead])
def popis_clanarina(db: Session = Depends(get_db)):
    return db.query(models.Clanarina).all()


@router.post("", response_model=schemas.ClanarinaRead, status_code=201)
def dodaj_clanarinu(podaci: schemas.ClanarinaCreate, db: Session = Depends(get_db)):
    if not db.get(models.Igrac, podaci.IgracID):
        raise HTTPException(status_code=400, detail="Odabrani igrac ne postoji")
    zapis = models.Clanarina(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/{clanarina_id}", response_model=schemas.ClanarinaRead)
def dohvati_clanarinu(clanarina_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Clanarina, clanarina_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    return zapis


@router.put("/{clanarina_id}", response_model=schemas.ClanarinaRead, dependencies=[Depends(samo_admin)])
def azuriraj_clanarinu(clanarina_id: int, podaci: schemas.ClanarinaCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Clanarina, clanarina_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    if not db.get(models.Igrac, podaci.IgracID):
        raise HTTPException(status_code=400, detail="Odabrani igrac ne postoji")
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{clanarina_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_clanarinu(clanarina_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Clanarina, clanarina_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    db.delete(zapis)
    db.commit()
