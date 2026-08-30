from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import admin_ili_trener, igrac_ili_trener, samo_admin, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/utakmica", tags=["Utakmica"], dependencies=[Depends(trenutni_korisnik)])


def _provjeri_veze(podaci: schemas.UtakmicaCreate, db: Session):
    if not db.get(models.Ekipa, podaci.EkipaID):
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")
    if not db.get(models.Stadion, podaci.StadionID):
        raise HTTPException(status_code=400, detail="Odabrani stadion ne postoji")


@router.get("", response_model=list[schemas.UtakmicaRead])
def popis_utakmica(db: Session = Depends(get_db)):
    return (
        db.query(models.Utakmica)
        .order_by(models.Utakmica.DatumVrijeme.desc())
        .all()
    )


@router.post("", response_model=schemas.UtakmicaRead, status_code=201, dependencies=[Depends(admin_ili_trener)])
def dodaj_utakmicu(podaci: schemas.UtakmicaCreate, db: Session = Depends(get_db)):
    _provjeri_veze(podaci, db)
    zapis = models.Utakmica(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/moje", response_model=list[schemas.UtakmicaRead])
def moje_utakmice(korisnik: dict = Depends(igrac_ili_trener), db: Session = Depends(get_db)):
    if korisnik["Uloga"] == "Igrac":
        igrac = db.get(models.Igrac, korisnik["IgracID"])
        ekipa_id_ovi = {igrac.EkipaID}
    else:
        ekipa_id_ovi = {
            t.EkipaID
            for t in db.query(models.Trening).filter_by(TrenerID=korisnik["TrenerID"]).all()
        }
    if not ekipa_id_ovi:
        return []
    return (
        db.query(models.Utakmica)
        .filter(models.Utakmica.EkipaID.in_(ekipa_id_ovi))
        .order_by(models.Utakmica.DatumVrijeme.asc())
        .all()
    )


@router.get("/{utakmica_id}", response_model=schemas.UtakmicaRead)
def dohvati_utakmicu(utakmica_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Utakmica, utakmica_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    return zapis


@router.put("/{utakmica_id}", response_model=schemas.UtakmicaRead, dependencies=[Depends(samo_admin)])
def azuriraj_utakmicu(utakmica_id: int, podaci: schemas.UtakmicaCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Utakmica, utakmica_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    _provjeri_veze(podaci, db)
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{utakmica_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_utakmicu(utakmica_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Utakmica, utakmica_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    db.delete(zapis)
    db.commit()
