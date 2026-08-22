from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, samo_trener, trenutni_korisnik

router = APIRouter(prefix="/api/trener", tags=["Trener"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.TrenerRead])
def popis_trenera():
    return list(database.treneri.values())


@router.get("/moj", response_model=schemas.TrenerRead)
def moj_profil(korisnik: dict = Depends(samo_trener)):
    return database.treneri[korisnik["TrenerID"]]


@router.get("/moje-ekipe", response_model=list[schemas.EkipaRead])
def moje_ekipe(korisnik: dict = Depends(samo_trener)):
    ekipa_id_ovi = {t["EkipaID"] for t in database.treninzi.values() if t["TrenerID"] == korisnik["TrenerID"]}
    return [database.ekipe[eid] for eid in ekipa_id_ovi if eid in database.ekipe]


@router.post("", response_model=schemas.TrenerRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_trenera(podaci: schemas.TrenerCreate):
    tid = database.sljedeci_id("trener")
    zapis = {"TrenerID": tid, **podaci.model_dump()}
    database.treneri[tid] = zapis
    return zapis


@router.get("/{trener_id}", response_model=schemas.TrenerRead)
def dohvati_trenera(trener_id: int):
    zapis = database.treneri.get(trener_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    return zapis


@router.put("/{trener_id}", response_model=schemas.TrenerRead, dependencies=[Depends(samo_admin)])
def azuriraj_trenera(trener_id: int, podaci: schemas.TrenerCreate):
    if trener_id not in database.treneri:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    zapis = {"TrenerID": trener_id, **podaci.model_dump()}
    database.treneri[trener_id] = zapis
    return zapis


@router.delete("/{trener_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_trenera(trener_id: int):
    if trener_id not in database.treneri:
        raise HTTPException(status_code=404, detail="Trener nije pronadjen")
    if any(t["TrenerID"] == trener_id for t in database.treninzi.values()):
        raise HTTPException(status_code=400, detail="Trener ima zakazane treninge")
    del database.treneri[trener_id]
