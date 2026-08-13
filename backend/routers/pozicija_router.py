from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, trenutni_korisnik

router = APIRouter(prefix="/api/pozicija", tags=["Pozicija"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.PozicijaRead])
def popis_pozicija():
    return list(database.pozicije.values())


@router.post("", response_model=schemas.PozicijaRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_poziciju(podaci: schemas.PozicijaCreate):
    pid = database.sljedeci_id("pozicija")
    zapis = {"PozicijaID": pid, **podaci.model_dump()}
    database.pozicije[pid] = zapis
    return zapis


@router.get("/{pozicija_id}", response_model=schemas.PozicijaRead)
def dohvati_poziciju(pozicija_id: int):
    zapis = database.pozicije.get(pozicija_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    return zapis


@router.put("/{pozicija_id}", response_model=schemas.PozicijaRead, dependencies=[Depends(samo_admin)])
def azuriraj_poziciju(pozicija_id: int, podaci: schemas.PozicijaCreate):
    if pozicija_id not in database.pozicije:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    zapis = {"PozicijaID": pozicija_id, **podaci.model_dump()}
    database.pozicije[pozicija_id] = zapis
    return zapis


@router.delete("/{pozicija_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_poziciju(pozicija_id: int):
    if pozicija_id not in database.pozicije:
        raise HTTPException(status_code=404, detail="Pozicija nije pronadjena")
    if any(i["PozicijaID"] == pozicija_id for i in database.igraci.values()):
        raise HTTPException(status_code=400, detail="Pozicija se koristi kod jednog ili vise igraca")
    del database.pozicije[pozicija_id]
