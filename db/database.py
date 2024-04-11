import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_FILE = os.getenv("MBKA_DB_FILE", "mbka.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"

# Создание движка SQLAlchemy с подключением к базе данных SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Создание фабрики сессий с привязкой к созданному движку
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для объявления моделей
Base = declarative_base()

# Функция-генератор для получения сессии, автоматически закрывает сессию после использования
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
