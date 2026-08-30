# SQLAlchemy modeli - definiraju stvarne tablice u MySQL bazi.
#
# Zamjenjuju rjecnike iz database.py. Nazivi tablica i polja su isti kao
# prije (Croatian nazivi) da schemas.py i routeri ostanu sto slicniji.

from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Pozicija(Base):
    __tablename__ = "pozicije"

    PozicijaID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Naziv: Mapped[str] = mapped_column(String(100))
    Opis: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Stadion(Base):
    __tablename__ = "stadioni"

    StadionID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Naziv: Mapped[str] = mapped_column(String(100))
    Grad: Mapped[str] = mapped_column(String(100))
    Kapacitet: Mapped[int | None] = mapped_column(nullable=True)


class Trener(Base):
    __tablename__ = "treneri"

    TrenerID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Ime: Mapped[str] = mapped_column(String(100))
    Prezime: Mapped[str] = mapped_column(String(100))
    Licenca: Mapped[str | None] = mapped_column(String(100), nullable=True)
    DatumRodjenja: Mapped[date | None] = mapped_column(nullable=True)


class Ekipa(Base):
    __tablename__ = "ekipe"

    EkipaID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Naziv: Mapped[str] = mapped_column(String(100))
    Liga: Mapped[str | None] = mapped_column(String(100), nullable=True)


class Igrac(Base):
    __tablename__ = "igraci"

    IgracID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Ime: Mapped[str] = mapped_column(String(100))
    Prezime: Mapped[str] = mapped_column(String(100))
    DatumRodjenja: Mapped[date | None] = mapped_column(nullable=True)
    PozicijaID: Mapped[int] = mapped_column(
        ForeignKey("pozicije.PozicijaID", ondelete="RESTRICT"), nullable=False
    )
    EkipaID: Mapped[int | None] = mapped_column(
        ForeignKey("ekipe.EkipaID", ondelete="RESTRICT"), nullable=True
    )

    pozicija: Mapped["Pozicija"] = relationship(lazy="joined")
    ekipa: Mapped["Ekipa | None"] = relationship(lazy="joined")


class Clanarina(Base):
    __tablename__ = "clanarine"

    ClanarinaID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    IgracID: Mapped[int] = mapped_column(
        ForeignKey("igraci.IgracID", ondelete="RESTRICT"), nullable=False
    )
    Iznos: Mapped[float]
    DatumUplate: Mapped[date]
    Razdoblje: Mapped[str | None] = mapped_column(String(50), nullable=True)

    igrac: Mapped["Igrac"] = relationship(lazy="joined")


class Utakmica(Base):
    __tablename__ = "utakmice"

    UtakmicaID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    EkipaID: Mapped[int] = mapped_column(
        ForeignKey("ekipe.EkipaID", ondelete="RESTRICT"), nullable=False
    )
    Protivnik: Mapped[str] = mapped_column(String(150))
    StadionID: Mapped[int] = mapped_column(
        ForeignKey("stadioni.StadionID", ondelete="RESTRICT"), nullable=False
    )
    DatumVrijeme: Mapped[datetime]
    RezultatNas: Mapped[int | None] = mapped_column(nullable=True)
    RezultatProtivnik: Mapped[int | None] = mapped_column(nullable=True)

    ekipa: Mapped["Ekipa"] = relationship(lazy="joined")
    stadion: Mapped["Stadion"] = relationship(lazy="joined")


class Trening(Base):
    __tablename__ = "treninzi"

    TreningID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    EkipaID: Mapped[int] = mapped_column(
        ForeignKey("ekipe.EkipaID", ondelete="RESTRICT"), nullable=False
    )
    TrenerID: Mapped[int] = mapped_column(
        ForeignKey("treneri.TrenerID", ondelete="RESTRICT"), nullable=False
    )
    StadionID: Mapped[int | None] = mapped_column(
        ForeignKey("stadioni.StadionID", ondelete="RESTRICT"), nullable=True
    )
    DatumVrijeme: Mapped[datetime]
    Trajanje: Mapped[int | None] = mapped_column(nullable=True)

    ekipa: Mapped["Ekipa"] = relationship(lazy="joined")
    trener: Mapped["Trener"] = relationship(lazy="joined")
    stadion: Mapped["Stadion | None"] = relationship(lazy="joined")


class Korisnik(Base):
    """Korisnicki racuni za prijavu - zamjenjuje hardkodirani KORISNICI rjecnik iz auth.py."""

    __tablename__ = "korisnici"

    KorisnickoIme: Mapped[str] = mapped_column(String(50), primary_key=True)
    LozinkaHash: Mapped[str] = mapped_column(String(255))
    Uloga: Mapped[str] = mapped_column(String(20))
    TrenerID: Mapped[int | None] = mapped_column(
        ForeignKey("treneri.TrenerID", ondelete="SET NULL"), nullable=True
    )
    IgracID: Mapped[int | None] = mapped_column(
        ForeignKey("igraci.IgracID", ondelete="SET NULL"), nullable=True
    )
