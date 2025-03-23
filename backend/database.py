import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Uncomment the following lines to see the SQL queries
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

NAME_DB = os.getenv("POSTGRES_DB")
PASSWORD_DB = os.getenv("POSTGRES_PASSWORD")
USER_DB = os.getenv("POSTGRES_USER")
HOST_DB = os.getenv("POSTGRES_HOST")
PORT_DB = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+psycopg2://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
