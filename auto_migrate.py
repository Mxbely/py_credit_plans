import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger()


def run_command(command):
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    return result


def upgrade_database():
    logger.info("Upgrading database...")
    run_command("poetry run alembic upgrade head")


def main():
    result = run_command(
        "poetry run alembic revision --autogenerate -m 'auto migration'"
    )
    if "No changes detected" in result.stdout:
        logger.info("No database changes detected")
    else:
        logger.info("Database changes detected")
    upgrade_database()


if __name__ == "__main__":
    main()
