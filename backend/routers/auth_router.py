from fastapi import APIRouter, Depends, HTTPException

import schemas
from auth import napravi_token, provjeri_lozinku, trenutni_korisnik, KORISNICI

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.PrijavaOdgovor)
def login(podaci: schemas.PrijavaZahtjev):
    if not provjeri_lozinku(podaci.KorisnickoIme, podaci.Lozinka):
        raise HTTPException(status_code=401, detail="Neispravno korisnicko ime ili lozinka")
    token = napravi_token(podaci.KorisnickoIme)
    uloga = KORISNICI[podaci.KorisnickoIme]["Uloga"]
    return schemas.PrijavaOdgovor(access_token=token, KorisnickoIme=podaci.KorisnickoIme, Uloga=uloga)


@router.get("/me")
def me(korisnik: dict = Depends(trenutni_korisnik)):
    return korisnik
