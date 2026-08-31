# Konekcija na MySQL bazu podataka.
#
# Ranije (demo bez baze) su svi podaci bili u Python rjecnicima u memoriji.
# Sada se spajamo na pravu MySQL bazu (vidi .env za DATABASE_URL) preko
# SQLAlchemy-a. Stvarne tablice su definirane u models.py, seed podaci u
# seed.py, a promjene sheme prate se Alembic migracijama (alembic/ folder).

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size = 10)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
