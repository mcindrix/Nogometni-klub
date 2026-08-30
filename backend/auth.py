# "Prijava" za aplikaciju - sada nasuprot pravoj MySQL bazi.
#
# Korisnici su u tablici korisnici (vidi models.Korisnik), lozinke se
# spremaju hashirane (bcrypt). Nakon uspjesne prijave korisnik dobije JWT
# token koji onda salje u Authorization headeru na svaki sljedeci zahtjev.

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models
from database import get_db

TAJNI_KLJUC = os.environ.get("AUTH_SECRET_KEY", "dev-secret-change-me")
ALGORITAM = "HS256"
TRAJANJE_TOKENA_MIN = 8 * 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def provjeri_lozinku(korisnicko_ime: str, lozinka: str, db: Session) -> bool:
    korisnik = db.get(models.Korisnik, korisnicko_ime)
    if korisnik is None:
        return False
    return bcrypt.checkpw(lozinka.encode(), korisnik.LozinkaHash.encode())


def dohvati_ulogu(korisnicko_ime: str, db: Session) -> str:
    korisnik = db.get(models.Korisnik, korisnicko_ime)
    return korisnik.Uloga


def napravi_token(korisnicko_ime: str) -> str:
    istek = datetime.now(timezone.utc) + timedelta(minutes=TRAJANJE_TOKENA_MIN)
    payload = {"sub": korisnicko_ime, "exp": istek}
    return jwt.encode(payload, TAJNI_KLJUC, algorithm=ALGORITAM)


def trenutni_korisnik(
    token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    try:
        payload = jwt.decode(token, TAJNI_KLJUC, algorithms=[ALGORITAM])
        korisnicko_ime = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token je istekao")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Neispravan token")

    korisnik = db.get(models.Korisnik, korisnicko_ime)
    return (
        {
            "KorisnickoIme": korisnicko_ime,
            "Uloga": korisnik.Uloga,
            "IgracID": korisnik.IgracID,
            "TrenerID": korisnik.TrenerID,
        }
        if korisnik
        else None
    )


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


def igrac_ili_trener(korisnik: dict = Depends(trenutni_korisnik)) -> dict:
    if korisnik["Uloga"] not in ("Igrac", "Trener"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Potrebna je Igrac ili Trener uloga")
    return korisnik
