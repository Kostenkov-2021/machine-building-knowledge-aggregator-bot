import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_FILE = os.getenv("MBKA_DB_FILE", "mbka.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
