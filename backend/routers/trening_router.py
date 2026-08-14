from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import admin_ili_trener, samo_admin, samo_igrac, trenutni_korisnik

router = APIRouter(prefix="/api/trening", tags=["Trening"], dependencies=[Depends(trenutni_korisnik)])


def _spoji(trening: dict) -> dict:
    return {
        **trening,
        "ekipa": database.ekipe[trening["EkipaID"]],
        "trener": database.treneri[trening["TrenerID"]],
        "stadion": database.stadioni.get(trening["StadionID"]) if trening["StadionID"] else None,
    }


def _provjeri_veze(podaci: schemas.TreningCreate):
    if podaci.EkipaID not in database.ekipe:
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")
    if podaci.TrenerID not in database.treneri:
        raise HTTPException(status_code=400, detail="Odabrani trener ne postoji")
    if podaci.StadionID is not None and podaci.StadionID not in database.stadioni:
        raise HTTPException(status_code=400, detail="Odabrani stadion ne postoji")


@router.get("", response_model=list[schemas.TreningRead])
def popis_treninga():
    treninzi = sorted(database.treninzi.values(), key=lambda t: t["DatumVrijeme"], reverse=True)
    return [_spoji(t) for t in treninzi]


@router.post("", response_model=schemas.TreningRead, status_code=201, dependencies=[Depends(admin_ili_trener)])
def dodaj_trening(podaci: schemas.TreningCreate):
    _provjeri_veze(podaci)
    trid = database.sljedeci_id("trening")
    zapis = {"TreningID": trid, **podaci.model_dump()}
    database.treninzi[trid] = zapis
    return _spoji(zapis)


@router.get("/moji", response_model=list[schemas.TreningRead])
def moji_treninzi(korisnik: dict = Depends(samo_igrac)):
    igrac = database.igraci[korisnik["IgracID"]]
    treninzi = sorted(
        (t for t in database.treninzi.values() if t["EkipaID"] == igrac["EkipaID"]),
        key=lambda t: t["DatumVrijeme"],
    )
    return [_spoji(t) for t in treninzi]


@router.get("/{trening_id}", response_model=schemas.TreningRead)
def dohvati_trening(trening_id: int):
    zapis = database.treninzi.get(trening_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    return _spoji(zapis)


@router.put("/{trening_id}", response_model=schemas.TreningRead, dependencies=[Depends(samo_admin)])
def azuriraj_trening(trening_id: int, podaci: schemas.TreningCreate):
    if trening_id not in database.treninzi:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    _provjeri_veze(podaci)
    zapis = {"TreningID": trening_id, **podaci.model_dump()}
    database.treninzi[trening_id] = zapis
    return _spoji(zapis)


@router.delete("/{trening_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_trening(trening_id: int):
    if trening_id not in database.treninzi:
        raise HTTPException(status_code=404, detail="Trening nije pronadjen")
    del database.treninzi[trening_id]
