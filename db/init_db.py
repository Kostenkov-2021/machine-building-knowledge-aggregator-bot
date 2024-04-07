from .database import engine
from .models import Base


def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
    print("Database and tables created successfully.")
