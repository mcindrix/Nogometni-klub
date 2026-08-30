from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import samo_admin, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/ekipa", tags=["Ekipa"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.EkipaRead])
def popis_ekipa(db: Session = Depends(get_db)):
    return db.query(models.Ekipa).all()


@router.post("", response_model=schemas.EkipaRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_ekipu(podaci: schemas.EkipaCreate, db: Session = Depends(get_db)):
    zapis = models.Ekipa(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/{ekipa_id}", response_model=schemas.EkipaRead)
def dohvati_ekipu(ekipa_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Ekipa, ekipa_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    return zapis


@router.put("/{ekipa_id}", response_model=schemas.EkipaRead, dependencies=[Depends(samo_admin)])
def azuriraj_ekipu(ekipa_id: int, podaci: schemas.EkipaCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Ekipa, ekipa_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{ekipa_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_ekipu(ekipa_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Ekipa, ekipa_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    koristi_se = (
        db.query(models.Igrac).filter_by(EkipaID=ekipa_id).first()
        or db.query(models.Utakmica).filter_by(EkipaID=ekipa_id).first()
        or db.query(models.Trening).filter_by(EkipaID=ekipa_id).first()
    )
    if koristi_se:
        raise HTTPException(status_code=400, detail="Ekipa ima povezane igrace, utakmice ili treninge")
    db.delete(zapis)
    db.commit()
