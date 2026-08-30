from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from auth import dohvati_ulogu, napravi_token, provjeri_lozinku, trenutni_korisnik
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.PrijavaOdgovor)
def login(podaci: schemas.PrijavaZahtjev, db: Session = Depends(get_db)):
    if not provjeri_lozinku(podaci.KorisnickoIme, podaci.Lozinka, db):
        raise HTTPException(status_code=401, detail="Neispravno korisnicko ime ili lozinka")
    token = napravi_token(podaci.KorisnickoIme)
    uloga = dohvati_ulogu(podaci.KorisnickoIme, db)
    return schemas.PrijavaOdgovor(access_token=token, KorisnickoIme=podaci.KorisnickoIme, Uloga=uloga)


@router.get("/me")
def me(korisnik: dict = Depends(trenutni_korisnik)):
    return korisnik
