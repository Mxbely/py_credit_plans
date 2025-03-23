import csv
import datetime
import logging

import fastapi

from backend.database import SessionLocal, get_db
from backend.models import Credit, Dictionary, Payment, Plan, User

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger()


files = [
    "users.csv",
    "dictionary.csv",
    "credits.csv",
    "plans.csv",
    "payments.csv",
]

classes = {
    "credits.csv": Credit,
    "dictionary.csv": Dictionary,
    "payments.csv": Payment,
    "plans.csv": Plan,
    "users.csv": User,
}


def write_to_db(file, db):
    with open(f"test_csv_set/{file}", "r", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            instance = classes[file]()
            for key, value in row.items():
                if isinstance(value, str) and value.count(".") == 2:
                    value = convert_date(value)
                elif value == "":
                    value = None
                setattr(instance, key, value)
            db.add(instance)
        db.commit()


def convert_date(date_string):
    return datetime.datetime.strptime(date_string, "%d.%m.%Y").date()


def main():
    db = next(get_db())

    for file in files:
        if not db.query(classes[file]).first():
            logger.info(f"Start upload {file}")
            write_to_db(file, db)
            logger.info(f"End of upload {file}")
        else:
            logger.info(f"{file} already exist")


if __name__ == "__main__":
    main()
