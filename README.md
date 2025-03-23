
# Credit Plans API

Credit Plans API – service for managing users credit plans.


## Technologies

- **FastAPI** – Main framework
- **SQLAlchemy** – ORM
- **PostgreSQL** – Database
- **Alembic** – for managing migrations
- **Docker, Docker Compose** – Containerization


## Project Structure

- `alembic/` - Migration service.
- `backend/` - Code for the FastAPI backend.
- `test_csv_set/` - Set of csv files for testing endpoints.
- `.env.sample` - Environment variables for configuring the project (e.g., for the database).
- `pyproject.toml` - Poetry-dependencies
- `Dockerfile` - Docker settings
- `compose.yml` - Configuration for running the services with Docker.


## How to Run

Clone this repository

### Step 1

Rename `.env.sample` to `.env`

### Step 2
Use next command for run project:

```bash
docker-compose up --build
```
### Step 3

API will be available by `127.0.0.1:8000`


## Documentation

Swagger documentation will be available by `127.0.0.1:8000/docs`
