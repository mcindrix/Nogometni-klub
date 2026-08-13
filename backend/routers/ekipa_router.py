from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, trenutni_korisnik

router = APIRouter(prefix="/api/ekipa", tags=["Ekipa"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.EkipaRead])
def popis_ekipa():
    return list(database.ekipe.values())


@router.post("", response_model=schemas.EkipaRead, status_code=201, dependencies=[Depends(samo_admin)])
def dodaj_ekipu(podaci: schemas.EkipaCreate):
    eid = database.sljedeci_id("ekipa")
    zapis = {"EkipaID": eid, **podaci.model_dump()}
    database.ekipe[eid] = zapis
    return zapis


@router.get("/{ekipa_id}", response_model=schemas.EkipaRead)
def dohvati_ekipu(ekipa_id: int):
    zapis = database.ekipe.get(ekipa_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    return zapis


@router.put("/{ekipa_id}", response_model=schemas.EkipaRead, dependencies=[Depends(samo_admin)])
def azuriraj_ekipu(ekipa_id: int, podaci: schemas.EkipaCreate):
    if ekipa_id not in database.ekipe:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    zapis = {"EkipaID": ekipa_id, **podaci.model_dump()}
    database.ekipe[ekipa_id] = zapis
    return zapis


@router.delete("/{ekipa_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_ekipu(ekipa_id: int):
    if ekipa_id not in database.ekipe:
        raise HTTPException(status_code=404, detail="Ekipa nije pronadjena")
    koristi_se = (
        any(i["EkipaID"] == ekipa_id for i in database.igraci.values())
        or any(u["EkipaID"] == ekipa_id for u in database.utakmice.values())
        or any(t["EkipaID"] == ekipa_id for t in database.treninzi.values())
    )
    if koristi_se:
        raise HTTPException(status_code=400, detail="Ekipa ima povezane igrace, utakmice ili treninge")
    del database.ekipe[ekipa_id]
