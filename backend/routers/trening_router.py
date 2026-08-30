from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import admin_ili_trener, igrac_ili_trener, samo_admin, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/trening", tags=["Trening"], dependencies=[Depends(trenutni_korisnik)])


def _provjeri_veze(podaci: schemas.TreningCreate, db: Session):
    if not db.get(models.Ekipa, podaci.EkipaID):
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")
    if not db.get(models.Trener, podaci.TrenerID):
        raise HTTPException(status_code=400, detail="Odabrani trener ne postoji")
    if podaci.StadionID is not None and not db.get(models.Stadion, podaci.StadionID):
        raise HTTPException(status_code=400, detail="Odabrani stadion ne postoji")


@router.get("", response_model=list[schemas.TreningRead])
def popis_treninga(db: Session = Depends(get_db)):
    return (
        db.query(models.Trening)
        .order_by(models.Trening.DatumVrijeme.desc())
        .all()
    )


@router.post("", response_model=schemas.TreningRead, status_code=201, dependencies=[Depends(admin_ili_trener)])
def dodaj_trening(podaci: schemas.TreningCreate, db: Session = Depends(get_db)):
    _provjeri_veze(podaci, db)
    zapis = models.Trening(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/moji", response_model=list[schemas.TreningRead])
def moji_treninzi(korisnik: dict = Depends(igrac_ili_trener), db: Session = Depends(get_db)):
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
        db.query(models.Trening)
        .filter(models.Trening.EkipaID.in_(ekipa_id_ovi))
        .order_by(models.Trening.DatumVrijeme.asc())
        .all()
    )


@router.get("/{trening_id}", response_model=schemas.TreningRead)
def dohvati_trening(trening_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Trening, trening_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    return zapis


@router.put("/{trening_id}", response_model=schemas.TreningRead, dependencies=[Depends(samo_admin)])
def azuriraj_trening(trening_id: int, podaci: schemas.TreningCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Trening, trening_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    _provjeri_veze(podaci, db)
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{trening_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_trening(trening_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Trening, trening_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    db.delete(zapis)
    db.commit()
