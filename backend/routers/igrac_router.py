from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, samo_igrac, trenutni_korisnik

router = APIRouter(prefix="/api/igrac", tags=["Igrac"], dependencies=[Depends(trenutni_korisnik)])


def _spoji(igrac: dict) -> dict:
    """Doda ugnijezdene objekte pozicija/ekipa za odgovor prema frontendu."""
    return {
        **igrac,
        "pozicija": database.pozicije[igrac["PozicijaID"]],
        "ekipa": database.ekipe.get(igrac["EkipaID"]) if igrac["EkipaID"] else None,
    }


def _provjeri_veze(podaci: schemas.IgracCreate):
    if podaci.PozicijaID not in database.pozicije:
        raise HTTPException(status_code=400, detail="Odabrana pozicija ne postoji")
    if podaci.EkipaID is not None and podaci.EkipaID not in database.ekipe:
        raise HTTPException(status_code=400, detail="Odabrana ekipa ne postoji")


@router.get("", response_model=list[schemas.IgracRead])
def popis_igraca():
    return [_spoji(i) for i in database.igraci.values()]


@router.post("", response_model=schemas.IgracRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_igraca(podaci: schemas.IgracCreate):
    _provjeri_veze(podaci)
    iid = database.sljedeci_id("igrac")
    zapis = {"IgracID": iid, **podaci.model_dump()}
    database.igraci[iid] = zapis
    return _spoji(zapis)


@router.get("/moj", response_model=schemas.IgracRead)
def moj_profil(korisnik: dict = Depends(samo_igrac)):
    return _spoji(database.igraci[korisnik["IgracID"]])


@router.get("/{igrac_id}", response_model=schemas.IgracRead)
def dohvati_igraca(igrac_id: int):
    zapis = database.igraci.get(igrac_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    return _spoji(zapis)


@router.put("/{igrac_id}", response_model=schemas.IgracRead, dependencies=[Depends(samo_admin)])
def azuriraj_igraca(igrac_id: int, podaci: schemas.IgracCreate):
    if igrac_id not in database.igraci:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    _provjeri_veze(podaci)
    zapis = {"IgracID": igrac_id, **podaci.model_dump()}
    database.igraci[igrac_id] = zapis
    return _spoji(zapis)


@router.delete("/{igrac_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_igraca(igrac_id: int):
    if igrac_id not in database.igraci:
        raise HTTPException(status_code=404, detail="Igrac nije pronadjen")
    if any(c["IgracID"] == igrac_id for c in database.clanarine.values()):
        raise HTTPException(status_code=400, detail="Igrac ima evidentirane clanarine pa ga nije moguce obrisati")
    del database.igraci[igrac_id]
