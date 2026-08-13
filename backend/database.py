# "Baza podataka" ove aplikacije.
#
# Pravi projekt bi ovdje imao konekciju na SQL Server/PostgreSQL, ali za
# ovaj prikazni (demo) projekt nema nikakve vanjske baze - svi podaci se
# drže u obicnim Python listama/rjecnicima dok backend radi. Kad se server
# ugasi, svi podaci se izgube i ponovno se generiraju seed podaci pri
# sljedecem pokretanju.

from datetime import date, datetime, timedelta

# svaka "tablica" je rjecnik oblika {id: podaci}
pozicije = {}
stadioni = {}
treneri = {}
ekipe = {}
igraci = {}
clanarine = {}
utakmice = {}
treninzi = {}

# brojaci za dodjelu sljedeceg ID-a po tablici
_zadnji_id = {
    "pozicija": 0,
    "stadion": 0,
    "trener": 0,
    "ekipa": 0,
    "igrac": 0,
    "clanarina": 0,
    "utakmica": 0,
    "trening": 0,
}


def sljedeci_id(tablica: str) -> int:
    _zadnji_id[tablica] += 1
    return _zadnji_id[tablica]


def ucitaj_pocetne_podatke():
    """Napuni bazu s nekoliko pocetnih zapisa da aplikacija nije prazna."""

    for naziv, opis in [
        ("Vratar", "Brani gol"),
        ("Branic", "Igra u obrani"),
        ("Vezni", "Povezuje obranu i napad"),
        ("Napadac", "Zaduzen za postizanje golova"),
    ]:
        pid = sljedeci_id("pozicija")
        pozicije[pid] = {"PozicijaID": pid, "Naziv": naziv, "Opis": opis}
    vratar, branic, vezni, napadac = 1, 2, 3, 4

    for naziv, grad, kapacitet in [
        ("Gradski stadion", "Zagreb", 15000),
        ("Stadion Kranjceviceva", "Zagreb", 8000),
        ("Stadion Rujevica", "Rijeka", 8600),
    ]:
        sid = sljedeci_id("stadion")
        stadioni[sid] = {"StadionID": sid, "Naziv": naziv, "Grad": grad, "Kapacitet": kapacitet}

    for ime, prezime, licenca, rodjen in [
        ("Ivan", "Horvat", "UEFA Pro", date(1975, 5, 12)),
        ("Ana", "Kovac", "UEFA A", date(1980, 9, 3)),
        ("Petar", "Babic", "UEFA B", date(1988, 1, 22)),
    ]:
        tid = sljedeci_id("trener")
        treneri[tid] = {
            "TrenerID": tid,
            "Ime": ime,
            "Prezime": prezime,
            "Licenca": licenca,
            "DatumRodjenja": rodjen,
        }

    for naziv, liga in [
        ("Prva momcad", "1. HNL"),
        ("Juniori", "Juniorska liga"),
    ]:
        eid = sljedeci_id("ekipa")
        ekipe[eid] = {"EkipaID": eid, "Naziv": naziv, "Liga": liga}
    prva_ekipa, juniori = 1, 2

    igraci_seed = [
        ("Luka", "Modric", date(1985, 9, 9), vezni, prva_ekipa),
        ("Marko", "Peric", date(1998, 2, 20), napadac, prva_ekipa),
        ("Josip", "Novak", date(2000, 11, 4), napadac, prva_ekipa),
        ("Ante", "Maric", date(1996, 6, 15), branic, prva_ekipa),
        ("Ivan", "Juric", date(1994, 3, 30), branic, prva_ekipa),
        ("Filip", "Kovacevic", date(1997, 7, 19), branic, prva_ekipa),
        ("Dario", "Vidovic", date(1993, 12, 2), vratar, prva_ekipa),
        ("Tomislav", "Barisic", date(1999, 4, 8), vezni, prva_ekipa),
        ("Nikola", "Radic", date(1995, 10, 27), vezni, prva_ekipa),
        ("Karlo", "Matic", date(2001, 8, 14), napadac, prva_ekipa),
        ("Mateo", "Saric", date(2002, 5, 6), napadac, juniori),
        ("Borna", "Blazevic", date(2003, 1, 17), branic, juniori),
        ("Roko", "Tomic", date(2003, 9, 25), vratar, juniori),
    ]
    for ime, prezime, rodjen, pozicija_id, ekipa_id in igraci_seed:
        iid = sljedeci_id("igrac")
        igraci[iid] = {
            "IgracID": iid,
            "Ime": ime,
            "Prezime": prezime,
            "DatumRodjenja": rodjen,
            "PozicijaID": pozicija_id,
            "EkipaID": ekipa_id,
        }

    for igrac_id, iznos, razdoblje in [(1, 50.0, "2026-Q1"), (2, 50.0, "2026-Q2"), (3, 45.0, "2026-Q2")]:
        cid = sljedeci_id("clanarina")
        clanarine[cid] = {
            "ClanarinaID": cid,
            "IgracID": igrac_id,
            "Iznos": iznos,
            "DatumUplate": date.today(),
            "Razdoblje": razdoblje,
        }

    for ekipa_id, protivnik, stadion_id, dana, rez_nas, rez_protiv in [
        (prva_ekipa, "NK Susjedgrad", 1, -7, 2, 1),
        (prva_ekipa, "HNK Primorje", 2, 3, None, None),
        (juniori, "NK Mladost", 3, -3, 3, 0),
    ]:
        uid = sljedeci_id("utakmica")
        utakmice[uid] = {
            "UtakmicaID": uid,
            "EkipaID": ekipa_id,
            "Protivnik": protivnik,
            "StadionID": stadion_id,
            "DatumVrijeme": datetime.now() + timedelta(days=dana),
            "RezultatNas": rez_nas,
            "RezultatProtivnik": rez_protiv,
        }

    for ekipa_id, trener_id, stadion_id, dana in [
        (prva_ekipa, 1, 1, -1),
        (prva_ekipa, 3, 1, -3),
        (juniori, 2, 2, -2),
    ]:
        trid = sljedeci_id("trening")
        treninzi[trid] = {
            "TreningID": trid,
            "EkipaID": ekipa_id,
            "TrenerID": trener_id,
            "StadionID": stadion_id,
            "DatumVrijeme": datetime.now() + timedelta(days=dana),
            "Trajanje": 90,
        }


ucitaj_pocetne_podatke()
