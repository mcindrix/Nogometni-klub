# Backend - Nogometni klub

FastAPI backend s MySQL bazom podataka (preko SQLAlchemy). Svi podaci
(pozicije, stadioni, treneri, ekipe, igraci, clanarine, utakmice,
treninzi, korisnici) traju u bazi - restart servera ih vise ne brise.

Shema baze i pocetni podaci vec postoje u MySQL kontejneru/volumeu
(`nk_mysql_data`) - dok god taj volume postoji, podaci ostaju kroz
restart servera i racunala. Ako se volume ikad izgubi, shemu (definiranu
u `models.py`) treba rucno rekreirati (npr. SQL-om ili privremenim
`models.Base.metadata.create_all(bind=engine)` pozivom) i podatke
ponovno unijeti.

## Preduvjeti

MySQL server dostupan na adresi iz `DATABASE_URL` (vidi `.env.example`).
U ovom projektu koristimo pravi MySQL 8 pokrenut u Docker kontejneru:

```bash
docker run -d --name nk-mysql \
  -e MYSQL_ROOT_PASSWORD=<lozinka> \
  -e MYSQL_DATABASE=nogometni_klub \
  -e MYSQL_USER=nk_app \
  -e MYSQL_PASSWORD=<lozinka> \
  -p 3306:3306 \
  -v nk_mysql_data:/var/lib/mysql \
  mysql:8.0
```

## Postavljanje

```bash
uv sync
cp .env.example .env   # pa upisi stvarne vrijednosti
```

## Pokretanje (uv)

```bash
uv run fastapi dev main.py
```

API je dostupan na `http://localhost:8000`, dokumentacija na
`http://localhost:8000/docs`.

## Prijava

Korisnici zive u tablici `korisnici` (lozinke hashirane bcryptom):

- `admin` / `admin123` (uloga Admin - moze sve)
- `trener` / `trener123` (uloga Trener - TrenerID 1)
- `igrac1` .. `igrac5` / `igrac123` (uloga Igrac - IgracID 1-5)
