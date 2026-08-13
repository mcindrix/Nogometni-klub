from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, trenutni_korisnik

router = APIRouter(prefix="/api/clanarina", tags=["Clanarina"], dependencies=[Depends(trenutni_korisnik)])


def _spoji_igraca(igrac: dict) -> dict:
    return {
        **igrac,
        "pozicija": database.pozicije[igrac["PozicijaID"]],
        "ekipa": database.ekipe.get(igrac["EkipaID"]) if igrac["EkipaID"] else None,
    }


def _spoji(clanarina: dict) -> dict:
    return {**clanarina, "igrac": _spoji_igraca(database.igraci[clanarina["IgracID"]])}


@router.get("", response_model=list[schemas.ClanarinaRead])
def popis_clanarina():
    return [_spoji(c) for c in database.clanarine.values()]


@router.post("", response_model=schemas.ClanarinaRead, status_code=201)
def dodaj_clanarinu(podaci: schemas.ClanarinaCreate):
    if podaci.IgracID not in database.igraci:
        raise HTTPException(status_code=400, detail="Odabrani igrac ne postoji")
    cid = database.sljedeci_id("clanarina")
    zapis = {"ClanarinaID": cid, **podaci.model_dump()}
    database.clanarine[cid] = zapis
    return _spoji(zapis)


@router.get("/{clanarina_id}", response_model=schemas.ClanarinaRead)
def dohvati_clanarinu(clanarina_id: int):
    zapis = database.clanarine.get(clanarina_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    return _spoji(zapis)


@router.put("/{clanarina_id}", response_model=schemas.ClanarinaRead, dependencies=[Depends(samo_admin)])
def azuriraj_clanarinu(clanarina_id: int, podaci: schemas.ClanarinaCreate):
    if clanarina_id not in database.clanarine:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    if podaci.IgracID not in database.igraci:
        raise HTTPException(status_code=400, detail="Odabrani igrac ne postoji")
    zapis = {"ClanarinaID": clanarina_id, **podaci.model_dump()}
    database.clanarine[clanarina_id] = zapis
    return _spoji(zapis)


@router.delete("/{clanarina_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_clanarinu(clanarina_id: int):
    if clanarina_id not in database.clanarine:
        raise HTTPException(status_code=404, detail="Clanarina nije pronadjena")
    del database.clanarine[clanarina_id]
