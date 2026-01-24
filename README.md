# SimpleAPI

A small FastAPI service for managing hotels and amenities.

## Project layout

The repository follows a simple production-ready structure:

- `src/` contains the FastAPI application code.
- `requirements.txt` lives at the repo root for standard tooling and Docker builds.
- `Dockerfile` runs the API using Gunicorn + Uvicorn workers.
- `.env.example` documents the environment variables used by the app.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000` and the docs at `/docs`.

## Environment variables

Copy `.env.example` to `.env` and adjust as needed:

- `PROJECT_NAME`: FastAPI title.
- `DATABASE_URL`: SQLAlchemy connection string.
- `PORT`: Port used by the container command.
- `GUNICORN_WORKERS`: Number of Gunicorn workers.

## Run with Docker (cloud-friendly)

```bash
docker build -t simpleapi .
docker run --env-file .env -p 8000:8000 simpleapi
```

This container binds to `0.0.0.0:$PORT`, which is compatible with most cloud platforms.
