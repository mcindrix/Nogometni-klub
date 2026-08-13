# Vrlo jednostavna "prijava" za demo aplikaciju.
#
# Korisnici nisu u bazi (nema baze), nego su hardkodirani ovdje. Nakon
# uspjesne prijave korisnik dobije JWT token koji onda salje u
# Authorization headeru na svaki sljedeci zahtjev.

import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

TAJNI_KLJUC = os.environ.get("AUTH_SECRET_KEY", "dev-secret-change-me")
ALGORITAM = "HS256"
TRAJANJE_TOKENA_MIN = 8 * 60

KORISNICI = {
    "admin": {"Lozinka": "admin123", "Uloga": "Admin"},
    "trener": {"Lozinka": "trener123", "Uloga": "Trener", "TrenerID": 1},
    "igrac1": {"Lozinka": "igrac123", "Uloga": "Igrac", "IgracID": 1},
    "igrac2": {"Lozinka": "igrac123", "Uloga": "Igrac", "IgracID": 2},
    "igrac3": {"Lozinka": "igrac123", "Uloga": "Igrac", "IgracID": 3},
    "igrac4": {"Lozinka": "igrac123", "Uloga": "Igrac", "IgracID": 4},
    "igrac5": {"Lozinka": "igrac123", "Uloga": "Igrac", "IgracID": 5},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def provjeri_lozinku(korisnicko_ime: str, lozinka: str) -> bool:
    korisnik = KORISNICI.get(korisnicko_ime)
    return korisnik is not None and korisnik["Lozinka"] == lozinka


def napravi_token(korisnicko_ime: str) -> str:
    istek = datetime.now(timezone.utc) + timedelta(minutes=TRAJANJE_TOKENA_MIN)
    payload = {"sub": korisnicko_ime, "exp": istek}
    return jwt.encode(payload, TAJNI_KLJUC, algorithm=ALGORITAM)


def trenutni_korisnik(token: str | None = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, TAJNI_KLJUC, algorithms=[ALGORITAM])
        korisnicko_ime = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token je istekao")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Neispravan token")
    
    korisnik = KORISNICI.get(korisnicko_ime)
    return {"KorisnickoIme": korisnicko_ime, "Uloga": korisnik["Uloga"], "IgracID": korisnik.get("IgracID"), 
            "TrenerID": korisnik.get("TrenerID")} if korisnik else None


def samo_admin(korisnik: dict = Depends(trenutni_korisnik)) -> dict:
    if korisnik["Uloga"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Potrebna je Admin uloga")
    return korisnik

def samo_trener(korisnik: dict = Depends(trenutni_korisnik)) -> dict:
    if korisnik["Uloga"] != "Trener":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Potrebna je Trener uloga")
    return korisnik


def samo_igrac(korisnik: dict = Depends(trenutni_korisnik)) -> dict:
    if korisnik["Uloga"] != "Igrac":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Potrebna je Igrac uloga")
    return korisnik


def admin_ili_trener(korisnik: dict = Depends(trenutni_korisnik)) -> dict:
    if korisnik["Uloga"] not in ("Admin", "Trener"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Potrebna je Admin ili Trener uloga")
    return korisnik