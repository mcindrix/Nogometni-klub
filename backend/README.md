# Backend - Nogometni klub

FastAPI backend bez prave baze podataka. Svi podaci (pozicije, stadioni,
treneri, ekipe, igraci, clanarine, utakmice, treninzi) drze se u memoriji
(vidi `database.py`) i pocetno se pune s nekoliko demo zapisa. Restart
servera vraca podatke na pocetno stanje.

## Pokretanje (uv)

```bash
uv sync
uv run fastapi dev main.py
```

API je dostupan na `http://localhost:8000`, dokumentacija na
`http://localhost:8000/docs`.

## Prijava

Nema registracije - dva hardkodirana korisnika u `auth.py`:

- `admin` / `admin123` (uloga Admin - moze sve)
- `korisnik` / `korisnik123` (uloga Korisnik - samo pregled)
