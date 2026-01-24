from fastapi import FastAPI

from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
import db.models.amenity  # ensure models are imported for table creation
import db.models.hotel  # ensure models are imported for table creation
import db.models.hotel_amenity  # ensure association table is imported


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    include_router(app)

    @app.on_event("startup")
    def on_startup() -> None:
        create_tables()

    return app


app = create_app()
