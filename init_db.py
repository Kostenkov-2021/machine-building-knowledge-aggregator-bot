from sqlalchemy import select
from db.database import engine, SessionLocal
from db.models import Base, User

def create_database():
    # Создание всех таблиц в базе данных, определённых в Base.metadata
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()

    # Вывод информации о созданных таблицах
    print(f"Tables: {Base.metadata.tables.keys()}")

    # Создание сессии для выполнения запросов к базе данных, Сессия автоматически закроется после выхода из блока with
    with SessionLocal() as db:
        # Получение всех строк из таблицы users
        users = db.execute(select(User)).scalars().all()
        print(f"Users table rows: {len(users)}")
