import subprocess
import sys


def run_command(command):
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    return result


def upgrade_database():
    print("Upgrading database...")
    run_command("poetry run alembic upgrade head")


if __name__ == "__main__":
    result = run_command(
        "poetry run alembic revision --autogenerate -m 'auto migration'"
    )
    if "No changes detected" in result.stdout:
        print("No changes detected")
    else:
        print("Changes detected")
    upgrade_database()
