from fastapi import APIRouter, Depends, HTTPException

import database
import schemas
from auth import samo_admin, trenutni_korisnik

router = APIRouter(prefix="/api/stadion", tags=["Stadion"], dependencies=[Depends(trenutni_korisnik)])


@router.get("", response_model=list[schemas.StadionRead])
def popis_stadiona():
    return list(database.stadioni.values())


@router.post("", response_model=schemas.StadionRead, status_code=201)
def dodaj_stadion(podaci: schemas.StadionCreate):
    sid = database.sljedeci_id("stadion")
    zapis = {"StadionID": sid, **podaci.model_dump()}
    database.stadioni[sid] = zapis
    return zapis


@router.get("/{stadion_id}", response_model=schemas.StadionRead)
def dohvati_stadion(stadion_id: int):
    zapis = database.stadioni.get(stadion_id)
    if not zapis:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    return zapis


@router.put("/{stadion_id}", response_model=schemas.StadionRead, dependencies=[Depends(samo_admin)])
def azuriraj_stadion(stadion_id: int, podaci: schemas.StadionCreate):
    if stadion_id not in database.stadioni:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    zapis = {"StadionID": stadion_id, **podaci.model_dump()}
    database.stadioni[stadion_id] = zapis
    return zapis


@router.delete("/{stadion_id}", status_code=204, dependencies=[Depends(samo_admin)])
def obrisi_stadion(stadion_id: int):
    if stadion_id not in database.stadioni:
        raise HTTPException(status_code=404, detail="Stadion nije pronadjen")
    koristi_se = any(u["StadionID"] == stadion_id for u in database.utakmice.values()) or any(
        t["StadionID"] == stadion_id for t in database.treninzi.values()
    )
    if koristi_se:
        raise HTTPException(status_code=400, detail="Stadion se koristi kod utakmice ili treninga")
    del database.stadioni[stadion_id]
