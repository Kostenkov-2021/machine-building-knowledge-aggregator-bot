from sqlalchemy import select
from db.database import engine, SessionLocal
from db.models import Base


def create_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()    
    print(f"Database and tables created successfully. Tables: {Base.metadata.tables.keys()}")
    db=SessionLocal()
    db.executes(select("users"))  # query object is now legacy. Use select() instead!
    print(f"DBG: users table rows: {db}")