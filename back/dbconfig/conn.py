import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .session import sessionmaker

user = os.getenv("POSTGRES_USER")
passwd = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

engine = create_engine(f"postgresql+psycopg://{user}:{passwd}@{host}:{port}/{db_name}")
SessionLocal = sessionmaker(bind=engine)

def get_dbconn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()