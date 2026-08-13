# Nogometni-klub

## Ideja
Upravljanje financijama, igračima, treninzima, trenerima nogometnog kluba i slično, kroz web aplikaciju.

## Tehnologije

- **Backend**: FastAPI (Python) - REST API, JWT prijava, podaci se drže u memoriji (nema baze podataka)
- **Frontend**: Angular - jedna stranica po modulu (igrači, ekipe, treneri, pozicije, stadioni, utakmice, treninzi, članarine)

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

Demo prijava: `admin` / `admin123` (Admin) ili `korisnik` / `korisnik123` (Korisnik).
