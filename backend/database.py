from sqlalchemy import create_engine
from sqlalchemy.orm import sesionmaker
from backend.database import (
    DATABASE_URL,
    HOST_DB,
    NAME_DB,
    PASSWORD_DB,
    PORT_DB,
    SessionLocal,
    USER_DB,
)
from dotenv import load_dotenv
import os

load_dotenv()

NAME_DB = os.getenv("POSTGRES_DB")
PASSWORD_DB = os.getenv("POSTGRES_PASSWORD")
USER_DB = os.getenv("POSTGRES_USER")
HOST_DB = os.getenv("POSTGRES_HOST")
PORT_DB = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+psycopg2://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{NAME_DB}:{PORT_DB}"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sesionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
