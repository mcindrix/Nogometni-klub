from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from auth import samo_admin, samo_igrac, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/igrac", tags=["Igrac"], dependencies=[Depends(trenutni_korisnik)])


def _provjeri_veze(podaci: schemas.IgracCreate, db: Session):
    if not db.get(models.Pozicija, podaci.PozicijaID):
        raise HTTPException(status_code=400, detail="Odabrana pozicija ne postoji")
    if podaci.EkipaID is not None and not db.get(models.Ekipa, podaci.EkipaID):
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")


@router.get("", response_model=list[schemas.IgracRead])
def popis_igraca(db: Session = Depends(get_db)):
    return db.query(models.Igrac).all()


@router.post("", response_model=schemas.IgracRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_igraca(podaci: schemas.IgracCreate, db: Session = Depends(get_db)):
    _provjeri_veze(podaci, db)
    zapis = models.Igrac(**podaci.model_dump())
    db.add(zapis)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.get("/moj", response_model=schemas.IgracRead)
def moj_profil(korisnik: dict = Depends(samo_igrac), db: Session = Depends(get_db)):
    return db.get(models.Igrac, korisnik["IgracID"])


@router.get("/{igrac_id}", response_model=schemas.IgracRead)
def dohvati_igraca(igrac_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Igrac, igrac_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    return zapis


@router.put("/{igrac_id}", response_model=schemas.IgracRead, dependencies=[Depends(samo_admin)])
def azuriraj_igraca(igrac_id: int, podaci: schemas.IgracCreate, db: Session = Depends(get_db)):
    zapis = db.get(models.Igrac, igrac_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    _provjeri_veze(podaci, db)
    for polje, vrijednost in podaci.model_dump().items():
        setattr(zapis, polje, vrijednost)
    db.commit()
    db.refresh(zapis)
    return zapis


@router.delete("/{igrac_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_igraca(igrac_id: int, db: Session = Depends(get_db)):
    zapis = db.get(models.Igrac, igrac_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    if db.query(models.Clanarina).filter_by(IgracID=igrac_id).first():
        raise HTTPException(status_code=400, detail="Igrac ima evidentirane clanarine pa ga nije moguce obrisati")
    db.delete(zapis)
    db.commit()
