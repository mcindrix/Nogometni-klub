from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import samo_admin, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/stadion", tags=["Stadion"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.StadionRead])
def popis_stadiona(db: Session = Depends(get_db)):
    return db.query(models.Stadion).all()


@router.post("", response_model=schemas.StadionRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_stadion(podaci: schemas.StadionCreate, db: Session = Depends(get_db)):
    zapis = models.Stadion(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/{stadion_id}", response_model=schemas.StadionRead)
def dohvati_stadion(stadion_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Stadion, stadion_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    return zapis


@router.put("/{stadion_id}", response_model=schemas.StadionRead, dependencies=[Depends(samo_admin)])
def azuriraj_stadion(stadion_id: int, podaci: schemas.StadionCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Stadion, stadion_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{stadion_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_stadion(stadion_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Stadion, stadion_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    koristi_se = (
        db.query(models.Utakmica).filter_by(StadionID=stadion_id).first()
        or db.query(models.Trening).filter_by(StadionID=stadion_id).first()
    )
    if koristi_se:
        raise HTTPException(status_code=400, detail="Stadion se koristi kod utakmice ili treninga")
    db.delete(zapis)
    db.commit()
