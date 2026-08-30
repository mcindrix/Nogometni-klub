from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import samo_admin, samo_trener, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/trener", tags=["Trener"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.TrenerRead])
def popis_trenera(db: Session = Depends(get_db)):
    return db.query(models.Trener).all()


@router.get("/moj", response_model=schemas.TrenerRead)
def moj_profil(korisnik: dict = Depends(samo_trener), db: Session = Depends(get_db)):
    return db.get(models.Trener, korisnik["TrenerID"])


@router.get("/moje-ekipe", response_model=list[schemas.EkipaRead])
def moje_ekipe(korisnik: dict = Depends(samo_trener), db: Session = Depends(get_db)):
    ekipa_id_ovi = {
        t.EkipaID
        for t in db.query(models.Trening).filter_by(TrenerID=korisnik["TrenerID"]).all()
    }
    if not ekipa_id_ovi:
        return []
    return db.query(models.Ekipa).filter(models.Ekipa.EkipaID.in_(ekipa_id_ovi)).all()


@router.post("", response_model=schemas.TrenerRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_trenera(podaci: schemas.TrenerCreate, db: Session = Depends(get_db)):
    zapis = models.Trener(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/{trener_id}", response_model=schemas.TrenerRead)
def dohvati_trenera(trener_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Trener, trener_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    return zapis


@router.put("/{trener_id}", response_model=schemas.TrenerRead, dependencies=[Depends(samo_admin)])
def azuriraj_trenera(trener_id: int, podaci: schemas.TrenerCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Trener, trener_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{trener_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_trenera(trener_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Trener, trener_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    if db.query(models.Trening).filter_by(TrenerID=trener_id).first():
        raise HTTPException(status_code=400, detail="Trener ima zakazane treninge")
    db.delete(zapis)
    db.commit()
