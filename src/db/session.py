from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        