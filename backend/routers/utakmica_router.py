from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import admin_ili_trener, samo_admin, samo_igrac, trenutni_korisnik

router = APIRouter(prefix="/api/utakmica", tags=["Utakmica"], dependencies=[Depends(trenutni_korisnik)])


def _spoji(utakmica: dict) -> dict:
    return {
        **utakmica,
        "ekipa": database.ekipe[utakmica["EkipaID"]],
        "stadion": database.stadioni[utakmica["StadionID"]],
    }


def _provjeri_veze(podaci: schemas.UtakmicaCreate):
    if podaci.EkipaID not in database.ekipe:
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")
    if podaci.StadionID not in database.stadioni:
        raise HTTPException(status_code=400, detail="Odabrani stadion ne postoji")


@router.get("", response_model=list[schemas.UtakmicaRead])
def popis_utakmica():
    utakmice = sorted(database.utakmice.values(), key=lambda u: u["DatumVrijeme"], reverse=True)
    return [_spoji(u) for u in utakmice]


@router.post("", response_model=schemas.UtakmicaRead, status_code=201, dependencies=[Depends(admin_ili_trener)])
def dodaj_utakmicu(podaci: schemas.UtakmicaCreate):
    _provjeri_veze(podaci)
    uid = database.sljedeci_id("utakmica")
    zapis = {"UtakmicaID": uid, **podaci.model_dump()}
    database.utakmice[uid] = zapis
    return _spoji(zapis)


@router.get("/moje", response_model=list[schemas.UtakmicaRead])
def moje_utakmice(korisnik: dict = Depends(samo_igrac)):
    igrac = database.igraci[korisnik["IgracID"]]
    utakmice = sorted(
        (u for u in database.utakmice.values() if u["EkipaID"] == igrac["EkipaID"]),
        key=lambda u: u["DatumVrijeme"],
    )
    return [_spoji(u) for u in utakmice]


@router.get("/{utakmica_id}", response_model=schemas.UtakmicaRead)
def dohvati_utakmicu(utakmica_id: int):
    zapis = database.utakmice.get(utakmica_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    return _spoji(zapis)


@router.put("/{utakmica_id}", response_model=schemas.UtakmicaRead, dependencies=[Depends(samo_admin)])
def azuriraj_utakmicu(utakmica_id: int, podaci: schemas.UtakmicaCreate):
    if utakmica_id not in database.utakmice:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    _provjeri_veze(podaci)
    zapis = {"UtakmicaID": utakmica_id, **podaci.model_dump()}
    database.utakmice[utakmica_id] = zapis
    return _spoji(zapis)


@router.delete("/{utakmica_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_utakmicu(utakmica_id: int):
    if utakmica_id not in database.utakmice:
        raise HTTPException(status_code=404, detail="Utakmica nije pronadjena")
    del database.utakmice[utakmica_id]
