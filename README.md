# Nogometni-klub

![Prijava](screenshots/login.png)

## Ideja
Upravljanje financijama, igračima, treninzima, trenerima nogometnog kluba i slično, kroz web aplikaciju.

## Tehnologije

- **Backend**: FastAPI (Python) - REST API, JWT prijava, podaci se drže u memoriji (nema baze podataka)
- **Frontend**: Angular - jedna stranica po modulu (igrači, ekipe, treneri, stadioni, utakmice, treninzi, članarine)

Nema konekcije na pravu bazu podataka - to je svjesna odluka za ovaj demo/prikazni projekt. Svi podaci
se generiraju pri pokretanju backenda (`backend/database.py`) i žive samo dok server radi.

## Pokretanje

Backend (potreban [uv](https://docs.astral.sh/uv/)):

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

Frontend (potreban Node.js):

```bash
cd frontend
npm install
npm start
```

Frontend je na `http://localhost:4200`, backend na `http://localhost:8000` (dokumentacija na `/docs`).

### Demo prijave

| Korisničko ime | Lozinka | Uloga |
| --- | --- | --- |
| `admin` | `admin123` | Admin |
| `trener` | `trener123` | Trener |
| `igrac1` – `igrac5` | `igrac123` | Igrač |

## Screenshotovi

### Admin

![Admin - Početna](screenshots/admin-pocetna.png)
![Admin - Treninzi](screenshots/admin-treninzi.png)
![Admin - Članarine](screenshots/admin-clanarine.png)

### Trener

![Trener - Početna](screenshots/trener-pocetna.png)
![Trener - Treninzi](screenshots/trener-treninzi.png)
![Trener - Članarine](screenshots/trener-clanarine.png)

### Igrač

![Igrač - Početna](screenshots/igrac-pocetna.png)
![Igrač - Treninzi](screenshots/igrac-treninzi.png)

## Uloge i pristupi

Legenda: ✅ pristup + dodavanje + brisanje · ➕ pristup (pregled, gdje je primjenjivo i dodavanje) bez brisanja · – bez pristupa

| Stranica | Admin | Trener | Igrač |
| --- | :---: | :---: | :---: |
| Početna | ➕ | ➕ | ➕ ¹ |
| Igrači | ✅ | ➕ | – |
| Ekipe | ✅ | – | – |
| Treneri | ✅ | – | – |
| Stadioni | ✅ | – | – |
| Utakmice | ✅ | ➕ | ➕ ² |
| Treninzi | ✅ | ➕ | ➕ ² |
| Članarine | ✅ | ➕ | – |

¹ Igrač vidi statistiku bez ukupnih naplaćenih članarina.
² Igrač vidi samo utakmice/treninge svoje ekipe, bez mogućnosti dodavanja.
