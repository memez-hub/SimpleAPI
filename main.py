from pathlib import Path
import sys

from fastapi import FastAPI


ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from db.base import Base  # noqa: E402
from db.session import engine  # noqa: E402
from apis.base import api_router  # noqa: E402
import db.models.hotel  # noqa: E402,F401
import db.models.amenity  # noqa: E402,F401
import db.models.hotel_amenity  # noqa: E402,F401


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    include_router(app)
    create_tables()
    return app


app = start_application()
