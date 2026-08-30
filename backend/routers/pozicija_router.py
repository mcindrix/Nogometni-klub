from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import samo_admin, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/pozicija", tags=["Pozicija"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.PozicijaRead])
def popis_pozicija(db: Session = Depends(get_db)):
    return db.query(models.Pozicija).all()


@router.post("", response_model=schemas.PozicijaRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_poziciju(podaci: schemas.PozicijaCreate, db: Session = Depends(get_db)):
    zapis = models.Pozicija(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/{pozicija_id}", response_model=schemas.PozicijaRead)
def dohvati_poziciju(pozicija_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Pozicija, pozicija_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    return zapis


@router.put("/{pozicija_id}", response_model=schemas.PozicijaRead, dependencies=[Depends(samo_admin)])
def azuriraj_poziciju(pozicija_id: int, podaci: schemas.PozicijaCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Pozicija, pozicija_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{pozicija_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_poziciju(pozicija_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Pozicija, pozicija_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    if db.query(models.Igrac).filter_by(PozicijaID=pozicija_id).first():
        raise HTTPException(status_code=400, detail="Pozicija se koristi kod jednog ili vise igraca")
    db.delete(zapis)
    db.commit()
