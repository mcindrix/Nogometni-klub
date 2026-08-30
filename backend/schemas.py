# Pydantic sheme - definiraju kako izgledaju podaci koje API prima (Create)
# i vraca (Read). Odvojeno od database.py jer to nisu "tablice", nego oblik
# JSON-a koji putuje izmedju frontenda i backenda.

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# ---- Auth -------------------------------------------------------------

class PrijavaZahtjev(BaseModel):
    KorisnickoIme: str
    Lozinka: str


class PrijavaOdgovor(BaseModel):
    access_token: str
    token_type: str = "bearer"
    KorisnickoIme: str
    Uloga: str


# ---- Pozicija -----------------------------------------------------------

class PozicijaCreate(BaseModel):
    Naziv: str
    Opis: str | None = None


class PozicijaRead(PozicijaCreate):
    model_config = ConfigDict(from_attributes=True)

    PozicijaID: int


# ---- Stadion --------------------------------------------------------------

class StadionCreate(BaseModel):
    Naziv: str
    Grad: str
    Kapacitet: int | None = None


class StadionRead(StadionCreate):
    model_config = ConfigDict(from_attributes=True)

    StadionID: int


# ---- Trener -----------------------------------------------------------

class TrenerCreate(BaseModel):
    Ime: str
    Prezime: str
    Licenca: str | None = None
    DatumRodjenja: date | None = None


class TrenerRead(TrenerCreate):
    model_config = ConfigDict(from_attributes=True)

    TrenerID: int


# ---- Ekipa --------------------------------------------------------------

class EkipaCreate(BaseModel):
    Naziv: str
    Liga: str | None = None


class EkipaRead(EkipaCreate):
    model_config = ConfigDict(from_attributes=True)

    EkipaID: int


# ---- Igrac --------------------------------------------------------------

class IgracCreate(BaseModel):
    Ime: str
    Prezime: str
    DatumRodjenja: date | None = None
    PozicijaID: int
    EkipaID: int | None = None


class IgracRead(IgracCreate):
    model_config = ConfigDict(from_attributes=True)

    IgracID: int
    pozicija: PozicijaRead
    ekipa: EkipaRead | None = None


# ---- Clanarina ----------------------------------------------------------

class ClanarinaCreate(BaseModel):
    IgracID: int
    Iznos: float
    DatumUplate: date
    Razdoblje: str | None = None


class ClanarinaRead(ClanarinaCreate):
    model_config = ConfigDict(from_attributes=True)

    ClanarinaID: int
    igrac: IgracRead


# ---- Utakmica -----------------------------------------------------------

class UtakmicaCreate(BaseModel):
    EkipaID: int
    Protivnik: str
    StadionID: int
    DatumVrijeme: datetime
    RezultatNas: int | None = None
    RezultatProtivnik: int | None = None


class UtakmicaRead(UtakmicaCreate):
    model_config = ConfigDict(from_attributes=True)

    UtakmicaID: int
    ekipa: EkipaRead
    stadion: StadionRead


# ---- Trening ------------------------------------------------------------

class TreningCreate(BaseModel):
    EkipaID: int
    TrenerID: int
    StadionID: int | None = None
    DatumVrijeme: datetime
    Trajanje: int | None = None


class TreningRead(TreningCreate):
    model_config = ConfigDict(from_attributes=True)

    TreningID: int
    ekipa: EkipaRead
    trener: TrenerRead
    stadion: StadionRead | None = None


# ---- Dashboard ------------------------------------------------------------

class DashboardStatistika(BaseModel):
    brojIgraca: int
    brojEkipa: int
    brojTrenera: int
    brojUtakmica: int
    brojTreninga: int
    ukupnoClanarina: float
