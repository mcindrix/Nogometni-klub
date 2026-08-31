# Backend - Nogometni klub

FastAPI backend s MySQL bazom podataka (preko SQLAlchemy). Svi podaci
(pozicije, stadioni, treneri, ekipe, igraci, clanarine, utakmice,
treninzi, korisnici) traju u bazi - restart servera ih vise ne brise.

Shema baze i pocetni podaci vec postoje u MySQL kontejneru/volumeu
(`nk_mysql_data`) - dok god taj volume postoji, podaci ostaju kroz
restart servera i racunala.

## Dijeljenje baze (GitHub / drugo racunalo)

`db/init.sql` je izvoz cijele baze (`mysqldump`) - shema I trenutni
podaci, u jednom fajlu koji se commita u repo. `docker-compose.yml` ga
automatski ucita pri PRVOM pokretanju praznog volumena. Bilo tko s
Dockerom, bez ijedne Python ovisnosti, dobije identicnu bazu:

```bash
cp .env.example .env   # pa upisi svoje lozinke (MYSQL_* varijable)
docker compose up -d
```

Napomena: `db/init.sql` se ne generira automatski kad se podaci promijene
- to je snapshot u trenutku izvoza. Za osvjeziti ga nakon stvarnih promjena:

```bash
docker exec nk-mysql mysqldump -u nk_app -p<lozinka> --databases nogometni_klub \
  --routines --triggers --single-transaction --no-tablespaces > db/init.sql
```

Ako baza ikad nosi stvarne (ne demo) korisnicke podatke, `db/init.sql`
**ne bi smio** ici u javni repo - ovdje je u redu jer su to samo demo
lozinke (admin123 i sl.), hashirane bcryptom.

## Postavljanje (bez Dockera, spajanje na vec pokrenutu bazu)

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
