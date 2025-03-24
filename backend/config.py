import os

from dotenv import load_dotenv

load_dotenv()

NAME_DB = os.getenv("POSTGRES_DB")
PASSWORD_DB = os.getenv("POSTGRES_PASSWORD")
USER_DB = os.getenv("POSTGRES_USER")
HOST_DB = os.getenv("POSTGRES_HOST")
PORT_DB = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+psycopg2://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
